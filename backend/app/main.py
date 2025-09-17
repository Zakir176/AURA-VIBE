from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
import os
import urllib.parse
from dotenv import load_dotenv
import time
import base64
import json
import requests


load_dotenv()  # load .env if present

app = FastAPI(title="AURA-VIBE API")

# CORS
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", f"{FRONTEND_ORIGIN.rstrip('/')}/auth/spotify/callback")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:3000", "http://localhost:5173", "https://aura-vibe.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


def _encode_state(state: dict) -> str:
    return urllib.parse.quote(json.dumps(state, separators=(",", ":")))


@app.get("/api/auth/spotify/login")
async def spotify_login(redirect: str | None = None):
    """Redirect user to Spotify authorize with server-managed state."""
    scopes = [
        "user-read-email",
        "user-read-private",
    ]
    state = {"redirectTo": redirect or "/"}
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": " ".join(scopes),
        "state": _encode_state(state),
    }
    url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    return RedirectResponse(url)


@app.get("/api/auth/spotify/callback")
async def spotify_callback(code: str | None = None, state: str | None = None, error: str | None = None):
    """Exchange authorization code for tokens and set httpOnly cookies, then redirect back to the app."""
    redirect_to = "/"
    if state:
        try:
            decoded = json.loads(urllib.parse.unquote(state))
            if isinstance(decoded, dict) and decoded.get("redirectTo"):
                redirect_to = str(decoded["redirectTo"]) or "/"
        except Exception:
            pass

    if error or not code:
        fail_url = f"{FRONTEND_ORIGIN.rstrip('/')}/login?error=spotify_auth_failed"
        return RedirectResponse(fail_url)

    # Exchange code for tokens
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    resp = requests.post(token_url, data=data, headers=headers, timeout=15)
    if resp.status_code != 200:
        fail_url = f"{FRONTEND_ORIGIN.rstrip('/')}/login?error=spotify_token_exchange_failed"
        return RedirectResponse(fail_url)
    token_payload = resp.json()

    access_token = token_payload.get("access_token")
    refresh_token = token_payload.get("refresh_token")
    expires_in = int(token_payload.get("expires_in", 3600))
    expires_at = int(time.time()) + expires_in

    # Redirect back to frontend and also set cookies
    dest = f"{FRONTEND_ORIGIN.rstrip('/')}{redirect_to}"
    r = RedirectResponse(dest)
    # Secure cookie settings; adjust domain as needed in production
    cookie_kwargs = {"httponly": True, "secure": True, "samesite": "lax", "path": "/"}
    r.set_cookie("sp_access_token", access_token or "", max_age=expires_in, **cookie_kwargs)
    if refresh_token:
        r.set_cookie("sp_refresh_token", refresh_token, max_age=60 * 60 * 24 * 30, **cookie_kwargs)
    r.set_cookie("sp_expires_at", str(expires_at), max_age=expires_in, **cookie_kwargs)
    return r


@app.get("/api/auth/session")
async def auth_session(request: Request):
    access_token = request.cookies.get("sp_access_token")
    expires_at = request.cookies.get("sp_expires_at")
    try:
        expires_at_int = int(expires_at) if expires_at else 0
    except Exception:
        expires_at_int = 0
    is_auth = bool(access_token) and (expires_at_int == 0 or time.time() < expires_at_int)
    return JSONResponse({
        "authenticated": is_auth,
        "expiresAt": expires_at_int
    })


@app.post("/api/auth/logout")
async def auth_logout():
    r = JSONResponse({"ok": True})
    cookie_kwargs = {"httponly": True, "secure": True, "samesite": "lax", "path": "/"}
    r.set_cookie("sp_access_token", "", max_age=0, **cookie_kwargs)
    r.set_cookie("sp_refresh_token", "", max_age=0, **cookie_kwargs)
    r.set_cookie("sp_expires_at", "0", max_age=0, **cookie_kwargs)
    return r


def _get_spotify_headers(request: Request):
    """Get Spotify API headers with access token from cookies."""
    access_token = request.cookies.get("sp_access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"Authorization": f"Bearer {access_token}"}


@app.get("/api/spotify/token")
async def get_spotify_token(request: Request):
    """Return access token from cookies for Web Playback SDK (local parity with serverless)."""
    access_token = request.cookies.get("sp_access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return JSONResponse({"access_token": access_token})


@app.get("/api/spotify/search")
async def spotify_search(request: Request, q: str, type: str = "track", limit: int = 20):
    """Search for tracks, artists, albums, or playlists."""
    headers = _get_spotify_headers(request)
    params = {"q": q, "type": type, "limit": limit}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return response.json()


@app.get("/api/spotify/me/playlists")
async def get_user_playlists(request: Request, limit: int = 20):
    """Get user's playlists."""
    headers = _get_spotify_headers(request)
    params = {"limit": limit}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return response.json()


@app.get("/api/spotify/playlists/{playlist_id}/tracks")
async def get_playlist_tracks(request: Request, playlist_id: str, limit: int = 20):
    """Get tracks from a specific playlist."""
    headers = _get_spotify_headers(request)
    params = {"limit": limit}
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return response.json()


@app.get("/api/spotify/me/top/tracks")
async def get_top_tracks(request: Request, time_range: str = "medium_term", limit: int = 20):
    """Get user's top tracks."""
    headers = _get_spotify_headers(request)
    params = {"time_range": time_range, "limit": limit}
    response = requests.get("https://api.spotify.com/v1/me/top/tracks", headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return response.json()


@app.get("/api/spotify/recommendations")
async def get_recommendations(request: Request, seed_tracks: str = "", seed_artists: str = "", limit: int = 20):
    """Get track recommendations."""
    headers = _get_spotify_headers(request)
    params = {"limit": limit}
    if seed_tracks:
        params["seed_tracks"] = seed_tracks
    if seed_artists:
        params["seed_artists"] = seed_artists
    response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return response.json()


@app.put("/api/spotify/player/play")
async def play_track(request: Request, data: dict):
    """Play a track or playlist."""
    headers = _get_spotify_headers(request)
    response = requests.put("https://api.spotify.com/v1/me/player/play", headers=headers, json=data)
    if response.status_code not in [200, 204]:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return {"success": True}


@app.put("/api/spotify/player/pause")
async def pause_playback(request: Request):
    """Pause playback."""
    headers = _get_spotify_headers(request)
    response = requests.put("https://api.spotify.com/v1/me/player/pause", headers=headers)
    if response.status_code not in [200, 204]:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return {"success": True}


@app.get("/api/spotify/player/currently-playing")
async def get_current_playback(request: Request):
    """Get current playback state."""
    headers = _get_spotify_headers(request)
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    if response.status_code == 204:
        return {"is_playing": False}
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Spotify API error")
    return response.json()


@app.get("/")
async def root():
    return JSONResponse({"message": "AURA-VIBE backend running"})


