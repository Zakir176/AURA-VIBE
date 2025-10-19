<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script><!-- src/App.vue -->
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
import AppHeader from '@/components/Layout/AppHeader.vue';
import ToastContainer from '@/components/Toast/ToastContainer.vue';
</script>