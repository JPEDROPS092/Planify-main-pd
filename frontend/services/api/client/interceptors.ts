/**
 * Interceptores para requisições e respostas da API
 * Gerencia autenticação, renovação de tokens e tratamento de erros
 */
import axios from 'axios';
import { useState, navigateTo } from '#imports';
import { useRuntimeConfig } from '#app';
import { tokenUtils } from '../auth/service';

/**
 * Configura interceptores para uma instância do Axios
 * @param api Instância do Axios para adicionar interceptores
 * @param options Opções opcionais para configuração
 */
export function setupInterceptors(api, options = {}) {
  // Estas variáveis agora serão passadas pelo useApiClient
  // ou acessadas dentro de funções de callback (closures)

  // Interceptor para adicionar o token de autenticação em cada requisição
  api.interceptors.request.use((config) => {
    // Acessando o estado dentro da função de callback
    const accessToken = useState<string | null>('auth.accessToken');

    // Usar o tokenUtils para obter tokens armazenados
    const { access } = tokenUtils.getStoredTokens();

    // Se tiver token no estado reativo, use-o
    if (accessToken.value) {
      config.headers.Authorization = `Bearer ${accessToken.value}`;
    }
    // Caso contrário, use o token do localStorage (via tokenUtils)
    else if (access) {
      config.headers.Authorization = `Bearer ${access}`;
      // Sincronizar com o estado
      accessToken.value = access;
    }

    return config;
  });

  // Interceptor para tratar erros de resposta
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      // Acessando os composables dentro do callback para evitar erros
      const runtimeConfig = useRuntimeConfig();
      const accessToken = useState<string | null>('auth.accessToken');
      const refreshToken = useState<string | null>('auth.refreshToken');

      const originalRequest = error.config;

      // Se o erro for 401 (não autorizado) e não for uma tentativa de refresh
      if (
        error.response &&
        error.response.status === 401 &&
        !originalRequest._retry &&
        !originalRequest.url?.includes('token/refresh')
      ) {
        originalRequest._retry = true;

        // Tentar atualizar o token
        const refresh =
          refreshToken.value || tokenUtils.getStoredTokens().refresh;

        if (refresh) {
          try {
            console.log('Tentando atualizar token automaticamente');
            const response = await axios.post(
              `${runtimeConfig.public.apiBaseUrl}/api/auth/token/refresh/`,
              { refresh }
            );

            if (response.data.access) {
              console.log('Token atualizado com sucesso');

              // Atualizar o token no estado reativo e localStorage
              const newAccess = response.data.access;
              const newRefresh = response.data.refresh || refresh;

              accessToken.value = newAccess;
              refreshToken.value = newRefresh;

              // Salvar no localStorage usando tokenUtils
              tokenUtils.saveTokens(newAccess, newRefresh);

              // Atualizar o header da requisição original
              originalRequest.headers.Authorization = `Bearer ${newAccess}`;

              // Reenviar a requisição original
              return api(originalRequest);
            }
          } catch (refreshError) {
            console.error(
              'Erro ao atualizar token automaticamente:',
              refreshError
            );

            // Limpar tokens e estado
            tokenUtils.clearTokens();
            accessToken.value = null;
            refreshToken.value = null;

            // Redirecionar para login
            navigateTo('/auth/login');
          }
        } else {
          // Limpar tokens e estado se não houver refresh token
          tokenUtils.clearTokens();
          accessToken.value = null;
          refreshToken.value = null;

          // Redirecionar para login
          navigateTo('/auth/login');
        }
      }

      return Promise.reject(error);
    }
  );

  return api;
}
