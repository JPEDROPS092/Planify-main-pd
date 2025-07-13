// filepath: lib/axios-instance.ts

import axios from "axios";
import type { AxiosRequestConfig, AxiosPromise, AxiosError } from "axios";

export const axiosInstance = axios.create({
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  timeout: 15000,
});

// Enhanced request interceptor for debugging
axiosInstance.interceptors.request.use(
  (config) => {
    // Get token from storage
    const token =
      localStorage.getItem("auth-token") ||
      sessionStorage.getItem("auth-token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log(
        `Making ${config.method?.toUpperCase()} request to:`,
        config.url
      );
      console.log("With token:", token.substring(0, 20) + "...");
    } else {
      console.warn("No auth token available for request:", config.url);
    }
    return config;
  },
  (error) => {
    console.error("Request interceptor error:", error);
    return Promise.reject(error);
  }
);

// Enhanced response interceptor for debugging
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error Details:", {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
    });

    if (error.response?.status === 401) {
      console.error("Unauthorized - token may be expired or invalid");
      // Clear token if unauthorized
      localStorage.removeItem("auth-token");
      sessionStorage.removeItem("auth-token");
    } else if (error.response?.status === 403) {
      console.error("Forbidden - user lacks permissions for this resource");
    }

    return Promise.reject(error);
  }
);

// ======================= A CORREÇÃO ESTÁ AQUI =======================

// Tipagem explícita para a configuração que o Orval passa
interface OrvalAxiosRequestConfig extends AxiosRequestConfig {
  signal?: AbortSignal;
}

/**
 * Mutator customizado que extrai o 'signal' corretamente.
 * O Orval/VueQuery passa o signal como uma propriedade de nível superior no config.
 * O Axios espera o signal dentro da sua própria propriedade de config.
 * Esta função faz essa "ponte".
 */
export const customMutator = <T>(
  config: OrvalAxiosRequestConfig
): AxiosPromise<T> => {
  // Extrai o `signal` do objeto de configuração.
  const { signal, ...rest } = config;

  // Passa o `signal` para o Axios da forma que ele espera.
  return axiosInstance({ ...rest, signal });
};

// ===================================================================

export default axiosInstance;

export type ErrorType<Error> = AxiosError<Error>;
