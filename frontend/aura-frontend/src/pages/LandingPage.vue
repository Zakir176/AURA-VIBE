<template>
  <main
    class="relative min-h-screen bg-gradient-to-b from-gray-900 via-gray-900 to-gray-800 text-white px-6 md:px-20 flex flex-col items-center overflow-hidden"
  >
    <!-- Floating Gradient Blobs -->
    <div
      class="fixed top-20 left-10 w-40 h-40 bg-gradient-to-br from-purple-600 to-pink-500 rounded-full opacity-30 animate-blob filter blur-3xl pointer-events-none"
    ></div>
    <div
      class="fixed bottom-32 right-10 w-56 h-56 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full opacity-20 animate-blob animation-delay-4000 filter blur-3xl pointer-events-none"
    ></div>

    <!-- Hero Section -->
    <motion-div
      v-motion="heroMotion"
      class="flex flex-col items-center text-center max-w-4xl pt-24 z-10"
    >
      <img
        src="@/assets/logo.png"
        alt="AURA VIBE Logo"
        class="w-36 mb-6 animate-pulse"
      />
      <h1
        class="text-6xl font-extrabold mb-4 bg-gradient-to-r from-purple-400 to-pink-500 text-transparent bg-clip-text"
      >
        AURA VIBE
      </h1>
      <p class="text-pink-300 text-xl mb-10 max-w-xl">
        Your intelligent AI-powered assistant to boost productivity and
        supercharge your study sessions.
      </p>
      <button
        @mouseenter="hovering = true"
        @mouseleave="hovering = false"
        :class="[
          'rounded-full px-8 py-3 font-semibold text-gray-900 shadow-lg transition-transform duration-300 ease-in-out',
          hovering ? 'scale-105 brightness-110' : 'scale-100 brightness-100',
          'bg-gradient-to-r from-purple-400 to-pink-500'
        ]"
      >
        Get Started
      </button>
    </motion-div>

    <!-- Features Section -->
    <section
      class="mt-24 grid grid-cols-1 md:grid-cols-3 gap-12 max-w-6xl w-full z-10"
    >
      <FeatureCard
        v-for="(feature, index) in features"
        :key="index"
        v-motion="featureMotion(index)"
        :title="feature.title"
        :icon="feature.icon"
        :description="feature.description"
      />
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useMotion } from '@vueuse/motion'
import FeatureCard from '@/components/FeatureCard.vue'

const hovering = ref(false)

const heroMotion = {
  initial: { opacity: 0, scale: 0.9 },
  enter: { opacity: 1, scale: 1, transition: { duration: 0.7, ease: 'easeOut' } },
}

// Staggered feature animation, delay based on index
const featureMotion = (index) => ({
  initial: { opacity: 0, y: 30 },
  enter: {
    opacity: 1,
    y: 0,
    transition: { delay: 0.3 + index * 0.3, duration: 0.6, ease: 'easeOut' },
  },
})

const features = [
  {
    title: 'Smart Assistance',
    icon: '💡',
    description: 'Conversational AI to answer questions and explain concepts.',
  },
  {
    title: 'Study Mode',
    icon: '📚',
    description: 'Organize tasks, generate summaries, and break down complex topics.',
  },
  {
    title: 'Productivity Tools',
    icon: '⏰',
    description: 'Timer, reminders, and adaptive focus strategies.',
  },
]
</script>

<style>
@keyframes blob {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
</style>
