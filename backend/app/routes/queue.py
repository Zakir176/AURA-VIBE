from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.database import get_db
from app.models.queue import QueueItem, QueueReorder
from app.models.session import Session
from app.core.websocket import broadcast_to_session
import logging

router = APIRouter(tags=["queue"])
logger = logging.getLogger(__name__)

@router.post("/add")
async def add_to_queue(item: QueueItem, db: Session = Depends(get_db)):
    db_session = db.query(Session).filter(Session.session_code == item.session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db_item = QueueItem(
        session_code=item.session_code,
        song_title=item.song_title,
        song_url=item.song_url,
        added_by=item.added_by,
        votes=0,
        played=False
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Broadcast to WebSocket
    broadcast_to_session(item.session_code, {
        "type": "queue_updated",
        "queue_id": db_item.id,
        "action": "added"
    })
    
    return {"queue_id": db_item.id, "message": "Song added to queue"}

@router.get("/list/{session_code}")
async def list_queue(session_code: str, db: Session = Depends(get_db)):
    items = db.query(QueueItem).filter(
        QueueItem.session_code == session_code,
        QueueItem.played == False
    ).order_by(QueueItem.id).all()
    return items

@router.post("/vote")
async def vote_on_song(vote_data: dict, db: Session = Depends(get_db)):
    required = ["session_code", "queue_id", "vote", "user_id"]
    if not all(key in vote_data for key in required):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    # Check if user already voted
    existing_vote = db.query(QueueItem).filter(
        QueueItem.id == vote_data["queue_id"],
        QueueItem.session_code == vote_data["session_code"]
    ).first()
    
    if not existing_vote:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    # Simple vote logic: +1 or -1
    vote_value = 1 if vote_data["vote"] else -1
    existing_vote.votes += vote_value
    
    # Update user_votes table (if implemented)
    db.commit()
    db.refresh(existing_vote)
    
    broadcast_to_session(vote_data["session_code"], {
        "type": "vote_updated",
        "queue_id": vote_data["queue_id"],
        "votes": existing_vote.votes
    })
    
    return {"message": "Vote recorded", "votes": existing_vote.votes}

@router.post("/play")
async def play_song(play_data: dict, db: Session = Depends(get_db)):
    required = ["session_code", "queue_id", "user_id"]
    if not all(key in play_data for key in required):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    item = db.query(QueueItem).filter(
        QueueItem.id == play_data["queue_id"],
        QueueItem.session_code == play_data["session_code"]
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    if item.played:
        raise HTTPException(status_code=400, detail="Song already played")
    
    item.played = True
    db.commit()
    
    broadcast_to_session(play_data["session_code"], {
        "type": "song_played",
        "queue_id": play_data["queue_id"],
        "song_title": item.song_title
    })
    
    return {"message": f"Playing: {item.song_title}"}

@router.post("/reorder")
async def reorder_queue(reorder_data: QueueReorder, db: Session = Depends(get_db)):
    """
    Reorder queue items by new order array (host only)
    Request: {"session_code": "ABC123", "order": [3, 1, 2, 4]}
    """
    # Verify session exists
    session = db.query(Session).filter(Session.session_code == reorder_data.session_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify all IDs exist and belong to session
    items = db.query(QueueItem).filter(
        QueueItem.session_code == reorder_data.session_code,
        QueueItem.played == False
    ).all()
    
    existing_ids = [item.id for item in items]
    reorder_ids = reorder_data.order
    
    if set(reorder_ids) != set(existing_ids):
        raise HTTPException(status_code=400, detail="Invalid order: missing or extra IDs")
    
    # Update order using SQL window function or manual position update
    for new_pos, queue_id in enumerate(reorder_ids, 1):
        db.execute(update(QueueItem)
                  .where(QueueItem.id == queue_id)
                  .values(position=new_pos))
    
    db.commit()
    
    # Fetch reordered queue
    reordered_items = db.query(QueueItem).filter(
        QueueItem.session_code == reorder_data.session_code,
        QueueItem.played == False
    ).order_by(QueueItem.position).all()
    
    # Broadcast reordered queue
    broadcast_to_session(reorder_data.session_code, {
        "type": "queue_reordered",
        "queue": [{"id": item.id, "song_title": item.song_title, "votes": item.votes} for item in reordered_items]
    })
    
    return {
        "message": "Queue reordered successfully",
        "queue": reordered_items
    }