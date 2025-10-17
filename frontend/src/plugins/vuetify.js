import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as mdi from '@mdi/js'  // Import everything from @mdi/js

// Vuetify setup
const vuetify = createVuetify({
  icons: {
    iconfont: 'mdiSvg',  // Use mdiSvg icons
    values: {
      // Example icon usage
      home: mdi.mdiHome,   // Replace with actual icon names from @mdi/js
    }
  }
})

export default vuetify
