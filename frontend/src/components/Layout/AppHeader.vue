<!-- src/components/Layout/AppHeader.vue -->
<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-3 text-xl font-bold text-gray-900">
          <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span class="text-white text-lg">🎵</span>
          </div>
          <span>AuraVibe</span>
        </router-link>

        <!-- Navigation -->
        <nav class="flex items-center space-x-6">
          <router-link 
            to="/" 
            class="text-gray-600 hover:text-gray-900 font-medium transition-colors duration-200"
            active-class="text-blue-600"
          >
            Home
          </router-link>
          <router-link 
            to="/create" 
            class="text-gray-600 hover:text-gray-900 font-medium transition-colors duration-200"
            active-class="text-blue-600"
          >
            Create Session
          </router-link>
          <router-link 
            to="/join" 
            class="text-gray-600 hover:text-gray-900 font-medium transition-colors duration-200"
            active-class="text-blue-600"
          >
            Join Session
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
// Component logic can be added here if needed
</script>