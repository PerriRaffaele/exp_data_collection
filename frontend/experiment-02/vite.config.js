import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  assetsInclude: ['**/*.png', '**/*.PNG', '**/*.jpg', '**/*.svg', '**/*.gif', '**/*.mp3', '**/*.wav', '**/*.ogg', '**/*.json'],
  publicDir: './public', // Specify the path to your public folder
})
