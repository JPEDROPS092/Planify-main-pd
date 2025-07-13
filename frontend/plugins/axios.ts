// filepath: plugins/axios.ts

import { axiosInstance } from "@/lib/axios-instance"; // Importe sua instância customizada
import { useAuthStore } from "@/stores/auth";

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();

  // 1. Configura a baseURL na instância que o Orval usa
  axiosInstance.defaults.baseURL = config.public.apiBase as string;
  console.log(
    `[Axios Plugin] baseURL configurada para: ${axiosInstance.defaults.baseURL}`
  );

  // 2. Interceptor de Requisição - O ponto mais importante
  axiosInstance.interceptors.request.use(
    (requestConfig) => {
      // É CRUCIAL chamar useAuthStore() AQUI DENTRO, e não fora do interceptor.
      // Isso garante que você sempre pegue a versão mais atualizada da store.
      const authStore = useAuthStore();

      // Verifique se o token existe ANTES de tentar usá-lo
      if (authStore.accessToken) {
        console.log(
          "[Axios Plugin] Token encontrado na store, anexando ao header."
        );
        requestConfig.headers.Authorization = `Bearer ${authStore.accessToken}`;
      } else {
        console.log(
          "[Axios Plugin] NENHUM token encontrado na store para esta requisição."
        );
      }

      return requestConfig;
    },
    (error) => {
      console.error(
        "[Axios Plugin] Erro na configuração da requisição:",
        error
      );
      return Promise.reject(error);
    }
  );

  // 3. Interceptor de Resposta - Lógica de logout e refresh
  axiosInstance.interceptors.response.use(
    (response) => response, // Se a resposta for OK, não faz nada
    async (error) => {
      const originalRequest = error.config;

      // Enhanced error logging for debugging
      console.error("[Axios Plugin] API Error Details:", {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        headers: error.response?.headers,
        requestHeaders: error.config?.headers,
      });

      // Handle 403 Forbidden errors specifically
      if (error.response?.status === 403) {
        console.error(
          "[Axios Plugin] 403 Forbidden Error - Permission denied for:",
          {
            url: error.config?.url,
            method: error.config?.method,
            userToken:
              error.config?.headers?.Authorization?.substring(0, 30) + "...",
            errorDetail: error.response?.data?.detail,
          }
        );
      }

      // Se o erro é 401 e ainda não tentamos renovar o token
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        const authStore = useAuthStore();

        // Tenta renovar o token se houver um refresh token
        if (authStore.refreshToken) {
          try {
            console.log(
              "[Axios Plugin] Token de acesso expirado. Tentando renovar..."
            );
            // A chamada para refresh deve ser feita com a instância do Axios
            const { data } = await axiosInstance.post(
              "/api/auth/jwt/refresh/",
              {
                refresh: authStore.refreshToken,
              }
            );

            // Sucesso na renovação: salva o novo token de acesso
            authStore.setTokens(data.access); // Apenas o de acesso, o de refresh continua o mesmo

            // Re-envia a requisição original com o novo token
            originalRequest.headers["Authorization"] = `Bearer ${data.access}`;
            return axiosInstance(originalRequest);
          } catch (refreshError) {
            console.error(
              "[Axios Plugin] Falha ao renovar o token. Deslogando.",
              refreshError
            );
            authStore.logout();
            navigateTo("/login");
            return Promise.reject(refreshError);
          }
        } else {
          // Se não há refresh token, apenas desloga
          console.log("[Axios Plugin] Erro 401 sem refresh token. Deslogando.");
          authStore.logout();
          navigateTo("/login");
        }
      }

      return Promise.reject(error);
    }
  );
});
