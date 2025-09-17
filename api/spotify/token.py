from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/api/spotify/token")
async def get_spotify_token(request: Request):
    """Get Spotify access token for Web Playback SDK."""
    access_token = request.cookies.get("sp_access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return JSONResponse({"access_token": access_token})
