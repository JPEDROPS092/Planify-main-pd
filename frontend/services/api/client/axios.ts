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
  let baseURL = customBaseURL || 'http://localhost:8000';

  // Se não tiver customBaseURL e estivermos no cliente, tentar usar a configuração do Nuxt
  if (!customBaseURL) {
    if (process.client) {
      try {
        const config = useRuntimeConfig();
        if (config && config.public && config.public.apiBaseUrl) {
          baseURL = config.public.apiBaseUrl;
        }
      } catch (e) {
        console.warn("useRuntimeConfig não disponível. Usando baseURL padrão para cliente.");
      }
    } else {
      // No lado do servidor, tentar usar variáveis de ambiente
      baseURL = process.env.NUXT_PUBLIC_API_BASE_URL || process.env.API_BASE_URL || baseURL;
    }
  }

  const api = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    withCredentials: true, // Importante para autenticação com cookies
  });

  setupInterceptors(api);

  return api;
};

// Variável para armazenar a instância global
let _axiosInstance: AxiosInstance | null = null;

// Função para obter a instância global ou criar uma nova
export const getAxiosInstance = (customBaseURL?: string): AxiosInstance => {
  if (!_axiosInstance) {
    _axiosInstance = createAxiosInstance(customBaseURL);
  }
  return _axiosInstance;
};

// Exportar uma instância padrão
export const axiosInstance = getAxiosInstance();
