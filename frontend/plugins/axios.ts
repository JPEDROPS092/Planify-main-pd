import { defineNuxtPlugin, useRuntimeConfig } from "#app";
import { useAuthStore } from "@/stores/auth";
import axiosInstance from "@/lib/axios-instance";

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();

  // 1. Define a baseURL usando a variável correta do config
  const apiBaseUrl = config.public.apiBase;
  axiosInstance.defaults.baseURL = apiBaseUrl;

  console.log(
    `[Axios Plugin] Configurando baseURL para: ${apiBaseUrl}\n` +
      `[Axios Plugin] Teste a conexão acessando: ${apiBaseUrl}/api/health/`
  );

  // 2. Interceptor de requisição para adicionar o token de autenticação
  axiosInstance.interceptors.request.use(
    (requestConfig) => {
      const authStore = useAuthStore();

      if (authStore.isLoggedIn && authStore.accessToken) {
        requestConfig.headers.Authorization = `Bearer ${authStore.accessToken}`;
        console.debug(
          `[Axios Plugin] Requisição autenticada para: ${requestConfig.url}`
        );
      } else {
        console.debug(
          `[Axios Plugin] Requisição sem autenticação para: ${requestConfig.url}`
        );
      }
      return requestConfig;
    },
    (error) => {
      console.error("[Axios Plugin] Erro no interceptor de requisição:", error);
      return Promise.reject(error);
    }
  );

  // 3. Interceptor de resposta para lidar com erros e logout automático
  axiosInstance.interceptors.response.use(
    (response) => {
      // Só loga se não for uma requisição de health check
      if (!response.config.url?.includes("/api/health/")) {
        console.debug(
          `[Axios Plugin] Resposta ${response.status} de: ${response.config.url}`
        );
      }
      return response;
    },
    async (error) => {
      // Se temos uma resposta do servidor
      if (error.response) {
        console.error(
          `[Axios Plugin] Erro ${error.response.status} em ${error.config.url}:`,
          error.response.data
        );

        // Se o token expirou (401), faça logout automático
        if (error.response.status === 401) {
          const authStore = useAuthStore();
          console.warn(
            "[Axios Plugin] Token expirado, realizando logout automático"
          );
          await authStore.logout();
          // O redirecionamento será feito pelo logout da store
        }
      }
      // Se o erro é de rede/conexão
      else if (error.request) {
        console.error(
          `[Axios Plugin] Erro de rede ao acessar ${error.config?.url}. ` +
            `Verifique se o backend está rodando em ${axiosInstance.defaults.baseURL}`
        );
      }
      // Outros tipos de erro
      else {
        console.error("[Axios Plugin] Erro:", error.message);
      }

      return Promise.reject(error);
    }
  );
});
