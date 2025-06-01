import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'url';

export default defineConfig({
  plugins: [vue()],
  
  resolve: {
    alias: {
      '~': fileURLToPath(new URL('./src', import.meta.url)),
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  
  build: {
    // Otimização do tamanho do bundle
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    
    // Divisão de chunks para melhorar o carregamento
    rollupOptions: {
      output: {
        manualChunks: {
          // Separar dependências do Vue em um chunk próprio
          'vue-core': ['vue', 'vue-router', 'pinia'],
          
          // Separar bibliotecas de UI em um chunk próprio
          'ui-libs': ['chart.js', 'vue-chartjs'],
          
          // Separar utilitários em um chunk próprio
          'utils': ['zod', 'date-fns'],
        },
        
        // Nomear os chunks de forma consistente
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      },
    },
    
    // Habilitar tree-shaking agressivo
    target: 'esnext',
    cssCodeSplit: true,
    assetsInlineLimit: 4096, // Inline de assets pequenos (< 4kb)
    sourcemap: false, // Desabilitar sourcemaps em produção
    
    // Comprimir o output
    reportCompressedSize: false, // Melhorar performance do build
  },
  
  // Otimizações de desenvolvimento
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'zod',
      'chart.js',
    ],
    exclude: ['vue-demi'],
  },
  
  // Configurações de servidor de desenvolvimento
  server: {
    hmr: {
      overlay: true,
    },
    fs: {
      strict: true,
    },
  },
});
