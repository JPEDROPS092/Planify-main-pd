// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  css: ['~/assets/css/tailwind.css'],
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/color-mode',
    '@pinia/nuxt',
    '@nuxt/image',
    '@nuxtjs/sentry',
  ],


  colorMode: {
    classSuffix: '',
    preference: 'system',
    fallback: 'light',
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000',
    },
  },
  app: {
    head: {
      title: 'Planify - Gerenciamento de Projetos',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Sistema de Gerenciamento de Projetos de Pesquisa e Desenvolvimento',
        },
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },
  },
  // Configurações do Vite integradas ao Nuxt
  vite: {
    resolve: {
      alias: {

        '~': './frontend',
         '@': './frontend',
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
  },
});
