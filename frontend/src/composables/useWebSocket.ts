// src/composables/useWebSocket.ts
import { ref, onUnmounted } from 'vue';
import { useToast } from './useToast';

export function useWebSocket(sessionCode: string) {
  const isConnected = ref(false);
  const ws = ref<WebSocket | null>(null);
  const reconnectAttempts = ref(0);
  const maxReconnectAttempts = 5;
  const reconnectInterval = ref<number | null>(null);

  const toast = useToast();

  const connect = () => {
    try {
      // Close existing connection
      if (ws.value) {
        ws.value.close();
      }

      // Create new WebSocket connection
      // In development, we use the Vite proxy at /ws which forwards to the backend
      // In production, we use the direct backend URL
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = import.meta.env.DEV ? window.location.host : 'aura-vibe.onrender.com';
      const wsUrl = `${protocol}//${host}/ws/${sessionCode}`;

      console.log(`🔌 Connecting to WebSocket: ${wsUrl}`);
      ws.value = new WebSocket(wsUrl);

      ws.value.onopen = () => {
        console.log('✅ WebSocket connected');
        isConnected.value = true;
        reconnectAttempts.value = 0;
      };

      ws.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 WebSocket message received:', data);

          // Handle different message types
          if (data.type === 'queue_updated' || data.type === 'vote_updated' || data.type === 'queue_reordered') {
            // Dispatch custom event for queue updates
            window.dispatchEvent(new CustomEvent('queue-updated', {
              detail: data
            }));
          } else if (data.type === 'playback_control') {
            // Dispatch custom event for playback controls
             window.dispatchEvent(new CustomEvent('playback-control', {
              detail: data
            }));
          } else if (data.type === 'playback_sync') {
             window.dispatchEvent(new CustomEvent('playback-sync', {
              detail: data
            }));
          } else if (data.type === 'user_joined') {
            toast.info('User Joined', `${data.username || 'A user'} joined the session`);
          } else if (data.type === 'song_added') {
            toast.success('Song Added', `"${data.song_title}" was added to the queue`);
          }
        } catch (error) {
          console.error('❌ Error parsing WebSocket message:', error);
        }
      };

      ws.value.onclose = (event) => {
        console.log(`🔌 WebSocket disconnected: ${event.code}`);
        isConnected.value = false;

        // Only attempt reconnect if it wasn't a normal closure
        if (event.code !== 1000 && reconnectAttempts.value < maxReconnectAttempts) {
          attemptReconnect();
        }
      };

      ws.value.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        isConnected.value = false;
        // Don't show toast on every error retry, it's annoying
        if (reconnectAttempts.value === maxReconnectAttempts) {
             toast.error('Connection Error', 'Failed to connect to live updates');
        }
      };

    } catch (error) {
      console.error('❌ WebSocket connection failed:', error);
      isConnected.value = false;
    }
  };

  const attemptReconnect = () => {
    if (reconnectAttempts.value < maxReconnectAttempts) {
      reconnectAttempts.value++;
      const delay = Math.min(1000 * reconnectAttempts.value, 10000); // Exponential backoff max 10s

      console.log(`🔄 Reconnecting... Attempt ${reconnectAttempts.value} in ${delay}ms`);

      reconnectInterval.value = window.setTimeout(() => {
        connect();
      }, delay);
    } else {
      console.log('❌ Max reconnection attempts reached');
      toast.warning('Connection Lost', 'Live updates disabled. Refresh to reconnect.');
    }
  };

  const disconnect = () => {
    if (reconnectInterval.value) {
      clearTimeout(reconnectInterval.value);
      reconnectInterval.value = null;
    }

    if (ws.value) {
      ws.value.close(1000, 'Normal closure');
      ws.value = null;
    }

    isConnected.value = false;
    console.log('🔌 WebSocket manually disconnected');
  };

  const sendMessage = (message: any) => {
    if (ws.value && isConnected.value) {
      try {
        ws.value.send(JSON.stringify(message));
      } catch (error) {
        console.error('❌ Error sending WebSocket message:', error);
      }
    }
  };

  onUnmounted(() => {
    disconnect();
  });

  return {
    isConnected,
    connect,
    disconnect,
    sendMessage
  };
}
