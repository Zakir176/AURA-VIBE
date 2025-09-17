<template>
  <v-container class="d-flex flex-column align-center justify-center py-12">
    <v-card class="pa-8" elevation="6" max-width="520">
      <v-card-title class="text-h5 font-weight-bold text-center">
        Join a Session
      </v-card-title>
      <v-divider class="my-4"></v-divider>

      <v-form @submit.prevent="join">
        <v-text-field
          v-model="sessionId"
          label="Session ID"
          outlined
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Password (optional)"
          outlined
          type="password"
        ></v-text-field>

        <v-btn type="submit" color="primary" block class="mt-4 rounded-pill">
          Join
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const sessionId = ref('')
const password = ref('')
const route = useRoute()

onMounted(() => {
  const prefill = route.query.id
  if (typeof prefill === 'string') {
    sessionId.value = prefill
  }
})

const join = () => {
  if (!sessionId.value) return
  // Placeholder: navigate to actual session route when available
  console.log('Joining session', { sessionId: sessionId.value, password: password.value })
  alert(`Attempting to join session: ${sessionId.value}`)
}
</script>

<style scoped>
</style>


