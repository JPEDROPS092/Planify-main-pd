// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Estilos globais (main.css para customizações, Tailwind CSS é injetado pelo módulo)
  css: [
    '~/assets/css/main.css',
  ],

  // Módulos utilizados no projeto
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/color-mode',
    '@pinia/nuxt',
    '@nuxt/image',
    '@nuxt/icon',
    // Adicione outros módulos conforme necessário
  ],

  // Configurações específicas do Pinia
  pinia: {
    storesDirs: ['./stores/**', './composables/stores/**'],
  },

  // Configuração do modo de cor (dark/light)
  colorMode: {
    classSuffix: '',
    preference: 'system',
    fallback: 'light',
    storageKey: 'planify-color-mode',
    dataValue: 'theme', // Uses data-theme instead of class
  },

  // Configuração de runtime para o Nuxt
  runtimeConfig: {
    // Chaves privadas que são expostas apenas no servidor
    apiSecret: process.env.NUXT_API_SECRET || 'planify_default_secret_2025',
    jwtSecret: process.env.NUXT_JWT_SECRET || 'planify_jwt_secret_2025',

    // Chaves públicas que são expostas ao cliente
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api',
      appName: 'Planify',
      appVersion: '1.0.0',
      environment: process.env.NODE_ENV || 'development',
    },
  },

  // Configurações da aplicação (SEO e meta tags)
  app: {
    head: {
      title: 'Planify - Gerenciamento de Projetos',
      titleTemplate: '%s | Planify',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: 'Sistema completo de Gerenciamento de Projetos de Pesquisa e Desenvolvimento com funcionalidades avançadas de colaboração e monitoramento.',
        },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'author', content: 'Planify Team' },
        { property: 'og:title', content: 'Planify - Gerenciamento de Projetos' },
        { property: 'og:description', content: 'Sistema completo de Gerenciamento de Projetos' },
        { property: 'og:type', content: 'website' },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
      ],
    },
  },

  // Aliases para melhorar a legibilidade dos imports
  alias: {
    '@composables': '~/composables',
    '@components': '~/components',
    '@shared': '~/components/shared',
    '@business': '~/components/business',
    '@ui': '~/components/ui',
    '@assets': '~/assets',
    '@services': '~/services',
    '@plugins': '~/plugins',
    '@pages': '~/pages',
    '@layouts': '~/layouts',
    '@types': '~/types',
    '@api': '~/api',
    '@stores': '~/stores',
    '@utils': '~/utils',
    '@lib': '~/lib',
  },

  // Configuração de auto-imports otimizada
  imports: {
    autoImport: true,
    dirs: [
      'composables/**',
      'utils/**',
      'stores/**',
      'stores/composables/**',
      'services/**', // Auto-import de services
    ],
    // Imports globais personalizados
    imports: [
      // Vue composables
      { name: 'default', as: 'PhosphorIcons', from: '@phosphor-icons/vue' },
      // Utilitários comuns
      { name: 'clsx', from: 'clsx' },
      { name: 'twMerge', from: 'tailwind-merge' },
    ],
  },

  // Configuração otimizada para auto-importação de componentes
  components: [
    {
      path: '~/components',
      extensions: ['.vue'],
      pathPrefix: false, // Remove prefixo para componentes na raiz
    },
    {
      path: '~/components/ui',
      prefix: 'Ui',
      extensions: ['.vue'],
    },
    {
      path: '~/components/shared',
      prefix: 'Shared',
      extensions: ['.vue'],
    },
    {
      path: '~/components/business',
      prefix: 'Business',
      extensions: ['.vue'],
    },
  ],

  // Plugins personalizados carregados em ordem específica
  plugins: [
    { src: '~/plugins/api.ts', mode: 'all' },
    { src: '~/plugins/auth.ts', mode: 'client' },
    { src: '~/plugins/icons.ts', mode: 'client' },
  ],

  // Configurações de build e otimização
  nitro: {
    compatibilityDate: '2025-06-04',
    experimental: {
      wasm: true,
    },
  },

  // Configurações de desenvolvimento
  devtools: { 
    enabled: true,
    timeline: {
      enabled: true,
    },
  },

  // Configurações de SSR
  ssr: true,

  // Diretório base para assets públicos
  dir: {
    public: 'public',
  },
});
