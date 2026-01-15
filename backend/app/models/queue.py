from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.core.database import Base
from pydantic import BaseModel, Field
from typing import List

# SQLAlchemy Model
class Queue(Base):
    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(String, nullable=False)
    session_code = Column(String, ForeignKey("sessions.session_code"), nullable=False)
    song_title = Column(String, nullable=False)
    artist_name = Column(String, nullable=True) # Added field
    song_url = Column(String, nullable=False)
    image = Column(String, nullable=False)
    added_by = Column(String, nullable=False)
    votes = Column(Integer, default=0, nullable=False)
    played = Column(Boolean, default=False, nullable=False)
    position = Column(Integer, default=0, nullable=False)

    def to_dict(self):
        return {
            "id": self.song_id, # Jamendo ID
            "queue_id": self.id, # Queue DB ID
            "name": self.song_title,
            "artist_name": self.artist_name,
            "audio": self.song_url,
            "image": self.image,
            "added_by": self.added_by,
            "votes": self.votes,
            "played": self.played,
            "position": self.position,
        }

class UserVote(Base):
    __tablename__ = "user_votes"
    user_id = Column(String, primary_key=True, index=True)
    queue_id = Column(Integer, ForeignKey("queue.id"), primary_key=True)
    vote_type = Column(Boolean, nullable=False) # True for upvote, False for downvote

# Pydantic Models (Schemas)

# For API Responses to match frontend expectations
class SongResponse(BaseModel):
    id: int
    song_id: str
    name: str = Field(alias='song_title')
    artist_name: str | None = None
    audio: str = Field(alias='song_url')
    image: str
    added_by: str
    votes: int
    user_vote_type: bool | None = None # True for upvote, False for downvote, None if no vote

    class Config:
        from_attributes = True
        populate_by_name = True


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