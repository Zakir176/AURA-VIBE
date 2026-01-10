<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { Howl } from 'howler'

interface AudioTrack {
  id: string;
  name: string;
  artist_name: string;
  audio: string;
  image: string;
}

const props = defineProps<{
  currentTrack: AudioTrack | null;
  playlist: AudioTrack[];
}>()

const emit = defineEmits<{
  (e: 'track-ended'): void;
  (e: 'play-status-changed', isPlaying: boolean): void;
}>()

const sound = ref<Howl | null>(null)
const isPlaying = ref(false)
const volume = ref(0.7) // Default volume
const fadeDuration = 1000 // 1 second for crossfade

let nextTrackTimeout: ReturnType<typeof setTimeout> | null = null

const loadAndPlayTrack = (track: AudioTrack) => {
  if (sound.value) {
    sound.value.unload() // Unload existing sound
    sound.value = null
  }

  sound.value = new Howl({
    src: [track.audio],
    html5: true, // Force HTML5 Audio to avoid Web Audio API buffer issues for longer tracks
    volume: 0, // Start muted for fade-in
    onplay: () => {
      isPlaying.value = true
      emit('play-status-changed', true)
      sound.value?.fade(0, volume.value, fadeDuration) // Fade in
    },
    onend: () => {
      isPlaying.value = false
      emit('play-status-changed', false)
      emit('track-ended') // Notify parent that track has ended
    },
    onstop: () => {
      isPlaying.value = false
      emit('play-status-changed', false)
    },
    onpause: () => {
      isPlaying.value = false
      emit('play-status-changed', false)
    },
    onerror: (id, error) => {
      console.error(`Howler.js error for track ${track.name} (ID: ${id}):`, error)
      emit('track-ended') // Try next track on error
    }
  })

  sound.value.play()
}

const play = () => {
  if (sound.value && !isPlaying.value) {
    sound.value.play()
  } else if (!sound.value && props.currentTrack) {
    loadAndPlayTrack(props.currentTrack)
  }
}

const pause = () => {
  if (sound.value && isPlaying.value) {
    sound.value.pause()
  }
}

const stop = () => {
  if (sound.value) {
    sound.value.stop()
  }
}

const setVolume = (newVolume: number) => {
  volume.value = newVolume
  if (sound.value) {
    sound.value.volume(newVolume)
  }
}

// Watch for currentTrack changes
watch(() => props.currentTrack, (newTrack, oldTrack) => {
  if (newTrack && newTrack.id !== oldTrack?.id) {
    // If a new track is selected, immediately load and play it.
    // The fade-out of the old track and fade-in of the new one will be handled by Howler.js
    loadAndPlayTrack(newTrack)
  } else if (!newTrack && sound.value) {
    stop() // Stop if no track is current
  }
})

onMounted(() => {
  if (props.currentTrack) {
    loadAndPlayTrack(props.currentTrack)
  }
})

onBeforeUnmount(() => {
  if (sound.value) {
    sound.value.unload()
  }
  if (nextTrackTimeout) {
    clearTimeout(nextTrackTimeout)
  }
})
</script>

<template>
  <div class="audio-player">
    <div v-if="props.currentTrack" class="flex items-center space-x-4">
      <img :src="props.currentTrack.image" alt="Track thumbnail" class="w-16 h-16 rounded-md object-cover"/>
      <div>
        <p class="text-lg font-semibold">{{ props.currentTrack.name }}</p>
        <p class="text-sm text-gray-500">{{ props.currentTrack.artist_name }}</p>
      </div>
      <div class="controls flex items-center space-x-2">
        <button @click="play" :disabled="isPlaying" class="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
          </svg>
        </button>
        <button @click="pause" :disabled="!isPlaying" class="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    <div v-else class="text-gray-500">No track currently playing.</div>
  </div>
</template>

<style scoped>
/* Add any specific styles for your player here */
</style>
