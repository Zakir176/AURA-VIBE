<template>
  <v-card class="music-player" elevation="4" v-if="isPlayerReady">
    <v-card-text class="pa-4">
      <v-row align="center" no-gutters>
        <!-- Track Info -->
        <v-col cols="12" md="4" class="d-flex align-center">
          <v-avatar size="56" class="mr-3">
            <v-img :src="currentTrack?.album?.images?.[0]?.url || '/default-album.png'" />
          </v-avatar>
          <div class="track-info">
            <div class="text-subtitle-2 font-weight-bold">{{ currentTrack?.name || 'No track' }}</div>
            <div class="text-caption text-medium-emphasis">{{ currentTrack?.artists?.[0]?.name || 'Unknown artist' }}</div>
          </div>
        </v-col>

        <!-- Player Controls -->
        <v-col cols="12" md="4" class="text-center">
          <div class="d-flex align-center justify-center">
            <v-btn icon="mdi-skip-previous" variant="text" @click="previousTrack" :disabled="!isPlayerReady" />
            <v-btn 
              :icon="isPlaying ? 'mdi-pause' : 'mdi-play'" 
              variant="text" 
              size="large"
              @click="togglePlay" 
              :disabled="!isPlayerReady"
              class="mx-2"
            />
            <v-btn icon="mdi-skip-next" variant="text" @click="nextTrack" :disabled="!isPlayerReady" />
          </div>
          
          <!-- Progress Bar -->
          <div class="mt-2">
            <v-slider
              v-model="progress"
              :max="duration"
              :min="0"
              step="1"
              @update:model-value="seekTo"
              :disabled="!isPlayerReady"
              color="primary"
              track-color="grey-lighten-2"
              hide-details
            />
            <div class="d-flex justify-space-between text-caption text-medium-emphasis mt-1">
              <span>{{ formatTime(progress) }}</span>
              <span>{{ formatTime(duration) }}</span>
            </div>
          </div>
        </v-col>

        <!-- Volume & Additional Controls -->
        <v-col cols="12" md="4" class="d-flex align-center justify-end">
          <v-btn icon="mdi-volume-high" variant="text" size="small" />
          <v-slider
            v-model="volume"
            :max="100"
            :min="0"
            step="1"
            @update:model-value="setVolume"
            :disabled="!isPlayerReady"
            color="primary"
            track-color="grey-lighten-2"
            hide-details
            class="mx-2"
            style="max-width: 100px;"
          />
          <v-btn icon="mdi-shuffle" variant="text" size="small" :color="isShuffled ? 'primary' : ''" @click="toggleShuffle" />
          <v-btn icon="mdi-repeat" variant="text" size="small" :color="repeatMode !== 'off' ? 'primary' : ''" @click="toggleRepeat" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  accessToken: {
    type: String,
    required: true
  }
})

// Player state
const isPlayerReady = ref(false)
const isPlaying = ref(false)
const currentTrack = ref(null)
const progress = ref(0)
const duration = ref(0)
const volume = ref(50)
const isShuffled = ref(false)
const repeatMode = ref('off') // 'off', 'context', 'track'

let player = null
let progressInterval = null

onMounted(async () => {
  await initializePlayer()
})

onUnmounted(() => {
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  if (player) {
    player.disconnect()
  }
})

async function initializePlayer() {
  if (!window.Spotify) {
    console.error('Spotify Web Playback SDK not loaded')
    return
  }

  player = new window.Spotify.Player({
    name: 'AURA VIBE Player',
    getOAuthToken: cb => cb(props.accessToken),
    volume: volume.value / 100
  })

  // Error handling
  player.addListener('initialization_error', ({ message }) => {
    console.error('Failed to initialize:', message)
  })

  player.addListener('authentication_error', ({ message }) => {
    console.error('Failed to authenticate:', message)
  })

  player.addListener('account_error', ({ message }) => {
    console.error('Failed to validate Spotify account:', message)
  })

  player.addListener('playback_error', ({ message }) => {
    console.error('Failed to perform playback:', message)
  })

  // Playback status updates
  player.addListener('player_state_changed', state => {
    if (!state) return

    isPlaying.value = !state.paused
    currentTrack.value = state.track_window.current_track
    progress.value = state.position
    duration.value = state.duration
    isShuffled.value = state.shuffle
    repeatMode.value = state.repeat_mode
  })

  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id)
    isPlayerReady.value = true
    startProgressTracking()
  })

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id)
    isPlayerReady.value = false
  })

  // Connect to the player
  const success = await player.connect()
  if (success) {
    console.log('Successfully connected to Spotify!')
  }
}

function startProgressTracking() {
  progressInterval = setInterval(() => {
    if (isPlaying.value && isPlayerReady.value) {
      progress.value += 1000
    }
  }, 1000)
}

function togglePlay() {
  if (!isPlayerReady.value) return
  player.togglePlay()
}

function previousTrack() {
  if (!isPlayerReady.value) return
  player.previousTrack()
}

function nextTrack() {
  if (!isPlayerReady.value) return
  player.nextTrack()
}

function seekTo(position) {
  if (!isPlayerReady.value) return
  player.seek(position)
}

function setVolume(vol) {
  volume.value = vol
  if (isPlayerReady.value) {
    player.setVolume(vol / 100)
  }
}

function toggleShuffle() {
  if (!isPlayerReady.value) return
  player.setShuffle(!isShuffled.value)
}

function toggleRepeat() {
  if (!isPlayerReady.value) return
  const modes = ['off', 'context', 'track']
  const currentIndex = modes.indexOf(repeatMode.value)
  const nextMode = modes[(currentIndex + 1) % modes.length]
  player.setRepeat(nextMode)
}

function formatTime(ms) {
  const minutes = Math.floor(ms / 60000)
  const seconds = Math.floor((ms % 60000) / 1000)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.music-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  border-radius: 0;
}

.track-info {
  min-width: 0;
}

.track-info > div {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
