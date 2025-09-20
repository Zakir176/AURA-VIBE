<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <h1 class="text-3xl font-bold mb-6">Login with Spotify</h1>
    <button
      @click="loginWithSpotify"
      class="bg-green-500 text-white px-6 py-3 rounded shadow hover:bg-green-600 transition"
    >
      Connect Spotify
    </button>
  </div>
</template>

<script setup>
const loginWithSpotify = () => {
  window.location.href = "http://localhost:8000/login";
};
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f7f7f9 0%, #eef1f6 100%);
}
.auth-card {
  border-radius: 28px;
  backdrop-filter: blur(10px);
}
.logo-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: #f2f2f7;
}
.headline {
  font-size: 22px;
  font-weight: 700;
}
.subhead {
  font-size: 14px;
  color: #6e6e73;
}
.apple-btn {
  background: #000;
  color: #fff;
  border-radius: 14px;
  text-transform: none;
  letter-spacing: 0;
}
.spotify-btn {
  background: #1DB954;
  color: #fff;
  border-radius: 14px;
  text-transform: none;
  letter-spacing: 0;
}
.footnote {
  color: #6e6e73;
  font-size: 12px;
}
@media (max-width: 600px) {
  .auth-card { border-radius: 24px; }
}
</style>


