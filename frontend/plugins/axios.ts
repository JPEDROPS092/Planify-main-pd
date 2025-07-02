import { defineNuxtPlugin, useRuntimeConfig } from "#app";
import { useAuthStore } from "@/stores/auth";
import axiosInstance from "@/api/axios-instance"; // Importa a instância que criamos

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const apiBaseUrl = config.public.apiBase;

  // 1. Define a baseURL na nossa instância global.
  axiosInstance.defaults.baseURL = apiBaseUrl;

  console.log(
    `[axios.ts plugin] Axios baseURL configurada para: ${apiBaseUrl}`
  );

  // 2. Interceptor de requisição para adicionar o token de autenticação.
  axiosInstance.interceptors.request.use((requestConfig) => {
    // A store precisa ser chamada aqui dentro para ser reativa.
    const authStore = useAuthStore();

    if (authStore.isLoggedIn && authStore.accessToken) {
      requestConfig.headers.Authorization = `Bearer ${authStore.accessToken}`;
      console.log(
        "[axios.ts plugin] Token de autorização adicionado ao header."
      );
    }
    return requestConfig;
  });

  // 3. Interceptor de resposta para lidar com erros e logout automático
  axiosInstance.interceptors.response.use(
    (response) => {
      console.log(
        "[axios.ts plugin] Resposta recebida:",
        response.status,
        response.config.url
      );
      return response;
    },
    async (error) => {
      console.error(
        "[Axios Error Interceptor] Ocorreu um erro na requisição:",
        error.response?.data || error.message
      );

      // Se o token expirou (401), faça logout automático
      if (error.response?.status === 401) {
        const authStore = useAuthStore();
        console.log(
          "[axios.ts plugin] Token expirado. Fazendo logout automático."
        );
        authStore.logout();
        // O redirecionamento será feito pelo logout da store
      }

      // Rejeita a promise para que o .catch() no seu código possa lidar com o erro
      return Promise.reject(error);
    }
  );

  // Não precisa retornar nada. Apenas configuramos a instância global.
});
