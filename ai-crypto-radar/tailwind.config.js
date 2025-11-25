/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                radar: {
                    black: '#050505',
                    dark: '#0a0b14',
                    panel: '#121420',
                    blue: '#00f0ff',
                    red: '#ff003c',
                    green: '#00ff9d',
                    text: '#e0e0e0',
                    dim: '#6b7280'
                }
            },
            fontFamily: {
                display: ['Orbitron', 'sans-serif'],
                body: ['Rajdhani', 'sans-serif'],
            },
            animation: {
                'spin-slow': 'spin 3s linear infinite',
                'pulse-fast': 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'scan': 'scan 2s linear infinite',
                'fade-in': 'fadeIn 0.5s ease-out forwards',
            },
            keyframes: {
                scan: {
                    '0%': { transform: 'translateY(-100%)' },
                    '100%': { transform: 'translateY(100%)' },
                },
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            }
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
