// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Ativa devtools para facilitar o debug durante o desenvolvimento
  devtools: { enabled: true },

  // Compatibility date for Nitro
  nitro: {
    compatibilityDate: '2025-06-02'
  },

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
  ],

  // TailwindCSS config extra (se houver)
  tailwindcss: {
    viewer: false,
  },

  // Modo de cor do sistema (dark/light)
  colorMode: {
    classSuffix: '',
    preference: 'system',
    fallback: 'light',
    storageKey: 'nuxt-color-mode',
  },

  // Configuração de runtime para o Nuxt
  runtimeConfig: {
    // Chaves privadas que são expostas apenas no servidor
    apiSecret: process.env.NUXT_API_SECRET || 'default_secret',

    // Chaves públicas que são expostas ao cliente
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000',
    },
  },

  // Configurações da aplicação (SEO básico e favicon)
  app: {
    head: {
      title: 'Planify - Gerenciamento de Projetos',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: 'Sistema de Gerenciamento de Projetos de Pesquisa e Desenvolvimento',
        },
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
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
    '@lib': '~/lib',
  },

  // Configuração de auto-imports. Nuxt 3 auto-importa de '~/composables', '~/utils' por padrão.
  // Adicionamos 'stores/composables/**' explicitamente para cobrir composables dentro da store.
  imports: {
    autoImport: true, // Habilita os auto-imports padrões do Nuxt
    dirs: [
      'composables/**', // Padrão do Nuxt, mas bom ser explícito
      'utils/**',       // Padrão do Nuxt
      'stores/composables/**', // Para composables específicos de stores
      'stores/**' // Para auto-importar stores Pinia (ex: useAuthStore de stores/auth.ts)
    ],
  },

  // Configuração para auto-importação de componentes.
  // Nuxt 3 escaneia o diretório '~/components' recursivamente.
  // Com 'pathPrefix: true' (ou omitindo pathPrefix, pois é o padrão para entradas de objeto),
  // os componentes são prefixados com o nome do diretório.
  // Ex: components/ui/Button.vue -> <UiButton />
  // Ex: components/shared/Card.vue -> <SharedCard />
  // Se você quiser que componentes na raiz de '~/components' não tenham prefixo,
  // e os de subdiretórios tenham, você pode configurar múltiplas entradas.
  // Para uma estrutura como a atual (business, shared, ui), o prefixo é geralmente desejável.
  components: [
    {
      path: '~/components',
      // Excluir arquivos index.ts para evitar conflitos de componentes
      extensions: ['.vue'],
      // pathPrefix: true, // true é o padrão para objetos, então pode ser omitido.
      // global: true, // Se quiser que todos sejam globais sem necessidade de import explícito em scripts (raro)
    }
    // Alternativamente, para controle mais granular:
    // { path: '~/components/global', global: true }, // Componentes globais sem prefixo
    // { path: '~/components/business', prefix: 'Business' },
    // { path: '~/components/shared', prefix: 'Shared' },
    // { path: '~/components/ui', prefix: 'Ui' },
  ],

  // Transpile arquivos se necessário (por exemplo, bibliotecas externas em ESM)
  // transpile: [],

  // Plugins personalizados (registro automático)
  plugins: [
    '~/plugins/api.ts',
    '~/plugins/auth.ts',
  ],

  // Diretório base para assets públicos
  dir: {
    public: 'public',
  },
});
