<!-- src/components/QRCodeScanner.vue -->
<template>
  <div>
    <qrcode-stream @decode="onDecode" @init="onInit" @error="onError" />
    <v-alert v-if="initError" type="error" variant="tonal" class="mt-4">
      {{ initError }}
    </v-alert>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { QrcodeStream } from 'vue-qrcode-reader'

const emit = defineEmits(['decoded'])

const initError = ref(null)

function onDecode(decodedText) {
  emit('decoded', decodedText)
}

function onInit(promise) {
  promise.catch(err => {
    initError.value = 'Camera access denied or not available.'
    console.error('QR scanner init error:', err)
  })
}

function onError(error) {
  console.error('QR scan error:', error)
}
</script>
