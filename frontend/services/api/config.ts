/**
 * Configuração e utilitários do cliente de API.
 *
 * O transporte real é o cliente gerado em `~/lib/api-client`
 * (openapi-typescript-codegen). Este módulo só expõe helpers usados pela
 * camada de serviços/componentes.
 */
import { ApiService, OpenAPI } from '~/lib/api-client';

/**
 * Acessa o cliente gerado já configurado pelo plugin `plugins/api.ts`
 * (OpenAPI.BASE / OpenAPI.TOKEN). Mantido por compatibilidade com o barrel.
 */
export const createApiClient = () => ({ ApiService, OpenAPI });

/**
 * Converte um objeto em `FormData` (uploads multipart).
 * - File: anexado diretamente.
 * - Array: cada item com a mesma chave.
 * - Objeto: serializado como JSON.
 * - Demais: convertidos para string.
 * Ignora chaves `undefined`/`null`.
 */
export function createFormData(data: Record<string, any>): FormData {
  const formData = new FormData();

  for (const key in data) {
    if (data[key] !== undefined && data[key] !== null) {
      if (data[key] instanceof File) {
        formData.append(key, data[key]);
      } else if (Array.isArray(data[key])) {
        data[key].forEach((item: any) => {
          formData.append(`${key}`, item);
        });
      } else if (typeof data[key] === 'object') {
        formData.append(key, JSON.stringify(data[key]));
      } else {
        formData.append(key, String(data[key]));
      }
    }
  }

  return formData;
}
