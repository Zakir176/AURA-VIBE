from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/token")
async def get_spotify_token(request: Request):
    """Get Spotify access token for Web Playback SDK."""
    access_token = request.cookies.get("sp_access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return JSONResponse({"access_token": access_token})
