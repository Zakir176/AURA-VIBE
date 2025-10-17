from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.queue import QueueItem, QueueAdd, QueueItemOut
from app.models.session import Session
from app.websocket import manager  # Import the WebSocket manager

router = APIRouter()

@router.post("/add", response_model=QueueItemOut)
async def add_to_queue(item: QueueAdd, db: Session = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == item.session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_item = QueueItem(
        session_code=item.session_code,
        song_title=item.song_title,
        song_url=item.song_url,
        added_by=item.added_by
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Broadcast queue update
    await manager.broadcast(
        item.session_code,
        {
            "event": "queue_updated",
            "song_title": db_item.song_title,
            "song_url": db_item.song_url,
            "added_by": db_item.added_by
        }
    )
    
    return QueueItemOut(
        song_title=db_item.song_title,
        song_url=db_item.song_url,
        added_by=db_item.added_by
    )

@router.get("/list/{session_code}", response_model=list[QueueItemOut])
async def list_queue(session_code: str, db: Session = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    items = db.query(QueueItem).filter(QueueItem.session_code == session_code).all()
    return [
        QueueItemOut(song_title=item.song_title, song_url=item.song_url, added_by=item.added_by)
        for item in items
    ]