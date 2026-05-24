/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17202a",
        mint: "#2ab7a9",
        coral: "#ee6c4d",
        amber: "#f6c85f",
        grape: "#6f5cc2"
      },
      boxShadow: {
        soft: "0 16px 40px rgba(23, 32, 42, 0.08)"
      }
    }
  },
  plugins: []
};
