<template>
  <div>
    <input
      type="text"
      v-model="searchQuery"
      @input="onSearch"
      placeholder="Search for a song on YouTube..."
      class="input-field"
    />
    <div v-if="results.length > 0" class="mt-2">
      <ul>
        <li
          v-for="song in results"
          :key="song.videoId"
          @click="selectSong(song)"
          class="p-2 hover:bg-gray-100 cursor-pointer"
        >
          <div class="flex items-center">
            <img :src="song.thumbnail" alt="thumbnail" class="w-12 h-12 mr-2" />
            <div>
              <div class="font-semibold">{{ song.title }}</div>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div v-if="loading" class="mt-2">Loading...</div>
    <div v-if="error" class="mt-2 text-red-500">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { youtubeAPI } from '@/services/api';
import type { Song } from '@/services/api';

const searchQuery = ref('');
const results = ref<any[]>([]);
const loading = ref(false);
const error = ref('');
const debounceTimer = ref<any>(null);

const emit = defineEmits(['select-song']);

const onSearch = () => {
  if (debounceTimer.value) {
    clearTimeout(debounceTimer.value);
  }
  debounceTimer.value = setTimeout(async () => {
    if (searchQuery.value.length < 3) {
      results.value = [];
      return;
    }
    loading.value = true;
    error.value = '';
    try {
      const response = await youtubeAPI.search(searchQuery.value);
      results.value = response;
    } catch (err: any) {
      error.value = 'Failed to search for songs.';
    } finally {
      loading.value = false;
    }
  }, 500);
};

const selectSong = (song: any) => {
  emit('select-song', {
    title: song.title,
    url: song.url,
  });
  searchQuery.value = '';
  results.value = [];
};
</script>
