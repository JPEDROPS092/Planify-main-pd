// plugins/api.ts
// Configura o cliente OpenAPI gerado (openapi-typescript-codegen, client axios).
// O cliente gerado NÃO expõe interceptors; a autenticação é feita via
// OpenAPI.TOKEN (resolver) e a base via OpenAPI.BASE.
import { OpenAPI } from '~/lib/api-client';
import { useAuthStore } from '~/stores/auth';

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();

  // Base da API (NUXT_PUBLIC_API_BASE_URL; default http://127.0.0.1:8000)
  OpenAPI.BASE = config.public.apiBaseUrl as string;
  OpenAPI.WITH_CREDENTIALS = true;

  // Bearer token resolvido a cada request a partir da store de auth.
  // O request.ts gerado injeta `Authorization: Bearer <token>` quando o
  // resolver retorna uma string não-vazia.
  OpenAPI.TOKEN = async () => {
    const authStore = useAuthStore();
    return authStore.accessToken ?? '';
  };
});
