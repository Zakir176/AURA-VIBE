from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import session, queue, youtube
from app.websocket import router as ws_router
from app.database import Base, engine


app = FastAPI()

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router, prefix="/session")
app.include_router(queue.router, prefix="/queue")
app.include_router(youtube.router)
app.include_router(ws_router)

@app.get("/")
async def root():
    return {"message": "Aura Vibe API"}

Base.metadata.create_all(bind=engine)