<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 font-sans text-gray-800 pb-32">
    <!-- Header -->
    <header class="flex items-center justify-between px-4 py-4 bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-20">
      <router-link to="/" class="p-2 -ml-2 text-gray-600 hover:text-gray-900 transition-colors rounded-full hover:bg-gray-100">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      
      <div class="flex flex-col items-center">
        <div class="flex items-center space-x-2">
            <h1 class="text-sm font-bold text-gray-900 tracking-tight">ROOM #{{ sessionCode }}</h1>
            <button @click="copySessionCode" class="text-gray-400 hover:text-blue-500 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v2M8 7h12"></path></svg>
            </button>
        </div>
        <div class="flex items-center space-x-1.5 mt-0.5">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
          </span>
          <span class="text-[10px] font-bold text-green-600 uppercase tracking-wider">Live</span>
        </div>
      </div>
      
      <div class="w-10 flex justify-end">
          <div class="flex items-center space-x-1 bg-gray-100 px-2 py-1 rounded-full">
            <svg class="w-3 h-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <span class="text-xs font-bold text-gray-600">4</span>
          </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-md mx-auto px-4 pt-6">
      
      <!-- Currently Playing Card -->
      <div class="mb-8">
        <div class="relative w-full aspect-square rounded-3xl shadow-2xl overflow-hidden mb-6 bg-white ring-1 ring-black/5">
            <transition name="fade" mode="out-in">
                <img v-if="currentSong" :key="currentSong.id" :src="currentSong.image" alt="Album Art" class="w-full h-full object-cover">
                <div v-else class="w-full h-full bg-gray-50 flex flex-col items-center justify-center text-gray-400 space-y-4">
                    <svg class="w-16 h-16 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                    <span class="font-medium">Queue is empty</span>
                </div>
            </transition>
            
            <!-- Overlay Gradient for text readability if needed -->
            <div v-if="currentSong" class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent pointer-events-none"></div>
        </div>
        
        <div class="text-center space-y-1">
          <h2 class="text-2xl md:text-3xl font-black text-gray-900 tracking-tight leading-tight">{{ currentSong?.name || 'Ready to Vibe?' }}</h2>
          <p class="text-lg text-gray-500 font-medium">{{ currentSong?.artist_name || 'Add a song to start' }}</p>
        </div>
      </div>

      <!-- Up Next Section -->
      <div class="mb-24">
        <div class="flex justify-between items-end mb-4 px-1">
          <h3 class="text-lg font-bold text-gray-900">Up Next</h3>
          <span class="text-xs font-bold text-gray-500 bg-gray-200/50 px-2 py-1 rounded-md">{{ queue.length }} tracks</span>
        </div>
        
        <transition-group name="list" tag="div" class="space-y-3">
          <div
            v-for="(song, index) in queue"
            :key="song.id"
            class="group bg-white p-3 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-3 transition-all hover:shadow-md hover:border-gray-200 active:scale-[0.98]"
          >
            <div class="relative flex-shrink-0">
                 <img :src="song.image" alt="Song thumbnail" class="w-14 h-14 rounded-xl object-cover shadow-sm">
                 <div class="absolute -top-2 -left-2 w-6 h-6 bg-gray-900 text-white text-xs font-bold rounded-full flex items-center justify-center border-2 border-white shadow-sm">
                     {{ index + 1 }}
                 </div>
            </div>
            
            <div class="flex-grow min-w-0">
              <p class="font-bold text-gray-900 truncate text-base">{{ song.name }}</p>
              <p class="text-sm text-gray-500 truncate">{{ song.artist_name }}</p>
              <div class="flex items-center mt-1 space-x-1">
                  <div class="w-4 h-4 rounded-full bg-gradient-to-tr from-blue-400 to-purple-500 flex items-center justify-center text-[8px] text-white font-bold">
                      {{ song.added_by.slice(0, 1).toUpperCase() }}
                  </div>
                  <span class="text-xs text-gray-400">added by {{ song.added_by.slice(0, 8) }}...</span>
              </div>
            </div>
            
            <button @click="upvote(song.id)" class="flex flex-col items-center justify-center w-10 h-10 rounded-full bg-gray-50 text-gray-400 hover:text-blue-500 hover:bg-blue-50 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg>
              <span class="font-bold text-xs -mt-1">{{ song.votes || 0 }}</span>
            </button>
          </div>
        </transition-group>
        
        <div v-if="queue.length === 0 && !currentSong" class="text-center py-10 opacity-50">
            <p class="text-gray-400 text-sm">The queue is empty. Be the DJ!</p>
        </div>
      </div>
    </main>

    <!-- Floating Search Bar -->
    <div 
      class="fixed left-0 right-0 p-4 transition-all duration-500 z-40"
      :class="currentSong ? 'bottom-[80px] md:bottom-[88px]' : 'bottom-0'"
    >
      <div class="max-w-md mx-auto shadow-2xl rounded-full">
        <SongSearchBar @select-song="onSongSelected" />
      </div>
    </div>
    
    <!-- Audio Player -->
    <AudioPlayer
      v-if="currentSong"
      ref="audioPlayerRef"
      :current-track="currentSong"
      :is-host="isHost"
      @track-ended="handleTrackEnded"
      @next="handleNext"
      @previous="handlePrevious"
      @play="onPlay"
      @pause="onPause"
      @seek="onSeek"
      @progress="onProgress"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { queueAPI, sessionAPI, Song, JamendoSong } from '@/services/api'
