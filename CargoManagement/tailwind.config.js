// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'space': "url('/src/assets/backgroundImage.jpg')",
      },
    },
  },
  plugins: [],
};
