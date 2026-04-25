/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  theme: {
    extend: {
      colors: {
        obsidian: '#05050B',
        cyan: {
          jarvis: '#00E5FF',
          deep: '#0088CC',
        },
        amber: {
          warn: '#FF9100',
        },
      },
      fontFamily: {
        hud: ['Rajdhani', 'Teko', 'sans-serif'],
        mono: ['"IBM Plex Mono"', '"JetBrains Mono"', 'monospace'],
      },
      animation: {
        'pulse-soft': 'pulse-soft 2.2s ease-in-out infinite',
        'scan': 'scan 8s linear infinite',
        'flicker': 'flicker 3s linear infinite',
        'boot': 'boot 0.6s ease-out both',
      },
      keyframes: {
        'pulse-soft': {
          '0%,100%': { opacity: '1', filter: 'drop-shadow(0 0 4px rgba(0,229,255,0.7))' },
          '50%': { opacity: '0.55', filter: 'drop-shadow(0 0 0 rgba(0,229,255,0))' },
        },
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        flicker: {
          '0%,19.9%,22%,62.9%,64%,64.9%,70%,100%': { opacity: '1' },
          '20%,21.9%,63%,63.9%,65%,69.9%': { opacity: '0.4' },
        },
        boot: {
          '0%': { opacity: '0', transform: 'translateY(6px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
