/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#16a34a', // green-600
          dark: '#15803d',    // green-700
        },
        secondary: {
          DEFAULT: '#111827', // gray-900
          light: '#1f2937',   // gray-800
        }
      }
    },
  },
  plugins: [],
}
