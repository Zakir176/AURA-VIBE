<template>
  <div class="min-h-screen bg-vibe-black font-sans text-gray-200 pb-40 overflow-x-hidden relative">
    <!-- Background Elements -->
    <div class="fixed inset-0 z-0 pointer-events-none overflow-hidden">
        <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-vibe-blue/10 rounded-full blur-[120px] animate-pulse-slow"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-vibe-purple/10 rounded-full blur-[150px] animate-pulse-slow animation-delay-2000"></div>
    </div>

    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-5 glass-blur border-b border-white/5 sticky top-0 z-40">
      <router-link to="/" class="p-2 -ml-2 text-gray-400 hover:text-white transition-all rounded-xl hover:bg-white/5 group border border-transparent hover:border-white/10">
        <svg class="w-6 h-6 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      
      <div class="flex flex-col items-center">
        <div class="flex items-center space-x-2">
            <h1 class="text-xs font-black text-gray-400 tracking-[0.2em] uppercase">ROOM CODE</h1>
            <div class="flex items-center space-x-2 px-3 py-1 bg-white/5 rounded-lg border border-white/10">
                <span class="text-sm font-black text-white tracking-widest">{{ sessionCode }}</span>
                <button @click="copySessionCode" class="text-gray-500 hover:text-vibe-indigo transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v2M8 7h12"></path></svg>
                </button>
            </div>
        </div>
        <div class="flex items-center space-x-1.5 mt-1.5">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-vibe-pink opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-vibe-pink"></span>
          </span>
          <span class="text-[10px] font-black text-vibe-pink uppercase tracking-[0.2em]">Live Session</span>
        </div>
      </div>
      
      <div class="flex items-center space-x-2 bg-white/5 px-3 py-1.5 rounded-xl border border-white/10">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
        <span class="text-xs font-black text-white">{{ participantCount }}</span>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-xl mx-auto px-6 pt-10 relative z-10">
      
      <!-- Currently Playing Card -->
      <div class="mb-14 group">
        <div class="relative w-full aspect-square rounded-[2.5rem] shadow-[0_40px_100px_-20px_rgba(0,0,0,0.8)] overflow-hidden mb-8 ring-1 ring-white/10 transition-all duration-700 group-hover:scale-[1.02] bg-vibe-navy">
            <div class="absolute inset-0 bg-gradient-to-t from-vibe-black via-transparent to-transparent opacity-60 z-10"></div>
            <transition name="fade" mode="out-in">
                <img v-if="currentSong" :key="currentSong.id" :src="currentSong.image" alt="Album Art" class="w-full h-full object-cover">
                <div v-else class="w-full h-full flex flex-col items-center justify-center text-gray-600 space-y-6">
                    <div class="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center border border-white/10 animate-pulse">
                        <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                    </div>
                    <span class="font-black text-sm tracking-widest uppercase opacity-40">Queue is empty</span>
                </div>
            </transition>
            
            <!-- Ambient Glow based on song -->
            <div v-if="currentSong" class="absolute -inset-10 bg-vibe-indigo/20 blur-[100px] -z-10 group-hover:opacity-100 transition-opacity duration-1000"></div>
        </div>
        
        <div class="text-center space-y-2">
          <div class="inline-block px-3 py-1 rounded-full bg-vibe-indigo/10 border border-vibe-indigo/20 text-vibe-indigo text-[10px] font-black uppercase tracking-widest mb-2" v-if="currentSong">
            Now Playing
          </div>
          <h2 class="text-4xl md:text-5xl font-black text-white tracking-tighter leading-none">{{ currentSong?.name || 'Ready to Vibe?' }}</h2>
          <p class="text-lg text-gray-500 font-bold tracking-tight">{{ currentSong?.artist_name || 'Add a song to start the party' }}</p>
        </div>
      </div>

      <!-- Up Next Section -->
      <div class="mb-32">
        <div class="flex justify-between items-center mb-8 px-2">
          <h3 class="text-xl font-black text-white tracking-tight uppercase">Up Next</h3>
          <div class="flex items-center space-x-3">
             <button v-if="isHost && isManualSort" @click="enableSmartSort" class="text-[10px] font-black text-vibe-indigo border border-vibe-indigo/30 hover:bg-vibe-indigo/20 px-3 py-1 rounded-full bg-vibe-indigo/10 transition-colors uppercase tracking-widest flex items-center gap-1">
                 <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                 Enable Smart Sort
             </button>
             <span class="text-[10px] font-black text-gray-500 border border-white/10 px-3 py-1 rounded-full bg-white/5">{{ upNextQueueLocal.length }} TRACKS</span>
          </div>
        </div>
        
        <draggable
          v-model="upNextQueueLocal"
          item-key="queue_id"
          class="space-y-4"
          :disabled="!isHost"
          @end="onDragEnd"
          ghost-class="opacity-40"
          drag-class="scale-105"
        >
          <template #item="{ element: song, index }">
            <div
              class="group glass-card p-4 rounded-[1.5rem] flex items-center space-x-4 transition-all hover:bg-white/10 active:scale-[0.98] border-white/5"
              :class="{ 'cursor-grab active:cursor-grabbing': isHost }"
            >
              <div class="relative flex-shrink-0">
                   <img :src="song.image" alt="Song thumbnail" class="w-16 h-16 rounded-2xl object-cover shadow-2xl ring-1 ring-white/10">
                   <div class="absolute -top-2 -left-2 w-7 h-7 bg-white text-vibe-black text-xs font-black rounded-lg flex items-center justify-center border-2 border-vibe-black shadow-lg">
                       {{ index + 1 }}
                   </div>
              </div>
              
              <div class="flex-grow min-w-0">
                <p class="font-black text-white truncate text-lg leading-tight">{{ song.name }}</p>
                <p class="text-sm text-gray-500 truncate font-bold">{{ song.artist_name }}</p>
                <div class="flex items-center mt-2 space-x-2">
                    <div class="px-2 py-0.5 rounded-md bg-white/5 border border-white/5 text-[9px] font-black text-gray-400 uppercase tracking-wider">
                        BY {{ song.added_by.slice(0, 8) }}
                    </div>
                </div>
              </div>
              
              <!-- Vote controls -->
              <div class="flex flex-col items-center space-y-1 bg-white/5 p-2 rounded-2xl border border-white/5 z-10" @mousedown.stop @touchstart.stop>
                <button data-testid="upvote-btn" @click="upvote(song.queue_id)" class="p-1 text-gray-500 hover:text-vibe-blue transition-all hover:scale-125">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 4l-8 8h16l-8-8z"></path></svg>
                </button>
                <span class="font-black text-sm text-white">{{ song.votes || 0 }}</span>
                <button data-testid="downvote-btn" @click="downvote(song.queue_id)" class="p-1 text-gray-500 hover:text-vibe-pink transition-all hover:scale-125">
                  <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 20l8-8H4l8 8z"></path></svg>
                </button>
              </div>

              <!-- Drag Handle (Host Only) -->
              <div v-if="isHost" class="flex-shrink-0 text-gray-600 group-hover:text-white transition-colors opacity-0 group-hover:opacity-100">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path></svg>
              </div>
            </div>
          </template>
        </draggable>
        
        <div v-if="upNextQueueLocal.length === 0 && !currentSong" class="text-center py-20">
            <div class="w-20 h-20 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-center mx-auto mb-6 opacity-20">
                <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            </div>
            <p class="text-gray-600 font-black text-xs tracking-widest uppercase">The queue is silent. Be the DJ!</p>
        </div>
      </div>
    </main>

    <!-- Floating Search Bar -->
    <div 
      class="fixed left-6 right-6 p-0 transition-all duration-500 z-50 md:left-auto md:right-10 md:bottom-32 md:w-96"
      :class="currentSong ? 'bottom-32' : 'bottom-10'"
    >
      <div class="max-w-md mx-auto shadow-[0_30px_60px_-15px_rgba(0,0,0,0.5)] rounded-3xl overflow-hidden glass-card border-white/10 focus-within:ring-2 focus-within:ring-vibe-indigo transition-all">
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
import { queueAPI, sessionAPI } from '@/services/api'
import type { Song, JamendoSong } from '@/services/api'
import { useWebSocket } from '@/composables/useWebSocket'
import { useSessionStore } from '@/stores/session'
import { useToast } from '@/composables/useToast'
import SongSearchBar from '@/components/SongSearchBar.vue'
import AudioPlayer from '@/components/AudioPlayer.vue'
import draggable from 'vuedraggable'

