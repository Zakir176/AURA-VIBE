<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <AppHeader />
    <main>
      <router-view />
    </main>
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import ToastContainer from '@/components/Toast/ToastContainer.vue';
</script>