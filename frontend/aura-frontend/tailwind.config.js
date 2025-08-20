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
        'primary-start': '#00CFFF',
        'primary-end': '#FF3EC8',
        glow: '#9C27B0',
        'bg-dark': '#0A0A0A',
        accent: '#84F9FF',
        text: '#E0E0E0',
      },
    },
  },
  plugins: [],
}
