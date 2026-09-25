import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  base: '/static/', 
  build: {
   
    outDir: path.resolve(__dirname, './static'),
    emptyOutDir: false,
    manifest: "manifest.json",
    rollupOptions: {
      input: {
        'index': path.resolve(__dirname, './assets/js/index.js'),
      },
      output: {
       
        entryFileNames: `js/[name]-bundle.js`,
      },
    },
  },
});