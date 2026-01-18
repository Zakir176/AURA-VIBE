from fastapi import APIRouter, HTTPException, Query
from app.services.jamendo_client import jamendo_client
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

router = APIRouter()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@router.get("/")
async def search(
    query: str, 
    provider: str = Query("jamendo", enum=["jamendo", "youtube", "spotify"])
):
    if provider == "jamendo":
        tracks, error = jamendo_client.search_tracks(query)
        if error:
            raise HTTPException(status_code=500, detail=error)
        return {"provider": "jamendo", "tracks": tracks}
    
    elif provider == "youtube":
        if not YOUTUBE_API_KEY:
            raise HTTPException(status_code=500, detail="YouTube API key not configured")
        
        try:
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
            
            search_response = youtube.search().list(
                q=query,
                part="snippet",
                maxResults=10,
                type="video",
                topicId="/m/04rlf",  # Music topic
                videoCategoryId="10" # Music category
            ).execute()
            
            tracks = []
            for item in search_response.get("items", []):
                snippet = item["snippet"]
                video_id = item["id"]["videoId"]
                tracks.append({
                    "id": video_id,
                    "name": snippet["title"],
                    "artist_name": snippet["channelTitle"],
                    "audio": f"https://www.youtube.com/watch?v={video_id}",
                    "image": snippet["thumbnails"]["high"]["url"]
                })
            return {"provider": "youtube", "tracks": tracks}

        except HttpError as e:
            raise HTTPException(status_code=e.resp.status, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    elif provider == "spotify":
        # Placeholder for Spotify search logic
        raise HTTPException(status_code=501, detail="Spotify search not implemented")
        
    else:
        raise HTTPException(status_code=400, detail="Invalid search provider")
