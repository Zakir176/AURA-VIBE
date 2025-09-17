<template>
  <v-container class="auth-container d-flex flex-column align-center justify-center py-12">
    <v-card class="auth-card pa-8" elevation="8" max-width="420">
      <div class="logo-circle mb-6">
        <v-icon size="36">mdi-music</v-icon>
      </div>
      <div class="headline text-center mb-1">Sign in</div>
      <div class="subhead text-center mb-6">Continue with Spotify</div>

      <v-btn class="spotify-btn mb-1" size="large" block @click="loginWithSpotify" aria-label="Sign in with Spotify">
        <v-icon size="20" class="mr-2">mdi-spotify</v-icon>
        Continue with Spotify
      </v-btn>

      <div class="footnote text-center mt-6">You’ll be redirected to authorize access.</div>
    </v-card>
  </v-container>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// These should come from environment or backend config
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const redirectTo = route.query.redirect || '/'

function loginWithSpotify() {
  const url = new URL(`${API_BASE}/api/auth/spotify/login`)
  if (redirectTo) url.searchParams.set('redirect', String(redirectTo))
  window.location.assign(url.toString())
}

// Apple login removed per project scope
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f7f7f9 0%, #eef1f6 100%);
}
.auth-card {
  border-radius: 28px;
  backdrop-filter: blur(10px);
}
.logo-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: #f2f2f7;
}
.headline {
  font-size: 22px;
  font-weight: 700;
}
.subhead {
  font-size: 14px;
  color: #6e6e73;
}
.apple-btn {
  background: #000;
  color: #fff;
  border-radius: 14px;
  text-transform: none;
  letter-spacing: 0;
}
.spotify-btn {
  background: #1DB954;
  color: #fff;
  border-radius: 14px;
  text-transform: none;
  letter-spacing: 0;
}
.footnote {
  color: #6e6e73;
  font-size: 12px;
}
@media (max-width: 600px) {
  .auth-card { border-radius: 24px; }
}
</style>


