// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Manter a data de compatibilidade é uma boa prática.
  compatibilityDate: "2024-07-26",

  // --- CONFIGURAÇÃO SPA ---
  // Desativa totalmente o SSR para todo o projeto
  ssr: false,

  // --- MÓDULOS ESSENCIAIS ---
  // A ordem dos módulos geralmente não é crítica, mas é bom mantê-los organizados.
  modules: [
    "@nuxtjs/tailwindcss",
    "@pinia/nuxt",
    "@nuxt/icon",
    "@vueuse/nuxt",
  ],

  // --- PLUGINS ---
  // Removido. A pasta `plugins` do Nuxt 3 carrega arquivos automaticamente.
  // Você não precisa listar os plugins aqui, a menos que queira controlar a ordem
  // de forma muito específica, o que raramente é necessário. O Nuxt lida com isso.

  // --- BUILD ---
  // ESSENCIAL: Garante que o TanStack Query funcione corretamente após o build.
  build: {
    transpile: ["@tanstack/vue-query"],
  },

  // --- VARIÁVEIS DE AMBIENTE ---
  runtimeConfig: {
    // Chaves privadas (apenas no servidor). Deixe como exemplo se não tiver.
    // apiSecret: process.env.NUXT_API_SECRET,

    // Chaves públicas (acessíveis no cliente)
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  // --- PINIA ---
  // Adiciona configuração para auto-imports, simplificando o uso da store.
  pinia: {
    autoImports: ["defineStore", "acceptHMRUpdate"],
  },

  // Adicionar `stores` explicitamente aqui é uma boa prática para clareza.
  imports: {
    dirs: ["stores"],
  },

  // --- CSS GLOBAL ---
  css: ["~/assets/css/main.css"],

  // --- TAILWIND CSS ---
  // Sua configuração está ótima. Nenhuma mudança necessária.
  tailwindcss: {
    exposeConfig: true,
    viewer: true,
  },

  // --- HEAD GLOBAL (SEO) ---
  // Adiciona metadados padrão para toda a aplicação. Melhora o SEO.
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      title: "Planify | Seu Gerenciador de Projetos", // Título padrão
      meta: [
        {
          name: "description",
          content:
            "Organize suas tarefas, projetos e equipes de forma eficiente com o Planify.",
        },
      ],
      link: [
        { rel: "icon", type: "image/svg+xml", href: "/favicon.svg" }, // Exemplo com SVG
      ],
    },
  },

  // --- DEVTOOLS ---
  // Sua configuração está perfeita.
  devtools: { enabled: true },
});
