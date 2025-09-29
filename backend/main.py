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
import requests
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

# Music Service Class
class MusicService:
    @staticmethod
    def search_youtube(query: str, limit: int = 10):
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return {"error": "YouTube API key not configured"}
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{query} official audio",
            "type": "video",
            "videoCategoryId": "10",  # Music category
            "maxResults": limit,
            "key": api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "error" in data:
                return {"error": data["error"]["message"]}
            
            results = []
            for item in data.get("items", []):
                # Clean up title (remove channel names and extra text)
                title = item["snippet"]["title"]
                # Remove common YouTube suffixes
                for suffix in ["(Official Audio)", "(Official Video)", "(Official Music Video)", "| Official Audio"]:
                    title = title.replace(suffix, "").strip()
                
                results.append({
                    "id": item["id"]["videoId"],
                    "title": title,
                    "artist": item["snippet"]["channelTitle"],
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                    "source": "youtube"
                })
            
            return {"results": results}
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def search_deezer(query: str, limit: int = 10):
        url = "https://api.deezer.com/search"
        params = {"q": query, "limit": limit}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            for track in data.get("data", []):
                results.append({
                    "id": track["id"],
                    "title": track["title"],
                    "artist": track["artist"]["name"],
                    "album": track["album"]["title"],
                    "duration": track["duration"],
                    "preview": track.get("preview"),  # 30-second preview
                    "thumbnail": track["album"]["cover_medium"],
                    "source": "deezer"
                })
            
            return {"results": results}
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_youtube_video_details(video_id: str):
        """Get additional details about a YouTube video"""
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return {"error": "YouTube API key not configured"}
        
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "contentDetails,snippet",
            "id": video_id,
            "key": api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if not data.get("items"):
                return {"error": "Video not found"}
            
            item = data["items"][0]
            
            # Parse duration (ISO 8601 format)
            duration_str = item["contentDetails"]["duration"]
            duration_seconds = MusicService.parse_duration(duration_str)
            
            return {
                "id": video_id,
                "title": item["snippet"]["title"],
                "artist": item["snippet"]["channelTitle"],
                "duration": duration_seconds,
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "description": item["snippet"]["description"]
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def parse_duration(duration_str: str) -> int:
        """Convert ISO 8601 duration to seconds"""
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
        
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        
        return hours * 3600 + minutes * 60 + seconds

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
        host_id=str(uuid.uuid4()),  # Anonymous host ID
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
    queue_items = db.query(QueueItem).filter(
        QueueItem.session_code == session_code,
        QueueItem.played == False
    ).count()
    
    return {
        "session_code": session.session_code,
        "session_name": session.session_name,
        "host_id": session.host_id,
        "participants": [{"username": p.username, "is_host": p.is_host} for p in participants],
        "queue_length": queue_items,
        "created_at": session.created_at.isoformat()
    }

# Music Search Endpoints
@app.get("/api/music/search")
async def search_music(query: str, limit: int = 10):
    """Search across multiple music services"""
    if not query or len(query.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    # Try YouTube first
    youtube_results = MusicService.search_youtube(query, limit)
    
    # If YouTube fails or has quota issues, fall back to Deezer
    if "error" in youtube_results:
        deezer_results = MusicService.search_deezer(query, limit)
        if "error" not in deezer_results:
            return deezer_results
        else:
            # Both services failed, return YouTube error
            raise HTTPException(status_code=500, detail=f"Music search failed: {youtube_results['error']}")
    
    return youtube_results

@app.get("/api/music/details/{video_id}")
async def get_music_details(video_id: str):
    """Get detailed information about a specific track"""
    details = MusicService.get_youtube_video_details(video_id)
    
    if "error" in details:
        raise HTTPException(status_code=404, detail=details["error"])
    
    return details

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
    
    # If duration not provided, try to get it from YouTube
    if not track_duration and track_id.startswith("yt_"):
        video_id = track_id.replace("yt_", "")
        details = MusicService.get_youtube_video_details(video_id)
        if "error" not in details:
            track_duration = details.get("duration")
    
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
            "track_id": track_id,
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
                "is_playing": item.is_playing,
                "created_at": item.created_at.isoformat()
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

@app.post("/api/session/{session_code}/queue/{item_id}/remove")
async def remove_queue_item(session_code: str, item_id: int, db: Session = Depends(get_db)):
    """Remove a track from queue (host only)"""
    queue_item = db.query(QueueItem).filter(
        QueueItem.id == item_id,
        QueueItem.session_code == session_code
    ).first()
    
    if not queue_item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    
    db.delete(queue_item)
    db.commit()
    
    # Broadcast removal
    await manager.broadcast_to_session({
        "type": "queue_updated",
        "message": "Track removed from queue",
        "removed_item_id": item_id
    }, session_code)
    
    return {"message": "Track removed from queue"}

@app.post("/api/session/{session_code}/queue/clear")
async def clear_queue(session_code: str, db: Session = Depends(get_db)):
    """Clear all items from queue (host only)"""
    db.query(QueueItem).filter(QueueItem.session_code == session_code).delete()
    db.commit()
    
    # Broadcast clear
    await manager.broadcast_to_session({
        "type": "queue_cleared",
        "message": "Queue cleared"
    }, session_code)
    
    return {"message": "Queue cleared"}

# Player Control Endpoints
@app.post("/api/session/{session_code}/player/play/{track_id}")
async def play_track(session_code: str, track_id: str, db: Session = Depends(get_db)):
    """Start playing a specific track"""
    session = db.query(DanceSession).filter(DanceSession.session_code == session_code).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Update session's current track
    session.current_track_id = track_id
    db.commit()
    
    # Broadcast play command
    await manager.broadcast_to_session({
        "type": "play_track",
        "track_id": track_id,
        "message": "Now playing"
    }, session_code)
    
    return {"message": "Playing track", "track_id": track_id}

@app.post("/api/session/{session_code}/player/pause")
async def pause_playback(session_code: str):
    """Pause playback"""
    await manager.broadcast_to_session({
        "type": "pause_playback",
        "message": "Playback paused"
    }, session_code)
    
    return {"message": "Playback paused"}

@app.post("/api/session/{session_code}/player/resume")
async def resume_playback(session_code: str):
    """Resume playback"""
    await manager.broadcast_to_session({
        "type": "resume_playback",
        "message": "Playback resumed"
    }, session_code)
    
    return {"message": "Playback resumed"}

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{session_code}")
async def websocket_endpoint(websocket: WebSocket, session_code: str):
    await manager.connect(websocket, session_code)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
            # For now, just echo for testing
            await websocket.send_json({"type": "echo", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_code)

# Health check
@app.get("/")
async def root():
    return {
        "message": "Aura Vibe API is running", 
        "version": "1.0.0",
        "music_services": ["YouTube", "Deezer"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "youtube": "available" if os.getenv("YOUTUBE_API_KEY") else "not_configured",
            "deezer": "available"
        }
    }

# Development endpoint to test music search
@app.get("/api/dev/test-search")
async def test_search(query: str = "drake"):
    """Test endpoint for music search (remove in production)"""
    youtube_results = MusicService.search_youtube(query, 5)
    deezer_results = MusicService.search_deezer(query, 5)
    
    return {
        "youtube": youtube_results,
        "deezer": deezer_results,
        "query": query
    }