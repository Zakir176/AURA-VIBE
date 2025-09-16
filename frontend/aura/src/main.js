// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Create Vuetify instance
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'auraTheme',
    themes: {
      auraTheme: {
        dark: false,
        colors: {
          primary: '#111111', // sleek black
          secondary: '#6C63FF', // accent purple/blue
          background: '#FFFFFF',
          surface: '#F5F5F7', // Apple-light grey
          error: '#FF6B6B',
        },
      },
    },
  },
  components,
  directives,
})


const app = createApp(App)

app.use(router)
app.use(vuetify)

app.mount('#app')
