<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
    <!-- Navigation -->
    <nav class="relative z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <span class="text-white font-bold text-lg">🎵</span>
            </div>
            <span class="text-2xl font-bold text-white">AuraVibe</span>
          </div>
          <div class="hidden md:flex items-center space-x-8">
            <a href="#features" class="text-gray-300 hover:text-white transition-colors duration-200">Features</a>
            <a href="#how-it-works" class="text-gray-300 hover:text-white transition-colors duration-200">How it Works</a>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <!-- Animated background elements -->
      <div class="absolute inset-0">
        <div class="absolute -top-40 -right-32 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div class="absolute -bottom-40 -left-32 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div class="absolute top-40 left-1/2 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
        <!-- Main heading -->
        <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
          <span class="block">Share the</span>
          <span class="block bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            Vibe
          </span>
        </h1>
        
        <p class="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-12 leading-relaxed">
          Create collaborative music sessions. Queue up your favorite tracks, share with friends, and vibe together in real-time.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
          <router-link 
            to="/create" 
            class="group relative bg-gradient-to-r from-blue-500 to-purple-600 text-white text-lg font-semibold py-4 px-8 rounded-2xl transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/25"
          >
            <span class="relative z-10 flex items-center space-x-2">
              <span>🎤 Create Session</span>
              <span class="group-hover:translate-x-1 transition-transform">→</span>
            </span>
          </router-link>
          
          <router-link 
            to="/join" 
            class="group border-2 border-gray-600 text-gray-300 text-lg font-semibold py-4 px-8 rounded-2xl transition-all duration-300 hover:border-white hover:text-white hover:scale-105"
          >
            <span class="flex items-center space-x-2">
              <span>🎧 Join Session</span>
            </span>
          </router-link>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-2xl mx-auto">
          <div class="text-center">
            <div class="text-3xl font-bold text-white mb-2">∞</div>
            <div class="text-gray-400">Sessions</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-white mb-2">⚡</div>
            <div class="text-gray-400">Real-time</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-white mb-2">🎵</div>
            <div class="text-gray-400">Songs Queued</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-white/5 backdrop-blur-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">Why AuraVibe?</h2>
          <p class="text-xl text-gray-300 max-w-2xl mx-auto">Everything you need for the perfect collaborative music experience</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="group p-8 bg-white/5 rounded-3xl border border-white/10 hover:border-purple-500/50 transition-all duration-300 hover:scale-105">
            <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl text-white">⚡</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Real-time Sync</h3>
            <p class="text-gray-300 leading-relaxed">Watch the queue update instantly across all devices. No more refreshing!</p>
          </div>

          <div class="group p-8 bg-white/5 rounded-3xl border border-white/10 hover:border-blue-500/50 transition-all duration-300 hover:scale-105">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl text-white">📱</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Easy Sharing</h3>
            <p class="text-gray-300 leading-relaxed">QR codes and simple session codes make joining effortless for everyone.</p>
          </div>

          <div class="group p-8 bg-white/5 rounded-3xl border border-white/10 hover:border-pink-500/50 transition-all duration-300 hover:scale-105">
            <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl text-white">👥</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Collaborative</h3>
            <p class="text-gray-300 leading-relaxed">Everyone contributes to the playlist. Build the perfect vibe together.</p>
          </div>

          <div class="group p-8 bg-white/5 rounded-3xl border border-white/10 hover:border-yellow-500/50 transition-all duration-300 hover:scale-105">
            <div class="w-16 h-16 bg-gradient-to-r from-yellow-500 to-orange-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl text-white">🎨</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Beautiful UI</h3>
            <p class="text-gray-300 leading-relaxed">Clean, modern interface that works perfectly on all your devices.</p>
          </div>

          <div class="group p-8 bg-white/5 rounded-3xl border border-white/10 hover:border-green-500/50 transition-all duration-300 hover:scale-105">
            <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-teal-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl text-white">🚀</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Lightning Fast</h3>
            <p class="text-gray-300 leading-relaxed">Built with modern tech for instant loading and smooth interactions.</p>
          </div>

          <div class="group p-8 bg-white/5 rounded-3xl border border-white/10 hover:border-red-500/50 transition-all duration-300 hover:scale-105">
            <div class="w-16 h-16 bg-gradient-to-r from-red-500 to-pink-600 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-2xl text-white">🎯</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">No Setup</h3>
            <p class="text-gray-300 leading-relaxed">Start sharing music immediately. No accounts, no downloads, no hassle.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">How It Works</h2>
          <p class="text-xl text-gray-300 max-w-2xl mx-auto">Get started in just three simple steps</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          <!-- Connecting line -->
          <div class="hidden md:block absolute top-20 left-1/3 right-1/3 h-1 bg-gradient-to-r from-blue-500 to-purple-600 transform -translate-y-1/2"></div>
          
          <div class="relative text-center group">
            <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 z-10 relative">
              <span class="text-2xl text-white">1</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Create Session</h3>
            <p class="text-gray-300">Click "Create Session" to start a new music room. Get your unique session code and QR code.</p>
          </div>

          <div class="relative text-center group">
            <div class="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 z-10 relative">
              <span class="text-2xl text-white">2</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Share & Join</h3>
            <p class="text-gray-300">Share the QR code or session code with friends. They can join instantly from any device.</p>
          </div>

          <div class="relative text-center group">
            <div class="w-20 h-20 bg-gradient-to-r from-pink-500 to-red-600 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 z-10 relative">
              <span class="text-2xl text-white">3</span>
            </div>
            <h3 class="text-2xl font-bold text-white mb-4">Queue & Enjoy</h3>
            <p class="text-gray-300">Add YouTube links to the queue. Watch it update in real-time and enjoy the music together!</p>
          </div>
        </div>

        <!-- Bottom CTA -->
        <div class="text-center mt-16">
          <router-link 
            to="/create" 
            class="inline-flex items-center space-x-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-xl font-semibold py-4 px-12 rounded-2xl transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/25"
          >
            <span>Start Your Session Now</span>
            <span class="text-2xl">🎶</span>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-white/10 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="flex items-center space-x-3 mb-4 md:mb-0">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">🎵</span>
            </div>
            <span class="text-xl font-bold text-white">AuraVibe</span>
          </div>
          <div class="text-gray-400">
            Made with ❤️ for music lovers everywhere
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// No script needed for this landing page, but you could add animations if desired
</script>

<style scoped>
/* Custom animations */
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

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}
</style>