import axios from "axios";
import type { AxiosError } from "axios";

/**
 * Cria e exporta uma instância única e base do Axios para toda a aplicação.
 *
 * Esta instância é intencionalmente "burra" e não contém configurações
 * de ambiente (como a baseURL).
 *
 * Toda a configuração dinâmica (baseURL, interceptors de autenticação)
 * será aplicada a esta instância pelo plugin Nuxt em `plugins/axios.ts`.
 * Isso garante que a configuração ocorra no momento correto do ciclo de vida do Nuxt,
 * evitando erros de contexto de SSR.
 *
 * IMPORTANTE:
 * A `baseURL` NÃO é definida aqui. Ela será injetada dinamicamente
 * pelo plugin `plugins/axios.ts`, que tem acesso seguro ao `runtimeConfig` do Nuxt.
 *
 * Este arquivo é deliberadamente "burro" para evitar erros de contexto
 * durante o processo de build e a inicialização do servidor.
 */
const axiosInstance = axios.create({
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  timeout: 15000, // 15 segundos
});

// Exporta a instância para que possa ser importada e configurada em outros lugares.
export default axiosInstance;

/**
 * Exporta um tipo de erro genérico que o Orval pode usar
 * para tipar os erros retornados pelas chamadas da API.
 */
export type ErrorType<Error> = AxiosError<Error>;
