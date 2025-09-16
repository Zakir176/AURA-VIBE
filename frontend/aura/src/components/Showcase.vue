<!-- src/components/Showcase.vue -->
<template>
  <section class="how-it-works">
    <v-container>
      <h2 class="section-title text-center mb-12">How It Works</h2>

      <v-row class="step-row" align="center" justify="center">
        <v-col cols="12" md="4" class="step-card">
          <div class="step-icon">1</div>
          <h3>Create Your Aura</h3>
          <p>Upload your playlist or start from scratch — Aura Vibe tailors the mood to your energy.</p>
        </v-col>

        <v-col cols="12" md="4" class="step-card">
          <div class="step-icon">2</div>
          <h3>Set the Vibe</h3>
          <p>Choose your vibe — chill, hype, or custom — and let AI mix transitions and moments.</p>
        </v-col>

        <v-col cols="12" md="4" class="step-card">
          <div class="step-icon">3</div>
          <h3>Play It Live</h3>
          <p>Sync across devices, accept requests in real-time, and keep the flow seamless.</p>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<style scoped>
.how-it-works {
  padding: 6rem 0;
  background-color: #fff;
  position: relative;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, #87CEEB, #E6E6FA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.step-row {
  gap: 2rem;
}

.step-card {
  text-align: center;
  padding: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.step-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(149, 120, 204, 0.5);
}
.step-icon {
  font-size: 2rem;
  font-weight: bold;
  width: 60px;
  height: 60px;
  line-height: 60px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #87CEEB, #E6E6FA);
  color: white;
  box-shadow: 0 4px 12px rgba(135, 206, 235, 0.4);
}
.step-card h3 {
  margin-top: 1rem;
  font-weight: 600;
}
.step-card p {
  color: #666;
  margin-top: 0.5rem;
}
</style>
