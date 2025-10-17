<template>
  <v-container fluid class="create-session-page fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="mx-auto pa-6 elevation-12" rounded="lg">
          <v-card-title class="text-h4 text-center mb-4">
            <v-icon size="40" color="secondary" class="mr-2">mdi-play-circle</v-icon>
            Create a New Session
          </v-card-title>

          <v-card-text>
            <!-- Session Creation Form -->
            <v-form @submit.prevent="handleCreateSession" ref="form">
              <v-text-field
                v-model="hostId"
                label="Host ID"
                placeholder="e.g., Host-1234"
                variant="outlined"
                prepend-inner-icon="mdi-account"
                :rules="[v => !!v || 'Host ID is required']"
                class="mb-4"
                required
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                prepend-icon="mdi-play-circle"
                :loading="loading"
              >
                Create Session
              </v-btn>
            </v-form>

            <!-- Show the session code and QR code if available -->
            <v-alert v-if="sessionCode" type="success" variant="tonal" class="mt-4">
              <div>Session Code: {{ sessionCode }}</div>
              <div>
                <img :src="qrCode" alt="QR Code" class="mt-2" />
              </div>
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createSession } from '@/services/api'

const router = useRouter()
const hostId = ref('')
const sessionCode = ref('')
const qrCode = ref('')
const loading = ref(false)

// Handle session creation and show the session code and QR code
const handleCreateSession = async () => {
  loading.value = true
  try {
    const response = await createSession(hostId.value) // Call the backend API to create session
    sessionCode.value = response.session_code // Set session code returned from backend
    qrCode.value = response.qr_code // Set QR code (base64 image)
  } catch (err) {
    console.error('Error creating session:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.create-session-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>
