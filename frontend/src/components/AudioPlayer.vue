<template>
  <div class="fixed bottom-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-xl border-t border-gray-200 shadow-2xl pb-safe">
    <div class="max-w-4xl mx-auto p-4">
      <div class="flex items-center gap-4">
        <!-- Track Info -->
        <div class="flex items-center space-x-3 flex-1 min-w-0">
          <div class="relative group">
            <img :src="props.currentTrack.image" alt="Track thumbnail" class="w-12 h-12 md:w-14 md:h-14 rounded-xl object-cover shadow-sm group-hover:scale-105 transition-transform duration-300"/>
            <div class="absolute inset-0 rounded-xl ring-1 ring-inset ring-black/10"></div>
          </div>
          <div class="min-w-0 flex-1">
            <div class="flex items-center gap-2">
                <p class="text-sm md:text-base font-bold text-gray-900 truncate">{{ props.currentTrack.name }}</p>
            </div>
            <p class="text-xs md:text-sm text-gray-500 truncate font-medium">{{ props.currentTrack.artist_name }}</p>
          </div>
        </div>

        <!-- Player Controls -->
        <div class="flex items-center space-x-3 md:space-x-6" :class="{ 'opacity-50 pointer-events-none': !props.isHost }">
          <button @click="emit('previous')" class="p-2 text-gray-400 hover:text-gray-900 transition-colors focus:outline-none rounded-full hover:bg-gray-100 hidden sm:block">
            <Rewind :size="24" class="fill-current" />
          </button>
          
          <button @click="togglePlayPause" class="w-12 h-12 bg-gray-900 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-gray-800 transition-all hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900">
            <Pause v-if="isPlaying" :size="24" fill="currentColor" />
            <Play v-else :size="24" fill="currentColor" class="ml-1" />
          </button>
          
          <button @click="emit('next')" class="p-2 text-gray-400 hover:text-gray-900 transition-colors focus:outline-none rounded-full hover:bg-gray-100">
            <FastForward :size="24" class="fill-current" />
          </button>
        </div>
        
        <!-- Volume & Progress (Desktop) -->
        <div class="hidden md:flex flex-1 items-center justify-end max-w-xs pl-4">
            <div class="w-full space-y-1 group">
                <div class="flex justify-between text-[10px] font-bold text-gray-400 font-mono tracking-wider">
                    <span>{{ formatTime(currentTime) }}</span>
                    <span>{{ formatTime(totalDuration) }}</span>
                </div>
                <div class="relative h-1.5 bg-gray-200 rounded-full cursor-pointer overflow-hidden" @click="handleSeek" :class="{ 'cursor-default': !props.isHost }">
                    <div class="absolute top-0 left-0 h-full bg-gray-900 rounded-full transition-all duration-100 group-hover:bg-blue-600" :style="{ width: `${progress}%` }"></div>
                </div>
            </div>
        </div>
      </div>
      
      <!-- Mobile Progress Bar -->
      <div class="md:hidden mt-3 -mx-4">
        <div class="relative h-1 bg-gray-100 cursor-pointer" @click="handleSeek" :class="{ 'cursor-default': !props.isHost }">
            <div class="absolute top-0 left-0 h-full bg-blue-500 transition-all duration-100" :style="{ width: `${progress}%` }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onBeforeUnmount, computed, shallowRef } from 'vue'
import { Howl } from 'howler'
import { Play, Pause, Rewind, FastForward } from 'lucide-vue-next'
import { useToast } from '@/composables/useToast'

interface AudioTrack {
  id: string | number;
  name: string;
  artist_name: string;
  audio: string;
  image: string;
}

const props = defineProps<{
  currentTrack: AudioTrack; // Made required as it's the core of the player
  isHost?: boolean;
}>()

const emit = defineEmits<{
  (e: 'track-ended'): void;
  (e: 'next'): void;
  (e: 'previous'): void;
  (e: 'play', progress: number, duration: number, currentTime: number): void;
  (e: 'pause', progress: number, duration: number, currentTime: number): void;
  (e: 'seek', percent: number, progress: number, duration: number, currentTime: number): void;
  (e: 'progress', percent: number, duration: number, currentTime: number): void;
}>()

const sound = shallowRef<Howl | null>(null)
const isPlaying = ref(false)
const progress = ref(0)
const volume = ref(0.5)
const currentTime = ref(0)
const totalDuration = ref(0)
const toast = useToast()

let progressInterval: number | null = null;

