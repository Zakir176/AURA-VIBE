<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-800">
    <!-- Header -->
    <header class="flex items-center justify-between px-4 py-6 bg-white border-b border-gray-200 shadow-sm fixed w-full z-10">
      <router-link to="/" class="text-gray-600 hover:text-gray-800 transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-label="Back"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      <h1 class="text-xl font-semibold">Join Session</h1>
      <div class="w-6 h-6"></div> <!-- Spacer to balance header -->
    </header>

    <!-- Main Content -->
    <main class="pt-24 pb-4">
      <div class="max-w-md mx-auto px-4 text-center">
        <!-- Musical Note Icon -->
        <div class="mb-8 w-24 h-24 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
          <svg class="w-12 h-12 text-blue-500 opacity-75" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 6l12-3"></path></svg>
        </div>

        <h2 class="text-4xl font-extrabold text-gray-800 mb-2">Enter session code</h2>
        <p class="text-gray-500 mb-8">Enter the 6-digit code provided by the host</p>

        <!-- Session Code Input Fields -->
        <form @submit.prevent="joinSession" class="mb-8">
          <div class="flex justify-center items-center space-x-2 mb-8">
            <input
              v-for="n in 3"
              :key="'code-part-1-' + n"
              :ref="el => codeInputs[n - 1] = el as HTMLInputElement"
              v-model="sessionCodeParts[n - 1]"
              @input="handleInput(n - 1)"
              @keydown.backspace="handleBackspace(n - 1)"
              type="text"
              maxlength="1"
              class="w-12 h-14 md:w-14 md:h-16 text-center text-2xl md:text-3xl font-extrabold bg-white border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition text-gray-700"
              inputmode="numeric"
              pattern="[0-9A-Za-z]"
              uppercase
            >
            <span class="text-4xl font-bold text-gray-400">-</span>
            <input
              v-for="n in 3"
              :key="'code-part-2-' + n"
              :ref="el => codeInputs[n + 2] = el as HTMLInputElement"
              v-model="sessionCodeParts[n + 2]"
              @input="handleInput(n + 2)"
              @keydown.backspace="handleBackspace(n + 2)"
              type="text"
              maxlength="1"
              class="w-12 h-14 md:w-14 md:h-16 text-center text-2xl md:text-3xl font-extrabold bg-white border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition text-gray-700"
              inputmode="numeric"
              pattern="[0-9A-Za-z]"
              uppercase
            >
          </div>

          <div class="flex items-center my-8">
            <hr class="flex-grow border-gray-200">
            <span class="px-4 text-gray-400 text-sm font-medium">OR</span>
            <hr class="flex-grow border-gray-200">
          </div>

          <!-- Scan QR Code Button -->
          <button
            @click="openQrScanner"
            type="button"
            class="w-full bg-white text-gray-700 font-bold py-4 px-8 rounded-full text-lg flex items-center justify-center space-x-3 border border-gray-300 shadow-sm hover:bg-gray-50 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            <span>Scan QR Code</span>
          </button>
        </form>

        <!-- QR Scanner Modal/Overlay -->
        <div v-if="showQrScanner" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div class="relative bg-white rounded-lg p-6 max-w-md w-full">
            <button @click="closeQrScanner" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-bold mb-4 text-center">Scan QR Code</h3>
            
            <div v-if="!hasCameraSupport" class="p-6 bg-yellow-50 rounded-lg border border-yellow-200 text-center">
              <p class="text-yellow-700 text-sm">
                Camera access is not supported or blocked. Please enter the code manually.
              </p>
            </div>

            <div v-else-if="cameraLoading" class="p-8 text-center">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <p class="text-gray-600">Loading camera...</p>
            </div>

            <div v-else-if="cameraError" class="p-6 bg-red-50 rounded-lg border border-red-200 text-center">
              <p class="text-red-700 text-sm mb-4">{{ cameraError }}</p>
              <button @click="initCamera" class="btn-secondary text-sm py-2 px-4">
                Try Again
              </button>
            </div>

            <div v-else>
              <div class="relative bg-black rounded-lg overflow-hidden mx-auto max-w-xs mb-4">
                <qrcode-stream 
                  v-if="cameraActive"
                  :camera="cameraState"
                  @decode="onQRCodeDecoded"
                  @init="onCameraInit"
                  class="w-full h-64"
                />
                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div class="border-2 border-white border-dashed w-48 h-48 rounded-lg"></div>
                </div>
              </div>
              <p class="text-sm text-gray-600 text-center">Point your camera at a session QR code</p>
            </div>
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
          @click="joinSession"
          :disabled="!fullSessionCode.length || loading"
          class="w-full bg-blue-600 text-white font-bold py-4 px-8 rounded-full text-xl flex items-center justify-center space-x-3 hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl shadow-blue-600/30 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">Connecting...</span>
          <span v-else>Connect to Aura</span>
        </button>
        <router-link to="/help" class="block text-center text-blue-500 text-sm mt-4 hover:underline">
          <svg class="w-4 h-4 inline-block mr-1 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.126-.92.597-.92 1.247v1m-4-10c0 1.465-1.278 2.575-3.006 2.907-.542.126-.92.597-.92 1.247v1m-4-10c0 1.465-1.278 2.575-3.006 2.907-.542.126-.92.597-.92 1.247v1"></path></svg>
          Trouble joining?
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { QrcodeStream } from 'vue-qrcode-reader'
import { sessionAPI } from '@/services/api'
import { getOrCreateUserId } from '@/utils/uuid'
import { useSessionStore } from '@/stores/session'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const sessionStore = useSessionStore()
const toast = useToast()

