<template>
  <div>
    <div ref="playerRef"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps<{
  videoId: string;
}>();

const playerRef = ref<HTMLElement | null>(null);
let player: YT.Player | null = null;
let apiReady = false;

const loadYouTubeAPI = () => {
  if (window.YT && window.YT.Player) {
    apiReady = true;
    createPlayer();
    return;
  }

  if (!document.querySelector('script[src="https://www.youtube.com/iframe_api"]')) {
    const tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    const firstScriptTag = document.getElementsByTagName('script')[0];
    if (firstScriptTag && firstScriptTag.parentNode) {
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    } else {
      document.head.appendChild(tag);
    }

    (window as any).onYouTubeIframeAPIReady = () => {
      apiReady = true;
      createPlayer();
    };
  }
};

const createPlayer = () => {
  if (!apiReady || !playerRef.value || !props.videoId) return;

  player = new YT.Player(playerRef.value, {
    height: '360',
    width: '640',
    videoId: props.videoId,
    playerVars: {
      playsinline: 1
    },
    events: {
      'onReady': onPlayerReady,
    }
  });
};

const onPlayerReady = (event: YT.PlayerEvent) => {
  event.target.playVideo();
};

watch(() => props.videoId, (newVideoId) => {
  if (player && newVideoId) {
    player.loadVideoById(newVideoId);
  } else if (!player && newVideoId) {
    createPlayer();
  }
});

onMounted(() => {
  loadYouTubeAPI();
});

onUnmounted(() => {
  if (player) {
    player.destroy();
  }
});

defineExpose({
  playVideo: () => player?.playVideo(),
  pauseVideo: () => player?.pauseVideo(),
  stopVideo: () => player?.stopVideo(),
  getCurrentTime: () => player?.getCurrentTime(),
  seekTo: (seconds: number) => player?.seekTo(seconds, true),
});

</script>
