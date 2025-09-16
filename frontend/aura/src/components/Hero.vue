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
  position: relative;
  overflow: hidden;
  background: #ffffff;
}

/* Blurred gradient overlay */
.hero::before {
  content: "";
  position: absolute;
  top: -200px;
  left: -200px;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(135, 206, 235, 0.6), rgba(230, 230, 250, 0.3));
  filter: blur(120px);
  z-index: 0;
}

.hero::after {
  content: "";
  position: absolute;
  bottom: -150px;
  right: -150px;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(214, 51, 132, 0.2), rgba(255, 107, 107, 0.15));
  filter: blur(100px);
  z-index: 0;
}

.gradient-text {
  background: linear-gradient(90deg, #87CEEB, #E6E6FA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.cta-btn {
  background: linear-gradient(90deg, #87CEEB, #E6E6FA);
  color: white;
  font-weight: bold;
  border-radius: 12px;
  transition: all 0.3s ease-in-out;
  z-index: 1;
}
.cta-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(135, 206, 235, 0.4);
}

.hero-image {
  max-width: 450px;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

/* Animations */
.fade-up-enter-active {
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.fade-up-enter-from {
  opacity: 0;
  transform: translateY(40px);
}
</style>
