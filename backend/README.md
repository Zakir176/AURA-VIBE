# Aura Vibe Backend

The backend for the Aura Vibe collaborative DJ platform, part of a monorepo at D:\code\GitHub\Personal\AURA-VIBE. This FastAPI-based backend handles session creation, user joining, queue management, and real-time updates via WebSocket for a shared music queue.

## Project Overview
- **Goal**: Enable users to join a session via QR code or session code to add songs to a shared queue, with a host playing music (YouTube API planned for MVP).
- **Tech Stack**:
  - **Backend**: FastAPI, SQLite (dev), WebSocket, Python 3.8+.
  - **Frontend** (in progress): Vue 3, Vuetify, to be integrated in ../frontend.
- **Status**: All endpoints and WebSocket are tested and functional.

## Endpoints
- **POST /session/create**: Creates a session. Input: {"host_id": "<uuid>"}. Output: {"session_code": "<8-char-code>", "qr_code": "<base64-png>"}.
- **POST /session/join**: Joins a session. Input: {"session_code": "<code>", "user_id": "<uuid>"}. Output: {"message": "..."}.
- **POST /queue/add**: Adds a song. Input: {"session_code": "<code>", "song_title": "<title>", "song_url": "<youtube-url>", "added_by": "<user_id>"}. Output: {"song_title": "<title>", "song_url": "<url>", "added_by": "<user_id>"}.
- **GET /queue/list/<session_code>**: Lists queue. Output: [{"song_title": "<title>", "song_url": "<url>", "added_by": "<user_id>"}, ...].
- **WebSocket /ws/<session_code>**: Broadcasts {"event": "queue_updated", "song_title": "<title>", "song_url": "<url>", "added_by": "<user_id>"} on queue additions.

## Setup
1. **Navigate to the backend directory**:
   `bash
   cd D:\code\GitHub\Personal\AURA-VIBE\backend
   `
2. **Activate the virtual environment**:
   `bash
   .\venv\Scripts\Activate.ps1
   `
   If no virtual environment exists, create one:
   `bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   `
3. **Install dependencies**:
   `bash
   pip install -r requirements.txt
   `
   Dependencies:
   - fastapi==0.115.0
   - uvicorn==0.30.6
   - sqlalchemy==2.0.35
   - pydantic==2.9.2
   - python-jose==3.3.0
   - qrcode==7.4.2
   - websockets==13.1
4. **Run the server**:
   `bash
   uvicorn app.main:app --reload
   `
   Access at http://localhost:8000.

## Testing
- **Test Endpoints** (using curl or Postman):
  `bash
  # Create session
  curl -X POST http://localhost:8000/session/create -H "Content-Type: application/json" -d "{\"host_id\": \"host123\"}"

  # Join session
  curl -X POST http://localhost:8000/session/join -H "Content-Type: application/json" -d "{\"session_code\": \"<session_code>\", \"user_id\": \"user123\"}"

  # Add to queue
  curl -X POST http://localhost:8000/queue/add -H "Content-Type: application/json" -d "{\"session_code\": \"<session_code>\", \"song_title\": \"Test Song\", \"song_url\": \"https://youtube.com/watch?v=test\", \"added_by\": \"user123\"}"

  # List queue
  curl http://localhost:8000/queue/list/<session_code>
  `
- **Test WebSocket** (using wscat):
  `bash
  npm install -g wscat
  wscat -c ws://localhost:8000/ws/<session_code>
  `
  Send: {"message": "Test update"} or add a song to trigger queue_updated.

## Database
- SQLite database: ura_vibe.db in ackend.
- Tables: sessions, queue.
- Inspect with SQLite CLI or DB Browser for SQLite:
  `sql
  SELECT * FROM sessions;
  SELECT * FROM queue;
  `

## Monorepo Structure
- **Backend**: D:\code\GitHub\Personal\AURA-VIBE\backend (this directory).
- **Frontend**: D:\code\GitHub\Personal\AURA-VIBE\frontend (Vue 3, in progress).
- Root README.md (optional): Create to describe the monorepo.

## Next Steps
- **Frontend Integration**: Develop Vue 3 + Vuetify frontend in ../frontend to connect to http://localhost:8000 and ws://localhost:8000/ws/<session_code>.
- **YouTube API**: Add search endpoint (GET /youtube/search).
- **Queue Voting**: Add voting endpoint (POST /queue/vote).
- **Deployment**: Backend to Render/Heroku, frontend to Vercel.

## Troubleshooting
- **Pylance Errors**: Ensure VS Code uses ackend\venv\Scripts\python.exe (Ctrl+Shift+P, Python: Select Interpreter).
- **WebSocket Errors**: Verify websockets==13.1 is installed (pip show websockets).
- **Database Issues**: Delete ura_vibe.db and restart server to recreate.

For issues, contact the backend developer with server logs or test outputs.
