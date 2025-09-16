// main.js
import { createApp } from 'vue'
import App from './App.vue'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// ✅ set your logo blue (replace #007BFF with your exact shade)
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'auraTheme',
    themes: {
      auraTheme: {
        dark: false,
        colors: {
          primary: '#007BFF',   // <-- your logo blue
          secondary: '#6C757D', // soft grey (can tweak)
          background: '#FFFFFF',
          surface: '#FFFFFF',
        },
      },
    },
  },
})

createApp(App).use(vuetify).mount('#app')
