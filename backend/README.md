# AURA-VIBE Backend (FastAPI)

Quick start:

- Create venv
```bash
python -m venv .venv
# Windows PowerShell
. .venv\\Scripts\\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
```

- Install deps
```bash
pip install -r requirements.txt
```

- Run server
```bash
uvicorn app.main:app --reload --port 8000
```

Environment:
- FRONTEND_ORIGIN (e.g., http://localhost:5173)
- APPLE_REDIRECT_FALLBACK (default: /auth/apple/callback)

Notes:
- Includes a development-only Apple authorize stub at `/api/auth/apple/authorize` that redirects back with mock tokens. Replace with real Apple Music auth later.
