# Aura Vibe Frontend

The frontend for Aura Vibe is a reactive, real-time web application built with Vue 3. It serves as the interface for both session hosts (who control playback) and participants (who contribute to the queue).

## 🚀 Tech Stack

- **Framework**: [Vue 3](https://vuejs.org/) (Composition API)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **State Management**: [Pinia](https://pinia.vuejs.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Routing**: [Vue Router](https://router.vuejs.org/)
- **Icons**: [Heroicons](https://heroicons.com/)
- **Testing**: [Vitest](https://vitest.dev/) (Unit) & [Playwright](https://playwright.dev/) (E2E)

## ✨ Key Features

### Real-Time Synchronization
Uses a custom `useWebSocket` composable to maintain a persistent connection with the backend. It leverages a browser-native Event Bus (`window.dispatchEvent`) to notify components of queue changes or playback sync without tight coupling.

### Global State Management
- **Session Store**: Tracks the current `session_code`, user `role`, and the live `queue`.
- **Toast Store**: A centralized system for displaying temporary notifications (success, error, info).

### Song Discovery
Integrated search bar that fetches results from multiple providers (Jamendo, YouTube) via the backend API.

### Interactive Queue
Participants can vote on songs to influence their position in the queue, while the host sees additional playback controls.

## 📂 Project Structure

```
src/
├── components/      # UI components (AudioPlayer, SongSearchBar, etc.)
├── composables/     # Reusable logic (useWebSocket, useToast)
├── services/        # API client and communication logic
├── stores/          # Pinia state stores
├── views/           # Page-level components (Landing, SessionPage, etc.)
└── types/           # TypeScript definitions
```

## 🛠️ Development

### Setup
```bash
npm install
```

### Run Locally
```bash
npm run dev
```

### Type-Check
```bash
npm run type-check
```

### Testing
```bash
# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e
```

## 🔌 WebSocket Events
The application listens for several WebSocket events via the `useWebSocket` composable:
- `queue_updated`: Refreshes the song list.
- `playback_sync`: Syncs the local player with the host.
- `participant_count_updated`: Updates the "Live" user indicator.
- `song_added`: Triggers a toast notification.
