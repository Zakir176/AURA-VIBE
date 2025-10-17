<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <router-link to="/" class="flex items-center space-x-3 text-xl font-bold text-gray-900 hover:text-blue-600 transition-colors">
          <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span class="text-white font-bold text-sm">🎵</span>
          </div>
          <span>AuraVibe</span>
        </router-link>
        
        <nav class="flex space-x-8">
          <router-link 
            to="/create" 
            class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="text-blue-600 border-b-2 border-blue-600"
          >
            Create Session
          </router-link>
          <router-link 
            to="/join" 
            class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            active-class="text-blue-600 border-b-2 border-blue-600"
          >
            Join Session
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
</script>