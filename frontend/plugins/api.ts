// Importa a função para definir um plugin no Nuxt
import { defineNuxtPlugin } from '#app';

// Define o plugin Nuxt
export default defineNuxtPlugin((nuxtApp) => {
  /**
   * Define uma função de fetch personalizada que será usada para chamadas de API.
   * Essa função verifica se o recurso solicitado é interno do Nuxt ou uma API externa.
   */
  const customFetch = (url, options = {}) => {
    // Verifica se o recurso faz parte do sistema interno do Nuxt (como assets, islands, imagens etc.)
    const isNuxtResource =
      url.includes('/_nuxt/') ||
      url.includes('/__nuxt_island/') ||
      url.includes('/builds/meta/') ||
      url.startsWith('/_ipx/') ||
      url.includes('/__nuxt/');

    // Se for um recurso interno do Nuxt, usa o $fetch padrão sem modificações
    if (isNuxtResource) {
      return $fetch(url, options);
    }

    /**
     * Configurações específicas para chamadas de API:
     * - Define a base da URL da API a partir da variável de ambiente ou localhost
     * - Adiciona credenciais (cookies, etc.)
     * - Define os headers padrão como JSON
     * - Adiciona interceptadores de requisição e resposta
     */
    const apiOptions = {
      ...options,
      baseURL: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      credentials: 'include',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        ...options.headers,
      },

      // Interceptador que roda antes da requisição ser enviada
      onRequest({ request, options }) {
        // Se estiver no cliente (navegador), pega o token do localStorage
        if (process.client) {
          const token = localStorage.getItem('auth_token');
          if (token) {
            // Adiciona o token no header Authorization
            options.headers = {
              ...options.headers,
              Authorization: `Bearer ${token}`,
            };
          }
        }
      },

      // Interceptador de erro que roda se a resposta da API retornar erro
      onResponseError({ request, response, options }) {
        // Se a resposta for 401 (não autorizado) e não for a rota de login/token
        if (
          response?.status === 401 &&
          !request.toString().includes('/api/auth/token/')
        ) {
          if (process.client) {
            // Remove os tokens salvos e redireciona o usuário para a página de login
            localStorage.removeItem('auth_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login';
          }
        }
      },
    };

    // Executa a requisição com as opções configuradas
    return $fetch(url, apiOptions);
  };

  /**
   * Fornece a função customFetch como 'apiFetch' no contexto do Nuxt,
   * mas sem sobrescrever o fetch global do Nuxt.
   * Isso evita conflitos com recursos internos.
   */
  nuxtApp.provide('apiFetch', customFetch);
});