const clear = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  if (sound.value) {
    sound.value.unload()
    sound.value = null
  }
  isPlaying.value = false
  progress.value = 0
  currentTime.value = 0
  totalDuration.value = 0
}

const setupSound = (track: AudioTrack, autoplay: boolean) => {
  clear()

  if (!props.isHost) {
    // If not host, do not initialize Howl
    return;
  }

  console.log('Initializing Howl with source:', track.audio)
  sound.value = new Howl({
    src: [track.audio],
    html5: true,
    format: ['mp3'],
    volume: volume.value,
    onload: () => {
      console.log('Howler loaded successfully')
      if (autoplay) {
        play()
      }
    },
    onplay: () => {
      isPlaying.value = true
      progressInterval = window.setInterval(updateProgress, 1000)
      const seek = sound.value?.seek() || 0;
      const dur = duration.value;
      emit('play', progress.value, dur, seek)
    },
    onpause: () => {
      isPlaying.value = false
      if(progressInterval) clearInterval(progressInterval)
      const seek = sound.value?.seek() || 0;
      const dur = duration.value;
      emit('pause', progress.value, dur, seek)
    },
    onstop: () => {
      isPlaying.value = false
      if(progressInterval) clearInterval(progressInterval)
      progress.value = 0
      emit('pause', 0, 0, 0)
    },
    onend: () => {
      isPlaying.value = false
      if(progressInterval) clearInterval(progressInterval)
      progress.value = 0
      emit('track-ended')
    },
    onloaderror: (id: number, err: unknown) => {
      console.error('Howler load error:', err)
      toast.error('Playback Error', 'Failed to load audio file.')
    },
    onplayerror: (id: number, err: unknown) => {
      console.error('Howler play error:', err)
      isPlaying.value = false // Ensure state is correct
      toast.info('Autoplay prevented', 'Click the play button to start the music.')
    },
  })
}


const play = () => {
  if (props.isHost && sound.value) {
    sound.value.play()
  }
}

const pause = () => {
  if (props.isHost && sound.value) {
    sound.value.pause()
  }
}

const togglePlayPause = () => {
  if (!props.isHost) return;
  
  if (isPlaying.value) {
    pause()
  } else {
    play()
  }
}

const duration = computed(() => {
  return sound.value?.duration() || 0
})

const handleSeek = (e: MouseEvent) => {
  if (!props.isHost) return;
  
  const target = e.currentTarget as HTMLElement;
  if (target) {
    const percent = e.offsetX / target.offsetWidth;
    seek(percent);
  }
}

const seek = (percent: number) => {
  if (props.isHost && sound.value) {
    const dur = duration.value;
    const seekTime = dur * percent;
    sound.value.seek(seekTime)
    
    // Update local state immediately
    progress.value = percent * 100;
    currentTime.value = seekTime;
    totalDuration.value = dur;
    
    emit('seek', percent, progress.value, dur, seekTime)
  }
}

const updateProgress = () => {
  if (sound.value) {
    const seek = sound.value.seek() || 0;
    const dur = duration.value;
    progress.value = (seek / dur) * 100;
    currentTime.value = seek;
    totalDuration.value = dur;
    emit('progress', progress.value, dur, seek)
  }
}

// Methods exposed to parent for external control (when not host)
const setPlaybackState = (playing: boolean, prog: number, current: number, total: number) => {
    console.log('AudioPlayer: setPlaybackState called', { playing, prog, current, total });
    isPlaying.value = playing;
    progress.value = prog;
    currentTime.value = current;
    totalDuration.value = total;
}

const setDuration = (dur: number) => {
    // Only used for display when not host, but duration is computed from sound.
    // If we want to display duration for guests, we need a separate state or prop.
    // For now, let's assume guests get progress % directly.
}

const formatTime = (secs: number) => {
  const minutes = Math.floor(secs / 60) || 0;
  const seconds = Math.floor(secs - minutes * 60) || 0;
  return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
};

watch(() => props.currentTrack, (newTrack, oldTrack) => {
  if (newTrack) {
    // Prevent re-initialization if the track ID is the same
    if (oldTrack && newTrack.id === oldTrack.id) {
        return;
    }
    const shouldAutoplay = !!oldTrack && newTrack.id !== oldTrack.id;
    setupSound(newTrack, shouldAutoplay)
  }
}, { immediate: true })


onBeforeUnmount(() => {
  clear()
})

// Expose methods for parent if needed (though it's better encapsulated now)
defineExpose({ play, pause, setPlaybackState, isPlaying })

</script>

<style scoped>
.pb-safe {
    padding-bottom: env(safe-area-inset-bottom);
}
</style>
