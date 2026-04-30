from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DbSession
from app.core.database import get_db
from app.models.session import Session, SessionCreate, SessionOut, SessionJoin
from app.core.auth import create_access_token
import uuid
import qrcode
import base64
from io import BytesIO

router = APIRouter()

@router.post("/create", response_model=SessionOut)
async def create_session(session: SessionCreate, db: DbSession = Depends(get_db)):
    session_code = str(uuid.uuid4())[:8]
    while db.query(Session).filter(Session.session_code == session_code).first():
        session_code = str(uuid.uuid4())[:8]
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(session_code)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    host_id = str(uuid.uuid4())
    
    db_session = Session(
        session_code=session_code, 
        host_id=host_id,
        name=session.name,
        duration=session.duration
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    token = create_access_token({"user_id": host_id, "session_code": session_code, "role": "host"})
    
    return SessionOut(
        session_code=session_code, 
        qr_code=qr_base64, 
        name=db_session.name,
        duration=db_session.duration,
        token=token
    )

@router.post("/join")
async def join_session(join: SessionJoin, db: DbSession = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == join.session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    guest_id = str(uuid.uuid4())
    token = create_access_token({"user_id": guest_id, "session_code": join.session_code, "role": "guest"})
    
    return {"message": "Joined session", "token": token}

@router.get("/{session_code}")
async def get_session(session_code: str, db: DbSession = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_code": db_session.session_code, 
        "name": db_session.name,
        "duration": db_session.duration
    }