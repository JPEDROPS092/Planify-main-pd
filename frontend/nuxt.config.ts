// nuxt.config.ts

export default defineNuxtConfig({
  compatibilityDate: "2024-07-26", // Use uma data recente

  // --- MÓDULOS ESSENCIAIS ---
  modules: [
    "@nuxtjs/tailwindcss",
    "nuxt-icon", // Para ícones SVG otimizados
    "@vueuse/nuxt", // Coleção de composables úteis
    // "@pinia/nuxt", // Descomente se for usar Pinia para estado global
  ],

  // --- PLUGINS ---
  // A ordem pode ser importante. O Axios deve ser configurado antes do TanStack Query ser usado.
  plugins: ["~/plugins/axios.ts", "~/plugins/tanstack-query.client.ts"],

  // --- VARIÁVEIS DE AMBIENTE ---
  runtimeConfig: {
    // Chaves privadas (apenas no servidor) - Ex: NUXT_API_KEY no seu .env
    // apiKey: process.env.NUXT_API_KEY,

    // Chaves públicas (acessíveis no cliente)
    public: {
      // Use o prefixo NUXT_PUBLIC_ no seu arquivo .env
      // Ex: NUXT_PUBLIC_API_BASE=http://localhost:8000
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  // --- TAILWIND CSS ---
  tailwindcss: {
    exposeConfig: true, // Para intellisense do VSCode
    viewer: true, // Habilita visualizador em http://localhost:3000/_tailwind/
  },

  // --- ALIASES DE IMPORTAÇÃO ---
  // Simplifica os imports no seu código
  alias: {
    "@api": "~/api",
    "@composables": "~/composables",
    "@components": "~/components",
    "@assets": "~/assets",
    "@layouts": "~/layouts",
    "@pages": "~/pages",
    "@plugins": "~/plugins",
  },

  // --- DEVTOOLS ---
  // Essencial para o desenvolvimento com Nuxt
  devtools: { enabled: true },

  // --- CSS GLOBAL ---
  css: ["~/assets/css/main.css"],
});
