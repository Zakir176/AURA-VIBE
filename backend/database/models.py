from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# SQLite for development, Postgres for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aura_vibe.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String(6), unique=True, index=True, nullable=False)
    host_id = Column(String(255), nullable=False)  # Spotify user ID or anonymous host ID
    session_name = Column(String(100), default="Aura Vibe Session")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    max_participants = Column(Integer, default=50)
    current_track_id = Column(String(255), nullable=True)  # YouTube video ID or track URI

class QueueItem(Base):
    __tablename__ = "queue_items"
    
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String(6), ForeignKey("sessions.session_code"), nullable=False)
    track_id = Column(String(255), nullable=False)  # YouTube video ID
    track_title = Column(String(255), nullable=False)
    track_artist = Column(String(255), nullable=True)
    track_duration = Column(Integer, nullable=True)  # in seconds
    added_by = Column(String(255), nullable=False)  # user ID or username
    votes = Column(Integer, default=0)
    is_playing = Column(Boolean, default=False)
    played = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String(6), ForeignKey("sessions.session_code"), nullable=False)
    user_id = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    is_host = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)