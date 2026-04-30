from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from typing import Optional
from pydantic import BaseModel

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-for-aura-vibe-change-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    session_code: str
    role: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        session_code: str = payload.get("session_code")
        role: str = payload.get("role")
        if user_id is None or session_code is None or role is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, session_code=session_code, role=role)
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    return verify_token(credentials.credentials)
