from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///./aura_vibe.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Session Model
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, unique=True, index=True)
    host_id = Column(String)

# Queue Model (UPDATED with position)
class QueueItem(Base):
    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, ForeignKey("sessions.session_code"))
    song_title = Column(String)
    song_url = Column(String)
    added_by = Column(String)
    votes = Column(Integer, default=0)
    played = Column(Boolean, default=False)
    position = Column(Integer, default=0)  # NEW: For reordering

# User Votes Model
class UserVote(Base):
    __tablename__ = "user_votes"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String)
    queue_id = Column(Integer)
    user_id = Column(String)
    vote_value = Column(Integer)

Base.metadata.create_all(bind=engine)