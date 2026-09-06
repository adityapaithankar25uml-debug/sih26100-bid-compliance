/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#0a101d',
          900: '#0a192f',
          850: '#112240',
          800: '#1e293b',
          700: '#334155',
          600: '#475569',
        },
        gov: {
          dark: '#0f172a',
          blue: '#1e40af',
          accent: '#2563eb',
          light: '#eff6ff',
          gold: '#d97706',
          slate: '#f8fafc',
        },
      },
    },
  },
  plugins: [],
}

