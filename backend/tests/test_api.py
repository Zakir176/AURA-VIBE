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

def test_create_session(client: TestClient):
    host_id = "test_host_id"
    session_name = "Test Session"
    session_duration = "1hr"
    
    response = client.post(
        "/session/create",
        json={"host_id": host_id, "name": session_name, "duration": session_duration}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "session_code" in data
    assert "qr_code" in data
    assert data["host_id"] == host_id
    assert data["name"] == session_name
    assert data["duration"] == session_duration

def test_join_session(client: TestClient):
    # First, create a session to join
    create_response = client.post(
        "/session/create",
        json={"host_id": "host123", "name": "Joinable Session", "duration": "2hrs"}
    )
    assert create_response.status_code == 200
    session_code = create_response.json()["session_code"]

    # Test successful join
    user_id = "user123"
    join_response = client.post(
        "/session/join",
        json={"session_code": session_code, "user_id": user_id}
    )
    assert join_response.status_code == 200
    join_data = join_response.json()
    assert join_data["message"] == f"User {user_id} joined session {session_code}"
    assert join_data["host_id"] == "host123"

def test_join_non_existent_session(client: TestClient):
    # Test joining a session that does not exist
    user_id = "user456"
    non_existent_code = "nonexist"
    join_response = client.post(
        "/session/join",
        json={"session_code": non_existent_code, "user_id": user_id}
    )
    assert join_response.status_code == 404
    assert join_response.json()["detail"] == "Session not found"

def test_get_session(client: TestClient):
    # First, create a session to retrieve
    host_id = "host_to_get"
    session_name = "Session To Get"
    session_duration = "3hrs"
    create_response = client.post(
        "/session/create",
        json={"host_id": host_id, "name": session_name, "duration": session_duration}
    )
    assert create_response.status_code == 200
    session_code = create_response.json()["session_code"]

    # Test successful retrieval
    get_response = client.get(f"/session/{session_code}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["session_code"] == session_code
    # qr_code is not returned in get_session as per current implementation, it's empty string
    assert get_data["qr_code"] == "" 
    assert get_data["host_id"] == host_id
    assert get_data["name"] == session_name
    assert get_data["duration"] == session_duration

def test_get_non_existent_session(client: TestClient):
    # Test retrieving a session that does not exist
    non_existent_code = "nonexist"
    get_response = client.get(f"/session/{non_existent_code}")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Session not found"

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

def test_add_song_to_queue_success(client: TestClient, session: Session):
    # Create a session first
    create_response = client.post(
        "/session/create",
        json={"host_id": "host_add_song", "name": "Add Song Session", "duration": "1hr"}
    )
    assert create_response.status_code == 200
    session_code = create_response.json()["session_code"]

    song_data = {
        "id": "jamendo_id_1",
        "name": "New Song",
        "artist_name": "New Artist",
        "audio": "http://audio.url/new_song.mp3",
        "image": "http://image.url/new_song.jpg",
        "added_by": "user_add_song"
    }

    response = client.post(
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
    assert data["added_by"] == song_data["added_by"]
    assert data["votes"] == 0
    assert data["user_vote_type"] is None # Initially no vote

    # Verify the song is in the database
    queue_item = session.query(Queue).filter(Queue.session_code == session_code, Queue.song_id == song_data["id"]).first()
    assert queue_item is not None
    assert queue_item.song_title == song_data["name"]

def test_add_song_to_non_existent_session(client: TestClient):
    song_data = {
        "id": "jamendo_id_2",
        "name": "Another Song",
        "artist_name": "Another Artist",
        "audio": "http://audio.url/another_song.mp3",
        "image": "http://image.url/another_song.jpg",
        "added_by": "user_add_song_fail"
    }
    non_existent_code = "nonexist"

    response = client.post(
        "/queue/add",
        json={"session_code": non_existent_code, "song_data": song_data}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

def test_list_queue_success(client: TestClient):
    # Create a session and add two songs
    create_response = client.post("/session/create", json={"host_id": "host_list", "name": "List Test", "duration": "1hr"})
    session_code = create_response.json()["session_code"]
    
    song1_data = {"id": "s1", "name": "Song One", "artist_name": "Artist 1", "audio": "url1", "image": "img1", "added_by": "user1"}
    song2_data = {"id": "s2", "name": "Song Two", "artist_name": "Artist 2", "audio": "url2", "image": "img2", "added_by": "user2"}
    
    client.post("/queue/add", json={"session_code": session_code, "song_data": song1_data})
    client.post("/queue/add", json={"session_code": session_code, "song_data": song2_data})

    response = client.get(f"/queue/list/{session_code}?user_id=test_user")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Song One"
    assert data[1]["name"] == "Song Two"

def test_list_empty_queue(client: TestClient):
    # Create a session
    create_response = client.post("/session/create", json={"host_id": "host_empty", "name": "Empty List Test", "duration": "1hr"})
    session_code = create_response.json()["session_code"]
    
    response = client.get(f"/queue/list/{session_code}?user_id=test_user")
    
    assert response.status_code == 200
    assert response.json() == []

def test_list_queue_ordered_by_votes(client: TestClient, session: Session):
    # Create a session and add two songs
    create_response = client.post("/session/create", json={"host_id": "host_vote_order", "name": "Vote Order Test", "duration": "1hr"})
    session_code = create_response.json()["session_code"]
    
    song1_data = {"id": "s1_order", "name": "Song One Order", "artist_name": "Artist 1", "audio": "url1", "image": "img1", "added_by": "user1"}
    song2_data = {"id": "s2_order", "name": "Song Two Order", "artist_name": "Artist 2", "audio": "url2", "image": "img2", "added_by": "user2"}
    
    client.post("/queue/add", json={"session_code": session_code, "song_data": song1_data})
    song2_response = client.post("/queue/add", json={"session_code": session_code, "song_data": song2_data})
    
    # Vote for the second song
    song2_queue_id = song2_response.json()["id"]
    db_song2 = session.query(Queue).filter(Queue.id == song2_queue_id).first()
    db_song2.votes = 10
    session.commit()

    response = client.get(f"/queue/list/{session_code}?user_id=test_user")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Song Two Order"  # Song 2 should be first due to more votes
    assert data[1]["name"] == "Song One Order"

@pytest.fixture(name="song_in_queue")
def song_in_queue_fixture(client: TestClient):
    create_response = client.post("/session/create", json={"host_id": "host_vote", "name": "Vote Test", "duration": "1hr"})
    session_code = create_response.json()["session_code"]
    
    song_data = {"id": "s_vote", "name": "Song To Vote On", "artist_name": "Artist Vote", "audio": "url_vote", "image": "img_vote", "added_by": "user_vote"}
    add_response = client.post("/queue/add", json={"session_code": session_code, "song_data": song_data})
    
    return {"session_code": session_code, "queue_id": add_response.json()["id"], "user_id": "voter1"}

def test_upvote_song(client: TestClient, song_in_queue):
    response = client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == 1
    assert response.json()["user_vote_type"] is True

def test_downvote_song(client: TestClient, song_in_queue):
    response = client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": False,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == -1
    assert response.json()["user_vote_type"] is False

def test_revoke_upvote(client: TestClient, song_in_queue):
    # First upvote
    client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    # Revoke upvote
    response = client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == 0
    assert response.json()["user_vote_type"] is None

def test_change_vote_from_up_to_down(client: TestClient, song_in_queue):
    # First upvote
    client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    # Change to downvote
    response = client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": song_in_queue["queue_id"],
        "vote": False,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 200
    assert response.json()["votes"] == -1
    assert response.json()["user_vote_type"] is False

def test_vote_on_non_existent_item(client: TestClient, song_in_queue):
    response = client.post("/queue/vote", json={
        "session_code": song_in_queue["session_code"],
        "queue_id": 9999,  # Non-existent queue_id
        "vote": True,
        "user_id": song_in_queue["user_id"]
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Queue item not found"
