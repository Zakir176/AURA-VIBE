import axios from 'axios'
import { useSessionStore } from '@/stores/session'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

// Request interceptor for logging and auth
api.interceptors.request.use(
  (config) => {
    try {
      const sessionStore = useSessionStore()
      if (sessionStore.token) {
        config.headers.Authorization = `Bearer ${sessionStore.token}`
      }
    } catch {
      // Ignore if pinia is not yet initialized
    }
    
    console.log(`🔄 API Call: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Success: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    // Log the detailed error
    console.error('❌ API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    })

    // Handle specific connection refused errors (e.g., backend server not running)
    if (error.code === 'ECONNREFUSED') {
      alert('Backend server is not running. Please start the backend on localhost:8000')
    }

    if (error.response) {
      if (error.response.status === 404) {
        console.error('API endpoint not found: ', error.response.config?.url)
      } else if (error.response.status === 500) {
        console.error('Internal Server Error on the backend.')
      } else if (error.response.status === 401 || error.response.status === 403) {
        console.error('Authentication Error. Please re-join the session.')
      }
    } else {
      console.error('Network error or server did not respond', error)
    }

    return Promise.reject(error)
  }
)

export interface CreateSessionRequest {
  name?: string
  duration?: string
}

export interface CreateSessionResponse {
  session_code: string
  qr_code: string
  name?: string
  duration?: string
  token: string
}

export interface JoinSessionRequest {
  session_code: string
}

export interface JoinSessionResponse {
  message: string
  token: string
}

export const sessionAPI = {
  createSession: async (data: CreateSessionRequest): Promise<CreateSessionResponse> => {
    try {
      const response = await api.post<CreateSessionResponse>('/session/create', data)
      return response.data
    } catch (error) {
      throw error
    }
  },

  joinSession: async (sessionCode: string): Promise<JoinSessionResponse> => {
    try {
      const response = await api.post<JoinSessionResponse>('/session/join', {
        session_code: sessionCode
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  getSession: async (sessionCode: string): Promise<CreateSessionResponse> => {
    try {
      const response = await api.get<CreateSessionResponse>(`/session/${sessionCode}`)
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export interface RawQueueItem {
  song_id: string
  id: number
  name: string
  artist_name: string
  audio: string
  image: string
  added_by: string
  votes: number
  user_vote_type?: boolean | null
}

export const queueAPI = {
  addSong: async (sessionCode: string, songData: AddSongPayload): Promise<Song> => {
    try {
      const response = await api.post<Song>('/queue/add', {
        session_code: sessionCode,
        song_data: songData
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  getQueue: async (sessionCode: string): Promise<Song[]> => {
    try {
      const response = await api.get<RawQueueItem[]>(`/queue/list/${sessionCode}`)
      return response.data.map(item => ({
        id: item.song_id,
        queue_id: item.id,
        name: item.name,
        artist_name: item.artist_name,
        audio: item.audio,
        image: item.image,
        added_by: item.added_by,
        votes: item.votes,
        user_vote_type: item.user_vote_type
      }));
    } catch (error) {
      throw error
    }
  },

  vote: async (sessionCode: string, queueId: number, vote: boolean): Promise<unknown> => {
    try {
      const response = await api.post('/queue/vote', {
        session_code: sessionCode,
        queue_id: queueId,
        vote: vote
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  playSong: async (sessionCode: string, queueId: number): Promise<unknown> => {
    try {
      const response = await api.post('/queue/play', {
        session_code: sessionCode,
        queue_id: queueId
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  reorderQueue: async (sessionCode: string, order: number[]): Promise<unknown> => {
    try {
      const response = await api.post('/queue/reorder', {
        session_code: sessionCode,
        order: order
      })
      return response.data
    } catch (error) {
      throw error
    }
  },

  toggleSmartSort: async (sessionCode: string, enabled: boolean): Promise<unknown> => {
    try {
      const response = await api.post('/queue/toggle-smart-sort', {
        session_code: sessionCode,
        enabled: enabled
      })
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export interface SearchSong {
  id: string;
  name: string;
  artist_name: string;
  audio: string;
  image: string;
}

export interface AddSongPayload {
  id: string
  name: string
  artist_name: string
  audio: string
  image: string
}

export interface Song {
  id: string
  queue_id: number
  name: string
  artist_name: string
  audio: string
  image: string
  added_by: string
  votes: number
  user_vote_type?: boolean | null
}

export type JamendoSong = SearchSong

export const searchAPI = {
  search: async (query: string, provider: string): Promise<SearchSong[]> => {
    try {
      const response = await api.get<{ tracks: SearchSong[] }>('/search', {
        params: { query, provider }
      });
      return response.data.tracks;
    } catch (error) {
      throw error;
    }
  }
};

export default api