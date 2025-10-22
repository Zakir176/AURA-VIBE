from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from pydantic import BaseModel

class QueueItem(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, index=True)
    song_title = Column(String)
    song_url = Column(String)
    added_by = Column(String)
    votes = Column(Integer, default=0)
    played = Column(Boolean, default=False)

class QueueAdd(BaseModel):
    session_code: str
    song_title: str
    song_url: str
    added_by: str

class QueueItemOut(BaseModel):
    queue_id: int
    song_title: str
    song_url: str
    added_by: str
    votes: int
    played: bool

    class Config:
        from_attributes = True  # Updated from orm_mode