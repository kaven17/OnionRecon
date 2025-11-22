/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,jsx,ts,tsx}"
    ],
    theme: {
      extend: {
        colors: {
          'sci-bg': '#0b0f14',
          'sci-panel': 'rgba(18,22,30,0.6)',
          'neon-cyan': '#00f0ff',
          'neon-purple': '#b04bff',
          'accent-orange': '#ff9f43'
        },
        fontFamily: {
          ui: ['"Orbitron"', 'ui-sans-serif', 'system-ui']
        },
        keyframes: {
          radar: {
            '0%': { transform: 'rotate(0deg)' },
            '100%': { transform: 'rotate(360deg)' }
          },
          pulseC: {
            '0%': { opacity: '0.2', transform: 'scale(0.98)' },
            '50%': { opacity: '0.9', transform: 'scale(1.02)' },
            '100%': { opacity: '0.2', transform: 'scale(0.98)' }
          }
        },
        animation: {
          radar: 'radar 30s linear infinite',
          pulseC: 'pulseC 2.4s ease-in-out infinite'
        }
      }
    },
    plugins: []
  }
  