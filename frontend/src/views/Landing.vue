<template>
  <v-container class="d-flex justify-center align-center" style="min-height: 100vh">
    <v-card class="pa-6 elevation-12" max-width="400">
      <v-card-title class="text-h4 text-center">Aura Vibe</v-card-title>
      <v-card-subtitle class="text-center">Collaborative DJ for your Party</v-card-subtitle>

      <v-card-actions class="d-flex justify-center mt-4">
        <v-btn color="primary" large @click="$router.push('/create')">Create Session</v-btn>
        <v-btn color="secondary" large @click="$router.push('/join')">Join Session</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
// No script needed for landing page
</script>

<style scoped>
/* Add styles as necessary */
</style>
