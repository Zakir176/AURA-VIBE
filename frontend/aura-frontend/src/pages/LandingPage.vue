<template>
  <main class="min-h-screen bg-bg-dark text-text flex flex-col items-center justify-center px-6 md:px-20">
    <!-- Hero Section -->
    <section class="flex flex-col items-center text-center max-w-3xl">
      <img src="@/assets/logo.png" alt="AURA VIBE Logo" class="w-36 mb-6" />
      <h1
        class="text-5xl font-extrabold mb-4 bg-gradient-to-r from-primary-start to-primary-end text-transparent bg-clip-text"
      >
        AURA VIBE
      </h1>
      <p class="text-accent mb-8 text-lg md:text-xl">
        Intelligent AI-powered study and productivity assistant designed to amplify focus, streamline workflow, and empower your learning.
      </p>
      <button
        class="bg-gradient-to-r from-primary-start to-primary-end text-bg-dark font-semibold px-8 py-3 rounded-full shadow-lg hover:brightness-110 transition"
      >
        Get Started
      </button>
    </section>

    <!-- Features Section -->
    <section
      class="mt-20 grid grid-cols-1 md:grid-cols-3 gap-10 max-w-5xl w-full"
    >
      <FeatureCard
        title="Smart Assistance"
        icon="💡"
        description="Conversational AI to answer questions and explain concepts."
      />
      <FeatureCard
        title="Study Mode"
        icon="📚"
        description="Organize tasks, generate summaries, and break down complex topics."
      />
      <FeatureCard
        title="Productivity Tools"
        icon="⏰"
        description="Timer, reminders, and adaptive focus strategies."
      />
    </section>
  </main>
</template>

<script setup>
import FeatureCard from '@/components/FeatureCard.vue'
</script>

<style scoped>
/* Optional: smooth scroll, or any extra styling */
</style>
