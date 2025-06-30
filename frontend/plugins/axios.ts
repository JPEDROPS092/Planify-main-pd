import { defineNuxtPlugin, useRuntimeConfig } from "#app";
import { useAuthStore } from "~/stores/auth";
import axiosInstance from "~/api/axios-instance"; // Importa a instância que criamos

export default defineNuxtPlugin(() => {
  // Pega a URL base do runtimeConfig. AQUI temos acesso garantido.
  const config = useRuntimeConfig();
  const apiBaseUrl = config.public.apiBase;

  // 1. Define a baseURL na nossa instância global.
  axiosInstance.defaults.baseURL = apiBaseUrl;

  console.log(
    `[axios.ts plugin] Axios baseURL configurada para: ${apiBaseUrl}`
  );

  // 2. Adiciona o interceptor para o token de autenticação.
  axiosInstance.interceptors.request.use((requestConfig) => {
    // A store precisa ser chamada aqui dentro para ser reativa.
    const authStore = useAuthStore();

    if (authStore.accessToken) {
      requestConfig.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return requestConfig;
  });

  // (Opcional, mas recomendado) Adiciona um interceptor de resposta para LOGAR erros.
  // Isso ajuda MUITO a debugar o que o backend está respondendo.
  axiosInstance.interceptors.response.use(
    (response) => response, // Se for sucesso, apenas retorna a resposta
    (error) => {
      console.error(
        "[Axios Error Interceptor] Ocorreu um erro na requisição:",
        error.response?.data || error.message
      );
      // Rejeita a promise para que o .catch() no seu código possa lidar com o erro
      return Promise.reject(error);
    }
  );

  // Não precisa retornar nada. Apenas configuramos a instância global.
});
