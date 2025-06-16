// plugins/api.ts
import { OpenAPI } from '../api/core/OpenAPI';
import { PlanifyApiClient } from '../api/PlanifyApiClient.ts';
import { AxiosHttpRequest } from '../api/core/AxiosHttpRequest';

export default defineNuxtPlugin(() => {
  // 1. Configurar a URL base da API a partir das variáveis de ambiente
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase || 'http://localhost:8000';
  
  // 2. Configurar o OpenAPI
  OpenAPI.BASE = apiBase;
  OpenAPI.WITH_CREDENTIALS = true;
  OpenAPI.CREDENTIALS = 'include';

  // 3. Configurar a autenticação (Token) com Resolver
  // O sistema já adiciona automaticamente "Bearer" quando o token é string
  OpenAPI.TOKEN = async () => {
    try {
      // Only access cookies on client side
      if (typeof window !== 'undefined') {
        const token = useCookie('auth-token');
        return token.value || ''; // Retorna apenas o token, sem "Bearer"
      }
      return '';
    } catch (error) {
      // Em caso de erro, retorna string vazia
      console.warn('Erro ao obter token de autenticação:', error);
      return '';
    }
  };

  // 4. Criar uma instância do cliente API principal com configuração adequada
  const apiClient = new PlanifyApiClient({
    BASE: apiBase,
    VERSION: '1.0.0',
    WITH_CREDENTIALS: true,
    CREDENTIALS: 'include',
    TOKEN: OpenAPI.TOKEN,
  }, AxiosHttpRequest);

  // 5. Disponibilizar o cliente para todo o app
  return {
    provide: {
      api: apiClient,
      openAPI: OpenAPI,
    },
  };
});