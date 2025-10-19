from fastapi import APIRouter, HTTPException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter(prefix="/youtube", tags=["youtube"])
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@router.get("/search")
async def search_youtube(query: str, maxResults: int = 10):
    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="YouTube API key not configured")
    
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    try:
        response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=maxResults,
            type="video"
        ).execute()
        return [
            {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                "url": f"https://youtube.com/watch?v={item['id']['videoId']}"
            }
            for item in response["items"]
        ]
    except HttpError as e:
        raise HTTPException(status_code=500, detail=f"YouTube API error: {str(e)}")