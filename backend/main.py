from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.models import SessionLocal, Session as DanceSession, QueueItem, Participant
import random
import string
import uuid
from datetime import datetime
import os
from typing import List, Dict

app = FastAPI(title="Aura Vibe API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://aura-vibe.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_code: str):
        await websocket.accept()
        if session_code not in self.active_connections:
            self.active_connections[session_code] = []
        self.active_connections[session_code].append(websocket)

    def disconnect(self, websocket: WebSocket, session_code: str):
        if session_code in self.active_connections:
            self.active_connections[session_code].remove(websocket)

    async def broadcast_to_session(self, message: dict, session_code: str):
        if session_code in self.active_connections:
            for connection in self.active_connections[session_code]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

# Utility functions
def generate_session_code(db: Session) -> str:
    """Generate a unique 6-character session code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not db.query(DanceSession).filter(DanceSession.session_code == code).first():
            return code

# Session Management Endpoints
@app.post("/api/session/create")
async def create_session(session_name: str = "Aura Vibe Session", db: Session = Depends(get_db)):
    """Create a new session and return session code"""
    session_code = generate_session_code(db)
    
    # Create session
    new_session = DanceSession(
        session_code=session_code,
        host_id=str(uuid.uuid4()),  # Anonymous host ID for now
        session_name=session_name
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "session_code": session_code,
        "session_name": session_name,
        "message": "Session created successfully"
    }

@app.post("/api/session/{session_code}/join")
async def join_session(session_code: str, username: str, db: Session = Depends(get_db)):
    """Join an existing session"""
    session = db.query(DanceSession).filter(
        DanceSession.session_code == session_code,
        DanceSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if user already exists in session
    existing_user = db.query(Participant).filter(
        Participant.session_code == session_code,
        Participant.username == username
    ).first()
    
    if not existing_user:
        # Add user to participants
        new_participant = Participant(
            session_code=session_code,
            user_id=str(uuid.uuid4()),
            username=username
        )
        db.add(new_participant)
        db.commit()
    
    return {
        "session_code": session_code,
        "session_name": session.session_name,
        "username": username,
        "message": "Joined session successfully"
    }

@app.get("/api/session/{session_code}/info")
async def get_session_info(session_code: str, db: Session = Depends(get_db)):
    """Get session information"""
    session = db.query(DanceSession).filter(DanceSession.session_code == session_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    participants = db.query(Participant).filter(Participant.session_code == session_code).all()
    
    return {
        "session_code": session.session_code,
        "session_name": session.session_name,
        "host_id": session.host_id,
        "participants": [{"username": p.username, "is_host": p.is_host} for p in participants],
        "created_at": session.created_at.isoformat()
    }

# Queue Management Endpoints
@app.post("/api/session/{session_code}/queue/add")
async def add_to_queue(
    session_code: str,
    track_id: str,
    track_title: str,
    track_artist: str = None,
    track_duration: int = None,
    added_by: str = "Anonymous",
    db: Session = Depends(get_db)
):
    """Add a track to the session queue"""
    session = db.query(DanceSession).filter(DanceSession.session_code == session_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    new_queue_item = QueueItem(
        session_code=session_code,
        track_id=track_id,
        track_title=track_title,
        track_artist=track_artist,
        track_duration=track_duration,
        added_by=added_by
    )
    
    db.add(new_queue_item)
    db.commit()
    db.refresh(new_queue_item)
    
    # Broadcast queue update to all connected clients
    await manager.broadcast_to_session({
        "type": "queue_updated",
        "message": "New track added to queue",
        "queue_item": {
            "id": new_queue_item.id,
            "track_title": track_title,
            "track_artist": track_artist,
            "added_by": added_by,
            "votes": 0
        }
    }, session_code)
    
    return {"message": "Track added to queue", "queue_item_id": new_queue_item.id}

@app.get("/api/session/{session_code}/queue")
async def get_queue(session_code: str, db: Session = Depends(get_db)):
    """Get current queue for session"""
    queue_items = db.query(QueueItem).filter(
        QueueItem.session_code == session_code,
        QueueItem.played == False
    ).order_by(QueueItem.votes.desc(), QueueItem.created_at.asc()).all()
    
    return {
        "queue": [
            {
                "id": item.id,
                "track_id": item.track_id,
                "track_title": item.track_title,
                "track_artist": item.track_artist,
                "track_duration": item.track_duration,
                "added_by": item.added_by,
                "votes": item.votes,
                "is_playing": item.is_playing
            }
            for item in queue_items
        ]
    }

@app.post("/api/session/{session_code}/queue/{item_id}/vote")
async def vote_queue_item(session_code: str, item_id: int, db: Session = Depends(get_db)):
    """Vote for a queue item"""
    queue_item = db.query(QueueItem).filter(
        QueueItem.id == item_id,
        QueueItem.session_code == session_code
    ).first()
    
    if not queue_item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    queue_item.votes += 1
    db.commit()
    
    # Broadcast vote update
    await manager.broadcast_to_session({
        "type": "vote_updated",
        "queue_item_id": item_id,
        "new_votes": queue_item.votes
    }, session_code)
    
    return {"message": "Vote added", "new_votes": queue_item.votes}

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{session_code}")
async def websocket_endpoint(websocket: WebSocket, session_code: str):
    await manager.connect(websocket, session_code)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_code)

# Health check
@app.get("/")
async def root():
    return {"message": "Aura Vibe API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}