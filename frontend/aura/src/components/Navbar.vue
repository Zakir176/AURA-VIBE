<template>
  <transition name="fade">
    <v-app-bar
      v-show="showNavbar"
      app
      flat
      height="70"
      :class="['navbar', { 'scrolled': isScrolled }]"
    >
      <v-container class="d-flex align-center justify-space-between">
        <!-- Logo + Brand -->
        <div class="d-flex align-center">
          <img src="\assets/logo.png" alt="Aura Vibe Logo" class="logo" />
          <span class="brand">Aura Vibe</span>
        </div>

        <!-- Desktop Links -->
        <v-row class="d-none d-md-flex" dense>
          <v-btn variant="text" class="nav-link" @click="scrollTo('home')">Home</v-btn>
          <v-btn variant="text" class="nav-link" @click="scrollTo('features')">Features</v-btn>
          <v-btn variant="text" class="nav-link" @click="scrollTo('pricing')">Pricing</v-btn>
          <v-btn variant="text" class="nav-link" @click="scrollTo('about')">About</v-btn>
        </v-row>

        <!-- CTA (desktop only) -->
        <v-btn class="d-none d-md-flex rounded-pill px-6 cta-btn" :to="{ name: 'CreateSession' }">
          Get Started
        </v-btn>

        <!-- Hamburger (mobile only) -->
        <v-btn
          icon
          class="d-flex d-md-none"
          @click="drawer = !drawer"
        >
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </v-container>
    </v-app-bar>
  </transition>

  <!-- Mobile Drawer -->
  <v-navigation-drawer
    v-model="drawer"
    temporary
    right
  >
    <v-list>
      <v-list-item @click="scrollTo('home'); drawer = false">
        <v-list-item-title>Home</v-list-item-title>
      </v-list-item>
      <v-list-item @click="scrollTo('features'); drawer = false">
        <v-list-item-title>Features</v-list-item-title>
      </v-list-item>
      <v-list-item @click="scrollTo('pricing'); drawer = false">
        <v-list-item-title>Pricing</v-list-item-title>
      </v-list-item>
      <v-list-item @click="scrollTo('about'); drawer = false">
        <v-list-item-title>About</v-list-item-title>
      </v-list-item>
    </v-list>
    <div class="pa-4">
      <v-btn color="primary" class="rounded-pill px-6" :to="{ name: 'CreateSession' }">
      Get Started
      </v-btn>
    </div>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const showNavbar = ref(true);
const isScrolled = ref(false);
const drawer = ref(false);

let lastScrollY = window.scrollY;

const handleScroll = () => {
  if (window.scrollY > lastScrollY && window.scrollY > 100) {
    showNavbar.value = false;
  } else {
    showNavbar.value = true;
  }
  isScrolled.value = window.scrollY > 50;
  lastScrollY = window.scrollY;
};

// Smooth scroll to section
const scrollTo = (id) => {
  const section = document.getElementById(id);
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
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
  background: transparent;
  transition: all 0.3s ease;
  box-shadow: none;
}
.navbar.scrolled {
  background: linear-gradient(135deg, rgba(58, 141, 255, 0.85), rgba(108, 99, 255, 0.85));
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  height: 50px;
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

.cta-btn {
  background: linear-gradient(135deg, #3a8dff, #6c63ff);
  color: white;
  font-weight: 600;
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
