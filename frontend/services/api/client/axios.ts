// src/client/axios.ts
import axios, { type AxiosInstance } from 'axios';
import { setupInterceptors } from './interceptors';
// import { useRuntimeConfig } from '#app'; // Para Nuxt 3

/**
 * Configuração do Axios para o Planify
 * Cria uma instância do Axios com interceptores para autenticação
 * e tratamento de erros padronizado.
 */
export const createAxiosInstance = (customBaseURL?: string): AxiosInstance => {
  let baseURL = customBaseURL || 'http://localhost:8000'; // Usar o customBaseURL se fornecido

  if (process.client) {
    // No lado do cliente, podemos tentar usar useRuntimeConfig se estiver em um contexto Nuxt.
    // Se este arquivo for usado fora do setup do Nuxt (ex: em um store Pinia simples),
    // useRuntimeConfig() pode não estar disponível diretamente.
    // Considere passar a config ou acessá-la de uma forma mais global se necessário.
    try {
      const config = useRuntimeConfig(); // Necessário se estiver em Nuxt 3
      baseURL = config.public.apiBaseUrl || baseURL;
    } catch (e) {
      console.warn("useRuntimeConfig não disponível. Usando baseURL padrão para cliente.");
      // Tentar pegar de variáveis de ambiente injetadas no build para o cliente, se houver
      // baseURL = import.meta.env.VITE_API_BASE_URL || baseURL; (para Vite)
    }
  } else {
    // No lado do servidor (SSR)
    // useRuntimeConfig pode não estar disponível aqui da mesma forma.
    // A variável de ambiente é uma forma mais segura.
    baseURL = process.env.NUXT_PUBLIC_API_BASE_URL || process.env.API_BASE_URL || baseURL;
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
