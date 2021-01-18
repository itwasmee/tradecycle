module.exports = {
  purge: {
    enabled: true,
    content: [
      './templates/*.html',
    './templates/**/*.html'],
  },
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Raleway', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      }
    },
  },
  variants: {},
  plugins: [],
}
