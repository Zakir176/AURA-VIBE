<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <AppHeader v-if="!route.meta.hideHeader" />
    <main>
      <router-view />
    </main>
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/Layout/AppHeader.vue';
import ToastContainer from '@/components/Toast/ToastContainer.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
</script>
