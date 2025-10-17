import { ref, onUnmounted } from 'vue'

export interface WebSocketMessage {
  type: string
  data?: any
}

export function useWebSocket(sessionCode: string) {
  const messages = ref<WebSocketMessage[]>([])
  const isConnected = ref(false)
  const error = ref<string | null>(null)
  
  let ws: WebSocket | null = null
  let reconnectAttempts = 0
  const maxReconnectAttempts = 5

  const connect = (): Promise<void> => {
    return new Promise((resolve, reject) => {
      if (!sessionCode) {
        error.value = 'Session code is required'
        reject(new Error('Session code is required'))
        return
      }

      try {
        ws = new WebSocket(`ws://localhost:8000/ws/${sessionCode}`)
        
        ws.onopen = () => {
          console.log('✅ WebSocket connected for session:', sessionCode)
          isConnected.value = true
          error.value = null
          reconnectAttempts = 0
          resolve()
        }
        
        ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data)
            messages.value.push(message)
            
            // Emit custom event for specific message types
            if (message.type === 'queue_updated') {
              window.dispatchEvent(new CustomEvent('queue-updated', { 
                detail: { sessionCode } 
              }))
            }
            
            console.log('📨 WebSocket message:', message)
          } catch (err) {
            console.error('❌ Error parsing WebSocket message:', err)
          }
        }
        
        ws.onclose = (event) => {
          console.log('🔌 WebSocket disconnected:', event.code, event.reason)
          isConnected.value = false
          
          // Attempt reconnect if not a normal closure
          if (event.code !== 1000 && reconnectAttempts < maxReconnectAttempts) {
            setTimeout(() => {
              reconnectAttempts++
              console.log(`🔄 Reconnecting... Attempt ${reconnectAttempts}`)
              connect()
            }, 2000 * reconnectAttempts)
          }
        }
        
        ws.onerror = (event) => {
          console.error('❌ WebSocket error:', event)
          error.value = 'WebSocket connection failed'
          reject(new Error('WebSocket connection failed'))
        }
        
      } catch (err) {
        console.error('❌ Failed to create WebSocket:', err)
        error.value = 'Failed to create WebSocket connection'
        reject(err)
      }
    })
  }

  const disconnect = () => {
    if (ws) {
      ws.close(1000, 'Manual disconnect')
      ws = null
    }
    isConnected.value = false
  }

  const sendMessage = (message: WebSocketMessage) => {
    if (ws && isConnected.value) {
      ws.send(JSON.stringify(message))
    } else {
      console.error('❌ WebSocket not connected')
    }
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    messages,
    isConnected,
    error,
    connect,
    disconnect,
    sendMessage
  }
}