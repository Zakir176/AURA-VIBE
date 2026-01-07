<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <router-link to="/" class="flex items-center space-x-3 text-lg font-semibold text-gray-900">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span class="text-white text-sm">🎵</span>
              </div>
              <span>AuraVibe</span>
            </router-link>
            <div class="h-6 w-px bg-gray-300"></div>
            <div>
              <p class="text-sm text-gray-600">Session</p>
              <p class="font-mono font-semibold text-gray-900">{{ sessionCode }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <!-- Connection Status -->
            <div class="flex items-center space-x-2">
              <div 
                :class="[
                  'w-3 h-3 rounded-full',
                  isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
                ]"
              ></div>
              <span class="text-sm text-gray-600">
                {{ isConnected ? 'Live' : 'Disconnected' }}
              </span>
            </div>
            
            <button 
              @click="copySessionCode"
              class="btn-secondary text-sm py-2 px-4"
            >
              Copy Code
            </button>
            <router-link to="/" class="text-gray-600 hover:text-gray-900 text-sm font-medium">
              Leave
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <YouTubePlayer ref="player" v-if="currentVideoId" :video-id="currentVideoId" class="mb-6" />
      <div v-if="isHost" class="card p-4 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Host Controls</h3>
        <div class="flex space-x-2">
          <button @click="hostPlay" class="btn-secondary py-2 px-4">Play</button>
          <button @click="hostPause" class="btn-secondary py-2 px-4">Pause</button>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Queue Section -->
        <div class="lg:col-span-2">
          <div class="card p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-2xl font-bold text-gray-900">Music Queue</h2>
              <button 
                @click="fetchQueue" 
                :disabled="loading"
                class="btn-secondary text-sm py-1 px-3 flex items-center space-x-1"
              >
                <span>🔄</span>
                <span>Refresh</span>
              </button>
            </div>
            
            <!-- Loading State -->
            <div v-if="loading" class="text-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p class="text-gray-600 mt-2">Loading queue...</p>
            </div>
            
            <!-- Empty State -->
            <div v-else-if="queue.length === 0" class="text-center py-12">
              <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl text-gray-400">🎵</span>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">No songs in queue</h3>
              <p class="text-gray-600">Add the first song to get the party started!</p>
            </div>

            <!-- Queue Items -->
            <div v-else class="space-y-3">
              <div 
                v-for="(song, index) in queue" 
                :key="index"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border hover:bg-white transition-colors duration-200"
              >
                <div class="flex items-center space-x-4 flex-1 min-w-0">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <span class="text-blue-600 font-semibold text-sm">{{ index + 1 }}</span>
                  </div>
                  <div class="min-w-0 flex-1">
                    <h3 class="font-semibold text-gray-900 truncate">{{ song.song_title }}</h3>
                    <p class="text-sm text-gray-600 truncate">Added by {{ song.added_by }}</p>
                  </div>
                </div>
                <button 
                  @click="playSong(song)"
                  class="btn-primary text-sm py-2 px-3 flex items-center space-x-1 ml-4 flex-shrink-0"
                >
                  <span>▶️</span>
                  <span>Play</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Song Section -->
        <div class="space-y-6">
          <div class="card p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Add Song</h3>
            <SongSearchBar @select-song="onSongSelected" class="mb-4" />
            <form @submit.prevent="addSong">
              <div class="space-y-4">
                <div>
                  <label for="songTitle" class="block text-sm font-medium text-gray-700 mb-1">
                    Song Title
                  </label>
                  <input
                    id="songTitle"
                    v-model="songTitle"
                    type="text"
                    required
                    class="input-field"
                    placeholder="Enter song name"
                    :disabled="addingSong"
                  >
                </div>
                
                <div>
                  <label for="songUrl" class="block text-sm font-medium text-gray-700 mb-1">
                    YouTube URL
                  </label>
                  <input
                    id="songUrl"
                    v-model="songUrl"
                    type="url"
                    required
                    class="input-field"
                    placeholder="https://www.youtube.com/watch?v=..."
                    :disabled="addingSong"
                  >
                </div>
                
                <button 
                  type="submit"
                  :disabled="!songTitle || !songUrl || addingSong"
                  class="btn-primary w-full py-3 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
                >
                  <span v-if="addingSong" class="animate-spin">⏳</span>
                  <span v-else>🎵</span>
                  <span>{{ addingSong ? 'Adding...' : 'Add to Queue' }}</span>
                </button>
              </div>
            </form>
          </div>

          <!-- Session Info -->
          <div class="card p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Session Info</h3>
            <div class="space-y-3">
              <div>
                <p class="text-sm text-gray-600 mb-1">Session Code</p>
                <p class="font-mono font-semibold text-lg">{{ sessionCode }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 mb-1">Your User ID</p>
                <p class="font-mono text-sm truncate bg-gray-100 p-2 rounded">{{ userId }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600 mb-1">Connection</p>
                <div class="flex items-center space-x-2">
                  <div 
                    :class="[
                      'w-2 h-2 rounded-full',
                      isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
                    ]"
                  ></div>
                  <span class="text-sm">{{ isConnected ? 'Connected to live updates' : 'Disconnected' }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="card p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div class="space-y-2">
              <button 
                @click="copySessionCode"
                class="w-full btn-secondary py-2 flex items-center justify-center space-x-2"
              >
                <span>📋</span>
                <span>Copy Session Code</span>
              </button>
              <button 
                @click="fetchQueue" 
                :disabled="loading"
                class="w-full btn-secondary py-2 flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                <span>🔄</span>
                <span>Refresh Queue</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { queueAPI } from '@/services/api'
import { getOrCreateUserId } from '@/utils/uuid'
import { useWebSocket } from '@/composables/useWebSocket'
import { useSessionStore } from '@/stores/session'
import { useToast } from '@/composables/useToast'
import SongSearchBar from '@/components/SongSearchBar.vue'
import YouTubePlayer from '@/components/YouTubePlayer.vue'

const route = useRoute()
const sessionStore = useSessionStore()
const { isHost } = storeToRefs(sessionStore)
const toast = useToast()
const sessionCode = route.params.sessionCode as string

const queue = ref<any[]>([])
const songTitle = ref('')
const songUrl = ref('')
const addingSong = ref(false)
const loading = ref(false)
const player = ref<InstanceType<typeof YouTubePlayer> | null>(null)
const userId = ref(getOrCreateUserId())
const currentVideoId = ref<string | null>(null)

// WebSocket integration
const { isConnected, connect, disconnect, sendMessage } = useWebSocket(sessionCode)

const fetchQueue = async () => {
  loading.value = true
  try {
    const songs = await queueAPI.getQueue(sessionCode)
    queue.value = songs
    sessionStore.setQueue(songs)
    toast.success('Queue Updated', 'Latest songs loaded successfully')
  } catch (error: any) {
    console.error('Failed to fetch queue:', error)
    const errorMessage = error.response?.data?.detail || 'Failed to load queue. Please check your connection.'
    toast.error('Queue Load Failed', errorMessage)
  } finally {
    loading.value = false
  }
}

const handleQueueUpdate = () => {
  console.log('Queue update received, refreshing...')
  fetchQueue()
}

const addSong = async () => {
  if (!songTitle.value || !songUrl.value) return
  
  addingSong.value = true
  try {
    await queueAPI.addSong(sessionCode, {
      song_title: songTitle.value,
      song_url: songUrl.value,
      added_by: userId.value
    })
    
    // Clear form
    songTitle.value = ''
    songUrl.value = ''
    
    toast.success('Song Added!', `"${songTitle.value}" added to queue`)
    console.log('Song added successfully')
    // Note: The WebSocket will trigger a queue refresh automatically
  } catch (error: any) {
    console.error('Failed to add song:', error)
    const errorMessage = error.response?.data?.detail || 'Failed to add song. Please try again.'
    toast.error('Add Song Failed', errorMessage)
  } finally {
    addingSong.value = false
  }
}

const copySessionCode = () => {
  navigator.clipboard.writeText(sessionCode)
  toast.success('Copied!', 'Session code copied to clipboard')
}

const onSongSelected = (song: { title: string, url:string }) => {
  songTitle.value = song.title
  songUrl.value = song.url
}

const playSong = (song: any) => {
  const url = new URL(song.song_url)
  const videoId = url.searchParams.get('v')
  if (videoId) {
    currentVideoId.value = videoId
    sendMessage({ type: 'playback_control', action: 'play', videoId })
  }
}

const hostPlay = () => {
  player.value?.playVideo()
  sendMessage({ type: 'playback_control', action: 'play' })
}

const hostPause = () => {
  player.value?.pauseVideo()
  sendMessage({ type: 'playback_control', action: 'pause' })
}

// Lifecycle
onMounted(async () => {
  await fetchQueue()
  connect()
  window.addEventListener('queue-updated', handleQueueUpdate)
  window.addEventListener('playback-action', (event: any) => {
    const { action, videoId } = event.detail
    if (action === 'play') {
      if (videoId && videoId !== currentVideoId.value) {
        currentVideoId.value = videoId
      }
      player.value?.playVideo()
    } else if (action === 'pause') {
      player.value?.pauseVideo()
    }
  })
})

onUnmounted(() => {
  disconnect()
  window.removeEventListener('queue-updated', handleQueueUpdate)
})
</script>