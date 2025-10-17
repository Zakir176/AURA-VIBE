# Aura Vibe Frontend - Vue 3 + Vuetify

A collaborative DJ platform frontend built with Vue 3 and Vuetify, allowing users to create and join music sessions with real-time queue management.

## 🚀 Features

- **Session Management**: Create and join music sessions with unique codes
- **QR Code Integration**: Share sessions via QR codes
- **Real-time Updates**: WebSocket integration for live queue updates
- **Responsive Design**: Works on mobile and desktop
- **Modern UI**: Beautiful Vuetify components with dark/light theme support

## 📋 Prerequisites

- Node.js 18+ and npm
- Backend API running (FastAPI backend on port 8000)

## 🛠️ Installation

### 1. Clone and Install Dependencies

```bash
# Create project directory
mkdir aura-vibe-frontend
cd aura-vibe-frontend

# Initialize package.json and install dependencies
npm install vue@^3.4.0 vue-router@^4.2.5 vuetify@^3.5.0 @mdi/font@^7.4.0 axios@^1.6.0 jsqr@^1.4.0 uuid@^9.0.1

npm install --save-dev @vitejs/plugin-vue@^5.0.0 vite@^5.0.0 vite-plugin-vuetify@^2.0.0
```

### 2. Project Structure

Create the following folder structure and add the provided files:

```
aura-vibe-frontend/
├── public/
│   └── index.html
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── QRCodeScanner.vue
│   │   └── SongAddForm.vue
│   ├── views/
│   │   ├── Landing.vue
│   │   ├── CreateSession.vue
│   │   ├── JoinSession.vue
│   │   └── QueueView.vue
│   ├── services/
│   │   ├── api.js
│   │   └── websocket.js
│   ├── plugins/
│   │   └── vuetify.js
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
├── package.json
├── vite.config.js
├── vercel.json
└── README.md
```

### 3. Create index.html

Create `public/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aura Vibe - Collaborative DJ</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

### 4. Create .env file

Create `.env` in the root directory:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

For production, create `.env.production`:

```env
VITE_API_URL=https://your-backend-url.com
VITE_WS_URL=wss://your-backend-url.com
```

## 🏃 Running Locally

### Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

**Important**: Make sure your FastAPI backend is running on `http://localhost:8000`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 🚢 Deployment to Vercel

### Option 1: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production
vercel --prod
```

### Option 2: GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "Import Project"
4. Select your GitHub repository
5. Configure:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_URL`: Your backend API URL
     - `VITE_WS_URL`: Your backend WebSocket URL

### Environment Variables on Vercel

Add these in Vercel Dashboard → Settings → Environment Variables:

```
VITE_API_URL=https://your-backend-url.com
VITE_WS_URL=wss://your-backend-url.com
```

## 📱 Usage Flow

### For Hosts:

1. Click "Create Session"
2. Share the session code or QR code with guests
3. Go to the queue to see added songs
4. Manage the music playback

### For Guests:

1. Click "Join Session"
2. Enter the session code OR scan the QR code
3. Add songs to the queue
4. See real-time updates

## 🔧 Configuration

### API Endpoints Used

The frontend communicates with these backend endpoints:

- `POST /session/create` - Create a new session
- `POST /session/join` - Join an existing session
- `GET /queue/list/{session_code}` - Get queue items
- `POST /queue/add` - Add song to queue
- `WS /ws/{session_code}` - WebSocket for real-time updates

### Customization

#### Change Theme Colors

Edit `src/plugins/vuetify.js`:

```javascript
colors: {
  primary: '#9C27B0',  // Purple
  secondary: '#673AB7', // Deep Purple
  accent: '#E91E63',    // Pink
}
```

#### Modify WebSocket Reconnection

Edit `src/services/websocket.js`:

```javascript
this.maxReconnectAttempts = 5  // Change max attempts
this.reconnectDelay = 3000      // Change delay (ms)
```

## 🐛 Troubleshooting

### Camera Not Working (QR Scanner)

- Ensure HTTPS is used (required for camera access)
- Check browser permissions
- Verify camera is not being used by another app

### WebSocket Connection Issues

- Check if backend WebSocket endpoint is accessible
- Verify CORS settings on backend
- Check browser console for connection errors

### API Errors

- Verify backend is running and accessible
- Check API_URL