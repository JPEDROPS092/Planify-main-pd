/**
 * Configuração base para os serviços da API do Planify
 * Fornece utilitários e configurações para comunicação com o backend
 */
import { useRuntimeConfig } from '#app';
import { useState } from '#imports';

/**
 * Função para obter a configuração da API de forma lazy
 * Garante que a configuração seja obtida apenas quando necessário
 * @returns Configuração básica da API
 */
export const getApiConfig = () => {
  return {
    baseURL: process.client ? useRuntimeConfig().public.apiBaseUrl : '',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  };
};

/**
 * Configuração estática da API (compatibilidade com código existente)
 * @deprecated Use getApiConfig() para obter a configuração dinamicamente
 */
export const API_CONFIG = {
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
};

/**
 * Função para obter o token de autenticação atual
 * Prioriza o estado reativo do Nuxt e faz fallback para localStorage
 * @returns Token de autenticação ou null se não estiver autenticado
 */
export const getAuthToken = (): string | null => {
  // Usar o estado reativo do Nuxt para o token
  const accessToken = useState<string | null>('auth.accessToken');

  if (accessToken.value) {
    return accessToken.value;
  }

  // Fallback para localStorage se o estado não estiver disponível
  if (process.client && localStorage.getItem('auth_token')) {
    const token = localStorage.getItem('auth_token');
    // Sincronizar com o estado
    accessToken.value = token;
    return token;
  }

  return null;
};

// Classe para gerenciar erros da API
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

// Função para criar FormData a partir de um objeto
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

// Função para determinar o Content-Type baseado no corpo da requisição
export function getContentType(data: any): string {
  // Se for FormData, o navegador definirá o boundary automaticamente
  if (data instanceof FormData) {
    return 'multipart/form-data';
  }

  // Para outros tipos, use application/json
  return 'application/json';
}

// Função para converter parâmetros de consulta em string de URL
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
