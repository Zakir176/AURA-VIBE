import axios from 'axios'

const API_BASE_URL = '/api'

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
  host_id: string
}

export interface JoinSessionRequest {
  session_code: string
  user_id: string
}

export interface JoinSessionResponse {
  message: string
  host_id: string
}

export interface AddSongPayload {
  id: string
  name: string
  artist_name: string
  audio: string
  image: string
  added_by: string
}

export interface AddSongRequest {
  session_code: string
  song_data: AddSongPayload
}

export interface Song extends AddSongPayload {
  // Any additional properties for a song in the queue can go here
  // For now, it extends AddSongPayload which already contains all necessary fields
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

export const queueAPI = {
  addSong: async (sessionCode: string, songData: AddSongPayload): Promise<Song> => {
    try {
      const response = await api.post<Song>('/queue/add', {
        session_code: sessionCode,
        song_data: songData
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
  },

  vote: async (sessionCode: string, queueId: number, vote: boolean, userId: string): Promise<any> => {
    try {
      const response = await api.post('/queue/vote', {
        session_code: sessionCode,
        queue_id: queueId,
        vote: vote,
        user_id: userId
      })
      return response.data
    } catch (error) {
      throw error
    }
  }
}

export interface JamendoSong {
  id: string; // Jamendo track ID
  name: string; // Track name
  artist_name: string; // Artist name
  audio: string; // URL to the audio file
  image: string; // URL to the track image/thumbnail
  // Add other relevant fields if necessary
}

export const jamendoAPI = {
  search: async (query: string): Promise<JamendoSong[]> => {
    try {
      const response = await api.get<{ tracks: JamendoSong[] }>('/jamendo/search', {
        params: { query }
      })
      return response.data.tracks
    } catch (error) {
      throw error
    }
  }
}



export default api