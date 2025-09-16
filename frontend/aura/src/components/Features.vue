<template>
  <section class="features">
    <v-container>
      <h2 class="section-title text-center mb-12">Why Choose Aura Vibe?</h2>

      <v-row>
        <v-col cols="12" md="4" class="feature-card">
          <v-icon size="48" color="primary" class="feature-icon">mdi-brain</v-icon>
          <h3>AI-Powered Mixing</h3>
          <p>Smart song transitions powered by AI — intros, outros, and vibes matched to the crowd.</p>
        </v-col>

        <v-col cols="12" md="4" class="feature-card">
          <v-icon size="48" color="primary" class="feature-icon">mdi-cellphone-music</v-icon>
          <h3>Live Requests</h3>
          <p>Guests can request songs instantly via Spotify integration.</p>
        </v-col>

        <v-col cols="12" md="4" class="feature-card">
          <v-icon size="48" color="primary" class="feature-icon">mdi-party-popper</v-icon>
          <h3>Seamless Vibes</h3>
          <p>Adaptive mood detection keeps the party flowing without awkward silences.</p>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<style scoped>
.features {
  padding: 6rem 0;
  background: #fff;
  position: relative;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, #007BFF, #6C757D);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px; /* Rounded corners for a softer look */
  background: rgba(255, 255, 255, 0.8); /* Slight glassmorphism */
  box-shadow: 0 4px 10px rgba(0, 123, 255, 0.1); /* Light shadow */
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 30px rgba(149, 120, 204, 0.5); /* Lavender shadow on hover */
}

.feature-icon {
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1); /* Icon zoom effect on hover */
}

.feature-card h3 {
  margin-top: 1rem;
  font-weight: 600;
  color: #333; /* Dark text for visibility */
}

.feature-card p {
  color: #555;
  margin-top: 0.5rem;
}
</style>
