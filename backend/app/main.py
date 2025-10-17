from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import session, queue
from app.websocket import router as websocket_router
from app.database import Base, engine

app = FastAPI(title="Aura Vibe API")

# Add CORS middleware - THIS IS WHAT'S MISSING
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",  # Alternative localhost
        "http://localhost:3000",  # React dev server (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

app.include_router(session.router, prefix="/session", tags=["session"])
app.include_router(queue.router, prefix="/queue", tags=["queue"])
app.include_router(websocket_router, prefix="/ws", tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "Aura Vibe API"}

Base.metadata.create_all(bind=engine)