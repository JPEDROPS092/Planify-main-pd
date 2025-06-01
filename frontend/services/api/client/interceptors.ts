/**
 * Interceptores para requisições e respostas da API
 * Gerencia autenticação, renovação de tokens e tratamento de erros
 */
import axios from 'axios';
import { useState, navigateTo, useRuntimeConfig } from '#imports';

/**
 * Configura interceptores para uma instância do Axios
 * @param api Instância do Axios para adicionar interceptores
 */
export function setupInterceptors(api: any) {
  const config = useRuntimeConfig();
  const accessToken = useState<string | null>('auth.accessToken');
  const refreshToken = useState<string | null>('auth.refreshToken');

  // Interceptor para adicionar o token de autenticação em cada requisição
  api.interceptors.request.use((config: any) => {
    // Usar o estado reativo do Nuxt em vez de acessar diretamente localStorage
    if (accessToken.value) {
      config.headers.Authorization = `Bearer ${accessToken.value}`;
    } else if (process.client && localStorage.getItem('auth_token')) {
      // Fallback: verificar localStorage caso o estado não esteja disponível
      const token = localStorage.getItem('auth_token');
      config.headers.Authorization = `Bearer ${token}`;
      // Sincronizar com o estado
      accessToken.value = token;
    }
    return config;
  });

  // Interceptor para tratar erros de resposta
  api.interceptors.response.use(
    (response: any) => response,
    async (error: any) => {
      const originalRequest = error.config;

      // Se o erro for 401 (não autorizado) e não for uma tentativa de refresh
      if (
        error.response &&
        error.response.status === 401 &&
        !originalRequest._retry &&
        !originalRequest.url?.includes('token/refresh')
      ) {
        originalRequest._retry = true;

        // Tentar atualizar o token usando o estado reativo
        if (refreshToken.value) {
          try {
            console.log('Tentando atualizar token automaticamente');
            const response = await axios.post(
              `${config.public.apiBaseUrl}/api/auth/token/refresh/`,
              {
                refresh: refreshToken.value,
              }
            );

            if (response.data.access) {
              console.log('Token atualizado com sucesso');
              // Atualizar o token no estado reativo e localStorage
              accessToken.value = response.data.access;

              if (process.client) {
                localStorage.setItem('auth_token', response.data.access);

                // Se um novo refresh token for fornecido, atualize-o também
                if (response.data.refresh) {
                  refreshToken.value = response.data.refresh;
                  localStorage.setItem('refresh_token', response.data.refresh);
                }
              }

              // Atualizar o header da requisição original
              originalRequest.headers.Authorization = `Bearer ${response.data.access}`;

              // Reenviar a requisição original com o api do axios
              return api(originalRequest);
            }
          } catch (refreshError) {
            console.error(
              'Erro ao atualizar token automaticamente:',
              refreshError
            );

            // Se falhar ao atualizar o token, limpar estado e redirecionar para login
            if (process.client) {
              localStorage.removeItem('auth_token');
              localStorage.removeItem('refresh_token');
            }
            accessToken.value = null;
            refreshToken.value = null;
            navigateTo('/login');
          }
        } else if (process.client && localStorage.getItem('refresh_token')) {
          // Fallback: tentar com o token do localStorage se disponível
          try {
            const localRefreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(
              `${config.public.apiBaseUrl}/api/auth/token/refresh/`,
              {
                refresh: localRefreshToken,
              }
            );

            if (response.data.access) {
              // Atualizar tokens
              accessToken.value = response.data.access;
              localStorage.setItem('auth_token', response.data.access);

              if (response.data.refresh) {
                refreshToken.value = response.data.refresh;
                localStorage.setItem('refresh_token', response.data.refresh);
              }

              // Atualizar o header da requisição original
              originalRequest.headers.Authorization = `Bearer ${response.data.access}`;

              // Reenviar a requisição original
              return api(originalRequest);
            }
          } catch (e) {
            console.error('Fallback refresh falhou:', e);
            // Limpar tudo e redirecionar
            accessToken.value = null;
            refreshToken.value = null;
            localStorage.removeItem('auth_token');
            localStorage.removeItem('refresh_token');
            navigateTo('/login');
          }
        }
      }

      return Promise.reject(error);
    }
  );

  return api;
}
