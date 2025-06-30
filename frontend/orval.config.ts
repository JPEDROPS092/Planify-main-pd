// orval.config.ts (CORRIGIDO)

// Pega a URL base do ambiente, com um fallback claro.
const apiBaseUrl = process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000";

export default {
  api: {
    // Usa a variável para construir a URL do schema.
    input: `${apiBaseUrl}/api/schema/`,

    output: {
      // O modo 'tags-split' é excelente para separar por recurso (auth, projects, tasks, etc.)
      mode: "tags-split",

      // O alvo deve ser uma pasta dedicada para a API, como 'api/'
      target: "./api",

      // Coloque os schemas em uma subpasta para organização
      schemas: "./api/schemas",

      // Use 'vue-query' para gerar hooks do TanStack Query
      client: "vue-query",

      // Garante que o código gerado seja "tree-shakable" e limpo
      clean: true,

      // Gera mocks que podem ser úteis para testes ou desenvolvimento offline
      mock: true,
    },

    hooks: {
      // Este é o gancho mais importante para a integração
      afterAllFilesWrite: "prettier --write", // Formata todo o código gerado com Prettier
    },

    override: {
      // Diga ao Orval para usar a instância global do 'axios' por padrão.
      mutator: {
        path: "./api/axios-instance.ts", // Caminho para um arquivo que exporta o axios
        name: "default", // Nome da exportação
      },
      // Configurações globais para o vue-query
      query: {
        useQuery: true, // Garante que queries sejam geradas
        useMutation: true, // Garante que mutações sejam geradas
        options: {
          // Opções padrão que serão aplicadas a todas as queries geradas
          staleTime: 1000 * 60 * 5, // 5 minutos
        },
      },
    },
  },
};
