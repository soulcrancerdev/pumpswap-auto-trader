import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

/**
 * Vite Build Tool Configuration
 * Configures plugins, build options, and development server
 */
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
  },
})

