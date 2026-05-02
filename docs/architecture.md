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

### Client -> Server
| Type | Role | Action | Description |
| :--- | :--- | :--- | :--- |
| `playback_control` | Host | `next`, `previous` | Moves the queue forward/backward. |
| `playback_sync` | Host | N/A | Synchronizes player state (time, status) with all clients. |

### Server -> Client
| Type | Description |
| :--- | :--- |
| `queue_updated` | Sent when the queue content or order changes. |
| `playback_sync` | Relayed from the host to all participants. |
| `participant_count_updated` | Sent when users join or leave the WebSocket. |
| `song_added` | Notification that a new track was added. |

## Role-Based Access Control (RBAC)
-   **Host**: Has full control over the `AudioPlayer`, can skip songs, and broadcasts sync data.
-   **Participant**: Can search for songs, add them to the queue, and vote on upcoming tracks.

## Future: AI Engine
The `ai-engine/` directory is reserved for future smart features, such as:
-   **Aura-Based Recommendations**: Suggesting songs that match the current "vibe" or mood of the session.
-   **Automated Queueing**: Filling gaps in the queue based on historical session data.
