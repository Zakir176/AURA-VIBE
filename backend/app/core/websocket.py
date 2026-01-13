from fastapi import APIRouter, WebSocket, Depends
from starlette.websockets import WebSocketDisconnect
import json
from app.core.database import get_db
from app.models.session import Session as SessionModel
from sqlalchemy.orm import Session
from app.models.queue import Queue # Need to import Queue model

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.playback_states: dict[str, dict] = {} # New: Stores last playback state per session

    async def connect(self, websocket: WebSocket, session_code: str):
        await websocket.accept()
        if session_code not in self.active_connections:
            self.active_connections[session_code] = []
        self.active_connections[session_code].append(websocket)
        print(f"Client connected to session {session_code}. Total: {len(self.active_connections[session_code])}")
        await self.broadcast(session_code, {
            "type": "participant_count_updated",
            "count": len(self.active_connections[session_code])
        })

    def disconnect(self, websocket: WebSocket, session_code: str):
        if session_code in self.active_connections:
            if websocket in self.active_connections[session_code]:
                self.active_connections[session_code].remove(websocket)
                print(f"Client disconnected from session {session_code}")
            if not self.active_connections[session_code]:
                del self.active_connections[session_code]

    async def broadcast(self, session_code: str, message: dict):
        if session_code in self.active_connections:
            # Create a copy of the list to iterate over, in case a disconnect happens during iteration
            for connection in list(self.active_connections[session_code]):
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    # Optionally remove dead connection here

manager = ConnectionManager()

async def broadcast_to_session(session_code: str, message: dict):
    await manager.broadcast(session_code, message)

@router.websocket("/ws/{session_code}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_code: str,
    db: Session = Depends(get_db) # Inject DB session
):
    await manager.connect(websocket, session_code)
    try:
        # Send initial playback state to newly connected client if available
        if session_code in manager.playback_states:
            await websocket.send_json(manager.playback_states[session_code])

        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                user_id = message_data.get("user_id") # Assuming user_id is sent with message
                
                # Retrieve session to check host
                session = db.query(SessionModel).filter(SessionModel.session_code == session_code).first()

                # Handle playback_control messages
                if message_data.get("type") == "playback_control":
                    if not session or session.host_id != user_id:
                        await websocket.send_json({"type": "error", "message": "Only the host can control playback."})
                        continue
                    
                    action = message_data.get("action")
                    if action == "next":
                        current_queue_items = db.query(Queue).filter(
                            Queue.session_code == session_code,
                            Queue.played == False
                        ).order_by(Queue.votes.desc(), Queue.id.asc()).all()

                        if len(current_queue_items) > 0:
                            song_to_mark_played = current_queue_items[0]
                            song_to_mark_played.played = True
                            db.add(song_to_mark_played)
                            db.commit()
                            
                            updated_queue_items = db.query(Queue).filter(
                                Queue.session_code == session_code,
                                Queue.played == False
                            ).order_by(Queue.votes.desc(), Queue.id.asc()).all()

                            await manager.broadcast(session_code, {
                                "type": "queue_updated",
                                "queue": [item.to_dict() for item in updated_queue_items]
                            })
                        else:
                            await websocket.send_json({"type": "info", "message": "End of Queue"})
                    elif action == "previous":
                        await websocket.send_json({"type": "info", "message": "Previous song functionality not yet fully implemented server-side."})
                
                # Handle playback_sync messages
                elif message_data.get("type") == "playback_sync":
                    if not session or session.host_id != user_id:
                        # Only host can send playback_sync messages for broadcasting
                        await websocket.send_json({"type": "error", "message": "Only the host can send playback sync data."})
                        continue
                    
                    # Store the latest playback state from the host
                    manager.playback_states[session_code] = message_data
                    
                    # Rebroadcast to all other clients (excluding the host sender)
                    await manager.broadcast(session_code, message_data)

                else:
                    # For other messages, just broadcast as before
                    await manager.broadcast(session_code, message_data)

            except json.JSONDecodeError:
                await manager.broadcast(session_code, {"message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_code)
        await manager.broadcast(session_code, {
            "type": "participant_count_updated",
            "count": len(manager.active_connections.get(session_code, []))
        })
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, session_code)
        await manager.broadcast(session_code, {
            "type": "participant_count_updated",
            "count": len(manager.active_connections.get(session_code, []))
        })
