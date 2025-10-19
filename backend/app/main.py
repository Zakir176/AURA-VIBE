from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import session, queue, youtube
from app.websocket import router as ws_router
from app.database import Base, engine

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router, prefix="/session")
app.include_router(queue.router, prefix="/queue")
app.include_router(youtube.router, prefix="/youtube")
app.include_router(ws_router)

@app.get("/")
async def root():
    return {"message": "Aura Vibe API"}