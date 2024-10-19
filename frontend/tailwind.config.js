/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#1a202c',
        'dark-secondary': '#2d3748',
        'dark-text': '#e2e8f0',
      }
    },
  },
  plugins: [],
  darkMode: 'class', // This allows us to use dark: prefix for dark mode styles
}

