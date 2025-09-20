import os
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
import requests

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

@router.get("/login")
def login():
    scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
    url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={scopes}"
    )
    return RedirectResponse(url)

@router.get("/callback")
def callback(request: Request, response: Response, code: str = None):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    r = requests.post(token_url, data=payload)
    token_info = r.json()
    access_token = token_info.get("access_token")
    refresh_token = token_info.get("refresh_token")
    # Set tokens in httpOnly cookies
    response = RedirectResponse(FRONTEND_ORIGIN)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)
    return response
