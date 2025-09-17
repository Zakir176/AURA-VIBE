<template>
  <v-app>
    <Hero id="home" />
    <Features id="features" />
    <Showcase id="how" />
    <Pricing id="pricing" />
    <Footer id="about" />
  </v-app>
</template>

<script setup>
import Hero from '@/components/Hero.vue'
import Features from '@/components/Features.vue'
import Showcase from '@/components/Showcase.vue'
import Pricing from '@/components/Pricing.vue'
import Footer from '@/components/Footer.vue'
</script>


