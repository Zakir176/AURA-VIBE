<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-block mb-6">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mx-auto">
            <span class="text-white font-bold text-lg">🎵</span>
          </div>
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">Join Session</h1>
        <p class="text-gray-600 mt-2">Enter a session code to join the music queue</p>
      </div>

      <div class="card p-8">
        <form @submit.prevent="joinSession">
          <div class="mb-6">
            <label for="sessionCode" class="block text-sm font-medium text-gray-700 mb-2">
              Session Code
            </label>
            <input
              id="sessionCode"
              v-model="sessionCode"
              type="text"
              required
              class="input-field text-center text-lg font-mono uppercase"
              placeholder="e.g. ABC123"
              :disabled="loading"
            >
          </div>

          <button 
            type="submit"
            :disabled="!sessionCode || loading"
            class="btn-primary w-full py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Joining Session...</span>
            <span v-else>🎧 Join Session</span>
          </button>
        </form>

        <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700 text-sm">{{ error }}</p>
        </div>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Don't have a code? Ask the session host for the QR code or session code.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { sessionAPI } from '@/services/api'
import { getOrCreateUserId } from '@/utils/uuid'
import { useSessionStore } from '@/stores/session'

const router = useRouter()
const sessionStore = useSessionStore()

const sessionCode = ref('')
const loading = ref(false)
const error = ref('')

const joinSession = async () => {
  if (!sessionCode.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const userId = getOrCreateUserId(sessionCode.value)
    await sessionAPI.joinSession(sessionCode.value, userId)
    
    // Store session info
    sessionStore.setSession(sessionCode.value, userId)
    
    // Redirect to session page
    router.push(`/session/${sessionCode.value}`)
    
  } catch (err: any) {
    console.error('Failed to join session:', err)
    error.value = err.response?.data?.detail || 'Failed to join session. Please check the code and try again.'
  } finally {
    loading.value = false
  }
}
</script>