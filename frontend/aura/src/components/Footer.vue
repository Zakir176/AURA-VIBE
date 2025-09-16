<template>
  <v-footer color="transparent" class="footer-section" padless>
    <div class="footer-container">
      <v-row justify="center" align="center" class="footer-content">
        <!-- Logo/Brand Name -->
        <v-col cols="12" sm="4" class="footer-brand">
          <h3 class="footer-title">Aura Vibe</h3>
        </v-col>
        
        <!-- Footer Links -->
        <v-col cols="12" sm="4" class="footer-links">
          <v-row justify="center">
            <v-col cols="auto">
              <v-btn flat href="#" class="footer-link">About</v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn flat href="#" class="footer-link">Privacy</v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn flat href="#" class="footer-link">Terms</v-btn>
            </v-col>
          </v-row>
        </v-col>

        <!-- Social Media Icons -->
        <v-col cols="12" sm="4" class="footer-social">
          <v-row justify="center">
            <v-col cols="auto">
              <v-btn flat href="https://twitter.com" target="_blank" class="social-icon">
                <v-icon>mdi-twitter</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn flat href="https://github.com" target="_blank" class="social-icon">
                <v-icon>mdi-github</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn flat href="https://linkedin.com" target="_blank" class="social-icon">
                <v-icon>mdi-linkedin</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <!-- Copyright -->
      <v-row justify="center" class="mt-4">
        <v-col cols="12" class="text-center">
          <p class="footer-text">
            &copy; 2025 Aura Vibe. All Rights Reserved.
          </p>
        </v-col>
      </v-row>
    </div>
  </v-footer>
</template>

<script setup>
// If needed, you can import social media icons dynamically or other components.
</script>

<style scoped>
.footer-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  padding: 2rem 0;
  color: #fff;
}

.footer-container {
  width: 100%;
  padding: 0 2rem;
}

.footer-content {
  text-align: center;
}

.footer-brand {
  margin-bottom: 1rem;
}

.footer-title {
  font-size: 2rem;
  font-weight: 600;
  color: #007BFF; /* primary color */
}

.footer-links .footer-link {
  color: #6C757D; /* secondary color */
  margin: 0 10px;
  font-size: 1rem;
}

.footer-links .footer-link:hover {
  color: #007BFF;
}

.footer-social .social-icon {
  color: #007BFF; /* Primary color for social icons */
  font-size: 1.5rem;
}

.footer-social .social-icon:hover {
  color: #0056b3; /* Darker primary on hover */
}

.footer-text {
  color: #6C757D; /* secondary color */
  font-size: 0.875rem;
  margin-top: 1rem;
}
</style>
