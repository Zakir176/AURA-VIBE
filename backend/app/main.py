from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import session, queue, jamendo
from app.core.websocket import router as ws_router
from app.core.database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:8000", "https://aura-vibe.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router, prefix="/session")
app.include_router(queue.router, prefix="/queue")
app.include_router(jamendo.router, prefix="/jamendo")
app.include_router(ws_router)

@app.get("/")
async def root():
    return {"message": "Aura Vibe API"}