<template>
  <v-container class="d-flex flex-column align-center justify-center py-12">
    <v-breadcrumbs class="mb-4" :items="breadcrumbs" aria-label="Breadcrumb">
      <template #divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>

    <v-card class="pa-10" elevation="6" max-width="880">
      <v-card-title class="text-h5 font-weight-bold text-center mb-2">
        Get Started
      </v-card-title>
      <v-card-subtitle class="text-center mb-6">
        Choose how you want to begin
      </v-card-subtitle>

      <v-row class="mt-2" align="stretch" justify="center" dense>
        <v-col cols="12" md="6" class="d-flex">
          <v-sheet class="pa-6 rounded-lg d-flex flex-column justify-space-between w-100" elevation="2">
            <div>
              <div class="d-flex align-center mb-3">
                <v-icon class="mr-2" color="primary">mdi-plus-circle</v-icon>
                <h3 class="text-h6 font-weight-bold mb-0">Create a Session</h3>
              </div>
              <p class="text-body-2 text-medium-emphasis mb-6">
                Host a new collaborative session and share the QR code or link.
              </p>
            </div>
            <v-btn color="primary" class="rounded-pill" block @click="onCreateClick" aria-label="Create a session">
              Create Session
            </v-btn>
          </v-sheet>
        </v-col>

        <v-col cols="12" md="6" class="d-flex">
          <v-sheet class="pa-6 rounded-lg d-flex flex-column justify-space-between w-100" elevation="2">
            <div>
              <div class="d-flex align-center mb-3">
                <v-icon class="mr-2" color="primary">mdi-login-variant</v-icon>
                <h3 class="text-h6 font-weight-bold mb-0">Join a Session</h3>
              </div>
              <p class="text-body-2 text-medium-emphasis mb-4">
                Enter a session ID to join an existing room.
              </p>
              <v-form @submit.prevent="onQuickJoin" ref="quickJoinFormRef">
                <v-text-field
                  v-model="quickJoinId"
                  label="Session ID"
                  placeholder="e.g., ABCD1234"
                  :rules="[rules.required, rules.idFormat]"
                  prepend-inner-icon="mdi-pound"
                  variant="outlined"
                  density="comfortable"
                  aria-label="Session ID"
                  autocomplete="off"
                  class="mb-3"
                ></v-text-field>
                <v-btn type="submit" variant="tonal" color="primary" class="rounded-pill" block aria-label="Join session">
                  Join Session
                </v-btn>
              </v-form>
            </div>
          </v-sheet>
        </v-col>
      </v-row>

      <!-- Music Player Integration -->
      <v-divider class="my-8"></v-divider>
      
      <div class="text-center mb-4">
        <h3 class="text-h6 font-weight-bold mb-2">Music Player</h3>
        <p class="text-body-2 text-medium-emphasis">Control your Spotify music while collaborating</p>
      </div>

      <MusicPlayer v-if="accessToken" :access-token="accessToken" />
      <v-alert v-else type="info" variant="text" class="text-center">
        <v-icon class="mr-2">mdi-music</v-icon>
        Music player will appear here once you're authenticated
      </v-alert>

      <v-expand-transition>
        <div v-if="message" class="text-center mt-6 text-medium-emphasis">
          {{ message }}
        </div>
      </v-expand-transition>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MusicPlayer from '@/components/MusicPlayer.vue'
import { useSpotify } from '@/composables/useSpotify'

const router = useRouter()
const { getCurrentPlayback } = useSpotify()

const breadcrumbs = [
  { title: 'Home', disabled: false, to: { name: 'Home' } },
  { title: 'Get Started', disabled: true }
]

const quickJoinId = ref('')
const message = ref('')
const quickJoinFormRef = ref(null)
const accessToken = ref('')

const rules = {
  required: (v) => !!v || 'Session ID is required',
  idFormat: (v) => !v || /^[A-Za-z0-9-]{4,16}$/.test(v) || 'Use 4-16 letters/numbers'
}

const onCreateClick = () => {
  console.log('analytics: click_create_session')
  router.push({ name: 'CreateSession' })
}

const onQuickJoin = () => {
  console.log('analytics: quick_join_attempt', { id: quickJoinId.value })
  if (!quickJoinId.value || !rules.idFormat(quickJoinId.value) === true) {
    message.value = 'Please enter a valid session ID.'
    return
  }
  message.value = ''
  router.push({ name: 'JoinSession', query: { id: quickJoinId.value } })
}

onMounted(async () => {
  // Get access token for music player
  try {
    const response = await fetch('/api/spotify/token', { credentials: 'include' })
    if (response.ok) {
      const data = await response.json()
      accessToken.value = data.access_token
    }
  } catch (error) {
    console.log('No access token available')
  }
})
</script>

<style scoped>
</style>