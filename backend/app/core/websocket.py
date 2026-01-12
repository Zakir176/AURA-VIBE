from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_code: str):
        await websocket.accept()
        if session_code not in self.active_connections:
            self.active_connections[session_code] = []
        self.active_connections[session_code].append(websocket)
        print(f"Client connected to session {session_code}. Total: {len(self.active_connections[session_code])}")

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
async def websocket_endpoint(websocket: WebSocket, session_code: str):
    await manager.connect(websocket, session_code)
    try:
        while True:
            data = await websocket.receive_text()
            # Try to parse the received text as JSON
            try:
                message_data = json.loads(data)
                # If it's valid JSON, broadcast it as-is
                await manager.broadcast(session_code, message_data)
            except json.JSONDecodeError:
                # If it's not JSON, wrap it in a message object
                await manager.broadcast(session_code, {"message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_code)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, session_code)
