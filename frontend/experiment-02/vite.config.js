import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  assetsInclude: ['**/*.png', '**/*.PNG', '**/*.jpg', '**/*.svg', '**/*.gif', '**/*.mp3', '**/*.wav', '**/*.ogg', '**/*.json'],
  publicDir: './public', // Specify the path to your public folder
  module: {
    async headers() {
      return [
        {
          source: '../../backend/:path*', // Specify the path to your backend folder
          headers: [
            { key: "Access-Control-Allow-Credentials", value: "true" },
            { key: "Access-Control-Allow-Origin", value: "*" },
            { key: "Access-Control-Allow-Methods", value: "GET, POST, PATCH, PUT, DELETE, OPTIONS" },
            { key: "Access-Control-Allow-Headers", value: "Origin, X-Requested-With, Content-Type, Accept, Authorization" }
          ]
        }
      ]
    }
  }
})
