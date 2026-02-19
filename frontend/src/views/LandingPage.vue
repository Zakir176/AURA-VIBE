<template>
  <div class="min-h-screen bg-vibe-black font-sans overflow-hidden relative selection:bg-vibe-indigo/30 selection:text-white">
    
    <!-- Background Elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div class="absolute -top-24 -left-24 w-[500px] h-[500px] bg-vibe-blue/20 rounded-full blur-[120px] animate-blob"></div>
        <div class="absolute top-1/4 -right-24 w-[400px] h-[400px] bg-vibe-purple/20 rounded-full blur-[100px] animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-24 left-1/4 w-[600px] h-[600px] bg-vibe-pink/10 rounded-full blur-[150px] animate-blob animation-delay-4000"></div>
    </div>

    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 transition-all duration-500" :class="{ 'glass-blur border-b border-white/5 py-4': isScrolled, 'bg-transparent py-6': !isScrolled }">
      <div class="max-w-7xl mx-auto px-6 lg:px-8">
        <div class="flex justify-between items-center">
          <div class="flex items-center space-x-3 group cursor-pointer">
            <div class="relative">
                <div class="absolute inset-0 bg-vibe-indigo blur-xl opacity-0 group-hover:opacity-60 transition-opacity duration-500 rounded-full"></div>
                <div class="w-10 h-10 bg-gradient-to-tr from-vibe-indigo to-vibe-purple rounded-xl flex items-center justify-center relative z-10 transform group-hover:scale-110 transition-transform duration-500 shadow-lg">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"></path></svg>
                </div>
            </div>
            <span class="text-2xl font-black tracking-tighter text-white">AURA VIBE</span>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/login"
              class="px-5 py-2 rounded-full text-sm font-bold text-gray-400 hover:text-white transition-all duration-300"
            >
              Login
            </router-link>
            <router-link
              to="/create"
              class="px-5 py-2 rounded-full text-sm font-bold bg-white text-vibe-black hover:bg-vibe-indigo hover:text-white transition-all duration-500 shadow-xl"
            >
              Get Started
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10">
      <div class="max-w-6xl mx-auto px-6 lg:px-8 text-center pt-32 md:pt-48 pb-24">
        
        <!-- Hero Section -->
        <div class="space-y-10 animate-fade-in-up">
            <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-vibe-indigo/10 border border-vibe-indigo/20 text-vibe-indigo text-xs font-bold uppercase tracking-widest mb-4">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-vibe-indigo opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-vibe-indigo"></span>
                </span>
                <span>Now in Beta</span>
            </div>
            <h1 class="text-7xl md:text-9xl font-black text-white leading-[0.9] tracking-tighter">
                LET THE ROOM <br/>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-vibe-blue via-vibe-purple to-vibe-pink animate-gradient-x py-2 inline-block">
                    DJ.
                </span>
            </h1>
            <p class="mt-8 text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto font-medium leading-relaxed">
                Connect your crowd. Share the queue. <br class="hidden md:block" /> Collaborative music for people who care about the vibe.
            </p>
        </div>

        <!-- Action Section -->
        <div class="mt-20 flex flex-col items-center space-y-10 animate-fade-in-up animation-delay-300">
          <router-link
            to="/create"
            class="group relative inline-flex items-center justify-center px-10 py-5 text-xl font-black text-white transition-all duration-500 bg-vibe-indigo rounded-2xl overflow-hidden shadow-[0_0_40px_-10px_rgba(79,70,229,0.5)] hover:shadow-vibe-indigo/40 hover:-translate-y-1"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-vibe-blue to-vibe-purple opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <span class="relative flex items-center space-x-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4"></path></svg>
                <span>CREATE SESSION</span>
            </span>
          </router-link>

          <div class="flex items-center w-full max-w-sm space-x-6">
              <div class="h-px bg-white/10 flex-1"></div>
              <span class="text-gray-500 font-black text-xs tracking-[0.3em] uppercase">OR JOIN</span>
              <div class="h-px bg-white/10 flex-1"></div>
          </div>

          <form @submit.prevent="joinSession" class="w-full max-w-md relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-vibe-blue/20 to-vibe-pink/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition duration-700"></div>
            <div class="relative flex items-center bg-white/5 border border-white/10 rounded-2xl focus-within:border-vibe-indigo/50 transition-all duration-300 group">
                <input
                    type="text"
                    v-model="sessionCode"
                    placeholder="ENTER SESSION CODE"
                    class="w-full bg-transparent border-0 rounded-2xl py-5 pl-8 pr-16 text-lg font-bold text-white placeholder-gray-600 focus:ring-0 focus:outline-none uppercase tracking-widest"
                >
                <button 
                    type="submit" 
                    class="absolute right-3 p-3 bg-white/10 rounded-xl text-white hover:bg-white hover:text-vibe-black transition-all duration-300 disabled:opacity-20 disabled:cursor-not-allowed"
                    :disabled="!sessionCode.trim()"
                >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Features Section -->
      <section class="py-24 relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div class="group glass-card p-10 rounded-[2.5rem] transition-all duration-500 hover:-translate-y-3">
              <div class="w-16 h-16 bg-vibe-blue/10 text-vibe-blue rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 group-hover:bg-vibe-blue group-hover:text-white transition-all duration-500 shadow-lg">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
              </div>
              <h3 class="text-2xl font-black text-white mb-4 tracking-tight uppercase">Real-time Queue</h3>
              <p class="text-gray-400 leading-relaxed font-medium">Vote on tracks instantly. See what's playing next and influence the vibe of the room in real-time.</p>
            </div>

            <!-- Feature 2 -->
            <div class="group glass-card p-10 rounded-[2.5rem] transition-all duration-500 hover:-translate-y-3">
              <div class="w-16 h-16 bg-vibe-purple/10 text-vibe-purple rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 group-hover:bg-vibe-purple group-hover:text-white transition-all duration-500 shadow-lg">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              </div>
              <h3 class="text-2xl font-black text-white mb-4 tracking-tight uppercase">No DJ Needed</h3>
              <p class="text-gray-400 leading-relaxed font-medium">Let the room decide. Democracy on the dance floor has never looked or sounded this good.</p>
            </div>

            <!-- Feature 3 -->
            <div class="group glass-card p-10 rounded-[2.5rem] transition-all duration-500 hover:-translate-y-3">
              <div class="w-16 h-16 bg-vibe-pink/10 text-vibe-pink rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 group-hover:bg-vibe-pink group-hover:text-white transition-all duration-500 shadow-lg">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 1v1m-6-1v1m-6 1v1m0-1H6m12 0h-1m-1 0h1m-1 0h1m-1 0h1M6 12v1m12-1v1m-1-1v1m-1-1v1m-1-1v1M6 18v1m12-1v1m-1-1v1m-1-1v1m-1-1v1m-1-1v1H6m0 0H5m1 0h1m12 0h1m-1 0h-1"></path></svg>
              </div>
              <h3 class="text-2xl font-black text-white mb-4 tracking-tight uppercase">Join by QR</h3>
              <p class="text-gray-400 leading-relaxed font-medium">Scan and join in seconds. No app download required. Just point, shoot, and start voting.</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="md:hidden fixed bottom-6 left-6 right-6 z-50 animate-fade-in-up">
      <div class="max-w-md mx-auto glass-card rounded-[2rem] px-8 py-4 shadow-[0_20px_50px_rgba(0,0,0,0.5)] border-white/5">
        <div class="flex justify-around items-center">
          <router-link to="/" class="p-3 text-vibe-indigo transition-all transform hover:scale-110" aria-label="Home">
            <svg class="w-7 h-7" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>
          </router-link>
          <router-link to="/sessions" class="p-3 text-gray-500 hover:text-white transition-all transform hover:scale-110" aria-label="Sessions">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 6l12-3"></path></svg>
          </router-link>
          <router-link to="/profile" class="p-3 text-gray-500 hover:text-white transition-all transform hover:scale-110" aria-label="Profile">
            <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
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
