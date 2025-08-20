<template>
  <div
    v-motion
    class="bg-surface p-6 rounded-xl shadow-md flex flex-col items-center text-center hover:shadow-lg transition cursor-default"
  >
    <div class="text-5xl mb-4" aria-hidden="true">
      {{ icon }}
    </div>
    <h3 class="text-xl font-semibold mb-2 text-primary-end">{{ title }}</h3>
    <p class="text-text">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  icon: String,
  description: String,
})
</script>
