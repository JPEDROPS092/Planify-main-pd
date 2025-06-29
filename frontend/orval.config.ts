// orval.config.ts
export default {
  api: {
    input: 'http://127.0.0.1:8000/api/schema/', // ou a URL da sua API
    output: {
      mode: 'tags-split',
      target: './composables/api',
      schemas: './composables/api/schemas',
      client: 'vue-query',
      composables: true, // importa como `useLoginQuery`, `useUsersQuery`, etc.
    },
  },
}
