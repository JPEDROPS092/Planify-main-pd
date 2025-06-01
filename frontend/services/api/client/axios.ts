import axios from 'axios';
import { setupInterceptors } from './interceptors';
import { ApiError } from '../client/config';

export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig();
  const accessToken = useState<string | null>('auth.accessToken');

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

  return {
    provide: {
      api,
    },
  };
});
