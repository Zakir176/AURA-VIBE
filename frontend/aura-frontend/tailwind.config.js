// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

// tailwind.config.js
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          start: '#a855f7', // purple-500
          end: '#ec4899',   // pink-500
        },
        bg: '#ffffff',
        text: '#1f2937', // gray-800
      },
    },
  }
}