// tailwind.config.js
module.exports = {
  purge: [
    "./src/**/*.css",
    "./*.html"
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [require('@tailwindcss/aspect-ratio')],
}
