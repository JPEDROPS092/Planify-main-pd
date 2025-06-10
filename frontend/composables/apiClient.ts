/**
 * API Client for Planify
 * Central utility for making API requests with proper authentication and error handling
 * Usa o plugin Axios configurado em vez de implementação personalizada
 */
import type { AxiosInstance, AxiosResponse } from 'axios';
import { getAxiosInstance } from '../services/api/client/axios';
import { ApiError, createFormData } from '../services/api/client/config';

// Types for API requests
export type ApiResponse<T = any> = {
  status: number;
  data: T;
  response: any;
};

export type ApiRequestConfig = {
  params?: Record<string, any>;
  headers?: Record<string, string>;
  withAuth?: boolean;
  [key: string]: any;
};

/**
 * API Client que utiliza o plugin Axios configurado
 */
export const createApiClient = () => {
  /**
   * Função para obter a instância do Axios configurada
   */
  const getClientInstance = (): AxiosInstance => {
    return getAxiosInstance();
  };

  /**
   * Processa a resposta da API e extrai os dados
   */
  const processResponse = <T>(response: AxiosResponse): T => {
    // Log the raw response data for debugging
    console.log('API Response:', response.config.url, response.data);

    // Para APIs que retornam { data: ... } como wrapper
    if (response.data && typeof response.data === 'object' && 'data' in response.data) {
      return response.data.data as T;
    }
    // Caso contrário, retorna o corpo da resposta diretamente
    return response.data as T;
  };

  /**
   * Processa erros da API de forma padronizada
   */
  const handleApiError = (error: any): never => {
    // Log the complete error for debugging
    console.error('API Error Full Details:', {
      config: error.config,
      response: error.response,
      message: error.message
    });

    if (error.response) {
      const { status, data, statusText } = error.response;

      // Handling Django REST Framework specific error formats
      let message = statusText || 'Erro na requisição';
      let detailedData = data;

      // Handle different error response formats from Django
      if (data) {
        if (data.detail) {
          message = data.detail;
        } else if (data.message) {
          message = data.message;
        } else if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
          // Django REST Framework often returns auth errors in non_field_errors
          message = data.non_field_errors[0];
        } else if (typeof data === 'string') {
          message = data;
        }

        // Handle specific auth errors
        if (status === 401) {
          if (message.includes('No active account') || message.includes('given credentials')) {
            message = 'Usuário e/ou senha incorreto(s)';
          } else if (message.includes('not found') || message.includes('inexistente')) {
            message = 'Este usuário não existe no sistema';
          }
        }
      }

      throw new ApiError(message, status, detailedData);
    }

    // Network ou outros erros
    throw new ApiError(
      error.message || 'Erro de conexão',
      0,
      null
    );
  };

  /**
   * HTTP methods shortcuts
   */
  return {
    get: async <T = any>(endpoint: string, config: ApiRequestConfig = {}): Promise<T> => {
      try {
        const api = getClientInstance();
        const response = await api.get(endpoint, config);
        return processResponse<T>(response);
      } catch (error) {
        return handleApiError(error);
      }
    },

    post: async <T = any>(endpoint: string, data?: any, config: ApiRequestConfig = {}): Promise<T> => {
      try {
        const api = getClientInstance();
        // Converter para FormData se necessário
        if (data && typeof data === 'object' && !(data instanceof FormData) && config.isFormData) {
          data = createFormData(data);
          // Axios detecta FormData automaticamente
        }
        const response = await api.post(endpoint, data, config);
        return processResponse<T>(response);
      } catch (error) {
        return handleApiError(error);
      }
    },

    put: async <T = any>(endpoint: string, data?: any, config: ApiRequestConfig = {}): Promise<T> => {
      try {
        const api = getClientInstance();
        if (data && typeof data === 'object' && !(data instanceof FormData) && config.isFormData) {
          data = createFormData(data);
        }
        const response = await api.put(endpoint, data, config);
        return processResponse<T>(response);
      } catch (error) {
        return handleApiError(error);
      }
    },

    patch: async <T = any>(endpoint: string, data?: any, config: ApiRequestConfig = {}): Promise<T> => {
      try {
        const api = getClientInstance();
        if (data && typeof data === 'object' && !(data instanceof FormData) && config.isFormData) {
          data = createFormData(data);
        }
        const response = await api.patch(endpoint, data, config);
        return processResponse<T>(response);
      } catch (error) {
        return handleApiError(error);
      }
    },

    delete: async <T = any>(endpoint: string, config: ApiRequestConfig = {}): Promise<T> => {
      try {
        const api = getClientInstance();
        const response = await api.delete(endpoint, config);
        return processResponse<T>(response);
      } catch (error) {
        return handleApiError(error);
      }
    },
  };
};

// Export the API client instance
export const apiClient = createApiClient();
