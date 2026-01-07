<template>
  <div class="min-h-screen bg-gray-50 font-sans">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md fixed top-0 left-0 right-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <div class="flex items-center space-x-3">
            <img src="/soundwave.png" alt="AuraVibe Logo" class="w-8 h-8">
            <span class="text-2xl font-semibold text-gray-800">Aura Vibe</span>
          </div>
          <div class="flex items-center">
            <router-link
              to="/login"
              class="text-lg font-medium text-gray-600 hover:text-blue-500 transition-colors"
            >
              Login
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="pt-20">
      <div class="max-w-lg mx-auto px-4 sm:px-6 lg:px-8 text-center pt-24 pb-16">
        <h1 class="text-6xl font-extrabold text-gray-800 leading-tight">
          Let everyone
          <span class="text-blue-500">DJ.</span>
        </h1>
        <p class="mt-6 text-xl text-gray-500">
          Collaborative music sessions made simple. No cables, just vibes.
        </p>

        <div class="mt-12 flex flex-col items-center">
          <router-link
            to="/create"
            class="w-full max-w-sm bg-blue-500 text-white font-bold py-4 px-8 rounded-full text-xl flex items-center justify-center space-x-3 hover:bg-blue-600 transition-colors shadow-lg hover:shadow-xl shadow-blue-500/30"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
            <span>Create Session</span>
          </router-link>

          <div class="my-6 text-gray-400 font-medium">OR JOIN</div>

          <form @submit.prevent="joinSession" class="w-full max-w-sm">
            <div class="relative">
              <input
                type="text"
                v-model="sessionCode"
                placeholder="Enter Session Code"
                class="w-full bg-white border-2 border-gray-200 rounded-full py-4 pl-6 pr-16 text-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent transition"
              >
              <button type="submit" class="absolute inset-y-0 right-0 flex items-center justify-center w-16 h-full text-blue-500 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Features Section -->
      <section class="py-16">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 class="flex items-center text-sm font-semibold text-gray-500 tracking-widest uppercase mb-6">
            <svg class="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 14l9-5-9-5-9 5 9 5z"></path><path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0112 20.055a11.952 11.952 0 01-6.824-5.998 12.078 12.078 0 01.665-6.479L12 14z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0112 20.055a11.952 11.952 0 01-6.824-5.998 12.078 12.078 0 01.665-6.479L12 14z"></path></svg>
            The Vibe
          </h2>
          <div class="space-y-6">
            <div class="bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-shadow flex items-center space-x-6">
              <div class="flex-shrink-0 w-16 h-16 bg-blue-100 text-blue-500 rounded-xl flex items-center justify-center">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-800">Real-time Queue</h3>
                <p class="text-gray-500 mt-1">Vote on tracks instantly.</p>
              </div>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-shadow flex items-center space-x-6">
              <div class="flex-shrink-0 w-16 h-16 bg-green-100 text-green-500 rounded-xl flex items-center justify-center">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-800">No DJ Needed</h3>
                <p class="text-gray-500 mt-1">Let the room decide the flow.</p>
              </div>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-sm hover:shadow-lg transition-shadow flex items-center space-x-6">
              <div class="flex-shrink-0 w-16 h-16 bg-purple-100 text-purple-500 rounded-xl flex items-center justify-center">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 1v1m-6-1v1m-6 1v1m0-1H6m12 0h-1m-1 0h1m-1 0h1m-1 0h1M6 12v1m12-1v1m-1-1v1m-1-1v1m-1-1v1M6 18v1m12-1v1m-1-1v1m-1-1v1m-1-1v1m-1-1v1H6m0 0H5m1 0h1m12 0h1m-1 0h-1"></path></svg>
              </div>
              <div>
                <h3 class="text-xl font-bold text-gray-800">Join by QR</h3>
                <p class="text-gray-500 mt-1">Scan and join in seconds.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-lg border-t border-gray-200 z-50">
      <div class="max-w-md mx-auto">
        <div class="flex justify-around items-center h-20">
          <router-link to="/" class="text-center text-blue-500 font-bold">
            <svg class="w-8 h-8 mx-auto" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
            <span class="text-xs">Home</span>
          </router-link>
          <router-link to="/sessions" class="text-center text-gray-500 hover:text-blue-500 transition-colors">
            <svg class="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 6l12-3"></path></svg>
            <span class="text-xs">Sessions</span>
          </router-link>
          <router-link to="/profile" class="text-center text-gray-500 hover:text-blue-500 transition-colors">
            <svg class="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
            <span class="text-xs">Profile</span>
          </router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const sessionCode = ref('');
const router = useRouter();

const joinSession = () => {
  if (sessionCode.value.trim()) {
    router.push(`/session/${sessionCode.value.trim()}`);
  }
};
</script>

<style scoped>
/* Scoped styles can be added here if needed, but Tailwind is preferred */
</style>