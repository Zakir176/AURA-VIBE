<template>
  <div>
    <input
      type="text"
      v-model="searchQuery"
      @input="onSearch"
      placeholder="Search for a song on Jamendo..."
      class="input-field"
    />
    <div v-if="results.length > 0" class="mt-2">
      <ul>
        <li
          v-for="song in results"
          :key="song.id"
          @click="selectSong(song)"
          class="p-2 hover:bg-gray-100 cursor-pointer"
        >
          <div class="flex items-center">
            <img :src="song.image" alt="thumbnail" class="w-12 h-12 mr-2" />
            <div>
              <div class="font-semibold">{{ song.name }}</div>
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
import { jamendoAPI } from '@/services/api';
import type { JamendoSong } from '@/services/api';

const searchQuery = ref('');
const results = ref<JamendoSong[]>([]);
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
      const response = await jamendoAPI.search(searchQuery.value);
      results.value = response;
    } catch (err: any) {
      error.value = 'Failed to search for songs.';
    } finally {
      loading.value = false;
    }
  }, 500);
};

const selectSong = (song: JamendoSong) => {
  emit('select-song', song);
  searchQuery.value = '';
  results.value = [];
};
</script>
