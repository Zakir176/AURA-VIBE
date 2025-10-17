<template>
  <div class="p-8 bg-gray-50 min-h-screen">
    <div class="max-w-md mx-auto">
      <h1 class="text-3xl font-bold text-blue-600 mb-6">Tailwind v3 Test</h1>
      
      <div class="card p-6 mb-4">
        <h2 class="text-xl font-semibold mb-4">Test Components</h2>
        
        <button class="btn-primary mb-4">
          Primary Button
        </button>
        
        <button class="btn-secondary mb-4">
          Secondary Button
        </button>
        
        <input type="text" class="input-field mb-4" placeholder="Test input field">
        
        <div class="flex space-x-4">
          <div class="bg-red-500 text-white p-3 rounded">Red</div>
          <div class="bg-green-500 text-white p-3 rounded">Green</div>
          <div class="bg-blue-500 text-white p-3 rounded">Blue</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>