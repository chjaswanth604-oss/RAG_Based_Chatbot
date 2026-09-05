/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f4ff',
          100: '#e0e9ff',
          500: '#4f46e5',
          600: '#4338ca',
          700: '#3730a3',
          900: '#1e1b4b',
        },
        dark: {
          bg: '#0f172a',
          card: '#1e293b',
          sidebar: '#0b1120',
          border: '#334155',
        }
      },
    },
  },
  plugins: [],
};
