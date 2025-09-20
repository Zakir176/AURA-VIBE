<template>
    <v-app>
    <Navbar />
    <router-view />
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Navbar from './components/Navbar.vue'

const isAuthenticated = ref(false);

function checkAuth() {
  isAuthenticated.value = document.cookie.includes('access_token');
}

function loginWithSpotify() {
  window.location.href = 'http://127.0.0.1:8000/login';
}

onMounted(() => {
  checkAuth();
});
</script>
