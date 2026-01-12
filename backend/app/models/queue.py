from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base
from pydantic import BaseModel
from typing import List

# SQLAlchemy Model
class Queue(Base):
    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, ForeignKey("sessions.session_code"))
    song_title = Column(String)
    song_url = Column(String)
    image = Column(String)
    added_by = Column(String)
    votes = Column(Integer, default=0)
    played = Column(Boolean, default=False)
    position = Column(Integer, default=0)

# Pydantic Models (Schemas)
class QueueCreate(BaseModel):
    session_code: str
    song_title: str
    song_url: str
    added_by: str

class SongData(BaseModel):
    id: str
    name: str
    artist_name: str
    audio: str
    image: str
    added_by: str

class AddSongRequest(BaseModel):
    session_code: str
    song_data: SongData


class QueueReorder(BaseModel):
    session_code: str
    order: List[int]

class QueueItem(QueueCreate):
    id: int
    votes: int
    played: bool
    position: int

    class Config:
        from_attributes = True