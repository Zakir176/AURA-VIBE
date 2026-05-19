import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.database import Base, get_db
from app.main import app
from unittest.mock import MagicMock
from app.models.queue import Queue, UserVote  # Import the Queue and UserVote models

# Create a test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestingSessionLocal() as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# ---------------------------------------------------------------------------
# Helper: create a session and return an authenticated TestClient + metadata
# ---------------------------------------------------------------------------
@pytest.fixture(name="authed_client")
def authed_client_fixture(client: TestClient):
    """Creates a live session and returns a client pre-authenticated as the host."""
    create_response = client.post(
        "/session/create",
        json={"name": "Auth Test Session", "duration": "1hr"}
    )
    assert create_response.status_code == 200
    data = create_response.json()
    token = data["token"]
    session_code = data["session_code"]
    host_id = data["host_id"]

    authed = TestClient(app, headers={"Authorization": f"Bearer {token}"})
    # Share the same DB override
    authed.app = client.app  # type: ignore[attr-defined]

    return {
        "client": authed,
        "session_code": session_code,
        "host_id": host_id,
        "token": token,
    }

# ---------------------------------------------------------------------------
# Session tests
# ---------------------------------------------------------------------------

def test_create_session(client: TestClient):
    response = client.post(
        "/session/create",
        json={"name": "Test Session", "duration": "1hr"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "session_code" in data
    assert "qr_code" in data
    assert "host_id" in data
    assert "token" in data
    assert data["name"] == "Test Session"
    assert data["duration"] == "1hr"

def test_join_session(client: TestClient):
    # First, create a session to join
    create_response = client.post(
        "/session/create",
        json={"name": "Joinable Session", "duration": "2hrs"}
    )
    assert create_response.status_code == 200
    session_code = create_response.json()["session_code"]
    host_id = create_response.json()["host_id"]

    # Test successful join
    join_response = client.post(
        "/session/join",
        json={"session_code": session_code}
    )
    assert join_response.status_code == 200
    join_data = join_response.json()
    # Message includes the auto-generated guest_id and session_code
    assert "joined session" in join_data["message"]
    assert session_code in join_data["message"]
    assert join_data["host_id"] == host_id
    assert "token" in join_data

def test_join_non_existent_session(client: TestClient):
    # Test joining a session that does not exist
    non_existent_code = "nonexist"
    join_response = client.post(
        "/session/join",
        json={"session_code": non_existent_code}
    )
    assert join_response.status_code == 404
    assert join_response.json()["detail"] == "Session not found"

def test_get_session(client: TestClient):
    # First, create a session to retrieve
    host_id_expected = None
    session_name = "Session To Get"
    session_duration = "3hrs"
    create_response = client.post(
        "/session/create",
        json={"name": session_name, "duration": session_duration}
    )
    assert create_response.status_code == 200
    session_code = create_response.json()["session_code"]
    host_id_expected = create_response.json()["host_id"]

    # Test successful retrieval
    get_response = client.get(f"/session/{session_code}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["session_code"] == session_code
    assert get_data["qr_code"] == ""
    assert get_data["host_id"] == host_id_expected
    assert get_data["name"] == session_name
    assert get_data["duration"] == session_duration

def test_get_non_existent_session(client: TestClient):
    # Test retrieving a session that does not exist
    non_existent_code = "nonexist"
    get_response = client.get(f"/session/{non_existent_code}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Session not found"

# ---------------------------------------------------------------------------
# Search tests
# ---------------------------------------------------------------------------

def test_search_jamendo_success(client: TestClient, mocker):
    mock_tracks = [
        {"id": "1", "name": "Song 1", "artist_name": "Artist 1", "audio": "url1", "image": "img1"},
        {"id": "2", "name": "Song 2", "artist_name": "Artist 2", "audio": "url2", "image": "img2"},
    ]
    mocker.patch("app.services.jamendo_client.jamendo_client.search_tracks", return_value=(mock_tracks, None))

    response = client.get("/search?query=test&provider=jamendo")
    
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "jamendo"
    assert data["tracks"] == mock_tracks

def test_search_jamendo_error(client: TestClient, mocker):
    mocker.patch("app.services.jamendo_client.jamendo_client.search_tracks", return_value=(None, "Jamendo API Error"))

    response = client.get("/search?query=test&provider=jamendo")
    
    assert response.status_code == 500
    assert response.json()["detail"] == "Jamendo API Error"

def test_search_invalid_provider(client: TestClient):
    response = client.get("/search?query=test&provider=invalid")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid search provider"

def test_search_youtube_success(client: TestClient, mocker):
    # Mock the os.getenv to return a fake API key
    mocker.patch("app.routes.search.YOUTUBE_API_KEY", "fake_key")

    # Mock the youtube service build and its chain of calls
    mock_youtube_instance = MagicMock()
    mock_youtube_instance.search().list().execute.return_value = {
        "items": [
            {
                "id": {"videoId": "yt_video_id_1"},
                "snippet": {
                    "title": "YouTube Song 1",
                    "channelTitle": "YT Channel 1",
                    "thumbnails": {"high": {"url": "http://yt.com/thumb1.jpg"}}
                }
            }
        ]
    }
    mocker.patch("app.routes.search.build", return_value=mock_youtube_instance)

    response = client.get("/search?query=test&provider=youtube")

    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "youtube"
    assert len(data["tracks"]) == 1
    track = data["tracks"][0]
    assert track["id"] == "yt_video_id_1"
    assert track["name"] == "YouTube Song 1"
    assert track["artist_name"] == "YT Channel 1"
    assert track["image"] == "http://yt.com/thumb1.jpg"

def test_search_youtube_no_api_key(client: TestClient, mocker):
    mocker.patch("app.routes.search.YOUTUBE_API_KEY", None)
    response = client.get("/search?query=test&provider=youtube")
    assert response.status_code == 500
    assert response.json()["detail"] == "YouTube API key not configured"

def test_search_spotify_not_implemented(client: TestClient):
    response = client.get("/search?query=test&provider=spotify")
    
    assert response.status_code == 501
    assert response.json()["detail"] == "Spotify search not implemented"

# ---------------------------------------------------------------------------
# Queue tests — all require an authenticated client
# ---------------------------------------------------------------------------

def test_add_song_to_queue_success(authed_client: dict, session: Session):
    ac = authed_client["client"]
    session_code = authed_client["session_code"]

    song_data = {
        "id": "jamendo_id_1",
        "name": "New Song",
        "artist_name": "New Artist",
        "audio": "http://audio.url/new_song.mp3",
        "image": "http://image.url/new_song.jpg",
        "added_by": "user_add_song"
    }

    response = ac.post(
        "/queue/add",
        json={"session_code": session_code, "song_data": song_data}
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["song_title"] == song_data["name"]
    assert data["artist_name"] == song_data["artist_name"]
    assert data["song_url"] == song_data["audio"]
    assert data["image"] == song_data["image"]
    assert data["votes"] == 0
    assert data["user_vote_type"] is None  # Initially no vote

    # Verify the song is in the database
    queue_item = session.query(Queue).filter(
        Queue.session_code == session_code,
        Queue.song_id == song_data["id"]
    ).first()
    assert queue_item is not None
    assert queue_item.song_title == song_data["name"]

def test_add_song_to_non_existent_session(authed_client: dict):
    """Auth passes (valid token for a real session), but the target session_code is different → 403."""
    ac = authed_client["client"]
    song_data = {
        "id": "jamendo_id_2",
        "name": "Another Song",
        "artist_name": "Another Artist",
        "audio": "http://audio.url/another_song.mp3",
        "image": "http://image.url/another_song.jpg",
        "added_by": "user_add_song_fail"
    }
    non_existent_code = "nonexist"

    response = ac.post(
        "/queue/add",
        json={"session_code": non_existent_code, "song_data": song_data}
    )
    # The token is scoped to a different session, so the route returns 403
    assert response.status_code == 403

def test_list_queue_success(authed_client: dict):
    ac = authed_client["client"]
    session_code = authed_client["session_code"]

    song1_data = {"id": "s1", "name": "Song One", "artist_name": "Artist 1", "audio": "url1", "image": "img1", "added_by": "user1"}
    song2_data = {"id": "s2", "name": "Song Two", "artist_name": "Artist 2", "audio": "url2", "image": "img2", "added_by": "user2"}

    ac.post("/queue/add", json={"session_code": session_code, "song_data": song1_data})
    ac.post("/queue/add", json={"session_code": session_code, "song_data": song2_data})

    response = ac.get(f"/queue/list/{session_code}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [d["name"] for d in data]
    assert "Song One" in names
    assert "Song Two" in names

def test_list_empty_queue(authed_client: dict):
    ac = authed_client["client"]
    session_code = authed_client["session_code"]

    response = ac.get(f"/queue/list/{session_code}")

    assert response.status_code == 200
    assert response.json() == []

def test_list_queue_ordered_by_votes(authed_client: dict, session: Session):
    ac = authed_client["client"]
    session_code = authed_client["session_code"]

    song1_data = {"id": "s1_order", "name": "Song One Order", "artist_name": "Artist 1", "audio": "url1", "image": "img1", "added_by": "user1"}
    song2_data = {"id": "s2_order", "name": "Song Two Order", "artist_name": "Artist 2", "audio": "url2", "image": "img2", "added_by": "user2"}

    ac.post("/queue/add", json={"session_code": session_code, "song_data": song1_data})
    song2_response = ac.post("/queue/add", json={"session_code": session_code, "song_data": song2_data})

    # Bump votes for song 2 directly in DB
    song2_queue_id = song2_response.json()["id"]
    db_song2 = session.query(Queue).filter(Queue.id == song2_queue_id).first()
    db_song2.votes = 10
    session.commit()

    response = ac.get(f"/queue/list/{session_code}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Song Two Order"  # Highest votes first
    assert data[1]["name"] == "Song One Order"

# ---------------------------------------------------------------------------
# Vote tests — fixture and tests all use authed client
# ---------------------------------------------------------------------------

@pytest.fixture(name="song_in_queue")
def song_in_queue_fixture(authed_client: dict):
    ac = authed_client["client"]
    session_code = authed_client["session_code"]

    song_data = {
        "id": "s_vote",
        "name": "Song To Vote On",
        "artist_name": "Artist Vote",
        "audio": "url_vote",
        "image": "img_vote",
        "added_by": "user_vote"
    }
    add_response = ac.post("/queue/add", json={"session_code": session_code, "song_data": song_data})
    assert add_response.status_code == 200

    return {
        "client": ac,
        "session_code": session_code,
        "queue_id": add_response.json()["id"],
        "user_id": "voter1"
    }

def test_upvote_song(song_in_queue):
    ac = song_in_queue["client"]
    response = ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == 1
    assert response.json()["user_vote_type"] is True

def test_downvote_song(song_in_queue):
    ac = song_in_queue["client"]
    response = ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": False,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == -1
    assert response.json()["user_vote_type"] is False

def test_revoke_upvote(song_in_queue):
    ac = song_in_queue["client"]
    # First upvote
    ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    # Revoke upvote (same direction again)
    response = ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == 0
    assert response.json()["user_vote_type"] is None

def test_change_vote_from_up_to_down(song_in_queue):
    ac = song_in_queue["client"]
    # First upvote
    ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    # Change to downvote
    response = ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": False,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == -1
    assert response.json()["user_vote_type"] is False

def test_vote_on_non_existent_item(song_in_queue):
    ac = song_in_queue["client"]
    response = ac.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": 9999,  # Non-existent queue_id
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Queue item not found"
