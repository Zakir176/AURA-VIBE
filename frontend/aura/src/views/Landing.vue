<template>
  <div class="d-flex flex-column align-center justify-center" style="height: 100vh;">
    <h1>Welcome to Aura Vibe</h1>
    <p>Discover and create your music session.</p>
    <v-btn color="primary" @click="goToSession">
      Get Started
    </v-btn>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
function goToSession() {
  router.push('/session')
}
</script>
