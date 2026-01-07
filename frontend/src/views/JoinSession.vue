<!-- src/views/JoinSession.vue -->
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
        <p class="text-gray-600 mt-2">Enter a session code or scan QR code to join the music queue</p>
      </div>

      <div class="card p-8">
        <!-- QR Code Scanner Toggle -->
        <div class="flex space-x-2 mb-6">
          <button
            @click="activeTab = 'manual'"
            :class="[
              'flex-1 py-2 px-4 rounded-lg font-medium transition-colors duration-200',
              activeTab === 'manual' 
                ? 'bg-blue-100 text-blue-700 border border-blue-200' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            📝 Enter Code
          </button>
          <button
            @click="activeTab = 'scan'"
            :class="[
              'flex-1 py-2 px-4 rounded-lg font-medium transition-colors duration-200',
              activeTab === 'scan' 
                ? 'bg-blue-100 text-blue-700 border border-blue-200' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            📷 Scan QR
          </button>
        </div>

        <!-- Manual Code Entry -->
        <div v-if="activeTab === 'manual'">
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
        </div>

        <!-- QR Code Scanner -->
        <div v-else class="text-center">
          <div v-if="!hasCameraSupport" class="p-6 bg-yellow-50 rounded-lg border border-yellow-200">
            <p class="text-yellow-700 text-sm">
              Camera access is not supported or blocked. Please enter the code manually.
            </p>
          </div>

          <div v-else-if="cameraLoading" class="p-8">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p class="text-gray-600">Loading camera...</p>
          </div>

          <div v-else-if="cameraError" class="p-6 bg-red-50 rounded-lg border border-red-200">
            <p class="text-red-700 text-sm mb-4">{{ cameraError }}</p>
            <button @click="initCamera" class="btn-secondary text-sm py-2 px-4">
              Try Again
            </button>
          </div>

          <div v-else class="space-y-4">
            <!-- Scanner Container -->
            <div class="relative bg-black rounded-lg overflow-hidden mx-auto max-w-xs">
              <qrcode-stream 
                v-if="cameraActive"
                :camera="cameraState"
                @decode="onQRCodeDecoded"
                @init="onCameraInit"
                class="w-full h-64"
              />
              
              <!-- Scanner Overlay -->
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div class="border-2 border-white border-dashed w-48 h-48 rounded-lg"></div>
              </div>
            </div>

            <p class="text-sm text-gray-600">Point your camera at a session QR code</p>

            <!-- Camera Controls -->
            <div class="flex justify-center space-x-4">
              <button 
                @click="toggleCamera"
                class="btn-secondary text-sm py-2 px-4 flex items-center space-x-2"
              >
                <span>{{ cameraActive ? '🛑' : '📷' }}</span>
                <span>{{ cameraActive ? 'Stop' : 'Start' }} Camera</span>
              </button>
              
              <button 
                @click="switchCamera"
                class="btn-secondary text-sm py-2 px-4 flex items-center space-x-2"
              >
                <span>🔄</span>
                <span>Switch Camera</span>
              </button>
            </div>
          </div>
        </div>

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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { QrcodeStream } from 'vue-qrcode-reader'
import { sessionAPI } from '@/services/api'
import { getOrCreateUserId } from '@/utils/uuid'
import { useSessionStore } from '@/stores/session'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const sessionStore = useSessionStore()
const toast = useToast()

const sessionCode = ref('')
const loading = ref(false)
const error = ref('')
const activeTab = ref<'manual' | 'scan'>('manual')

// QR Scanner State
const hasCameraSupport = ref(true)
const cameraLoading = ref(false)
const cameraError = ref('')
const cameraActive = ref(false)
const cameraState = ref<'auto' | 'on' | 'off'>('off')
const currentCamera = ref(0)
const availableCameras = ref<MediaDeviceInfo[]>([])

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
    sessionCode.value = extractedCode.toUpperCase()
    toast.success('QR Code Scanned!', `Session code: ${sessionCode.value}`)
    
    // Automatically join session after short delay
    setTimeout(() => {
      joinSession()
    }, 1000)
    
    // Stop camera after successful scan
    cameraState.value = 'off'
    cameraActive.value = false
  } else {
    toast.error('Invalid QR Code', 'Please scan a valid AuraVibe session QR code')
  }
}

// Toggle camera on/off
const toggleCamera = () => {
  if (cameraActive.value) {
    cameraState.value = 'off'
    cameraActive.value = false
  } else {
    cameraState.value = 'auto'
    cameraActive.value = true
  }
}

// Switch between front/back camera
const switchCamera = async () => {
  if (availableCameras.value.length <= 1) {
    toast.info('Camera Switch', 'Only one camera available')
    return
  }
  
  currentCamera.value = (currentCamera.value + 1) % availableCameras.value.length
  cameraState.value = 'off'
  
  // Brief pause before restarting with new camera
  setTimeout(() => {
    cameraState.value = 'auto'
  }, 300)
}

const joinSession = async () => {
  if (!sessionCode.value) {
    toast.warning('Invalid Code', 'Please enter a valid session code')
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    const userId = getOrCreateUserId()
    const response = await sessionAPI.joinSession(sessionCode.value, userId)
    
    // Store session info
    sessionStore.setSession(sessionCode.value, userId, response.host_id)
    
    toast.success('Session Joined!', `You've joined session ${sessionCode.value}`)
    
    // Redirect to session page
    router.push(`/session/${sessionCode.value}`)
    
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