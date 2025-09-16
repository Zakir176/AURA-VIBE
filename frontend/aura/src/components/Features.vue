<template>
  <section class="features">
    <v-container>
      <h2 class="section-title text-center mb-12">Why Choose Aura Vibe?</h2>

      <v-row>
        <v-col cols="12" md="4" class="feature-card">
          <v-icon size="48" color="primary">mdi-brain</v-icon>
          <h3>AI-Powered Mixing</h3>
          <p>Smart song transitions powered by AI — intros, outros, and vibes matched to the crowd.</p>
        </v-col>

        <v-col cols="12" md="4" class="feature-card">
          <v-icon size="48" color="primary">mdi-cellphone-music</v-icon>
          <h3>Live Requests</h3>
          <p>Guests can request songs instantly via Spotify integration.</p>
        </v-col>

        <v-col cols="12" md="4" class="feature-card">
          <v-icon size="48" color="primary">mdi-party-popper</v-icon>
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
  background: linear-gradient(90deg, #87CEEB, #E6E6FA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 30px rgba(135, 206, 235, 0.2);
}
.feature-card h3 {
  margin-top: 1rem;
  font-weight: 600;
}
.feature-card p {
  color: #555;
  margin-top: 0.5rem;
}
</style>
