/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['montserrat', 'sans-serif'],
        'playfair': ['Playfair Display', 'serif'],
        'montserrat': ['Montserrat', 'sans-serif'],
        'lato': ['Lato', 'sans-serif'],
        'raleway': ['Raleway', 'sans-serif'],
      },
      colors: {
        // Dark mode colors (default)
        'primary': '#111111',
        'secondary': '#3C3D37',
        'accent': '#C8C177',
        'light': '#ECDFCC',
        'gold': '#B8860B',
        'gold-hover': '#DAA520',
        
        // Light mode colors
        'primary-light': '#ECDFCC',
        'secondary-light': '#C8C177',
        'accent-light': '#3C3D37',
        'dark': '#111111',
        'gold-light': '#B8860B',
        'gold-hover-light': '#DAA520',
      },
      opacity: {
        '85': '0.85',
      },
      brightness: {
        '95': '.95',
      },
    },
  },
  plugins: [],
  darkMode: 'class', // This allows us to use dark: prefix for dark mode styles
}

