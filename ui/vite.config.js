import { defineConfig } from 'vite';
import path from 'path';
import react from '@vitejs/plugin-react';
import svgr from 'vite-plugin-svgr';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), svgr({ include: '**/*.svg' })],
  resolve: {
    alias: {
      '@Api': path.resolve(__dirname, 'src/api/'),
      '@Components': path.resolve(__dirname, 'src/components/'),
      '@Container': path.resolve(__dirname, 'src/container/'),
      '@Helpers': path.resolve(__dirname, 'src/helpers/'),
      '@Hooks': path.resolve(__dirname, 'src/hooks/'),
      '@Img': path.resolve(__dirname, 'src/resources/images/'),
      '@Modals': path.resolve(__dirname, 'src/components/modals'),
      '@Src': path.resolve(__dirname, 'src/'),
      '@State': path.resolve(__dirname, 'src/store/state'),
      '@Store': path.resolve(__dirname, 'src/store/'),
      '@Styles': path.resolve(__dirname, 'src/styles/'),
    },
  },
});