import { getOrCreateUserId } from '@/utils/uuid'
import { useWebSocket } from '@/composables/useWebSocket'
import { useSessionStore } from '@/stores/session'
import { useToast } from '@/composables/useToast'
import SongSearchBar from '@/components/SongSearchBar.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'

const route = useRoute()
const sessionStore = useSessionStore()
const toast = useToast()
const sessionCode = route.params.sessionCode as string
const userId = ref(getOrCreateUserId())

const queue = ref<Song[]>([])
const loading = ref(false)
const addingSong = ref(false)
const isHost = ref(false)
const audioPlayerRef = ref<InstanceType<typeof AudioPlayer> | null>(null)

const currentSong = computed(() => queue.value[0] || null)

const { isConnected, connect, disconnect, sendMessage } = useWebSocket(sessionCode)

const fetchSessionDetails = async () => {
  try {
    const session = await sessionAPI.getSession(sessionCode)
    if (session.host_id === userId.value) {
      isHost.value = true
    }
  } catch (error) {
    console.error('Failed to fetch session details:', error)
  }
}

const fetchQueue = async () => {
  loading.value = true
  try {
    const songs = await queueAPI.getQueue(sessionCode)
    queue.value = songs
    sessionStore.setQueue(songs)
  } catch (error: any) {
    console.error('Failed to fetch queue:', error)
    toast.error('Queue Load Failed', error.response?.data?.detail || 'Failed to load queue.')
  } finally {
    loading.value = false
  }
}

const handleQueueUpdate = () => fetchQueue()

const addSong = async (jamendoSong: JamendoSong) => {
  addingSong.value = true
  try {
    const payload = {
      id: jamendoSong.id,
      name: jamendoSong.name,
      artist_name: jamendoSong.artist_name,
      audio: jamendoSong.audio,
      image: jamendoSong.image,
      added_by: userId.value,
    }
    await queueAPI.addSong(sessionCode, payload)
    toast.success('Song Added!', `"${jamendoSong.name}" is now in the queue.`)
    // The queue will be updated via websocket event
  } catch (error: any) {
    console.error('Failed to add song:', error)
    toast.error('Add Song Failed', error.response?.data?.detail || 'Could not add song.')
  } finally {
    addingSong.value = false
  }
}

const onSongSelected = (jamendoSong: JamendoSong) => {
  addSong(jamendoSong)
}

