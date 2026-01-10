from fastapi import APIRouter, HTTPException, Depends
from dotenv import load_dotenv
import os
import requests

router = APIRouter()

load_dotenv()
JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")

@router.get("/search")
async def search_tracks(query: str):
    if not JAMENDO_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Jamendo Client ID not configured.")

    base_url = "https://api.jamendo.com/v3.0/tracks/"
    params = {
        "client_id": JAMENDO_CLIENT_ID,
        "format": "json",
        "fuzzysearch": query,
        "limit": 20, # Limit to 20 tracks for search results
        "groupby": "track_name", # Group results by track name to avoid duplicates
        "order": "popularity_desc", # Order by popularity
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data["headers"]["status"] == "success":
            return {"tracks": data["results"]}
        else:
            raise HTTPException(status_code=500, detail=f"Jamendo API error: {data['headers']['error_message']}")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Jamendo API: {e}")
    except KeyError:
        raise HTTPException(status_code=500, detail="Invalid response from Jamendo API.")