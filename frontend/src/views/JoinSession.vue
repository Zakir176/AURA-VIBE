<template>
  <div class="min-h-screen bg-vibe-black font-sans text-gray-200 selection:bg-vibe-indigo/30">
    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-6 glass-blur border-b border-white/5 fixed w-full z-10">
      <router-link to="/" class="p-2 text-gray-400 hover:text-white transition-all rounded-xl hover:bg-white/5 border border-transparent hover:border-white/10 group">
        <svg class="w-6 h-6 transform group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7"></path></svg>
      </router-link>
      <h1 class="text-xl font-black text-white tracking-tight uppercase">Join Session</h1>
      <div class="w-10"></div> <!-- Spacer to balance header -->
    </header>

    <!-- Main Content -->
    <main class="pt-32 pb-4">
      <div class="max-w-md mx-auto px-6 text-center">
        <!-- Musical Note Icon -->
        <div class="mb-10 w-24 h-24 bg-vibe-indigo/10 rounded-[2rem] flex items-center justify-center mx-auto shadow-[0_0_50px_-10px_rgba(79,70,229,0.3)] border border-vibe-indigo/20">
          <svg class="w-12 h-12 text-vibe-indigo" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 6l12-3"></path></svg>
        </div>

        <h2 class="text-4xl font-black text-white mb-2 tracking-tight uppercase">Enter code</h2>
        <p class="text-gray-500 mb-10 font-bold text-sm tracking-wide">Enter the 6-character code from the host</p>

        <!-- Session Code Input Fields -->
        <form @submit.prevent="joinSession" class="mb-10">
          <div class="flex justify-center items-center space-x-3 mb-10">
            <input
              v-for="n in 3"
              :key="'code-part-1-' + n"
              :ref="el => codeInputs[n - 1] = el as HTMLInputElement"
              v-model="sessionCodeParts[n - 1]"
              @input="handleInput(n - 1)"
              @keydown.backspace="handleBackspace(n - 1)"
              type="text"
              maxlength="1"
              class="w-12 h-16 md:w-16 md:h-20 text-center text-3xl font-black bg-white/5 border border-white/10 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-vibe-indigo focus:border-transparent transition-all text-white uppercase tracking-tighter"
              inputmode="text"
              pattern="[0-9A-Za-z]"
            >
            <span class="text-2xl font-black text-gray-700">-</span>
            <input
              v-for="n in 3"
              :key="'code-part-2-' + n"
              :ref="el => codeInputs[n + 2] = el as HTMLInputElement"
              v-model="sessionCodeParts[n + 2]"
              @input="handleInput(n + 2)"
              @keydown.backspace="handleBackspace(n + 2)"
              type="text"
              maxlength="1"
              class="w-12 h-16 md:w-16 md:h-20 text-center text-3xl font-black bg-white/5 border border-white/10 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-vibe-indigo focus:border-transparent transition-all text-white uppercase tracking-tighter"
              inputmode="text"
              pattern="[0-9A-Za-z]"
            >
          </div>

          <div class="flex items-center my-10">
            <hr class="flex-grow border-white/5">
            <span class="px-6 text-gray-600 text-[10px] font-black tracking-[0.3em]">OR</span>
            <hr class="flex-grow border-white/5">
          </div>

          <!-- Scan QR Code Button -->
          <button
            @click="openQrScanner"
            type="button"
            class="w-full bg-white/5 text-white font-black py-5 px-8 rounded-2xl text-lg flex items-center justify-center space-x-3 border border-white/10 hover:bg-white/10 transition-all uppercase tracking-widest group shadow-2xl"
          >
            <svg class="w-6 h-6 transform group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v1m6 1v1m-6-1v1m-6 1v1m0-1H6m12 0h-1m-1 0h1m-1 0h1m-1 0h1M6 12v1m12-1v1m-1-1v1m-1-1v1m-1-1v1M6 18v1m12-1v1m-1-1v1m-1-1v1m-1-1v1m-1-1v1H6m0 0H5m1 0h1m12 0h1m-1 0h-1"></path></svg>
            <span>Scan QR Code</span>
          </button>
        </form>

        <!-- QR Scanner Modal/Overlay -->
        <div v-if="showQrScanner" class="fixed inset-0 glass-blur flex items-center justify-center z-50 p-6">
          <div class="relative bg-vibe-navy border border-white/10 rounded-[2.5rem] p-8 max-w-md w-full shadow-[0_50px_100px_rgba(0,0,0,0.8)]">
            <button @click="closeQrScanner" class="absolute top-6 right-6 p-2 text-gray-500 hover:text-white transition-colors rounded-xl hover:bg-white/5">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
            <h3 class="text-2xl font-black mb-6 text-center text-white uppercase tracking-tight">Scan Session QR</h3>
            
            <div v-if="!hasCameraSupport" class="p-6 bg-vibe-pink/10 rounded-2xl border border-vibe-pink/20 text-center">
              <p class="text-vibe-pink text-sm font-black uppercase tracking-wider">
                Camera access not supported or blocked.
              </p>
            </div>

            <div v-else-if="cameraLoading" class="p-10 text-center">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-vibe-indigo mx-auto mb-6"></div>
              <p class="text-gray-500 font-bold uppercase text-xs tracking-widest">Waking up camera...</p>
            </div>

            <div v-else-if="cameraError" class="p-6 bg-vibe-pink/10 rounded-2xl border border-vibe-pink/20 text-center">
              <p class="text-vibe-pink text-xs font-black uppercase tracking-wider mb-4">{{ cameraError }}</p>
              <button @click="initCamera" class="px-6 py-2 bg-white text-vibe-black font-black rounded-xl text-xs uppercase tracking-widest shadow-xl">
                Try Again
              </button>
            </div>

            <div v-else>
              <div class="relative bg-black rounded-3xl overflow-hidden mx-auto max-w-xs mb-6 shadow-2xl ring-1 ring-white/20">
                <qrcode-stream 
                  v-if="cameraActive"
                  :camera="cameraState"
                  @decode="onQRCodeDecoded"
                  @init="onCameraInit"
                  class="w-full h-80"
                />
                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div class="border-4 border-vibe-indigo border-dashed w-56 h-56 rounded-3xl opacity-40 animate-pulse"></div>
                </div>
              </div>
              <p class="text-xs font-bold text-gray-500 text-center uppercase tracking-widest">Point camera at the host's screen</p>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 p-4 bg-vibe-pink/10 border border-vibe-pink/20 rounded-2xl text-center">
          <p class="text-vibe-pink text-xs font-black uppercase tracking-wider leading-relaxed">{{ error }}</p>
        </div>
      </div>
    </main>

    <!-- Fixed Bottom Button -->
    <div class="fixed bottom-0 left-0 right-0 p-6 glass-blur border-t border-white/5">
      <div class="max-w-md mx-auto">
        <button 
          @click="joinSession"
          :disabled="!fullSessionCode.length || loading"
          class="w-full bg-vibe-indigo text-white font-black py-5 px-8 rounded-2xl text-lg flex items-center justify-center space-x-3 hover:bg-vibe-purple transition-all duration-500 shadow-[0_0_40px_-5px_rgba(79,70,229,0.4)] hover:shadow-vibe-indigo/60 disabled:opacity-20 disabled:cursor-not-allowed group uppercase tracking-[0.1em]"
        >
          <span v-if="loading">Connecting...</span>
          <span v-else class="flex items-center">
             <span>Connect to Aura</span>
             <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { QrcodeStream } from 'vue-qrcode-reader'
import { sessionAPI } from '@/services/api'
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
    const response = await sessionAPI.joinSession(fullSessionCode.value)
    
    // Store session info
    sessionStore.setSession(fullSessionCode.value, response.token, 'guest')
    
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