from fastapi import APIRouter, HTTPException, Depends
from app.services.jamendo_client import jamendo_client, JamendoClient

router = APIRouter()

@router.get("/search")
async def search_tracks(query: str):
    tracks, error = jamendo_client.search_tracks(query)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return {"tracks": tracks}