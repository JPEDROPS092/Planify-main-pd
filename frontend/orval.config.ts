// orval.config.ts

export default {
  api: {
    input: `${process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000"}/api/schema/`,
    output: {
      mode: "tags-split",
      target: "./api",
      schemas: "./api/schemas",
      client: "vue-query",
      clean: true,
      override: {
        // --- AJUSTE AQUI ---
        mutator: {
          path: "./lib/axios-instance.ts", // O caminho continua o mesmo
          name: "customMutator", // O nome agora é o da FUNÇÃO que criamos
        },
        // -------------------
      },
    },
    hooks: {
      afterAllFilesWrite: "prettier --write",
    },
  },
};
