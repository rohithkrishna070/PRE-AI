// ==============================================================================
// Vite Configuration (vite.config.js)
// ------------------------------------------------------------------------------
// CONCEPT EXPLANATION:
// Vite is a ultra-fast build tool and dev server for modern frontend applications.
//
// Proxy Setup:
// `server.proxy`: Intercepts API requests starting with `/api` and proxies them 
// to your FastAPI Backend at `http://localhost:8000`.
// ==============================================================================

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
