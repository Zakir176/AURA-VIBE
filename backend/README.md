# Aura Vibe Backend
>>
>> Backend for the Aura Vibe collaborative DJ platform in `D:\code\GitHub\Personal\AURA-VIBE`. Handles session creation, QR code generation/scanning, queue management, voting, playback, and real-time updates via WebSocket.
>>
>> ## Project Overview
>> - **Goal**: Users join sessions via QR code/session code to add/vote/play songs (YouTube API for MVP).
>> - **Tech Stack**: FastAPI, SQLite (dev), WebSocket, Python 3.8+.
>> - **Status**: All endpoints and WebSocket tested and working.
>>
>> ## Endpoints
>> | Method | Endpoint                     | Description                     |
>> |--------|------------------------------|---------------------------------|
>> | POST   | `/session/create`            | Create session, returns `session_code`, `qr_code`. |
>> | POST   | `/session/join`              | Join session with `session_code`, `user_id`. |
>> | POST   | `/session/scan`              | Scan QR code image, returns `session_code`. |
>> | POST   | `/queue/add`                 | Add song, broadcasts `queue_updated`. |
>> | GET    | `/queue/list/{session_code}` | List queue items. |
>> | POST   | `/queue/vote`                | Vote on song, prevents duplicates, broadcasts `vote_updated`. |
>> | POST   | `/queue/play`                | Mark song as played (host only), broadcasts `song_played`. |
>> | GET    | `/youtube/search`            | Search YouTube videos (requires API key). |
>> | WS     | `/ws/{session_code}`         | WebSocket for `queue_updated`, `vote_updated`, `song_played` events. |

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
