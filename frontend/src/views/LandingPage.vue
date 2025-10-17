<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <div class="mb-8">
        <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <span class="text-2xl text-white">🎵</span>
        </div>
        <h1 class="text-5xl font-bold text-gray-900 mb-4">AuraVibe</h1>
        <p class="text-xl text-gray-600 max-w-md mx-auto">
          Create and join music sessions. Queue up your favorite tracks and vibe together.
        </p>
      </div>

      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center max-w-md mx-auto">
        <router-link 
          to="/create" 
          class="btn-primary text-lg px-8 py-4 w-full sm:w-auto"
        >
          🎤 Create Session
        </router-link>
        <router-link 
          to="/join" 
          class="btn-secondary text-lg px-8 py-4 w-full sm:w-auto"
        >
          🎧 Join Session
        </router-link>
      </div>

      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
        <div class="card p-6 text-center">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span class="text-blue-600 text-xl">⚡</span>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Real-time Sync</h3>
          <p class="text-gray-600 text-sm">Live queue updates across all devices</p>
        </div>
        
        <div class="card p-6 text-center">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span class="text-green-600 text-xl">📱</span>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Easy Sharing</h3>
          <p class="text-gray-600 text-sm">QR codes for quick session joining</p>
        </div>
        
        <div class="card p-6 text-center">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <span class="text-purple-600 text-xl">🎶</span>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Collaborative</h3>
          <p class="text-gray-600 text-sm">Everyone can add to the queue</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>