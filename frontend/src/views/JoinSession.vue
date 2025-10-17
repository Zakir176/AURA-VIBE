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
              class="input-field text-center text-lg font-mono"
              placeholder="e.g. ABC123"
              :disabled="loading"
            >
          </div>

          <button 
            type="submit"
            :disabled="!sessionCode || loading"
            class="btn-primary w-full py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Joining...</span>
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

const router = useRouter()
const sessionCode = ref('')
const loading = ref(false)
const error = ref('')

const joinSession = async () => {
  if (!sessionCode.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    // TODO: Replace with actual API call
    console.log('Joining session:', sessionCode.value)
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // For now, just redirect (we'll add proper validation later)
    router.push(`/session/${sessionCode.value}`)
    
  } catch (err) {
    console.error('Failed to join session:', err)
    error.value = 'Failed to join session. Please check the code and try again.'
  } finally {
    loading.value = false
  }
}
</script>