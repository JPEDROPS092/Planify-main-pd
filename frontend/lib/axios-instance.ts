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

// Exporta o tipo de erro para uso em outras partes da aplicação
export type ErrorType<Error> = AxiosError<Error>;

// Função customizada para mutation
export const customMutator = <T>(
  config: AxiosRequestConfig
): AxiosPromise<T> => {
  return axiosInstance(config);
};
