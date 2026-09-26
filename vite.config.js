import { defineConfig } from 'vite';
import path from 'path';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: '/static/', 
  build: {
   
    outDir: path.resolve(__dirname, './static'),
    emptyOutDir: false,
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        'index': path.resolve(__dirname, './assets/js/index.js'),
        'app': path.resolve(__dirname, './assets/main.jsx'),
        'style': path.resolve(__dirname, './assets/styles/style.css'),
      },
      output: {
       
        entryFileNames: `js/[name]-bundle.js`,
        assetFileNames: `css/[name].css`,
      },
    },
  },
});