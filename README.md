# Aura Vibe 

Aura Vibe is a real-time collaborative DJ platform where users join music sessions via QR code or session code to add songs to a shared queue, with a host controlling playback (YouTube API planned for MVP). Built as a monorepo with a FastAPI backend and Vue 3 frontend.

[![Status](https://img.shields.io/badge/Backend-Complete-green)](https://github.com/yourusername/auravibe) [![Status](https://img.shields.io/badge/Frontend-In_Progress-yellow)](https://github.com/yourusername/auravibe) [![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## ? Features

### ?? Core Functionality
- **Instant Session Creation**: Start a session with one click.
- **QR Code Sharing**: Share sessions via QR codes or unique codes.
- **YouTube Song Search**: Search for songs on YouTube directly within the app.
- **Real-time Sync**: Live queue updates via WebSocket.
- **Collaborative Queue**: Users add songs to a shared queue.
- **YouTube Integration**: Planned support for YouTube URLs.

### ?? User Experience
- **No Registration**: Join sessions instantly.
- **Mobile-Friendly**: Responsive design (frontend in progress).
- **Simple Joining**: Scan QR code or enter session code.

### ?? Technical Features
- **WebSocket Updates**: Real-time queue synchronization.
- **SQLite Database**: Lightweight storage for sessions and queues.
- **FastAPI Backend**: Modern, high-performance API.
- **Vue 3 Frontend**: In development with Tailwind CSS.

## ??? Monorepo Structure

```
AuraVibe/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── routes/          # API route handlers
│   │   ├── models/          # SQLAlchemy models
│   │   ├── websocket.py     # WebSocket management
│   │   └── database.py      # Database configuration
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variable template
│   └── README.md            # Backend-specific instructions
├── frontend/                # Vue 3 + Tailwind CSS frontend
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── services/        # API service layer
│   │   ├── composables/     # Reusable Vue composables
│   │   ├── router/          # Vue Router
│   │   └── main.ts          # App entry
│   ├── package.json         # Node dependencies
│   └── README.md            # Frontend-specific instructions
├── README.md                # This file
└── LICENSE                  # MIT License
```

## ?? Quick Start

### Prerequisites
- **Node.js**: 18+ (for frontend)
- **Python**: 3.8+ (for backend)
- **Git**: For cloning the repository
- **Modern Browser**: Chrome, Firefox, Safari, or Edge

### Clone the Repository
`bash
git clone https://github.com/yourusername/auravibe.git
cd auravibe
`

### Backend Setup
1. Navigate to the backend directory:
   `bash
   cd backend
   `
2. Create a `.env` file from the example:
   `bash
   cp .env.example .env
   `
3. Add your YouTube API key to the `.env` file.
4. Create and activate a virtual environment:
   `bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows
   # or: source venv/bin/activate  # On macOS/Linux
   `
5. Install dependencies:
   `bash
   pip install -r requirements.txt
   `
6. Run the server:
   `bash
   uvicorn app.main:app --reload
   `
   Backend available at http://localhost:8000.

### Frontend Setup
The frontend is under development. Once complete:
1. Navigate to the frontend directory:
   `bash
   cd frontend
   `
2. Install dependencies:
   `bash
   npm install
   `
3. Run the development server:
   `bash
   npm run dev
   `
   Frontend will be available at http://localhost:5173.

## ?? How to Use

### Creating a Session
1. Send a POST request to create a session:
   `bash
   curl -X POST http://localhost:8000/session/create -H "Content-Type: application/json" -d "{\"host_id\": \"host123\"}"
   `
2. Receive a session_code (e.g., da7fc799) and qr_code (base64 PNG).
3. Share the code or QR code with friends.

### Joining a Session
1. Join with a session code:
   `bash
   curl -X POST http://localhost:8000/session/join -H "Content-Type: application/json" -d "{\"session_code\": \"da7fc799\", \"user_id\": \"user123\"}"
   `

### Managing the Queue
1. Add a song:
   `bash
   curl -X POST http://localhost:8000/queue/add -H "Content-Type: application/json" -d "{\"session_code\": \"da7fc799\", \"song_title\": \"Test Song\", \"song_url\": \"https://youtube.com/watch?v=test\", \"added_by\": \"user123\"}"
   `
2. List the queue:
   `bash
   curl http://localhost:8000/queue/list/da7fc799
   `
3. Connect to WebSocket for real-time updates:
   `bash
   wscat -c ws://localhost:8000/ws/da7fc799
   `

## ??? Development

### Backend Tech Stack
- **FastAPI**: 0.115.0
- **SQLAlchemy**: 2.0.35
- **Pydantic**: 2.9.2
- **Uvicorn**: 0.30.6
- **WebSocket**: websockets 13.1
- **Dependencies**: See ackend/requirements.txt

### Frontend Tech Stack

- **Vue 3**: Composition API

- **Tailwind CSS**: Utility-first CSS framework

- **Pinia**: State management

- **Vue Router**: Client-side routing

- **Axios**: HTTP client

- **uuid**: UUID generation

- **vue-qrcode-reader**: QR code scanning

- **Dependencies**: See `frontend/package.json`

### API Endpoints
| Method | Endpoint                     | Description                     |
|--------|------------------------------|---------------------------------|
| POST   | /session/create            | Create a new music session      |
| POST   | /session/join              | Join an existing session        |
| POST   | /queue/add                 | Add a song to the queue         |
| GET    | /queue/list/{session_code} | Get session queue               |
| GET    | /youtube/search            | Search for a YouTube video      |
| WS     | /ws/{session_code}         | WebSocket for real-time updates |

### Environment Variables
- **Backend**: Create a `.env` file in the `backend` directory. See `.env.example`.
  - `YOUTUBE_API_KEY`: Your Google Cloud YouTube Data API v3 key.
- **Frontend**: The `VITE_API_BASE_URL` is hardcoded to `http://localhost:8000` in `frontend/src/services/api.ts`. This can be changed to a `.env` file if needed.

##  Contributing
1. Fork the repository.
2. Create a feature branch: git checkout -b feature/amazing-feature.
3. Commit changes: git commit -m 'Add amazing feature'.
4. Push: git push origin feature/amazing-feature.
5. Open a Pull Request.

### Guidelines
- Follow PEP 8 for Python (backend).
- Use Vue 3 Composition API (frontend, once implemented).
- Ensure mobile responsiveness.
- Update documentation for changes.

##  Testing
- **Backend**:
  `bash
  # Install pytest
  pip install pytest
  # Run tests (once implemented)
  pytest backend/tests/
  `
  Manual testing:
  `bash
  curl http://localhost:8000
  wscat -c ws://localhost:8000/ws/<session_code>
  `
- **Frontend** (planned):
  `bash
  npm run test:unit  # Unit tests with Vitest (TBD)
  npm run test:e2e   # E2E tests (TBD)
  `

##  Performance
- **Backend**: FastAPI ensures low-latency API responses (< 100ms).
- **WebSocket**: Latency < 100ms for queue updates.
- **Frontend**: Target First Contentful Paint < 1.5s (once implemented).

##  Troubleshooting
- **Backend Errors**:
  - Pylance issues: Select ackend\venv\Scripts\python.exe in VS Code.
  - WebSocket failure: Verify websockets==13.1 (pip show websockets).
  - Database issues: Delete ackend/aura_vibe.db and restart server.
- **Frontend Errors** (once implemented):
  - CORS: Ensure backend is at http://localhost:8000.
  - WebSocket: Check connection to ws://localhost:8000/ws/<session_code>.

For help, open an issue at https://github.com/yourusername/auravibe/issues.

##  License
MIT License - see [LICENSE](LICENSE) for details.

##  Acknowledgments
- FastAPI and Vue.js communities.
- Contributors to the Aura Vibe project.

##  Contact
- Project Lead: [Your Name](mailto:your.email@example.com)
- GitHub: [yourusername](https://github.com/yourusername)

---

<div align='center'>

**Made with  and  for music lovers**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)](https://vuejs.org/)

</div>
