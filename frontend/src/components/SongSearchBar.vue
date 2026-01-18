<template>
  <div class="relative z-50">
    <div class="relative group">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
        </div>
        <input
            type="text"
            v-model="searchQuery"
            @input="onSearch"
            placeholder="Search for a song..."
            class="block w-full pl-10 pr-3 py-3 border border-gray-200 rounded-full leading-5 bg-gray-50 text-gray-900 placeholder-gray-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all shadow-sm"
        />
        <div v-if="loading" class="absolute inset-y-0 right-0 pr-3 flex items-center">
            <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        </div>
    </div>

    <div v-if="results.length > 0" class="absolute bottom-full left-0 right-0 mb-2 bg-white rounded-2xl shadow-xl border border-gray-100 max-h-96 overflow-y-auto overflow-x-hidden">
      <ul class="py-2">
        <li
          v-for="song in results"
          :key="song.id"
          @click="selectSong(song)"
          class="px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors border-b border-gray-50 last:border-0"
        >
          <div class="flex items-center space-x-3">
            <img :src="song.image" alt="thumbnail" class="w-10 h-10 rounded-lg object-cover shadow-sm bg-gray-100" />
            <div class="min-w-0 flex-1">
              <div class="text-sm font-semibold text-gray-900 truncate">{{ song.name }}</div>
              <div class="text-xs text-gray-500 truncate">{{ song.artist_name }}</div>
            </div>
            <div class="flex-shrink-0">
                <button class="p-1.5 rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                </button>
            </div>
          </div>
        </li>
      </ul>
    </div>
    
    <div v-if="error" class="absolute bottom-full left-0 right-0 mb-2 p-3 bg-red-50 text-red-600 rounded-xl text-sm border border-red-100 shadow-lg text-center">
        {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { searchAPI } from '@/services/api';
import type { SearchSong } from '@/services/api';

const searchQuery = ref('');
const results = ref<SearchSong[]>([]);
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
      const response = await searchAPI.search(searchQuery.value, 'jamendo');
      results.value = response;
    } catch (err: any) {
      error.value = 'Failed to search for songs.';
    } finally {
      loading.value = false;
    }
  }, 500);
};

const selectSong = (song: SearchSong) => {
  emit('select-song', song);
  searchQuery.value = '';
  results.value = [];
};
</script>
