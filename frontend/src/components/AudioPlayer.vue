<template>
  <div class="fixed bottom-0 left-0 right-0 z-50 glass-blur border-t border-white/5 shadow-[0_-20px_50px_rgba(0,0,0,0.5)]">
    <div class="max-w-4xl mx-auto px-6 py-4">
      <!-- Progress Bar (Above player for better visibility) -->
      <div class="absolute top-0 left-0 right-0 h-1 bg-white/5 cursor-pointer group" @click="handleSeek" :class="{ 'cursor-default': !props.isHost }">
          <div class="absolute top-0 left-0 h-full bg-gradient-to-r from-vibe-blue to-vibe-indigo transition-all duration-100 group-hover:from-vibe-purple group-hover:to-vibe-pink" :style="{ width: `${progress}%` }"></div>
          <!-- Seek Handle -->
          <div v-if="props.isHost" class="absolute h-3 w-3 bg-white rounded-full -top-1 shadow-[0_0_10px_rgba(255,255,255,0.8)] opacity-0 group-hover:opacity-100 transition-opacity" :style="{ left: `${progress}%`, marginLeft: '-6px' }"></div>
      </div>

      <div class="flex items-center gap-6 mt-2">
        <!-- Track Info -->
        <div class="flex items-center space-x-4 flex-1 min-w-0 relative">
          <div class="relative group flex-shrink-0 flex items-center justify-center w-12 h-12 md:w-16 md:h-16">
            <!-- Visualizer Canvas -->
            <canvas ref="visualizerCanvas" class="absolute pointer-events-none z-[-1] transition-opacity duration-500" :class="{ 'opacity-100': isPlaying, 'opacity-0': !isPlaying }" width="160" height="160" style="width: 160px; height: 160px; left: 50%; top: 50%; transform: translate(-50%, -50%);"></canvas>
            
            <img :src="props.currentTrack.image" alt="Track thumbnail" class="w-full h-full rounded-2xl object-cover shadow-2xl group-hover:scale-105 transition-transform duration-500 ring-1 ring-white/10 relative z-10"/>
            <div v-if="isPlaying" class="absolute inset-0 bg-vibe-indigo/20 animate-pulse rounded-2xl z-20 pointer-events-none"></div>
          </div>
          <div class="min-w-0 flex-1 ml-2">
            <h4 class="text-sm md:text-xl font-black text-white truncate tracking-tight">{{ props.currentTrack.name }}</h4>
            <p class="text-xs md:text-sm text-gray-500 truncate font-bold uppercase tracking-wider">{{ props.currentTrack.artist_name }}</p>
          </div>
        </div>

        <!-- Player Controls -->
        <div class="flex items-center space-x-4 md:space-x-8" :class="{ 'opacity-30 pointer-events-none': !props.isHost }">
          <button @click="emit('previous')" class="p-2 text-gray-400 hover:text-white transition-all transform hover:scale-110 active:scale-90 hidden sm:block">
            <Rewind :size="28" class="fill-current" />
          </button>
          
          <button @click="togglePlayPause" class="w-14 h-14 md:w-16 md:h-16 bg-white text-vibe-black rounded-[1.5rem] flex items-center justify-center shadow-[0_0_30px_rgba(255,255,255,0.3)] hover:shadow-white/50 hover:scale-105 active:scale-95 transition-all focus:outline-none">
            <Pause v-if="isPlaying" :size="32" fill="currentColor" />
            <Play v-else :size="32" fill="currentColor" class="ml-1" />
          </button>
          
          <button @click="emit('next')" class="p-2 text-gray-400 hover:text-white transition-all transform hover:scale-110 active:scale-90">
            <FastForward :size="28" class="fill-current" />
          </button>
        </div>
        
        <!-- Time Info (Desktop) -->
        <div class="hidden md:flex flex-col items-end min-w-[80px]">
            <span class="text-xs font-black text-white tabular-nums">{{ formatTime(currentTime) }}</span>
            <span class="text-[10px] font-black text-gray-600 tabular-nums uppercase">{{ formatTime(totalDuration) }}</span>
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

const visualizerCanvas = ref<HTMLCanvasElement | null>(null)
let analyser: AnalyserNode | null = null
let animationFrameId: number | null = null

let progressInterval: number | null = null;

const clear = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  if (sound.value) {
    sound.value.unload()
    sound.value = null
  }
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
    animationFrameId = null
  }
  isPlaying.value = false
  progress.value = 0
  currentTime.value = 0
  totalDuration.value = 0
}

const initVisualizer = () => {
  if (!Howler.ctx) return;
  if (!analyser) {
    analyser = Howler.ctx.createAnalyser();
    analyser.fftSize = 256;
    analyser.smoothingTimeConstant = 0.8;
    Howler.masterGain.connect(analyser);
  }
}

