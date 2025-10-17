import axios from 'axios'

export const createSession = async (hostId) => {
  try {
    // Replace the URL with your actual backend URL if needed
    const response = await axios.post('http://localhost:8000/session/create', {
      hostId,
    })

    // Returning the session code and QR code from the backend response
    return {
      session_code: response.data.session_code,
      qr_code: response.data.qr_code, // Assuming backend returns base64 encoded QR code
    }
  } catch (error) {
    console.error('Error creating session:', error)
    throw error
  }
}
