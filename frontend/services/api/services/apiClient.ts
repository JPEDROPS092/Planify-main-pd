/**
 * API Client for Planify
 * Central utility for making API requests with proper authentication and error handling
 * Usa o plugin Axios configurado em vez de implementação personalizada
 */
import { ApiError, createFormData, formatQueryParams } from '../client/config';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { getAxiosInstance } from '../client/axios';

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
    if (error.response) {
      const { status, data, statusText } = error.response;
      const message =
        data?.detail ||
        data?.message ||
        statusText ||
        'Erro na requisição';

      throw new ApiError(message, status, data);
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
