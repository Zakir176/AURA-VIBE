<template>
  <div
    class="bg-white p-6 rounded-xl shadow-md border border-gray-200 text-center transform transition-transform duration-300 hover:scale-105 hover:shadow-xl cursor-pointer"
  >
    <div class="text-5xl mb-4">{{ icon }}</div>
    <h3 class="text-xl font-bold mb-2 text-purple-600">{{ title }}</h3>
    <p class="text-gray-600">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  icon: String,
  description: String,
})
</script>
