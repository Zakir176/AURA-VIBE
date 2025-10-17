import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 API Call: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Success: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error(`❌ API Error:`, error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export interface CreateSessionRequest {
  host_id: string
}

export interface CreateSessionResponse {
  session_code: string
  qr_code: string
}

export interface JoinSessionRequest {
  session_code: string
  user_id: string
}

export interface JoinSessionResponse {
  message: string
}

export interface AddSongRequest {
  session_code: string
  song_title: string
  song_url: string
  added_by: string
}

export interface Song {
  song_title: string
  song_url: string
  added_by: string
}

export const sessionAPI = {
  createSession: async (hostId: string): Promise<CreateSessionResponse> => {
    const response = await api.post<CreateSessionResponse>('/session/create', { 
      host_id: hostId 
    })
    return response.data
  },
  
  joinSession: async (sessionCode: string, userId: string): Promise<JoinSessionResponse> => {
    const response = await api.post<JoinSessionResponse>('/session/join', { 
      session_code: sessionCode, 
      user_id: userId 
    })
    return response.data
  }
}

export const queueAPI = {
  addSong: async (sessionCode: string, songData: Omit<AddSongRequest, 'session_code'>): Promise<Song> => {
    const response = await api.post<Song>('/queue/add', {
      session_code: sessionCode,
      ...songData
    })
    return response.data
  },
  
  getQueue: async (sessionCode: string): Promise<Song[]> => {
    const response = await api.get<Song[]>(`/queue/list/${sessionCode}`)
    return response.data
  }
}

export default api