const sessionCodeParts = ref<string[]>(['', '', '', '', '', ''])
const codeInputs = ref<(HTMLInputElement | null)[]>([])
const loading = ref(false)
const error = ref('')
const showQrScanner = ref(false)

// QR Scanner State
const hasCameraSupport = ref(true)
const cameraLoading = ref(false)
const cameraError = ref('')
const cameraActive = ref(false)
const cameraState = ref<'auto' | 'on' | 'off'>('off')
const currentCamera = ref(0)
const availableCameras = ref<MediaDeviceInfo[]>([])

const fullSessionCode = computed(() => {
  return sessionCodeParts.value.join('').toUpperCase()
})

const handleInput = (index: number) => {
  // Ensure only one character and it's alphanumeric
  if (sessionCodeParts.value[index] !== undefined) {
    sessionCodeParts.value[index] = sessionCodeParts.value[index].replace(/[^0-9a-zA-Z]/g, '').slice(0, 1)
  }

  if (sessionCodeParts.value[index] && index < 5) {
    codeInputs.value[index + 1]?.focus()
  }
}

const handleBackspace = (index: number) => {
  if (!sessionCodeParts.value[index] && index > 0) {
    codeInputs.value[index - 1]?.focus()
  }
}

// Check camera support
const checkCameraSupport = async () => {
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      hasCameraSupport.value = false
      return
    }
    
    const devices = await navigator.mediaDevices.enumerateDevices()
    const videoDevices = devices.filter(device => device.kind === 'videoinput')
    availableCameras.value = videoDevices
    
    if (videoDevices.length === 0) {
      hasCameraSupport.value = false
      cameraError.value = 'No camera found on this device'
    }
  } catch (err) {
    console.error('Camera check failed:', err)
    hasCameraSupport.value = false
    cameraError.value = 'Cannot access camera'
  }
}

const openQrScanner = async () => {
  showQrScanner.value = true
  await nextTick() // Ensure modal is rendered
  if (hasCameraSupport.value) {
    initCamera()
  }
}

const closeQrScanner = () => {
  showQrScanner.value = false
  cameraState.value = 'off' // Turn off camera when modal closes
  cameraActive.value = false
}

// Initialize camera
const initCamera = async () => {
  if (!hasCameraSupport.value) return
  
  cameraLoading.value = true
  cameraError.value = ''
  
  try {
    // Test camera access
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    })
    
    // Stop the test stream
    stream.getTracks().forEach(track => track.stop())
    
    cameraState.value = 'auto'
    cameraActive.value = true
    
  } catch (err: any) {
    console.error('Camera init failed:', err)
    cameraError.value = err.message || 'Failed to access camera'
    hasCameraSupport.value = false
  } finally {
    cameraLoading.value = false
  }
}

// Camera initialization handler
const onCameraInit = async (promise: Promise<any>) => {
  try {
    await promise
    cameraError.value = ''
  } catch (err: any) {
    console.error('QR Scanner init failed:', err)
    
    if (err.name === 'NotAllowedError') {
      cameraError.value = 'Camera access denied. Please allow camera permissions.'
    } else if (err.name === 'NotFoundError') {
      cameraError.value = 'No camera found on this device.'
    } else if (err.name === 'NotSupportedError') {
      cameraError.value = 'This browser does not support camera access.'
    } else if (err.name === 'NotReadableError') {
      cameraError.value = 'Camera is already in use by another application.'
    } else {
      cameraError.value = 'Unable to access camera. Please try again.'
    }
    
    hasCameraSupport.value = false
  }
}

// QR Code decoded handler
const onQRCodeDecoded = (decodedString: string) => {
  console.log('QR Code detected:', decodedString)
  
  // Extract session code from QR code data
  // Expected format: session code or full URL with session code
  let extractedCode = decodedString
  
  // If it's a URL, try to extract the session code
  if (decodedString.includes('/session/')) {
    const match = decodedString.match(/\/session\/([A-Z0-9]+)/i)
    if (match && match[1]) {
      extractedCode = match[1]
    }
  }
  
  // Validate session code format (alphanumeric, 6 chars)
  if (/^[A-Z0-9]{6}$/i.test(extractedCode)) {
    sessionCodeParts.value = extractedCode.toUpperCase().split('')
    toast.success('QR Code Scanned!', `Session code: ${fullSessionCode.value}`)
    
    // Automatically join session after short delay
    setTimeout(() => {
      joinSession()
    }, 1000)
    
    // Stop camera after successful scan
    closeQrScanner()
  } else {
    toast.error('Invalid QR Code', 'Please scan a valid AuraVibe session QR code')
  }
}

const joinSession = async () => {
  if (fullSessionCode.value.length !== 6) {
    toast.warning('Invalid Code', 'Please enter a 6-digit session code')
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    const userId = getOrCreateUserId()
    const response = await sessionAPI.joinSession(fullSessionCode.value, userId)
    
    // Store session info
    sessionStore.setSession(fullSessionCode.value, userId, response.host_id)
    
    toast.success('Session Joined!', `You've joined session ${fullSessionCode.value}`)
    
    // Redirect to session page
    router.push(`/session/${fullSessionCode.value}`)
    
  } catch (err: any) {
    console.error('Failed to join session:', err)
    const errorMessage = err.response?.data?.detail || 'Failed to join session. Please check the code and try again.'
    error.value = errorMessage
    toast.error('Join Failed', errorMessage)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  checkCameraSupport()
})

onUnmounted(() => {
  // Clean up camera
  cameraState.value = 'off'
})
</script>