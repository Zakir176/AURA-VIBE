<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 font-sans overflow-hidden relative">
    
    <!-- Background Elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div class="absolute -top-24 -left-24 w-96 h-96 bg-blue-400/20 rounded-full blur-3xl mix-blend-multiply animate-blob"></div>
        <div class="absolute top-0 -right-4 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl mix-blend-multiply animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-96 h-96 bg-pink-400/20 rounded-full blur-3xl mix-blend-multiply animate-blob animation-delay-4000"></div>
    </div>

    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 transition-all duration-300" :class="{ 'bg-white/70 backdrop-blur-lg shadow-sm': isScrolled, 'bg-transparent': !isScrolled }">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-20">
          <div class="flex items-center space-x-3 group cursor-pointer">
            <div class="relative">
                <div class="absolute inset-0 bg-blue-500 blur opacity-20 group-hover:opacity-40 transition-opacity duration-300 rounded-full"></div>
                <img src="/soundwave.png" alt="AuraVibe Logo" class="w-8 h-8 relative z-10 transform group-hover:scale-110 transition-transform duration-300">
            </div>
            <span class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-800 to-gray-600">Aura Vibe</span>
          </div>
          <div class="flex items-center">
            <router-link
              to="/login"
              class="px-6 py-2 rounded-full text-sm font-semibold text-gray-600 hover:text-white hover:bg-gray-900 transition-all duration-300"
            >
              Login
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10 pt-20">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center pt-20 pb-16">
        
        <!-- Hero Section -->
        <div class="space-y-8 animate-fade-in-up">
            <h1 class="text-6xl md:text-8xl font-black text-gray-900 leading-tight tracking-tight">
            Let everyone
            <span class="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 animate-gradient-x">
                DJ.
            </span>
            </h1>
            <p class="mt-6 text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto font-light leading-relaxed">
            Collaborative music sessions made simple.<br class="hidden md:block" /> No cables, just vibes.
            </p>
        </div>

        <!-- Action Section -->
        <div class="mt-16 flex flex-col items-center space-y-8 animate-fade-in-up animation-delay-300">
          <router-link
            to="/create"
            class="group relative inline-flex items-center justify-center px-8 py-4 text-lg font-bold text-white transition-all duration-200 bg-gray-900 font-pj rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900 hover:bg-gray-800 hover:shadow-2xl hover:-translate-y-1"
          >
            <div class="absolute -inset-3 transition-all duration-1000 opacity-30 group-hover:opacity-100 group-hover:duration-200 blur-lg filter bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 rounded-full"></div>
            <span class="relative flex items-center space-x-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                <span>Create Session</span>
            </span>
          </router-link>

          <div class="flex items-center w-full max-w-xs space-x-4">
              <div class="h-px bg-gray-300 flex-1"></div>
              <span class="text-gray-400 font-medium text-sm tracking-widest uppercase">or join</span>
              <div class="h-px bg-gray-300 flex-1"></div>
          </div>

          <form @submit.prevent="joinSession" class="w-full max-w-md relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 rounded-full blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
            <div class="relative flex items-center bg-white rounded-full shadow-sm">
                <input
                    type="text"
                    v-model="sessionCode"
                    placeholder="Enter Session Code"
                    class="w-full bg-transparent border-0 rounded-full py-4 pl-8 pr-16 text-lg text-gray-800 placeholder-gray-400 focus:ring-0 focus:outline-none"
                >
                <button 
                    type="submit" 
                    class="absolute right-2 p-2 bg-gray-100 rounded-full text-gray-500 hover:text-blue-600 hover:bg-blue-50 transition-all duration-200"
                    :disabled="!sessionCode.trim()"
                >
                    <svg class="w-6 h-6 transform rotate-0 group-hover:rotate-0 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Features Section -->
      <section class="py-20 relative">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div class="group bg-white/60 backdrop-blur-xl p-8 rounded-3xl shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20">
              <div class="w-14 h-14 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">Real-time Queue</h3>
              <p class="text-gray-500 leading-relaxed">Vote on tracks instantly. See what's playing next and influence the vibe of the room.</p>
            </div>

            <!-- Feature 2 -->
            <div class="group bg-white/60 backdrop-blur-xl p-8 rounded-3xl shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20">
              <div class="w-14 h-14 bg-green-100 text-green-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">No DJ Needed</h3>
              <p class="text-gray-500 leading-relaxed">Let the room decide the flow. Democracy on the dance floor has never looked this good.</p>
            </div>

            <!-- Feature 3 -->
            <div class="group bg-white/60 backdrop-blur-xl p-8 rounded-3xl shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border border-white/20">
              <div class="w-14 h-14 bg-purple-100 text-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 1v1m-6-1v1m-6 1v1m0-1H6m12 0h-1m-1 0h1m-1 0h1m-1 0h1M6 12v1m12-1v1m-1-1v1m-1-1v1m-1-1v1M6 18v1m12-1v1m-1-1v1m-1-1v1m-1-1v1m-1-1v1H6m0 0H5m1 0h1m12 0h1m-1 0h-1"></path></svg>
              </div>
              <h3 class="text-xl font-bold text-gray-900 mb-3">Join by QR</h3>
              <p class="text-gray-500 leading-relaxed">Scan and join in seconds. No app download required. Just point, shoot, and vote.</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-xl border-t border-gray-200/50 z-50 pb-safe">
      <div class="max-w-md mx-auto">
        <div class="flex justify-around items-center h-20">
          <router-link to="/" class="flex flex-col items-center text-gray-900 font-medium" aria-label="Home">
            <div class="p-1.5 rounded-xl bg-gray-100">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
            </div>
          </router-link>
          <router-link to="/sessions" class="flex flex-col items-center text-gray-400 hover:text-gray-900 transition-colors" aria-label="Sessions">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 6l12-3"></path></svg>
          </router-link>
          <router-link to="/profile" class="flex flex-col items-center text-gray-400 hover:text-gray-900 transition-colors" aria-label="Profile">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
          </router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const sessionCode = ref('');
const router = useRouter();
const isScrolled = ref(false);

const joinSession = () => {
  if (sessionCode.value.trim()) {
    router.push(`/session/${sessionCode.value.trim()}`);
  }
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
.animation-delay-300 {
    animation-delay: 300ms;
}

@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

@keyframes fade-in-up {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-up {
    animation: fade-in-up 0.8s ease-out forwards;
}

@keyframes gradient-x {
    0%, 100% {
        background-size: 200% 200%;
        background-position: left center;
    }
    50% {
        background-size: 200% 200%;
        background-position: right center;
    }
}

.animate-gradient-x {
    animation: gradient-x 3s ease infinite;
}

/* Safe area padding for mobile bottom nav */
.pb-safe {
    padding-bottom: env(safe-area-inset-bottom);
}
</style>
