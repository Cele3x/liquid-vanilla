/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        // 'sans': ['"Raleway"', 'sans-serif'],
        'sans': ['montserrat', 'sans-serif'],
        'raleway': ['"Raleway"', 'sans-serif'],
        'playfair': ['"Playfair Display"', 'serif'],
        'montserrat': ['Montserrat', 'sans-serif'],
      },
      colors: {
        'primary': '#111111',
        'secondary': '#3C3D37',
        'accent': '#c8c177',
        'light': '#ECDFCC',
        'gold': '#b8860b',
        'gold-hover': '#daa520',
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

