<template >
  <v-container  fluid class="pricing-section d-flex align-center justify-center">
    <div class="glass-card" >
      <h2 class="title">Our Pricing</h2>
      <p class="subtitle">Choose a plan that fits your needs</p>

      <v-row class="mt-6" justify="center" align="stretch">
        <v-col cols="12" sm="4" v-for="(plan, index) in plans" :key="index">
          <v-card class="pricing-card" elevation="0" data-pricing-card>
            <v-card-title class="text-h6">{{ plan.name }}</v-card-title>
            <v-card-subtitle class="price">{{ plan.price }}</v-card-subtitle>
            <v-card-text class="features">
              <ul>
                <li v-for="(feature, i) in plan.features" :key="i">{{ feature }}</li>
              </ul>
            </v-card-text>
            <v-card-actions>
              <v-btn color="primary" block>Choose Plan</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const plans = [
  {
    name: "Basic",
    price: "$19/mo",
    features: ["1 user", "5 projects", "Basic support"],
  },
  {
    name: "Pro",
    price: "$49/mo",
    features: ["5 users", "50 projects", "Priority support"],
  },
  {
    name: "Enterprise",
    price: "$99/mo",
    features: ["Unlimited users", "Unlimited projects", "24/7 support"],
  },
];

onMounted(() => {
  const cards = document.querySelectorAll('[data-pricing-card]')
  gsap.from(cards, {
    opacity: 0,
    y: 24,
    duration: 0.6,
    ease: 'power2.out',
    stagger: 0.12,
    scrollTrigger: {
      trigger: cards[0] || '.pricing-section',
      start: 'top 85%'
    }
  })
})
</script>

<style scoped>
/* Background section */
.pricing-section {
  min-height: 100vh;
  background: url('https://www.transparenttextures.com/patterns/cubes.png'),
    linear-gradient(135deg, #e3f2fd, #ffffff);
  background-size: cover;
  padding: 2rem;
}

/* Glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 3rem;
  max-width: 1100px;
  width: 100%;
  color: #000;
}

/* Headings */
.title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #000;
}
.subtitle {
  text-align: center;
  font-size: 1.25rem;
  color: #6c757d; /* secondary */
}

/* Cards */
.pricing-card {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 12px;
  transition: transform 0.3s ease;
  padding: 1.5rem;
  text-align: center;
  backdrop-filter: blur(10px);
}

.pricing-card:hover {
  transform: translateY(-5px);
}

.price {
  font-size: 1.75rem;
  font-weight: bold;
  color: #007bff; /* primary */
  margin-bottom: 1rem;
}

.features {
  font-size: 0.95rem;
  color: #333;
}

.features ul {
  list-style: none;
  padding: 0;
  margin: 0 0 1rem;
}

.features li {
  margin-bottom: 0.5rem;
}
</style>
