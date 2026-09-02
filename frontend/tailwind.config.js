/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        char: {
          950: '#0d0b09',
          900: '#14110F',
          800: '#1E1A16',
          700: '#2A2420',
        },
        saffron: {
          400: '#f0b45c',
          500: '#E8A33D',
          600: '#c9832a',
        },
        chili: {
          500: '#C1442B',
          600: '#a3371f',
        },
        cream: {
          100: '#F2E8DC',
          400: '#A69A8C',
        },
      },
      fontFamily: {
        display: ['"Fraunces"', 'serif'],
        body: ['"Manrope"', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'monospace'],
      },
      keyframes: {
        pulseSlow: {
          '0%, 100%': { opacity: 0.55 },
          '50%': { opacity: 1 },
        },
        riseIn: {
          '0%': { opacity: 0, transform: 'translateY(14px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      animation: {
        'pulse-slow': 'pulseSlow 2.4s ease-in-out infinite',
        'rise-in': 'riseIn 0.6s ease-out both',
      },
    },
  },
  plugins: [],
}
