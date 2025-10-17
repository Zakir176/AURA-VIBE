<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <router-link to="/" class="flex items-center space-x-3 text-lg font-semibold text-gray-900">
              <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span class="text-white text-sm">🎵</span>
              </div>
              <span>AuraVibe</span>
            </router-link>
            <div class="h-6 w-px bg-gray-300"></div>
            <div>
              <p class="text-sm text-gray-600">Session</p>
              <p class="font-mono font-semibold text-gray-900">{{ sessionCode }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <button 
              @click="copySessionCode"
              class="btn-secondary text-sm py-2 px-4"
            >
              Copy Code
            </button>
            <router-link to="/" class="text-gray-600 hover:text-gray-900 text-sm font-medium">
              Leave
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Queue Section -->
        <div class="lg:col-span-2">
          <div class="card p-6">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Music Queue</h2>
            
            <div v-if="queue.length === 0" class="text-center py-12">
              <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl text-gray-400">🎵</span>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">No songs in queue</h3>
              <p class="text-gray-600">Add the first song to get the party started!</p>
            </div>

            <div v-else class="space-y-3">
              <div 
                v-for="(song, index) in queue" 
                :key="index"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border"
              >
                <div class="flex items-center space-x-4">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span class="text-blue-600 font-semibold text-sm">{{ index + 1 }}</span>
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ song.song_title }}</h3>
                    <p class="text-sm text-gray-600">Added by {{ song.added_by }}</p>
                  </div>
                </div>
                <a 
                  :href="song.song_url" 
                  target="_blank"
                  class="btn-primary text-sm py-1 px-3"
                >
                  Play
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Song Section -->
        <div class="space-y-6">
          <div class="card p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Add Song</h3>
            <form @submit.prevent="addSong">
              <div class="space-y-4">
                <div>
                  <label for="songTitle" class="block text-sm font-medium text-gray-700 mb-1">
                    Song Title
                  </label>
                  <input
                    id="songTitle"
                    v-model="songTitle"
                    type="text"
                    required
                    class="input-field"
                    placeholder="Enter song name"
                  >
                </div>
                
                <div>
                  <label for="songUrl" class="block text-sm font-medium text-gray-700 mb-1">
                    YouTube URL
                  </label>
                  <input
                    id="songUrl"
                    v-model="songUrl"
                    type="url"
                    required
                    class="input-field"
                    placeholder="https://www.youtube.com/watch?v=..."
                  >
                </div>
                
                <button 
                  type="submit"
                  :disabled="!songTitle || !songUrl || addingSong"
                  class="btn-primary w-full py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="addingSong">Adding...</span>
                  <span v-else>Add to Queue</span>
                </button>
              </div>
            </form>
          </div>

          <!-- Session Info -->
          <div class="card p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Session Info</h3>
            <div class="space-y-3">
              <div>
                <p class="text-sm text-gray-600">Session Code</p>
                <p class="font-mono font-semibold">{{ sessionCode }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Your User ID</p>
                <p class="font-mono text-sm truncate">{{ userId }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const sessionCode = route.params.sessionCode as string

const queue = ref<any[]>([])
const songTitle = ref('')
const songUrl = ref('')
const addingSong = ref(false)
const userId = ref('user-' + Math.random().toString(36).substr(2, 9))

// Mock data for now
onMounted(() => {
  // TODO: Replace with actual API calls
  queue.value = [
    {
      song_title: "Bohemian Rhapsody",
      song_url: "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
      added_by: "user-abc123"
    },
    {
      song_title: "Sweet Child O' Mine",
      song_url: "https://www.youtube.com/watch?v=1w7OgIMMRc4", 
      added_by: "user-def456"
    }
  ]
})

const addSong = async () => {
  if (!songTitle.value || !songUrl.value) return
  
  addingSong.value = true
  try {
    // TODO: Replace with actual API call
    console.log('Adding song:', { songTitle: songTitle.value, songUrl: songUrl.value })
    
    // Mock adding song
    queue.value.push({
      song_title: songTitle.value,
      song_url: songUrl.value,
      added_by: userId.value
    })
    
    // Clear form
    songTitle.value = ''
    songUrl.value = ''
    
  } catch (error) {
    console.error('Failed to add song:', error)
  } finally {
    addingSong.value = false
  }
}

const copySessionCode = () => {
  navigator.clipboard.writeText(sessionCode)
  // You could add a toast notification here
  alert('Session code copied to clipboard!')
}
</script>