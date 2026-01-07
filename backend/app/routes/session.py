from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session import Session, SessionCreate, SessionOut, SessionJoin
import uuid
import qrcode
import base64
from io import BytesIO

router = APIRouter()

@router.post("/create", response_model=SessionOut)
async def create_session(session: SessionCreate, db: Session = Depends(get_db)):
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
    
    db_session = Session(session_code=session_code, host_id=session.host_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return SessionOut(session_code=session_code, qr_code=qr_base64, host_id=session.host_id)

@router.post("/join")
async def join_session(join: SessionJoin, db: Session = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == join.session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": f"User {join.user_id} joined session {join.session_code}", "host_id": db_session.host_id}