from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel

class QueueItem(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, index=True)
    song_title = Column(String)
    song_url = Column(String)
    added_by = Column(String)
    votes = Column(Integer, default=0)  # Added votes column

class QueueAdd(BaseModel):
    session_code: str
    song_title: str
    song_url: str
    added_by: str

class QueueItemOut(BaseModel):
    song_title: str
    song_url: str
    added_by: str
    votes: int  # Include votes in output

    class Config:
        orm_mode = True