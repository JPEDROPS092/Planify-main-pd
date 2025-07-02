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
