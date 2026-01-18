from sqlalchemy import Column, Integer, String
from app.core.database import Base
from pydantic import BaseModel
import uuid

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, unique=True, index=True)
    host_id = Column(String)
    name = Column(String, nullable=True)
    duration = Column(String, nullable=True)

class SessionCreate(BaseModel):
    host_id: str
    name: str | None = None
    duration: str | None = None

class SessionOut(BaseModel):
    session_code: str
    qr_code: str
    host_id: str
    name: str | None = None
    duration: str | None = None

class SessionJoin(BaseModel):
    session_code: str
    user_id: str