// --- Player Controls ---

const handleNext = () => {
  if (queue.value.length > 1) {
    // Note: This is a simple client-side queue rotation.
    // For a more robust system, the "host" would control the queue
    // and broadcast the new song to all clients.
    const songToEnd = queue.value.shift()
    if (songToEnd) {
      queue.value.push(songToEnd)
    }
    sendMessage({ type: 'playback_control', action: 'next' })
  } else {
    toast.info("End of Queue", "No other songs to play.")
  }
}

const handlePrevious = () => {
  if (queue.value.length > 1) {
    const songToStart = queue.value.pop()
    if (songToStart) {
      queue.value.unshift(songToStart)
    }
    sendMessage({ type: 'playback_control', action: 'previous' })
  } else {
    toast.info("Start of Queue", "No previous song to play.")
  }
}

const handleTrackEnded = () => {
  console.log('Track has ended, playing next.')
  handleNext()
}

const upvote = async (songId: number) => {
  console.log(`Upvoting song ${songId}`)
  try {
    await queueAPI.vote(sessionCode, songId, true, userId.value)
    // Queue update will happen via WebSocket 'vote_updated' event
    toast.success('Voted!', 'Your vote has been recorded.')
  } catch (error: any) {
    console.error('Failed to vote:', error)
    toast.error('Vote Failed', error.response?.data?.detail || 'Could not record vote.')
  }
}

const copySessionCode = () => {
  navigator.clipboard.writeText(sessionCode)
  toast.success('Copied!', 'Session code copied to clipboard')
}

// --- Playback Sync ---

const onPlay = (progress: number, duration: number, currentTime: number) => {
    sendMessage({ type: 'playback_sync', action: 'play', progress, duration, currentTime })
}

const onPause = (progress: number, duration: number, currentTime: number) => {
    sendMessage({ type: 'playback_sync', action: 'pause', progress, duration, currentTime })
}

const onSeek = (percent: number, progress: number, duration: number, currentTime: number) => {
    sendMessage({ type: 'playback_sync', action: 'seek', percent, progress, duration, currentTime })
}

const onProgress = (percent: number, duration: number, currentTime: number) => {
    sendMessage({ type: 'playback_sync', action: 'progress', progress: percent, duration, currentTime })
}

const handlePlaybackSync = (event: Event) => {
  const customEvent = event as CustomEvent;
  const data = customEvent.detail;
  console.log('SessionPage: Received playback-sync event', data, 'isHost:', isHost.value);
  
  if (isHost.value) return; 
  
  if (audioPlayerRef.value) {
    const { action, progress, duration, currentTime } = data;
    console.log('SessionPage: Updating AudioPlayer state', action);
    
    if (action === 'play') {
        audioPlayerRef.value.setPlaybackState(true, progress, currentTime, duration);
    } else if (action === 'pause') {
        audioPlayerRef.value.setPlaybackState(false, progress, currentTime, duration);
    } else if (action === 'seek') {
        // Keep current playing state
        // @ts-ignore
        const isPlaying = audioPlayerRef.value.isPlaying; 
        audioPlayerRef.value.setPlaybackState(isPlaying, progress, currentTime, duration);
    } else if (action === 'progress') {
        audioPlayerRef.value.setPlaybackState(true, progress, currentTime, duration);
    }
  } else {
    console.warn('SessionPage: AudioPlayer ref is missing');
  }
}

onMounted(() => {
  fetchSessionDetails()
  fetchQueue()
  connect()
  window.addEventListener('queue-updated', handleQueueUpdate)
  window.addEventListener('playback-sync', handlePlaybackSync)
})

onUnmounted(() => {
  disconnect()
  window.removeEventListener('queue-updated', handleQueueUpdate)
  window.removeEventListener('playback-sync', handlePlaybackSync)
})
</script>

<style scoped>
/* List Transitions */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-active {
  position: absolute;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
