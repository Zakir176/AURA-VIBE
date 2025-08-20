<template>
  <main class="bg-gray-900 text-white font-sans overflow-x-hidden">
    <!-- Background blobs -->
    <div class="absolute top-0 left-0 w-72 h-72 bg-purple-600 rounded-full mix-blend-multiply blur-3xl opacity-30 animate-blob"></div>
    <div class="absolute bottom-0 right-0 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply blur-3xl opacity-20 animate-blob animation-delay-4000"></div>

    <!-- Hero Section -->
    <section class="min-h-screen flex flex-col items-center justify-center text-center px-6 md:px-20 relative z-10">
      <img src="@/assets/logo.png" alt="AURA VIBE Logo" class="w-28 md:w-36 mb-6 animate-pulse" />
      <h1 class="text-5xl md:text-7xl font-extrabold bg-gradient-to-r from-purple-400 to-pink-500 text-transparent bg-clip-text mb-4">
        AURA VIBE
      </h1>
      <p class="text-pink-200 text-xl max-w-xl mb-8">
        Your intelligent AI-powered assistant to supercharge productivity and focus.
      </p>
      <button
        class="bg-gradient-to-r from-purple-500 to-pink-500 text-gray-900 font-semibold px-8 py-3 rounded-full shadow-lg hover:scale-105 transform transition"
      >
        Get Started
      </button>
    </section>

    <!-- Features -->
    <section class="py-24 px-6 md:px-20 bg-gray-950 relative z-10">
      <h2 class="text-3xl md:text-5xl font-bold text-center mb-16">🚀 Core Features</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-12 max-w-6xl mx-auto">
        <FeatureCard
          title="Smart Assistance"
          icon="💡"
          description="Conversational AI to answer questions, explain concepts, and assist with research."
        />
        <FeatureCard
          title="Study Mode"
          icon="📚"
          description="Organize tasks, generate notes, create summaries, and break down tough topics."
        />
        <FeatureCard
          title="Productivity Tools"
          icon="⏰"
          description="Integrated timer, reminders, and adaptive focus strategies to keep you on track."
        />
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-24 px-6 md:px-20 bg-gray-900 relative z-10 text-center">
      <h2 class="text-3xl md:text-5xl font-bold mb-12">🛠️ How It Works</h2>
      <div class="max-w-4xl mx-auto space-y-10 text-pink-200 text-lg leading-relaxed">
        <div>
          <h3 class="text-2xl font-semibold text-white mb-2">1. Ask Anything</h3>
          <p>Use natural language to ask questions, explore ideas, or request help — no syntax needed.</p>
        </div>
        <div>
          <h3 class="text-2xl font-semibold text-white mb-2">2. Get Smart Output</h3>
          <p>AURA VIBE generates summaries, lists, concepts, and study plans instantly.</p>
        </div>
        <div>
          <h3 class="text-2xl font-semibold text-white mb-2">3. Stay Productive</h3>
          <p>Use built-in tools like timers and reminders to keep your flow focused and distraction-free.</p>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="py-24 px-6 md:px-20 bg-gray-950 relative z-10">
      <h2 class="text-3xl md:text-5xl font-bold text-center mb-16">💬 What Users Say</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-6xl mx-auto text-gray-200">
        <div class="bg-gray-800 p-6 rounded-xl shadow-md">
          <p>"AURA VIBE completely changed the way I study. The AI breaks things down so simply."</p>
          <span class="block mt-4 text-pink-300 font-semibold">— Aliyah, Medical Student</span>
        </div>
        <div class="bg-gray-800 p-6 rounded-xl shadow-md">
          <p>"It’s like having a personal assistant for my work sessions. The timer + reminders are perfect."</p>
          <span class="block mt-4 text-purple-300 font-semibold">— Rafiq, UX Designer</span>
        </div>
      </div>
    </section>

    <!-- Final Call To Action -->
    <section class="py-24 text-center bg-gray-900 relative z-10">
      <h2 class="text-4xl font-bold mb-6">Ready to transform how you work?</h2>
      <p class="text-lg text-pink-200 mb-8">Join thousands using AURA VIBE for smarter productivity.</p>
      <button class="bg-gradient-to-r from-purple-500 to-pink-500 text-gray-900 font-semibold px-10 py-4 rounded-full shadow-xl hover:scale-105 transform transition">
        Try It Free
      </button>
    </section>

    <!-- Footer -->
    <footer class="py-10 px-6 bg-gray-950 text-center text-gray-500 text-sm">
      <p>© 2025 AURA VIBE. Built with ❤️ by the E.C.H.O. team.</p>
      <p>
        <a href="https://github.com/Zakir176/AURA-VIBE" target="_blank" class="underline text-pink-400">GitHub Repo</a>
      </p>
    </footer>
  </main>
</template>

<script setup>
import FeatureCard from '@/components/FeatureCard.vue'
</script>

<style>
@keyframes blob {
  0%, 100% {
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
