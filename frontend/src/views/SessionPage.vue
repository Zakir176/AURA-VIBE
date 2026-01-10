<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
    <!-- Header -->
    <header class="flex items-center justify-between px-4 py-5 bg-white border-b border-gray-200 shadow-sm fixed w-full top-0 z-10">
      <router-link to="/" class="text-gray-600 hover:text-gray-800 transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-label="Back"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      <div class="text-center">
        <h1 class="text-lg font-semibold flex items-center">
          Room #{{ sessionCode }}
          <button @click="copySessionCode" class="ml-2 text-gray-400 hover:text-blue-500">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v2M8 7h12"></path></svg>
          </button>
        </h1>
        <div class="flex items-center justify-center space-x-1.5 text-xs text-green-600 font-bold">
          <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span>Live Session</span>
        </div>
      </div>
      <button class="bg-gray-100 rounded-full px-4 py-2 text-sm font-semibold flex items-center space-x-2">
        <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
        <span>4</span>
      </button>
    </header>

    <!-- Main Content -->
    <main class="pt-24 pb-28">
      <div class="max-w-md mx-auto px-4">
        <!-- Currently Playing -->
        <div class="text-center mb-8">
          <div class="relative w-full aspect-square rounded-3xl shadow-2xl overflow-hidden mb-6">
            <img v-if="currentSong" :src="currentSong.image" alt="Album Art" class="w-full h-full object-cover">
            <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center">
              <span class="text-gray-500">No song playing</span>
            </div>
          </div>
          <h2 class="text-3xl font-extrabold">{{ currentSong?.name || 'No song playing' }}</h2>
          <p class="text-lg text-gray-500 font-medium">{{ currentSong?.artist_name || 'No artist' }}</p>

          <!-- Progress Bar (will be handled by AudioPlayer later) -->
          <div class="mt-6">
            <div class="h-2 bg-gray-200 rounded-full">
              <div class="h-2 bg-blue-500 rounded-full" style="width: 0%;"></div>
            </div>
            <div class="flex justify-between text-xs font-mono text-gray-500 mt-1.5">
              <span>0:00</span>
              <span>0:00</span>
            </div>
          </div>

          <!-- Playback Controls (will be handled by AudioPlayer later) -->
          <div class="flex items-center justify-center space-x-8 mt-6">
            <button class="text-gray-500 hover:text-gray-800 transition-colors">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20"><path d="M8.445 14.832A1 1 0 0010 14.832V5.168a1 1 0 00-1.555-.832L4.12 8.168a1 1 0 000 1.664l4.325 3.001zM11.555 4.336a1 1 0 011.555.832v9.664a1 1 0 01-1.555.832l-4.325-3.001a1 1 0 010-1.664l4.325-3.001z"></path></svg>
            </button>
            <button @click="togglePlayPause" class="w-20 h-20 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-blue-600 transition-all scale-105">
              <svg v-if="!isPlaying" class="w-10 h-10 ml-1" fill="currentColor" viewBox="0 0 20 20"><path d="M4.018 15.59a1 1 0 001.414.038l8.36-7.522a1 1 0 000-1.414l-8.36-7.522a1 1 0 00-1.452 1.376L5.61 8 4.018 9.59a1 1 0 000 1.414z"></path></svg>
              <svg v-else class="w-10 h-10" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clip-rule="evenodd"></path></svg>
            </button>
            <button class="text-gray-500 hover:text-gray-800 transition-colors">
              <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20"><path d="M4.12 5.168a1 1 0 00-1.555.832v8.001a1 1 0 001.555.832L8.445 12l-4.325-3.001zM15.88 5.168a1 1 0 00-1.555.832v8.001a1 1 0 001.555.832L20.205 12l-4.325-3.001z"></path></svg>
            </button>
          </div>
        </div>
        <!-- Up Next -->
        <div>
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-bold">Up Next</h3>
            <span class="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full">{{ queue.length }} songs</span>
          </div>
          <div class="space-y-3">
            <div
              v-for="song in queue"
              :key="song.id"
              class="bg-white p-3 rounded-xl shadow-sm flex items-center space-x-4 transition-all hover:shadow-md"
            >
              <img :src="song.image" alt="Song thumbnail" class="w-16 h-16 rounded-lg object-cover">
              <div class="flex-grow">
                <p class="font-bold text-lg">{{ song.name }}</p>
                <p class="text-gray-500">{{ song.artist_name }}</p>
                <p class="text-xs text-gray-400 mt-1">
                  <svg class="w-3 h-3 inline -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  Added by {{ song.added_by }}
                </p>
              </div>
              <button @click="upvote(song.id)" class="flex flex-col items-center justify-center text-gray-500 hover:text-blue-500 p-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path></svg>
                <span class="font-bold text-sm">{{ song.votes || 0 }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Add Song Bar -->
    <div class="fixed bottom-0 left-0 right-0 p-4 bg-white/80 backdrop-blur-md border-t border-gray-200">
      <div class="max-w-md mx-auto flex items-center space-x-3">
        <SongSearchBar @select-song="onSongSelected" class="flex-grow" />
        <button class="w-12 h-12 flex-shrink-0 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center shadow-sm hover:bg-gray-200">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>
        </button>
      </div>
    </div>
    <AudioPlayer
      v-if="currentSong"
      :current-track="currentSong"
      :playlist="queue"
      @track-ended="handleTrackEnded"
      @play-status-changed="handlePlayStatusChanged"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { queueAPI, Song, JamendoSong } from '@/services/api'
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
const player = ref<InstanceType<typeof AudioPlayer> | null>(null)
const isPlaying = ref(false)

const currentSong = computed(() => queue.value[0] || null)


const { isConnected, connect, disconnect, sendMessage } = useWebSocket(sessionCode)

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

const togglePlayPause = () => {
  if (isPlaying.value) {
    player.value?.pause()
    sendMessage({ type: 'playback_control', action: 'pause' }) // Notify others of pause
  } else {
    player.value?.play()
    sendMessage({ type: 'playback_control', action: 'play' }) // Notify others of play
  }
  // isPlaying will be updated by handlePlayStatusChanged
}

const handleTrackEnded = () => {
  // Logic to play next song in the queue
  // For now, just log and reset isPlaying
  console.log('Track has ended.')
  // isPlaying.value = false; // AudioPlayer will emit play-status-changed
  // You would typically advance the queue here
  // sendMessage({ type: 'track_ended', session_code: sessionCode })
}

const handlePlayStatusChanged = (status: boolean) => {
  isPlaying.value = status
}

const upvote = (songId: number) => {
  console.log(`Upvoting song ${songId}`)
  // This would typically send a message via WebSocket or call an API
  // e.g., sendMessage({ type: 'vote', song_id: songId })
  const song = queue.value.find(s => s.id === songId)
  if (song) {
    song.votes = (song.votes || 0) + 1
  }
}

const copySessionCode = () => {
  navigator.clipboard.writeText(sessionCode)
  toast.success('Copied!', 'Session code copied to clipboard')
}

onMounted(() => {
  fetchQueue()
  connect()
  window.addEventListener('queue-updated', handleQueueUpdate)
})

onUnmounted(() => {
  disconnect()
  window.removeEventListener('queue-updated', handleQueueUpdate)
})
</script>
