from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import update, func
from typing import List
from app.core.database import get_db
from app.models.queue import Queue, QueueReorder, AddSongRequest, SongResponse, UserVote
from app.models.session import Session as SessionModel
from app.core.websocket import broadcast_to_session
from app.core.auth import get_current_user, TokenData
import logging

router = APIRouter(tags=["queue"])
logger = logging.getLogger(__name__)

@router.post("/add", response_model=SongResponse)
async def add_to_queue(item: AddSongRequest, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    if current_user.session_code != item.session_code:
        raise HTTPException(status_code=403, detail="Not authorized for this session")

    db_session = db.query(SessionModel).filter(SessionModel.session_code == item.session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    max_pos = db.query(func.max(Queue.position)).filter(Queue.session_code == item.session_code).scalar() or 0
    
    db_item = Queue(
        session_code=item.session_code,
        song_id=item.song_data.id,
        song_title=item.song_data.name,
        artist_name=item.song_data.artist_name,
        song_url=item.song_data.audio,
        image=item.song_data.image,
        added_by=current_user.user_id,
        votes=0,
        played=False,
        position=max_pos + 1
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Broadcast to WebSocket
    await broadcast_to_session(item.session_code, {
        "type": "queue_updated",
        "queue_id": db_item.id,
        "action": "added"
    })
    
    return SongResponse(
        id=db_item.id,
        song_id=db_item.song_id,
        name=db_item.song_title,
        artist_name=db_item.artist_name,
        audio=db_item.song_url,
        image=db_item.image,
        added_by=db_item.added_by,
        votes=db_item.votes,
        user_vote_type=None
    )

@router.get("/list/{session_code}", response_model=List[SongResponse], response_model_by_alias=False)
async def list_queue(session_code: str, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    if current_user.session_code != session_code:
        raise HTTPException(status_code=403, detail="Not authorized for this session")

    db_session = db.query(SessionModel).filter(SessionModel.session_code == session_code).first()
    manual_sort = db_session.manual_sort if db_session else False

    if manual_sort:
        items = db.query(Queue).filter(
            Queue.session_code == session_code,
            Queue.played == False,
            Queue.song_url.isnot(None)
        ).order_by(Queue.position.asc(), Queue.id.asc()).all()
    else:
        items = db.query(Queue).filter(
            Queue.session_code == session_code,
            Queue.played == False,
            Queue.song_url.isnot(None)
        ).order_by(Queue.votes.desc(), Queue.id.asc()).all()
    
    response_items = []
    for item in items:
        user_vote = db.query(UserVote).filter(
            UserVote.user_id == current_user.user_id,
            UserVote.queue_id == item.id
        ).first()
        
        user_vote_type = None
        if user_vote:
            user_vote_type = user_vote.vote_type
            
        response_items.append(SongResponse(
            id=item.id,
            song_id=item.song_id,
            name=item.song_title,
            artist_name=item.artist_name,
            audio=item.song_url,
            image=item.image,
            added_by=item.added_by,
            votes=item.votes,
            user_vote_type=user_vote_type
        ))
    
    return response_items

@router.post("/vote")
async def vote_on_song(vote_data: dict, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    required = ["session_code", "queue_id", "vote"]
    if not all(key in vote_data for key in required):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    if current_user.session_code != vote_data["session_code"]:
        raise HTTPException(status_code=403, detail="Not authorized for this session")
    
    queue_item = db.query(Queue).filter(
        Queue.id == vote_data["queue_id"],
        Queue.session_code == vote_data["session_code"]
    ).first()
    
    if not queue_item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    vote_type = vote_data["vote"] # True for upvote, False for downvote
    
    existing_user_vote = db.query(UserVote).filter(
        UserVote.user_id == current_user.user_id,
        UserVote.queue_id == queue_item.id
    ).first()
    
    new_user_vote_type = None

    if existing_user_vote:
        if existing_user_vote.vote_type == vote_type:
            # User is revoking their vote
            if vote_type: # Was an upvote
                queue_item.votes -= 1
            else: # Was a downvote
                queue_item.votes += 1
            db.delete(existing_user_vote)
            new_user_vote_type = None
        else:
            # User is changing their vote
            if vote_type: # New vote is upvote
                queue_item.votes += 2
            else: # New vote is downvote
                queue_item.votes -= 2
            existing_user_vote.vote_type = vote_type
            db.add(existing_user_vote)
            new_user_vote_type = vote_type
    else:
        # New vote
        if vote_type:
            queue_item.votes += 1
        else:
            queue_item.votes -= 1
        
        new_vote = UserVote(
            user_id=current_user.user_id,
            queue_id=queue_item.id,
            vote_type=vote_type
        )
        db.add(new_vote)
        new_user_vote_type = vote_type
            
    db.commit()
    db.refresh(queue_item)
    
    await broadcast_to_session(vote_data["session_code"], {
        "type": "vote_updated",
        "queue_id": queue_item.id,
        "votes": queue_item.votes
    })
    
    return {"message": "Vote recorded", "votes": queue_item.votes, "user_vote_type": new_user_vote_type}

@router.post("/play")
async def play_song(play_data: dict, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "host":
        raise HTTPException(status_code=403, detail="Only the host can play songs")

    required = ["session_code", "queue_id"]
    if not all(key in play_data for key in required):
        raise HTTPException(status_code=400, detail="Missing required fields")
        
    if current_user.session_code != play_data["session_code"]:
        raise HTTPException(status_code=403, detail="Not authorized for this session")
    
    item = db.query(Queue).filter(
        Queue.id == play_data["queue_id"],
        Queue.session_code == play_data["session_code"]
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    if item.played:
        raise HTTPException(status_code=400, detail="Song already played")
    
    item.played = True
    db.commit()
    
    await broadcast_to_session(play_data["session_code"], {
        "type": "song_played",
        "queue_id": play_data["queue_id"],
        "song_title": item.song_title
    })
    
    return {"message": f"Playing: {item.song_title}"}

@router.post("/reorder")
async def reorder_queue(reorder_data: QueueReorder, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "host":
        raise HTTPException(status_code=403, detail="Only the host can reorder the queue")

    if current_user.session_code != reorder_data.session_code:
        raise HTTPException(status_code=403, detail="Not authorized for this session")

    session = db.query(SessionModel).filter(SessionModel.session_code == reorder_data.session_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    items = db.query(Queue).filter(
        Queue.session_code == reorder_data.session_code,
        Queue.played == False
    ).all()
    
    existing_ids = [item.id for item in items]
    reorder_ids = reorder_data.order
    
    if set(reorder_ids) != set(existing_ids):
        raise HTTPException(status_code=400, detail="Invalid order: missing or extra IDs")
    
    for new_pos, queue_id in enumerate(reorder_ids, 1):
        db.execute(update(Queue)
                  .where(Queue.id == queue_id)
                  .values(position=new_pos))
    
    session.manual_sort = True
    db.commit()
    
    reordered_items = db.query(Queue).filter(
        Queue.session_code == reorder_data.session_code,
        Queue.played == False
    ).order_by(Queue.position).all()
    
    await broadcast_to_session(reorder_data.session_code, {
        "type": "queue_reordered",
        "queue": [{"id": item.id, "song_title": item.song_title, "votes": item.votes} for item in reordered_items]
    })
    
    return {
        "message": "Queue reordered successfully",
        "queue": reordered_items
    }

@router.post("/toggle-smart-sort")
async def toggle_smart_sort(data: dict, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "host":
        raise HTTPException(status_code=403, detail="Only the host can toggle smart sort")
        
    session_code = data.get("session_code")
    enabled = data.get("enabled", True)
    
    if current_user.session_code != session_code:
        raise HTTPException(status_code=403, detail="Not authorized for this session")
        
    db_session = db.query(SessionModel).filter(SessionModel.session_code == session_code).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    db_session.manual_sort = not enabled
    db.commit()
    
    if db_session.manual_sort:
        items = db.query(Queue).filter(
            Queue.session_code == session_code,
            Queue.played == False
        ).order_by(Queue.position.asc(), Queue.id.asc()).all()
    else:
        items = db.query(Queue).filter(
            Queue.session_code == session_code,
            Queue.played == False
        ).order_by(Queue.votes.desc(), Queue.id.asc()).all()
        
    await broadcast_to_session(session_code, {
        "type": "queue_reordered",
        "queue": [{"id": item.id, "song_title": item.song_title, "votes": item.votes} for item in items]
    })
    
    return {"message": "Sort mode updated", "manual_sort": db_session.manual_sort}