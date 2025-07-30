import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // --- AÑADIR ESTA LÍNEA ---
  // Le decimos a Vite que todos los assets deben usar '/static/' como base.
  base: '/static/',
})
