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

    def disconnect(self, websocket: WebSocket, session_code: str):
        if session_code in self.active_connections:
            self.active_connections[session_code].remove(websocket)
            if not self.active_connections[session_code]:
                del self.active_connections[session_code]

    async def broadcast(self, session_code: str, message: dict):
        if session_code in self.active_connections:
            for connection in self.active_connections[session_code]:
                await connection.send_text(json.dumps(message))

manager = ConnectionManager()

@router.websocket("/{session_code}")
async def websocket_endpoint(websocket: WebSocket, session_code: str):
    await manager.connect(websocket, session_code)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast queue updates (e.g., when a song is added)
            await manager.broadcast(session_code, {"message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_code)