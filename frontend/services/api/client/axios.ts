// src/client/axios.ts
import axios, { type AxiosInstance } from 'axios';
import { setupInterceptors } from './interceptors';
import { useRuntimeConfig } from '#app'; // Uncommented for Nuxt 3

/**
 * Configuração do Axios para o Planify
 * Cria uma instância do Axios com interceptores para autenticação
 * e tratamento de erros padronizado.
 */
export const createAxiosInstance = (customBaseURL?: string): AxiosInstance => {
  // Priorize o customBaseURL passado pelo plugin
  let baseURL = customBaseURL || 'http://127.0.0.1:8000';

  // Se não tiver customBaseURL e estivermos no cliente, tentar usar a configuração do Nuxt
  if (!customBaseURL) {
    try {
      if (process.client) {
        const config = useRuntimeConfig();
        if (config && config.public && config.public.apiBaseUrl) {
          baseURL = config.public.apiBaseUrl;
        }
        console.log('Usando URL para API:', baseURL);
      } else {
        // No lado do servidor, tentar usar variáveis de ambiente
        baseURL = process.env.NUXT_PUBLIC_API_BASE_URL || process.env.API_BASE_URL || baseURL;
      }
    } catch (e) {
      console.warn("useRuntimeConfig não disponível. Usando baseURL padrão:", baseURL);
    }
  }

  const api = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    withCredentials: false, // Changed to false since we're using JWT tokens in headers, not cookies
  });

  setupInterceptors(api);

  return api;
};

// Variável para armazenar a instância global
let _axiosInstance: AxiosInstance | null = null;

// Função para obter a instância global ou criar uma nova
export const getAxiosInstance = (customBaseURL?: string): AxiosInstance => {
  if (!_axiosInstance || customBaseURL) {
    _axiosInstance = createAxiosInstance(customBaseURL);
  }
  return _axiosInstance;
};

// Exportar uma instância padrão
export const axiosInstance = getAxiosInstance();
