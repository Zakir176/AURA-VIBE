# AURA-VIBE
🎵 AI-powered collaborative DJ system where party guests request songs and ECHO engine creates seamless transitions with beat matching, key harmony, and intelligent mixing. Transform any party into an unforgettable experience!
# 🎵 AURA VIBE
### *AI-Powered Collaborative DJ System*

**Powered by ECHO Intelligence**

Transform any party into an unforgettable experience with crowd-sourced music requests and AI-driven seamless mixing. AURA VIBE lets party guests become co-DJs while our ECHO engine ensures perfect transitions and maintains the perfect vibe.

---

## ✨ What is AURA VIBE?

AURA VIBE is an intelligent DJ system that bridges the gap between crowd participation and professional mixing. Guests submit song requests through a simple web interface, and our ECHO AI engine creates seamless transitions with beat matching, key harmony, and energy flow management.

### 🎯 Core Features

- **🙋‍♂️ Crowd-Sourced Requests**: Guests add songs to the queue via mobile-friendly interface
- **🎛️ AI-Powered Mixing**: ECHO engine handles beat matching, key compatibility, and transition timing
- **📊 Smart Queue Management**: Voting system with intelligent conflict resolution
- **🎨 Vibe Modes**: Chill, Hype, Throwback themes that adapt mixing style
- **📱 Real-Time Updates**: Live queue visibility and party analytics
- **🔊 Professional Output**: High-quality audio streaming ready for any sound system

---

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Party Guests  │────│   AURA VIBE      │────│   Audio Output  │
│   (Requests)    │    │   Web Interface  │    │   (Speakers)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                       ┌────────▼────────┐              │
                       │  Request Queue  │              │
                       │   Management    │              │
                       └────────┬────────┘              │
                                │                        │
                       ┌────────▼────────┐              │
                       │  ECHO AI Engine │──────────────┘
                       │  - Beat Analysis│
                       │  - Key Matching │
                       │  - Transitions  │
                       └─────────────────┘
```

### 🛠️ Tech Stack

**Frontend**
- Vue.js 3 with mobile-first design
- Real-time WebSocket connections
- Progressive Web App (PWA) capabilities

**Backend**
- Node.js with Express framework
- WebSocket server for real-time updates
- RESTful API architecture

**Audio Processing (ECHO Engine)**
- Python-based audio analysis
- Essentia & librosa for music analysis
- Custom transition algorithms
- Real-time audio streaming

**Data & APIs**
- Spotify Web API integration
- PostgreSQL for queue management
- Redis for real-time data caching

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ with pip
- Spotify Developer Account
- PostgreSQL database

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/aura-vibe.git
   cd aura-vibe
   ```

2. **Install dependencies**
   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd ../backend
   npm install

   # ECHO Engine
   cd ../echo-engine
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   ```bash
   cp .env.example .env
   # Configure your Spotify API credentials and database settings
   ```

4. **Database Setup**
   ```bash
   npm run db:migrate
   npm run db:seed
   ```

5. **Start Development Servers**
   ```bash
   # Terminal 1: Frontend
   cd frontend && npm run dev

   # Terminal 2: Backend
   cd backend && npm run dev

   # Terminal 3: ECHO Engine
   cd echo-engine && python main.py
   ```

---

## 🎛️ ECHO Engine Features

The heart of AURA VIBE is our ECHO (Enhanced Collaborative Harmonic Orchestrator) engine:

### 🎵 Audio Analysis
- **Beat Detection**: Precise BPM analysis and grid alignment
- **Key Detection**: Camelot wheel compatibility matching
- **Energy Analysis**: Dynamic mood and intensity tracking
- **Genre Classification**: Smart categorization for better flow

### 🔄 Intelligent Mixing
- **Seamless Transitions**: Auto-generated crossfades and beat drops
- **Harmonic Mixing**: Key-compatible song sequencing
- **Energy Curve Management**: Maintains optimal party energy flow
- **Conflict Resolution**: Handles incompatible song combinations

### 📊 Smart Features
- **Crowd Analytics**: Real-time party mood analysis
- **Predictive Queuing**: Anticipates next best song choices
- **Adaptive Learning**: Improves from successful party sessions

---

## 🎨 Party Modes

### 🌊 **Chill Mode**
- Smooth, extended transitions
- Emphasis on melodic compatibility
- Lower energy threshold management

### 🔥 **Hype Mode**  
- Quick, energetic transitions
- Beat drop synchronization
- High-energy track prioritization

### 🕺 **Throwback Mode**
- Era-aware mixing styles
- Nostalgic transition techniques
- Decade-specific energy patterns

---

## 📱 API Documentation

### Core Endpoints

```javascript
// Add song to queue
POST /api/queue/add
{
  "songId": "spotify:track:xxxxx",
  "requestedBy": "user_name",
  "voteWeight": 1
}

// Get current queue
GET /api/queue/current

// Vote for song
POST /api/queue/vote/:songId
{
  "userId": "user_id",
  "vote": "up" | "down"
}

// Get party analytics
GET /api/analytics/current
```

### WebSocket Events
```javascript
// Real-time queue updates
socket.on('queue:updated', (queue) => {})

// Now playing updates  
socket.on('now:playing', (track) => {})

// Party stats
socket.on('party:stats', (analytics) => {})
```

---

## 🤝 Contributing

We welcome contributions to make AURA VIBE even better! 

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`npm test`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### 📋 Todo List
- [ ] Advanced ML-based transition prediction
- [ ] Multi-room party support
- [ ] Voice announcement system
- [ ] Mobile app (React Native)
- [ ] Integration with hardware DJ controllers
- [ ] Custom sound effects library
- [ ] Party playlist export feature

---

## 🎵 Use Cases

- **House Parties**: Let guests control the music democratically
- **Events & Weddings**: Professional mixing with crowd interaction
- **Bars & Clubs**: Reduce DJ costs while maintaining quality
- **Corporate Events**: Engaging, interactive entertainment
- **Streaming Parties**: Remote collaborative DJ sessions

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Spotify Web API for music data
- Essentia library for audio analysis
- The open-source DJ community for inspiration
- Beta testers who helped shape AURA VIBE

---

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/aura-vibe/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/aura-vibe/discussions)
- 📧 **Email**: auravibe.support@yourdomain.com

---

**Made with ❤️ for party people everywhere**

*Turn up the vibe, let AURA VIBE and ECHO handle the mix!*
