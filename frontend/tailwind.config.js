/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#1E201E',
        'secondary': '#3C3D37',
        'accent': '#697565',
        'light': '#ECDFCC',
      }
    },
  },
  plugins: [],
  darkMode: 'class', // This allows us to use dark: prefix for dark mode styles
}

