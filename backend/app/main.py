from fastapi import FastAPI
from app.routes import session, queue
from app.websocket import router as websocket_router
from app.database import Base, engine

app = FastAPI(title="Aura Vibe API")

app.include_router(session.router, prefix="/session", tags=["session"])
app.include_router(queue.router, prefix="/queue", tags=["queue"])
app.include_router(websocket_router, prefix="/ws", tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "Aura Vibe API"}

Base.metadata.create_all(bind=engine)