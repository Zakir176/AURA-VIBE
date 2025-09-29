import os
import requests
from fastapi import HTTPException

class MusicService:
    @staticmethod
    def search_youtube(query: str, limit: int = 10):
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return {"error": "YouTube API key not configured"}
        
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": f"{query} official audio",
            "type": "video",
            "videoCategoryId": "10",  # Music category
            "maxResults": limit,
            "key": api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "error" in data:
                return {"error": data["error"]["message"]}
            
            results = []
            for item in data.get("items", []):
                results.append({
                    "id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "artist": item["snippet"]["channelTitle"],
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                    "source": "youtube"
                })
            
            return {"results": results}
            
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def search_deezer(query: str, limit: int = 10):
        url = "https://api.deezer.com/search"
        params = {"q": query, "limit": limit}
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            for track in data.get("data", []):
                results.append({
                    "id": track["id"],
                    "title": track["title"],
                    "artist": track["artist"]["name"],
                    "album": track["album"]["title"],
                    "duration": track["duration"],
                    "preview": track.get("preview"),  # 30-second preview
                    "thumbnail": track["album"]["cover_medium"],
                    "source": "deezer"
                })
            
            return {"results": results}
            
        except Exception as e:
            return {"error": str(e)}