import { ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export function useSpotify() {
  const isLoading = ref(false)
  const error = ref(null)

  async function makeRequest(endpoint, options = {}) {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Search for tracks
  async function searchTracks(query, limit = 20) {
    return makeRequest(`/api/spotify/search?q=${encodeURIComponent(query)}&type=track&limit=${limit}`)
  }

  // Get user's playlists
  async function getUserPlaylists() {
    return makeRequest('/api/spotify/me/playlists')
  }

  // Get playlist tracks
  async function getPlaylistTracks(playlistId) {
    return makeRequest(`/api/spotify/playlists/${playlistId}/tracks`)
  }

  // Get user's top tracks
  async function getTopTracks(timeRange = 'medium_term', limit = 20) {
    return makeRequest(`/api/spotify/me/top/tracks?time_range=${timeRange}&limit=${limit}`)
  }

  // Get recommendations
  async function getRecommendations(seedTracks = [], seedArtists = [], limit = 20) {
    const params = new URLSearchParams()
    if (seedTracks.length) params.append('seed_tracks', seedTracks.join(','))
    if (seedArtists.length) params.append('seed_artists', seedArtists.join(','))
    params.append('limit', limit)
    
    return makeRequest(`/api/spotify/recommendations?${params}`)
  }

  // Play a track
  async function playTrack(trackUri) {
    return makeRequest('/api/spotify/player/play', {
      method: 'PUT',
      body: JSON.stringify({ uris: [trackUri] })
    })
  }

  // Play a playlist
  async function playPlaylist(playlistUri, offset = 0) {
    return makeRequest('/api/spotify/player/play', {
      method: 'PUT',
      body: JSON.stringify({ 
        context_uri: playlistUri,
        offset: { position: offset }
      })
    })
  }

  // Pause playback
  async function pausePlayback() {
    return makeRequest('/api/spotify/player/pause', {
      method: 'PUT'
    })
  }

  // Get current playback state
  async function getCurrentPlayback() {
    return makeRequest('/api/spotify/player/currently-playing')
  }

  return {
    isLoading,
    error,
    searchTracks,
    getUserPlaylists,
    getPlaylistTracks,
    getTopTracks,
    getRecommendations,
    playTrack,
    playPlaylist,
    pausePlayback,
    getCurrentPlayback
  }
}
