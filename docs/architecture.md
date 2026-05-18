# Aura Vibe Architecture

Aura Vibe is a real-time collaborative DJ platform built with a modern monorepo architecture. It enables multiple users to contribute to a shared music queue in real-time.

## System Overview

The system consists of three main parts:
1.  **Backend (FastAPI)**: A high-performance Python API that handles session logic, database management, and WebSocket orchestration.
2.  **Frontend (Vue 3)**: A reactive web application built with TypeScript, Pinia, and Tailwind CSS.
3.  **Database (SQLite)**: A lightweight relational database for storing session state and queue data.

## Data Flow

### 1. Session Management
-   **Creation**: A host creates a session. The backend generates a unique `session_code`, a JWT token, and a QR code.
-   **Joining**: Participants join via `session_code` or by scanning the QR code. They receive a JWT token with their role (`host` or `participant`).

### 2. Music Search & Queue
-   The backend integrates with multiple providers (Jamendo, YouTube) to fetch music metadata.
-   When a user adds a song, it is persisted in the database and broadcasted to all connected clients via WebSockets.

### 3. Real-Time Synchronization
WebSockets are the backbone of the "vibe." They handle:
-   **Queue Updates**: Automatic refreshing of the song list when items are added, voted on, or played.
-   **Playback Sync**: The host broadcasts their player state (current time, play/pause) so all participants see what is currently playing.
-   **Participant Presence**: Live count of active users in a session.

## WebSocket Protocol

All messages are JSON-encoded and follow a type-based structure:

### Client -> Server (JSON)
| Type | Role | Payload | Description |
| :--- | :--- | :--- | :--- |
| `playback_control` | Host | `{ "action": "next" \| "previous" }` | Moves the queue forward/backward. |
| `playback_sync` | Host | `{ "status": "playing" \| "paused", "currentTime": float }` | Synchronizes player state with all clients. |

### Server -> Client (JSON)
| Type | Payload | Description |
| :--- | :--- | :--- |
| `queue_updated` | `{ "queue_id": int, "action": "added" }` | Sent when a new song is added to the queue. |
| `vote_updated` | `{ "queue_id": int, "votes": int }` | Sent when a song's vote count changes. |
| `song_played` | `{ "queue_id": int, "song_title": string }` | Sent when a song starts playing. |
| `playback_sync` | `{ "status": string, "currentTime": float }` | Relayed from the host to all participants. |
| `participant_count_updated` | `{ "count": int }` | Updates the live count of users in the session. |
| `queue_reordered` | `{ "queue": [...] }` | Sent when the queue order changes (manual or smart sort). |

## Database Schema

### `sessions` Table
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Internal ID. |
| `session_code` | String (Unique) | Human-readable code for joining. |
| `host_id` | String | Unique identifier for the host. |
| `name` | String (Nullable) | Optional name for the session. |
| `manual_sort` | Boolean | Whether the host is manually ordering the queue. |

### `queue` Table
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Internal ID. |
| `song_id` | String | External ID (e.g., Jamendo ID). |
| `session_code` | String (FK) | Reference to the session. |
| `song_title` | String | Title of the song. |
| `artist_name` | String | Artist of the song. |
| `song_url` | String | URL to the audio stream. |
| `image` | String | URL to the album/cover image. |
| `added_by` | String | ID of the user who added it. |
| `votes` | Integer | Total vote count. |
| `played` | Boolean | Whether the song has been played. |
| `position` | Integer | Sorting position for manual mode. |

### `user_votes` Table
| Column | Type | Description |
| :--- | :--- | :--- |
| `user_id` | String | Unique ID of the participant. |
| `queue_id` | Integer (FK) | Reference to the queue item. |
| `vote_type` | Boolean | `True` for upvote, `False` for downvote. |

## Role-Based Access Control (RBAC)
-   **Host**: Has full control over the `AudioPlayer`, can skip songs, reorder the queue, and broadcasts sync data.
-   **Participant**: Can search for songs, add them to the queue, and vote on upcoming tracks.

## Future: AI Engine
The `ai-engine/` directory is reserved for future smart features, such as:
-   **Aura-Based Recommendations**: Suggesting songs that match the current "vibe" or mood of the session.
-   **Automated Queueing**: Filling gaps in the queue based on historical session data.