const route = useRoute()
const sessionStore = useSessionStore()
const toast = useToast()
const sessionCode = route.params.sessionCode as string

const queue = ref<Song[]>([])
const loading = ref(false)
const addingSong = ref(false)
const participantCount = ref(0)
const isManualSort = ref(false)
const audioPlayerRef = ref<InstanceType<typeof AudioPlayer> | null>(null)

const isHost = computed(() => sessionStore.isHost)
const currentSong = computed(() => queue.value[0] || null)
const upNextQueueLocal = computed({
  get: () => queue.value.slice(1),
  set: (newValue) => {
    queue.value = [queue.value[0], ...newValue];
  }
})

const { connect, disconnect, sendMessage } = useWebSocket(sessionCode)

const fetchSessionDetails = async () => {
  try {
    const res = await sessionAPI.getSession(sessionCode)
    isManualSort.value = (res as any).manual_sort || false
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
  } catch (error: unknown) {
    console.error('Failed to fetch queue:', error)
    toast.error('Queue Load Failed', (error as Error & { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Failed to load queue.')
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
    }
    await queueAPI.addSong(sessionCode, payload)
    toast.success('Song Added!', `"${jamendoSong.name}" is now in the queue.`)
    fetchQueue() // Immediately update the queue for the user who added the song
  } catch (error: unknown) {
    console.error('Failed to add song:', error)
    toast.error('Add Song Failed', (error as Error & { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Could not add song.')
  } finally {
    addingSong.value = false
  }
}

const onSongSelected = (jamendoSong: JamendoSong) => {
  addSong(jamendoSong)
}

// --- Player Controls ---

const handleNext = () => {
  sendMessage({ type: 'playback_control', action: 'next' })
}

const handlePrevious = () => {
  sendMessage({ type: 'playback_control', action: 'previous' })
}

const handleTrackEnded = () => {
  console.log('Track has ended, playing next.')
  handleNext()
}

const onDragEnd = async () => {
  if (!isHost.value) return;
  const order = queue.value.map(s => s.queue_id);
  try {
    await queueAPI.reorderQueue(sessionCode, order);
    isManualSort.value = true;
    toast.success('Queue Reordered', 'Smart sorting is temporarily paused.');
  } catch (error) {
     console.error('Failed to reorder', error);
     toast.error('Reorder Failed');
     fetchQueue(); // Revert on failure
  }
}

const enableSmartSort = async () => {
   try {
      const res = await queueAPI.toggleSmartSort(sessionCode, true)
      isManualSort.value = (res as any).manual_sort;
      toast.success('Smart Sort Enabled', 'Queue is now ordered by votes.');
      fetchQueue();
   } catch(e) {
      console.error('Failed to toggle smart sort', e);
      toast.error('Action Failed');
   }
}

const upvote = async (songId: number) => {
  console.log(`Upvoting song ${songId}`)
  try {
    await queueAPI.vote(sessionCode, songId, true)
    // Queue update will happen via WebSocket 'vote_updated' event
    toast.success('Voted!', 'Your vote has been recorded.')
  } catch (error: unknown) {
    console.error('Failed to vote:', error)
    toast.error('Vote Failed', (error as Error & { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Could not record vote.')
  }
}

const downvote = async (songId: number) => {
  console.log(`Downvoting song ${songId}`)
  try {
    await queueAPI.vote(sessionCode, songId, false)
    // Queue update will happen via WebSocket 'vote_updated' event
    toast.success('Voted!', 'Your vote has been recorded.')
  } catch (error: unknown) {
    console.error('Failed to vote:', error)
    toast.error('Vote Failed', (error as Error & { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Could not record vote.')
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

const handlePlaybackControl = (event: Event) => {
  const customEvent = event as CustomEvent;
  const data = customEvent.detail;
  
  if (data.type === 'error') {
    toast.error('Playback Control Error', data.message);
  } else if (data.type === 'info') {
    toast.info('Info', data.message);
  }
}

const handleParticipantCountUpdated = (event: Event) => {
  const customEvent = event as CustomEvent;
  participantCount.value = customEvent.detail.count;
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
        // Use the playing state provided in the sync message or default to current
        const isPlayingRemote = data.playing ?? audioPlayerRef.value.isPlaying;
        audioPlayerRef.value.setPlaybackState(isPlayingRemote, progress, currentTime, duration);
    } else if (action === 'progress') {
        const isPlayingRemote = data.playing ?? true; // Progress usually means it's playing
        audioPlayerRef.value.setPlaybackState(isPlayingRemote, progress, currentTime, duration);
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
  window.addEventListener('playback_control', handlePlaybackControl)
  window.addEventListener('participant_count_updated', handleParticipantCountUpdated)
})

onUnmounted(() => {
  disconnect()
  window.removeEventListener('queue-updated', handleQueueUpdate)
  window.removeEventListener('playback-sync', handlePlaybackSync)
  window.removeEventListener('playback_control', handlePlaybackControl)
  window.removeEventListener('participant_count_updated', handleParticipantCountUpdated)
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
