import axios, { type AxiosInstance } from 'axios';
import { setupInterceptors } from './interceptors';
import { ApiError } from '../client/config';

/**
 * Plugin Axios para o Nuxt
 * Configura uma instância global do Axios com interceptores para autenticação
 * e tratamento de erros padronizado
 */
export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const accessToken = useState<string | null>('auth.accessToken');

  // Criar instância do Axios com configurações padrão
  const api = axios.create({
    baseURL: config.public.apiBaseUrl,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    withCredentials: true, // Importante para autenticação com cookies
  });

  // Configurar interceptores para a instância da API
  setupInterceptors(api);

  // Disponibilizar a instância da API globalmente via $api
  return {
    provide: {
      api,
    },
  };
});
