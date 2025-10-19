from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.queue import QueueItem, QueueAdd, QueueItemOut
from app.models.session import Session
from app.websocket import manager

# Removed duplicate prefix here
router = APIRouter(tags=["queue"])

@router.post("/add", response_model=QueueItemOut)
async def add_to_queue(item: QueueAdd, db: Session = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == item.session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_item = QueueItem(
        session_code=item.session_code,
        song_title=item.song_title,
        song_url=item.song_url,
        added_by=item.added_by,
        votes=0
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    await manager.broadcast(
        item.session_code,
        {
            "event": "queue_updated",
            "song_title": db_item.song_title,
            "song_url": db_item.song_url,
            "added_by": db_item.added_by,
            "votes": db_item.votes
        }
    )
    
    return QueueItemOut(
        song_title=db_item.song_title,
        song_url=db_item.song_url,
        added_by=db_item.added_by,
        votes=db_item.votes
    )

@router.get("/list/{session_code}", response_model=list[QueueItemOut])
async def list_queue(session_code: str, db: Session = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    items = db.query(QueueItem).filter(QueueItem.session_code == session_code).all()
    return [
        QueueItemOut(song_title=item.song_title, song_url=item.song_url, added_by=item.added_by, votes=item.votes)
        for item in items
    ]

@router.post("/vote")
async def vote_song(vote_data: dict, db: Session = Depends(get_db)):
    if not all(key in vote_data for key in ["session_code", "queue_id", "vote", "user_id"]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    item = db.query(QueueItem).filter(QueueItem.id == vote_data["queue_id"]).first()
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    if vote_data["session_code"] != item.session_code:
        raise HTTPException(status_code=400, detail="Invalid session code")
    
    if vote_data["vote"] not in [-1, 1]:
        raise HTTPException(status_code=400, detail="Vote must be 1 or -1")
    
    item.votes = (item.votes or 0) + vote_data["vote"]
    db.commit()
    
    await manager.broadcast(vote_data["session_code"], {
        "event": "vote_updated",
        "queue_id": item.id,
        "song_title": item.song_title,
        "votes": item.votes
    })
    
    return {"queue_id": item.id, "song_title": item.song_title, "votes": item.votes}
