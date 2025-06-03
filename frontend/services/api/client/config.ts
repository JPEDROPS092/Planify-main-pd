/**
 * Configuração do cliente API
 * Configura o cliente Axios com base nas configurações do Nuxt
 */
import axios from 'axios';
import { setupInterceptors } from './interceptors';
import { useRuntimeConfig } from '#app';

// Classe para erros da API
export class ApiError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data: any = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }

  /**
   * Retorna uma mensagem amigável baseada no status HTTP
   */
  get friendlyMessage(): string {
    switch (this.status) {
      case 400:
        return 'Dados inválidos. Por favor, verifique as informações enviadas.';
      case 401:
        return 'Sessão expirada ou não autenticado. Por favor, faça login novamente.';
      case 403:
        return 'Você não tem permissão para acessar este recurso.';
      case 404:
        return 'O recurso solicitado não foi encontrado.';
      case 422:
        return 'Não foi possível processar a solicitação. Verifique os dados enviados.';
      case 429:
        return 'Muitas requisições. Por favor, aguarde um momento e tente novamente.';
      case 500:
      case 502:
      case 503:
      case 504:
        return 'Erro no servidor. Por favor, tente novamente mais tarde.';
      default:
        return (
          this.message ||
          'Ocorreu um erro inesperado. Por favor, tente novamente.'
        );
    }
  }
}

/**
 * Configuração estática da API (compatibilidade com código existente)
 * @deprecated Use useApiClient() para obter o cliente API configurado
 */
export const API_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
};

// Variável para armazenar a instância do cliente no lado do cliente
let clientInstance: any = null;

/**
 * Composable para obter o cliente API configurado
 * Deve ser chamado dentro de componentes Vue, plugins, ou outros composables
 */
export const useApiClient = () => {
  // Só criar a instância uma vez no lado do cliente
  if (process.client && clientInstance) {
    return clientInstance;
  }

  // Tentar obter a configuração do runtime
  let baseURL = 'http://localhost:8000';
  try {
    const runtimeConfig = useRuntimeConfig();
    baseURL = runtimeConfig.public.apiBaseUrl || baseURL;
  } catch (e) {
    console.warn('useRuntimeConfig não disponível, usando URL padrão');
  }

  const client = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    withCredentials: true,
  });

  // Configurar interceptores
  setupInterceptors(client);

  // Armazenar a instância para reutilização no lado do cliente
  if (process.client) {
    clientInstance = client;
  }

  return client;
};

/**
 * Composable para obter o token de autenticação
 */
export const useAuthToken = () => {
  // Usar o estado reativo do Nuxt para o token
  const accessToken = useState<string | null>('auth.accessToken');

  // Função para obter o token atual
  const getToken = (): string | null => {
    if (accessToken.value) {
      return accessToken.value;
    }

    // Fallback para localStorage
    if (process.client && localStorage.getItem('auth_token')) {
      const token = localStorage.getItem('auth_token');
      // Sincronizar com o estado
      accessToken.value = token;
      return token;
    }

    return null;
  };

  return {
    getToken,
    accessToken
  };
};

// Funções de utilidade que não dependem de composables Nuxt

/**
 * Função para criar FormData a partir de um objeto
 */
export function createFormData(data: Record<string, any>): FormData {
  const formData = new FormData();

  for (const key in data) {
    if (data[key] !== undefined && data[key] !== null) {
      // Se for um arquivo, adicione diretamente
      if (data[key] instanceof File) {
        formData.append(key, data[key]);
      }
      // Se for um array, adicione cada item com o mesmo nome de chave
      else if (Array.isArray(data[key])) {
        data[key].forEach((item: any) => {
          formData.append(`${key}`, item);
        });
      }
      // Se for um objeto (mas não um File), converta para JSON string
      else if (typeof data[key] === 'object') {
        formData.append(key, JSON.stringify(data[key]));
      }
      // Caso contrário, converta para string
      else {
        formData.append(key, String(data[key]));
      }
    }
  }

  return formData;
}

/**
 * Função para determinar o Content-Type baseado no corpo da requisição
 */
export function getContentType(data: any): string {
  // Se for FormData, o navegador definirá o boundary automaticamente
  if (data instanceof FormData) {
    return 'multipart/form-data';
  }

  // Para outros tipos, use application/json
  return 'application/json';
}

/**
 * Função para converter parâmetros de consulta em string de URL
 */
export function formatQueryParams(params: Record<string, any>): string {
  if (!params || Object.keys(params).length === 0) {
    return '';
  }

  const queryParams = new URLSearchParams();

  for (const key in params) {
    if (params[key] !== undefined && params[key] !== null) {
      if (Array.isArray(params[key])) {
        params[key].forEach((value: any) => {
          queryParams.append(key, String(value));
        });
      } else {
        queryParams.append(key, String(params[key]));
      }
    }
  }

  return queryParams.toString();
}
