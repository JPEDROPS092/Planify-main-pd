// plugins/api.ts
import { OpenAPI } from '../api/core/OpenAPI';
import { PlanifyApiClient } from '../api/PlanifyApiClient.ts';

export default defineNuxtPlugin(() => {
  // 1. Configurar a URL base da API a partir das variáveis de ambiente
  const config = useRuntimeConfig();
  OpenAPI.BASE = config.public.apiBase;

  // 2. Configurar a autenticação (Token)
  // O OpenAPI gerado usa a propriedade TOKEN para autenticação
  // Vamos definir uma função que retorna o token do cookie
  
  OpenAPI.TOKEN = () => {
    try {
      const token = useCookie('auth-token');
      return token.value ? `Bearer ${token.value}` : undefined;
    } catch (error) {
      // Em caso de erro, retorna undefined (sem autenticação)
      console.warn('Erro ao obter token de autenticação:', error);
      return undefined;
    }
  };

  // 3. Configurar outras opções do OpenAPI
  OpenAPI.WITH_CREDENTIALS = true;
  OpenAPI.CREDENTIALS = 'include';
  
  // Configurar timeout padrão
  OpenAPI.TIMEOUT = 10000; // 10 segundos

  // 4. Interceptar erros de autenticação
  OpenAPI.interceptors = {
    response: {
      use: (response: any) => response,
      error: (error: any) => {
        if (error.status === 401) {
          // Token expirado ou inválido
          const tokenCookie = useCookie('auth-token');
          const userCookie = useCookie('auth-user');
          
          tokenCookie.value = null;
          userCookie.value = null;
          
          // Redirecionar para login apenas se não estivermos já na página de auth
          if (!window.location.pathname.startsWith('/auth')) {
            navigateTo('/auth/login');
          }
        }
        return Promise.reject(error);
      }
    }
  };

  // 5. Criar uma instância do cliente API principal
  const apiClient = new PlanifyApiClient();

  // 6. Disponibilizar o cliente para todo o app
  return {
    provide: {
      api: apiClient,
      openAPI: OpenAPI,
    },
  };
});