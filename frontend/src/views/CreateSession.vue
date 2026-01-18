<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
    <!-- Header -->
    <header class="flex items-center justify-between px-4 py-6 bg-white border-b border-gray-200 shadow-sm fixed w-full z-10">
      <router-link to="/" class="text-gray-600 hover:text-gray-800 transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      <h1 class="text-xl font-semibold">Create Session</h1>
      <div class="w-6 h-6"></div> <!-- Spacer to balance header -->
    </header>

    <!-- Main Content -->
    <main class="pt-24 pb-4">
      <div class="max-w-md mx-auto px-4">
        <!-- Name Your Vibe -->
        <div class="mb-8">
          <label for="session-name" class="block text-sm font-medium text-gray-500 mb-2 uppercase tracking-wide">Name Your Vibe</label>
          <input
            id="session-name"
            type="text"
            v-model="sessionName"
            placeholder="e.g. Chill Friday Mix"
            class="w-full px-5 py-3 border border-gray-300 rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent text-lg placeholder-gray-400"
          >
        </div>

        <!-- Duration -->
        <div class="mb-8">
          <label class="block text-sm font-medium text-gray-500 mb-2 uppercase tracking-wide">Duration</label>
          <div class="flex bg-gray-200 rounded-full p-1 space-x-1">
            <button
              v-for="durationOpt in durationOptions"
              :key="durationOpt.value"
              @click="sessionDuration = durationOpt.value"
              :class="{
                'bg-white text-blue-600 shadow-md': sessionDuration === durationOpt.value,
                'text-gray-600': sessionDuration !== durationOpt.value
              }"
              class="flex-1 py-2 px-4 rounded-full text-center font-medium transition-all duration-200"
            >
              {{ durationOpt.label }}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-center">
          <p class="text-red-700 text-sm">{{ error }}</p>
        </div>
      </div>
    </main>

    <!-- Fixed Bottom Button -->
    <div class="fixed bottom-0 left-0 right-0 p-4 bg-white border-t border-gray-200 shadow-md">
      <div class="max-w-md mx-auto">
        <button 
          @click="createAndStartSession"
          :disabled="loading"
          class="w-full bg-blue-600 text-white font-bold py-4 px-8 rounded-full text-xl flex items-center justify-center space-x-3 hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl shadow-blue-600/30 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">Starting Session...</span>
          <span v-else>
            <span>Create & Start Session</span>
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { sessionAPI } from '@/services/api'
import { generateUUID } from '@/utils/uuid'
import { useSessionStore } from '@/stores/session'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const sessionStore = useSessionStore()
const toast = useToast()

const loading = ref(false)
const error = ref('')
const sessionName = ref('')
const sessionDuration = ref('2hrs') // Default to 2 hours

const durationOptions = [
  { label: '1 hr', value: '1hr' },
  { label: '2 hrs', value: '2hrs' },
  { label: '4 hrs', value: '4hrs' },
  { label: '∞', value: 'infinity' },
]

const createAndStartSession = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const hostId = generateUUID()
    const response = await sessionAPI.createSession({
      host_id: hostId,
      name: sessionName.value,
      duration: sessionDuration.value,
    })
    
    // Store session info
    sessionStore.setSession(response.session_code, hostId, response.host_id)
    
    toast.success('Session Created!', `Redirecting to session ${response.session_code}`, {
      duration: 3000,
    })

    router.push(`/session/${response.session_code}`)
    
  } catch (err: any) {
    console.error('Failed to create session:', err)
    const errorMessage = err.response?.data?.detail || 'Failed to create session. Please try again.'
    error.value = errorMessage
    toast.error('Session Creation Failed', errorMessage)
  } finally {
    loading.value = false
  }
}
</script>