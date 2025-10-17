from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from pydantic import BaseModel

class QueueItem(Base):
    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, ForeignKey("sessions.session_code"))
    song_title = Column(String)
    song_url = Column(String)
    added_by = Column(String)

class QueueAdd(BaseModel):
    session_code: str
    song_title: str
    song_url: str
    added_by: str

class QueueItemOut(BaseModel):
    song_title: str
    song_url: str
    added_by: str