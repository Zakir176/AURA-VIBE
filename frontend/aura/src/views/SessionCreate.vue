<template>
  <v-container class="d-flex flex-column align-center justify-center py-12">
    <v-card class="pa-8" elevation="6" max-width="600">
      <v-card-title class="text-h5 font-weight-bold text-center">
        Create a Session
      </v-card-title>
      <v-divider class="my-4"></v-divider>

      <!-- Session Form -->
      <v-form @submit.prevent="createSession">
        <v-text-field
          v-model="sessionName"
          label="Session Name"
          outlined
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Session Password"
          outlined
          type="password"
          required
        ></v-text-field>

        <v-text-field
          v-model.number="duration"
          label="Duration (minutes)"
          outlined
          type="number"
          min="10"
          required
        ></v-text-field>

        <v-btn
          type="submit"
          color="primary"
          block
          class="mt-4 rounded-pill"
        >
          Create Session
        </v-btn>
      </v-form>

      <!-- Session Preview -->
      <v-expand-transition>
        <div v-if="sessionCreated" class="text-center mt-6">
          <p><strong>Session ID:</strong> {{ sessionId }}</p>
          <p><strong>Password:</strong> {{ password }}</p>
          <v-img
            :src="qrCode"
            alt="Session QR Code"
            max-width="200"
            class="mx-auto mt-3"
          ></v-img>
        </div>
      </v-expand-transition>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import QRCode from "qrcode";

const sessionName = ref("");
const password = ref("");
const duration = ref(30); // default 30 min
const sessionCreated = ref(false);
const sessionId = ref("");
const qrCode = ref("");

// Generate a random session ID
const generateSessionId = () => {
  return Math.random().toString(36).substr(2, 8).toUpperCase();
};

const createSession = async () => {
  sessionId.value = generateSessionId();
  const sessionLink = `${window.location.origin}/join/${sessionId.value}`;

  // Generate QR code
  qrCode.value = await QRCode.toDataURL(sessionLink);

  sessionCreated.value = true;

  console.log("Session Created:", {
    sessionName: sessionName.value,
    password: password.value,
    duration: duration.value,
    sessionId: sessionId.value,
  });
};
</script>

<style scoped>
.v-card {
  border-radius: 20px;
  background: white;
}

.v-btn {
  font-weight: 600;
}

p {
  font-size: 1rem;
}
</style>
