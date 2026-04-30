from fastapi import APIRouter, WebSocket, Depends, Query, status
from starlette.websockets import WebSocketDisconnect
import json
from app.core.database import get_db
from app.models.session import Session as SessionModel
from sqlalchemy.orm import Session
from app.models.queue import Queue
from app.core.auth import verify_token, TokenData

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.playback_states: dict[str, dict] = {}
        self.user_data: dict[WebSocket, TokenData] = {}

    async def connect(self, websocket: WebSocket, session_code: str, token_data: TokenData):
        await websocket.accept()
        if session_code not in self.active_connections:
            self.active_connections[session_code] = []
        self.active_connections[session_code].append(websocket)
        self.user_data[websocket] = token_data
        
        print(f"Client connected to session {session_code} as {token_data.role}. Total: {len(self.active_connections[session_code])}")
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
        if websocket in self.user_data:
            del self.user_data[websocket]

    async def broadcast(self, session_code: str, message: dict):
        if session_code in self.active_connections:
            for connection in list(self.active_connections[session_code]):
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")

manager = ConnectionManager()

async def broadcast_to_session(session_code: str, message: dict):
    await manager.broadcast(session_code, message)

@router.websocket("/ws/{session_code}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_code: str,
    token: str = Query(None),
    db: Session = Depends(get_db)
):
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
        
    try:
        token_data = verify_token(token)
    except Exception as e:
        print(f"Token validation failed: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    if token_data.session_code != session_code:
        print("Token session code mismatch")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, session_code, token_data)
    try:
        if session_code in manager.playback_states:
            await websocket.send_json(manager.playback_states[session_code])

        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                
                if message_data.get("type") == "playback_control":
                    if token_data.role != "host":
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
                
                elif message_data.get("type") == "playback_sync":
                    if token_data.role != "host":
                        await websocket.send_json({"type": "error", "message": "Only the host can send playback sync data."})
                        continue
                    
                    manager.playback_states[session_code] = message_data
                    await manager.broadcast(session_code, message_data)

                else:
                    # Generic broadcasting (e.g., chat, though not implemented yet)
                    pass

            except json.JSONDecodeError:
                pass
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
