<template>
  <v-container fluid class="join-session-page fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="mx-auto pa-6 elevation-12" rounded="lg">
          <v-card-title class="text-h4 text-center mb-4">
            <v-icon size="40" color="secondary" class="mr-2">mdi-login</v-icon>
            Join Session
          </v-card-title>

          <v-card-text>
            <!-- Tabs for Join Method -->
            <v-tabs v-model="tab" color="primary" class="mb-6" grow>
              <v-tab value="code">
                <v-icon class="mr-2">mdi-text</v-icon>
                Enter Code
              </v-tab>
              <v-tab value="scan">
                <v-icon class="mr-2">mdi-qrcode-scan</v-icon>
                Scan QR Code
              </v-tab>
            </v-tabs>

            <!-- Error Alert -->
            <v-alert v-if="error" type="error" variant="tonal" class="mb-4" closable @click:close="error = null">
              {{ error }}
            </v-alert>

            <!-- Success Alert -->
            <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
              {{ success }}
            </v-alert>

            <!-- Tab Content -->
            <v-window v-model="tab">
              <!-- Enter Code Tab -->
              <v-window-item value="code">
                <v-form @submit.prevent="joinSession" ref="form">
                  <p class="text-body-1 mb-4">
                    Enter the session code provided by the host:
                  </p>
                  
                  <v-text-field
                    v-model="sessionCode"
                    label="Session Code"
                    placeholder="e.g., ABC123"
                    variant="outlined"
                    prepend-inner-icon="mdi-ticket-confirmation"
                    :rules="[v => !!v || 'Session code is required']"
                    class="mb-4"
                    required
                  ></v-text-field>

                  <v-btn
                    type="submit"
                    color="primary"
                    size="large"
                    block
                    prepend-icon="mdi-login"
                    :loading="loading"
                  >
                    Join Session
                  </v-btn>
                </v-form>
              </v-window-item>

              <!-- Scan QR Code Tab -->
              <v-window-item value="scan">
                <p class="text-body-1 mb-4">
                  Scan the QR code displayed on the host's device:
                </p>
                
                <QRCodeScanner @decoded="handleQRScan" />
              </v-window-item>
            </v-window>
          </v-card-text>

          <v-card-actions class="justify-center">
            <v-btn
              text
              prepend-icon="mdi-arrow-left"
              @click="$router.push('/')"
            >
              Back to Home
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { v4 as uuidv4 } from 'uuid'
import { api } from '@/services/api'
import QRCodeScanner from '@/components/QRCodeScanner.vue'

const router = useRouter()
const route = useRoute()

const tab = ref('code')
const sessionCode = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(null)
const form = ref(null)

// Check for session code in URL query params
onMounted(() => {
  if (route.query.code) {
    sessionCode.value = route.query.code
  }
})

const joinSession = async () => {
  if (!form.value.validate()) {
    return
  }

  loading.value = true
  error.value = null
  success.value = null

  try {
    const userId = uuidv4()
    
    const response = await api.joinSession(sessionCode.value.toUpperCase(), userId)
    
    // Store user session data
    sessionStorage.setItem('sessionCode', sessionCode.value.toUpperCase())
    sessionStorage.setItem('userId', userId)
    sessionStorage.setItem('isHost', 'false')
    
    success.value = 'Successfully joined session!'
    
    // Redirect to queue after a short delay
    setTimeout(() => {
      router.push(`/session/${sessionCode.value.toUpperCase()}`)
    }, 1500)
  } catch (err) {
    error.value = 'Failed to join session. Please check the session code and try again.'
    console.error('Error joining session:', err)
  } finally {
    loading.value = false
  }
}

const handleQRScan = (decodedText) => {
  // Extract session code from QR code data
  // Assuming QR code contains just the session code or a URL with the code
  let code = decodedText
  
  if (decodedText.includes('code=')) {
    const urlParams = new URLSearchParams(decodedText.split('?')[1])
    code = urlParams.get('code')
  }
  
  sessionCode.value = code
  tab.value = 'code'
  
  // Auto-join after scanning
  setTimeout(() => {
    joinSession()
  }, 500)
}
</script>

<style scoped>
.join-session-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>