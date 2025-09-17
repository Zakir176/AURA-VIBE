<template>
  <section class="hero d-flex align-center">
    <v-container>
      <v-row align="center" no-gutters>
        <!-- Left side: Text -->
        <v-col cols="12" md="6" class="text-left">
          <h1 class="text-h2 font-weight-bold mb-4 hero-heading">
            Experience the Future of <span class="gradient-text">Creativity</span>
          </h1>

          <p class="text-subtitle-1 mb-8 hero-subtitle">
            Aura Vibe blends intelligence with design — simple, elegant, fast.
          </p>

          <v-btn size="x-large" class="cta-btn" :to="{ name: 'Login', query: { redirect: '/get-started' } }">
            Get Started →
          </v-btn>
        </v-col>

        <!-- Right side: Image -->
        <v-col cols="12" md="6" class="text-center">
          <transition name="fade-up" appear>
            <img ref="imageRef" src="/assets/soundwave.png" alt="Aura Mockup" class="hero-image" />
          </transition>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const imageRef = ref(null)

onMounted(() => {
  if (imageRef.value) {
    gsap.from(imageRef.value, {
      opacity: 0,
      y: 40,
      scale: 0.98,
      duration: 1,
      ease: 'power3.out'
    })

    gsap.to(imageRef.value, {
      yPercent: 6,
      ease: 'none',
      scrollTrigger: {
        trigger: imageRef.value,
        start: 'top bottom',
        end: 'bottom top',
        scrub: true
      }
    })
  }
})
</script>

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
  background: radial-gradient(circle, #4393b3, #8c8ce0);
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
  background: linear-gradient(90deg, #4393b3, #8c8ce0);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.cta-btn {
  background: linear-gradient(90deg, #4393b3, #8c8ce0);
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

.hero-heading {
  position: relative;
  z-index: 1;
  color: #0d1b2a; /* dark text for visibility */
}

.hero-subtitle {
  position: relative;
  z-index: 1;
  color: #5c6b7a; /* subtle secondary */
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
