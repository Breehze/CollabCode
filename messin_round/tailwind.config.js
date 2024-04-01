/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {
        colors: {
            io_dark : "#496989",
            io_light: "#E2F4C5",
            io_mid_light : "#A8CD9F",
            io_mid_dark : "#58A399"
        }
    } 
  },
  plugins: [
        require('tailwindcss-animated')
    ],
}

