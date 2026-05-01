<template>
  <div class="min-h-screen bg-vibe-black font-sans text-gray-200 selection:bg-vibe-indigo/30">
    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-6 glass-blur border-b border-white/5 fixed w-full z-10">
      <router-link to="/" class="p-2 text-gray-400 hover:text-white transition-all rounded-xl hover:bg-white/5 border border-transparent hover:border-white/10 group">
        <svg class="w-6 h-6 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      <h1 class="text-xl font-black text-white tracking-tight uppercase">Create Session</h1>
      <div class="w-10"></div> <!-- Spacer to balance header -->
    </header>

    <!-- Main Content -->
    <main class="pt-32 pb-4">
      <div class="max-w-md mx-auto px-6">
        <!-- Name Your Vibe -->
        <div class="mb-10">
          <label for="session-name" class="block text-[10px] font-black text-gray-500 mb-3 uppercase tracking-[0.2em]">Name Your Vibe</label>
          <input
            id="session-name"
            type="text"
            v-model="sessionName"
            placeholder="E.G. CHILL FRIDAY MIX"
            class="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-vibe-indigo focus:border-transparent text-lg font-black text-white placeholder-gray-700 uppercase tracking-wider transition-all"
          >
        </div>

        <!-- Duration -->
        <div class="mb-10">
          <label class="block text-[10px] font-black text-gray-500 mb-3 uppercase tracking-[0.2em]">Duration</label>
          <div class="flex bg-white/5 rounded-2xl p-1.5 border border-white/5">
            <button
              v-for="durationOpt in durationOptions"
              :key="durationOpt.value"
              @click="sessionDuration = durationOpt.value"
              :class="{
                'bg-white text-vibe-black shadow-xl': sessionDuration === durationOpt.value,
                'text-gray-500 hover:text-white': sessionDuration !== durationOpt.value
              }"
              class="flex-1 py-2 rounded-xl text-center text-xs font-black transition-all duration-300 uppercase tracking-widest"
            >
              {{ durationOpt.label }}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 p-4 bg-vibe-pink/10 border border-vibe-pink/20 rounded-2xl text-center">
          <p class="text-vibe-pink text-xs font-black uppercase tracking-wider">{{ error }}</p>
        </div>
      </div>
    </main>

    <!-- Fixed Bottom Button -->
    <div class="fixed bottom-0 left-0 right-0 p-6 glass-blur border-t border-white/5">
      <div class="max-w-md mx-auto">
        <button 
          @click="createAndStartSession"
          :disabled="loading"
          class="w-full bg-vibe-indigo text-white font-black py-5 px-8 rounded-2xl text-lg flex items-center justify-center space-x-3 hover:bg-vibe-purple transition-all duration-500 shadow-[0_0_40px_-5px_rgba(79,70,229,0.4)] hover:shadow-vibe-indigo/60 disabled:opacity-20 disabled:cursor-not-allowed group uppercase tracking-[0.1em]"
        >
          <span v-if="loading">Starting Session...</span>
          <span v-else class="flex items-center">
            <span>Create & Start Session</span>
            <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
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
    const response = await sessionAPI.createSession({
      name: sessionName.value,
      duration: sessionDuration.value,
    })
    
    // Store session info
    sessionStore.setSession(response.session_code, response.token, 'host')
    
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