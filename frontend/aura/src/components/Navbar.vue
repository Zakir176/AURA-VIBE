<template>
  <transition name="fade">
    <v-app-bar
      v-show="showNavbar"
      app
      flat
      height="70"
      class="navbar"
    >
      <v-container class="d-flex align-center justify-space-between">
        <!-- Logo -->
        <div class="d-flex align-center">
          <img src="\assets/logo.png" alt="Aura Vibe Logo" class="logo" />
          <span class="brand">Aura Vibe</span>
        </div>

        <!-- Links -->
        <v-row class="d-none d-md-flex" dense>
          <v-btn variant="text" class="nav-link">Home</v-btn>
          <v-btn variant="text" class="nav-link">Features</v-btn>
          <v-btn variant="text" class="nav-link">Pricing</v-btn>
          <v-btn variant="text" class="nav-link">About</v-btn>
        </v-row>

        <!-- CTA -->
        <v-btn color="primary" class="rounded-pill px-6">Get Started</v-btn>
      </v-container>
    </v-app-bar>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const showNavbar = ref(true);
let lastScrollY = window.scrollY;

const handleScroll = () => {
  if (window.scrollY > lastScrollY && window.scrollY > 100) {
    // scrolling down → hide navbar
    showNavbar.value = false;
  } else {
    // scrolling up → show navbar
    showNavbar.value = true;
  }
  lastScrollY = window.scrollY;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<style scoped>
.navbar {
  background: linear-gradient(
    135deg,
    rgba(0, 123, 255, 0.85),
    rgba(0, 180, 255, 0.85)
  );
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.logo {
  height: 100px;
  margin-right: 10px;
}

.brand {
  font-weight: 600;
  font-size: 1.2rem;
  color: white;
}

.nav-link {
  color: white !important;
  font-weight: 500;
  text-transform: none;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
