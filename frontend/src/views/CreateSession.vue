<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <router-link to="/" class="inline-block mb-6">
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mx-auto">
            <span class="text-white font-bold text-lg">🎵</span>
          </div>
        </router-link>
        <h1 class="text-3xl font-bold text-gray-900">Create Session</h1>
        <p class="text-gray-600 mt-2">Start a new music session for your friends to join</p>
      </div>

      <div class="card p-8">
        <div class="text-center">
          <button 
            @click="createSession"
            :disabled="loading"
            class="btn-primary w-full py-4 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Creating Session...</span>
            <span v-else>🎤 Create Music Session</span>
          </button>
        </div>

        <div v-if="sessionData" class="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
          <h3 class="text-xl font-semibold text-gray-900 text-center mb-4">Session Created! 🎉</h3>
          
          <div class="bg-white rounded-lg p-4 mb-4 border">
            <p class="text-sm text-gray-600 mb-1">Session Code:</p>
            <p class="text-2xl font-mono font-bold text-blue-600">{{ sessionData.session_code }}</p>
          </div>

          <div class="text-center mb-4">
            <p class="text-sm text-gray-600 mb-2">Scan QR Code to join:</p>
            <img 
              v-if="sessionData.qr_code && sessionData.qr_code !== 'mock-base64-qr-code'"
              :src="`data:image/png;base64,${sessionData.qr_code}`" 
              alt="QR Code" 
              class="mx-auto border rounded-lg shadow-sm w-48 h-48"
            />
            <div v-else class="w-48 h-48 bg-gray-200 rounded-lg flex items-center justify-center mx-auto">
              <span class="text-gray-500">QR Code Preview</span>
            </div>
          </div>

          <button 
            @click="goToSession"
            class="btn-primary w-full py-3"
          >
            Enter Session
          </button>
        </div>

        <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-700 text-sm">{{ error }}</p>
        </div>
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
const sessionData = ref<any>(null)
const error = ref('')

const createSession = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const hostId = generateUUID()
    const response = await sessionAPI.createSession(hostId)
    sessionData.value = response
    
    // Store session info
    sessionStore.setSession(response.session_code, hostId)
    
    toast.success('Session Created!', `Share code: ${response.session_code}`, {
      duration: 10000,
    })
    
  } catch (err: any) {
    console.error('Failed to create session:', err)
    const errorMessage = err.response?.data?.detail || 'Failed to create session. Please try again.'
    error.value = errorMessage
    toast.error('Session Creation Failed', errorMessage)
  } finally {
    loading.value = false
  }
}

const goToSession = () => {
  if (sessionData.value?.session_code) {
    router.push(`/session/${sessionData.value.session_code}`)
  }
}
</script>