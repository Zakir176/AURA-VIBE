<template>
  <section class="hero d-flex align-center">
    <v-container>
      <v-row align="center">
        <!-- Left side: Text -->
        <v-col cols="12" md="6" class="text-left">
          <transition name="fade-up" appear>
            <h1 class="display-2 font-weight-bold mb-6">
              Experience the Future of <span class="gradient-text">Creativity</span>
            </h1>
          </transition>

          <transition name="fade-up" appear>
            <p class="subtitle-1 mb-8 text-grey-darken-1">
              Aura Vibe helps you craft powerful, AI-driven experiences with simplicity, elegance, and speed.
            </p>
          </transition>

          <transition name="fade-up" appear>
            <v-btn size="x-large" class="cta-btn">
              Get Started →
            </v-btn>
          </transition>
        </v-col>

        <!-- Right side: Image -->
        <v-col cols="12" md="6" class="text-center">
          <transition name="fade-up" appear>
            <img src="\assets/logo.png" alt="Aura Mockup" class="hero-image" />
          </transition>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<style scoped>
.hero {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 40%, #ffe5e5 100%);
}

/* .gradient-text {
  background: linear-gradient(90deg, #D63384, #FF6B6B, #FFB84D);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; 
}
*/
.cta-btn {
  background: linear-gradient(90deg, #D63384, #FF6B6B, #FFB84D);
  color: white;
  font-weight: bold;
  border-radius: 12px;
  transition: all 0.3s ease-in-out;
}
.cta-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(214, 51, 132, 0.4);
}

.hero-image {
  max-width: 450px;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}
.fade-up-enter-active {
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(40px);
}
</style>
