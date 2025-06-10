// plugins/api.ts (versão nova e correta)
import { OpenAPI } from '~/lib/api-client';
import { useAuthStore } from '~/stores/auth'; // Supondo que você tenha uma store de auth

export default defineNuxtPlugin((nuxtApp) => {
  // Define a URL base da sua API
  OpenAPI.BASE = os.BACKEND_URL; // Use variáveis de ambiente aqui!

  // Interceptor para adicionar o token de autenticação em cada requisição
  OpenAPI.interceptors.request.use((request) => {
    const authStore = useAuthStore();
    const token = authStore.token; // Pega o token da sua store

    if (token && request.headers) {
      request.headers['Authorization'] = `Bearer ${token}`;
    }
    return request;
  });

  // Opcional: Interceptor para tratar erros 401 (token expirado) globalmente
  OpenAPI.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.status === 401) {
        const authStore = useAuthStore();
        authStore.logout(); // Ex: Forçar logout
        // Redirecionar para a página de login
        // return navigateTo('/auth/login');
      }
      return Promise.reject(error);
    }
  );
});
