/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0a0e1a',
          card: '#111827',
          'card-hover': '#1a2236',
        },
        primary: {
          DEFAULT: '#10b981',
          soft: '#10b98120',
          glow: '#10b98140',
        },
        secondary: {
          DEFAULT: '#3b82f6',
          soft: '#3b82f620',
        },
        usdt: '#26a17b',
        ton: '#0098ea',
        success: '#22c55e',
        warning: '#f59e0b',
        danger: '#ef4444',
        text: {
          DEFAULT: '#f1f5f9',
          muted: '#64748b',
          secondary: '#94a3b8',
        },
        border: '#1e293b',
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
        '3xl': '20px',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
