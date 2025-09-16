<template>
  <section class="hero d-flex align-center">
    <v-container>
      <v-row align="center" no-gutters>
        <!-- Left side: Text -->
        <v-col cols="12" md="6" class="text-left">
          <transition name="fade-up" appear>
            <h1 class="display-2 font-weight-bold mb-6 hero-heading">
              Experience the Future of <span class="gradient-text">Creativity</span>
            </h1>
          </transition>

          <transition name="fade-up" appear>
            <p class="subtitle-1 mb-8 text-grey-darken-1 hero-subtitle">
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
            <img src="/assets/soundwave.png" alt="Aura Mockup" class="hero-image" />
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
  padding-top: 20px; /* Space for small screens */
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
  max-width: 100%;
  max-height: 400px;
  object-fit: cover;
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

/* Responsive Adjustments */
@media (max-width: 960px) {
  .hero {
    padding-top: 80px; /* Add space for the fixed navbar on smaller screens */
  }

  .hero-heading {
    font-size: 2.5rem; /* Smaller font for mobile */
  }

  .hero-subtitle {
    font-size: 1rem; /* Smaller font for subtitle */
  }

  .cta-btn {
    font-size: 1.1rem;
    padding: 12px 20px;
  }

  .hero-image {
    max-height: 250px;
  }
}

@media (max-width: 600px) {
  .hero-heading {
    font-size: 2rem; /* Even smaller font for mobile devices */
  }

  .hero-subtitle {
    font-size: 0.9rem;
  }

  .cta-btn {
    font-size: 1rem;
    padding: 10px 18px;
  }

  .hero-image {
    max-height: 200px;
  }
}
</style>
