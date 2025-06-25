// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  plugins: ['~/plugins/vue-query'],
  modules: ['@nuxtjs/tailwindcss'], // Temporarily removed 'shadcn-nuxt'
  nitro: {
    compatibilityDate: '2025-06-16'
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000/api/',
    },
  },
  // Disable shadcn-nuxt for now to avoid the index.ts error
  // shadcn: {
  //   prefix: '', // prefixo para componentes shadcn
  //   componentDir: './components/ui' // diretório onde os componentes serão gerados
  // },
  tailwindcss: {
    exposeConfig: true,
    config: {
      darkMode: 'class',
      content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './app.vue',
        './components/ui/**/*.{js,vue,ts}'
      ],
      theme: {
        extend: {
          colors: {
            'primary': {
              DEFAULT: '#3D7DF8',
              '50': '#EBF1FE',
              '100': '#D6E4FD',
              '200': '#ADC9FB',
              '300': '#85AFF9',
              '400': '#5C94F7',
              '500': '#3D7DF8',
              '600': '#0F5AE8',
              '700': '#0C46B6',
              '800': '#093384',
              '900': '#051F52'
            },
          }
        }
      }
    }
  }
})
