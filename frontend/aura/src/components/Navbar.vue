<template>
  <v-app-bar
    app
    flat
    elevate-on-scroll
    class="navbar"
  >
    <!-- Logo -->
    <v-toolbar-title class="text-h5 font-weight-bold text-primary">
      AURA
    </v-toolbar-title>

    <!-- Desktop Links -->
    <v-spacer></v-spacer>
    <div class="d-none d-md-flex align-center">
      <v-btn text to="#home">Home</v-btn>
      <v-btn text to="#features">Features</v-btn>
      <v-btn text to="#pricing">Pricing</v-btn>
      <v-btn text to="#about">About</v-btn>
      <v-btn text to="#contact">Contact</v-btn>
    </div>

    <!-- CTA -->
    <v-btn
      class="ml-4"
      color="primary"
      rounded
      depressed
      to="#get-started"
    >
      Get Started
    </v-btn>

    <!-- Mobile Menu -->
    <v-app-bar-nav-icon class="d-md-none" @click="drawer = !drawer"></v-app-bar-nav-icon>
  </v-app-bar>

  <!-- Drawer for Mobile -->
  <v-navigation-drawer
    v-model="drawer"
    temporary
    right
  >
    <v-list>
      <v-list-item v-for="item in menu" :key="item.text" :to="item.link">
        <v-list-item-title>{{ item.text }}</v-list-item-title>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item to="#get-started">
        <v-btn block color="primary" rounded>Get Started</v-btn>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref } from "vue";

const drawer = ref(false);

const menu = [
  { text: "Home", link: "#home" },
  { text: "Features", link: "#features" },
  { text: "Pricing", link: "#pricing" },
  { text: "About", link: "#about" },
  { text: "Contact", link: "#contact" },
];
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
}
</style>
