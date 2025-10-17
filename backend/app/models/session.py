from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel
import uuid

# SQLAlchemy Model
class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, unique=True, index=True)
    host_id = Column(String)  # Unique identifier for the host

# Pydantic Models
class SessionCreate(BaseModel):
    host_id: str

class SessionOut(BaseModel):
    session_code: str
    qr_code: str  # Base64 encoded QR code image

class SessionJoin(BaseModel):
    session_code: str
    user_id: str