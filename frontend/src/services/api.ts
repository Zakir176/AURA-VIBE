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

    // Handle other potential error scenarios
    if (error.response) {
      // If the error contains a response (i.e., the request was made and the server responded)
      if (error.response.status === 404) {
        console.error('API endpoint not found: ', error.response.config?.url)
      } else if (error.response.status === 500) {
        console.error('Internal Server Error on the backend.')
      }
    } else {
      // If the error doesn't contain a response, it's likely a network error
      console.error('Network error or server did not respond', error)
    }

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
    try {
      const response = await api.post<CreateSessionResponse>('/session/create', { 
        host_id: hostId 
      })
      return response.data
    } catch (error) {
      // You can also handle errors specifically for this API call here if needed
      throw error
    }
  },

  joinSession: async (sessionCode: string, userId: string): Promise<JoinSessionResponse> => {
    try {
      const response = await api.post<JoinSessionResponse>('/session/join', { 
        session_code: sessionCode, 
        user_id: userId 
      })
      return response.data
    } catch (error) {
      // You can also handle errors specifically for this API call here if needed
      throw error
    }
  }
}

export const queueAPI = {
  addSong: async (sessionCode: string, songData: Omit<AddSongRequest, 'session_code'>): Promise<Song> => {
    try {
      const response = await api.post<Song>('/queue/add', {
        session_code: sessionCode,
        ...songData
      })
      return response.data
    } catch (error) {
      // Handle errors specifically for adding a song if needed
      throw error
    }
  },
  
  getQueue: async (sessionCode: string): Promise<Song[]> => {
    try {
      const response = await api.get<Song[]>(`/queue/list/${sessionCode}`)
      return response.data
    } catch (error) {
      // Handle errors specifically for getting the queue if needed
      throw error
    }
  }
}

export interface YouTubeSong {
  videoId: string;
  title: string;
  thumbnail: string;
  url: string;
}

export const youtubeAPI = {
  search: async (query: string, maxResults: number = 5): Promise<YouTubeSong[]> => {
    try {
      const response = await api.get<YouTubeSong[]>('/youtube/search', {
        params: { query, maxResults }
      })
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export default api
