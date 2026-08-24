/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          900: '#210B2C',
          800: '#341845',
          700: '#55286F',
          600: '#6B3689',
          300: '#BC96E6',
          100: '#D8B4E2',
          50: '#F1E9F6',
        },
        mauve: '#AE759F',
        pending: {
          bg: '#FDF1E3',
          fg: '#92400E',
        },
        done: {
          bg: '#E4F5EA',
          fg: '#166534',
        },
        locked: {
          bg: '#F0EEF3',
          fg: '#5B5568',
        },
        alert: {
          bg: '#FCE8E6',
          fg: '#B3261E',
        },
        bg: '#F6F5F8',
        surface: '#FFFFFF',
        border: '#E4E1EA',
        textMain: '#1F1B2E',
        text2: '#6B6478',
        text3: '#9A93A8',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        custom: '0 1px 2px rgba(33,11,44,.06), 0 1px 8px rgba(33,11,44,.04)',
      },
      borderRadius: {
        'custom': '10px',
      }
    },
  },
  plugins: [],
}