const drawVisualizer = () => {
  if (!visualizerCanvas.value || !analyser) return;
  const canvas = visualizerCanvas.value;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const width = canvas.width;
  const height = canvas.height;
  const centerX = width / 2;
  const centerY = height / 2;
  
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);
  
  const draw = () => {
    animationFrameId = requestAnimationFrame(draw);
    
    if (!isPlaying.value) return; // Let opacity fade handle the visual transition
    
    analyser!.getByteFrequencyData(dataArray);
    
    let bassSum = 0;
    for(let i = 0; i < 8; i++) {
        bassSum += dataArray[i]!;
    }
    const bassAvg = bassSum / 8; 
    const normalizedBass = bassAvg / 255; // 0 to 1
    
    ctx.clearRect(0, 0, width, height);
    
    // The image is 64x64 on desktop (radius 32). Let's base radius at 42 to leave a gap.
    const baseRadius = 42;
    const pulse = normalizedBass * 18; // Max expansion
    
    // Main reactive ring
    ctx.beginPath();
    ctx.arc(centerX, centerY, baseRadius + pulse, 0, 2 * Math.PI);
    ctx.lineWidth = 3 + (normalizedBass * 3);
    
    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, `rgba(99, 102, 241, ${0.4 + normalizedBass * 0.4})`); // vibe-indigo
    gradient.addColorStop(1, `rgba(236, 72, 153, ${0.4 + normalizedBass * 0.4})`); // vibe-pink
    
    ctx.strokeStyle = gradient;
    ctx.stroke();
    
    // Outer subtle glow ring
    ctx.beginPath();
    ctx.arc(centerX, centerY, baseRadius + pulse + 8, 0, 2 * Math.PI);
    ctx.lineWidth = 1;
    ctx.strokeStyle = `rgba(168, 85, 247, ${0.1 + normalizedBass * 0.2})`; // vibe-purple
    ctx.stroke();
  };
  
  draw();
}

const setupSound = (track: AudioTrack, autoplay: boolean) => {
  clear()

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
      
      initVisualizer()
      if (!animationFrameId) {
         drawVisualizer()
      }
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
  console.log('AudioPlayer: play requested', { soundExists: !!sound.value, state: sound.value?.state() })
  if (sound.value) {
    if (sound.value.state() === 'unloaded') {
      setupSound(props.currentTrack, true)
    } else {
      sound.value.play()
    }
  } else if (props.currentTrack) {
    setupSound(props.currentTrack, true)
  }
}

const pause = () => {
  console.log('AudioPlayer: pause requested', { soundExists: !!sound.value, state: sound.value?.state() })
  if (sound.value) {
    sound.value.pause()
  }
}

const togglePlayPause = () => {
  if (!sound.value) {
     console.log('AudioPlayer: togglePlayPause triggered with no sound, trying to play');
     play();
     return;
  }
  
  const isCurrentlyPlaying = sound.value.playing();
  console.log('AudioPlayer: togglePlayPause', { isCurrentlyPlaying });
  
  if (isCurrentlyPlaying) {
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
  if (sound.value) {
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
    const seek = sound.value.seek() as number || 0;
    const dur = duration.value;
    
    // Guard against division by zero/NaN
    if (dur > 0) {
      progress.value = (seek / dur) * 100;
      currentTime.value = seek;
      totalDuration.value = dur;
      emit('progress', progress.value, dur, seek)
    }
  }
}

// Methods exposed to parent for external control (when not host)
const setPlaybackState = (playing: boolean, prog: number, current: number, total: number) => {
    console.log('AudioPlayer: sync received', { playing, current, localPlaying: isPlaying.value });
    
    // Update UI refs
    progress.value = prog;
    currentTime.value = current;
    totalDuration.value = total;

    if (!sound.value) {
        console.warn('AudioPlayer: Sync received but sound not initialized');
        return;
    }

    // Sync position if it drifts too much (> 2 seconds)
    const localSeek = sound.value.seek() as number;
    if (Math.abs(localSeek - current) > 2) {
        console.log('AudioPlayer: Syncing seek position', { localSeek, remoteSeek: current });
        sound.value.seek(current);
    }

    if (playing && !sound.value.playing()) {
        console.log('AudioPlayer: Remote play triggered');
        sound.value.play();
    } else if (!playing && sound.value.playing()) {
        console.log('AudioPlayer: Remote pause triggered');
        sound.value.pause();
    }
    
    // Ensure local reactive state is in sync (it will also be updated by Howl event handlers)
    isPlaying.value = playing;
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
