/**
 * Tipos da API.
 *
 * Fonte única de verdade: o cliente gerado em `~/lib/api-client`
 * (gerado a partir do schema OpenAPI do backend). Reexportamos tudo aqui
 * para que `~/services/api` continue sendo o ponto de importação dos
 * componentes/stores.
 */
export * from '~/lib/api-client';

/**
 * Formato genérico de resposta paginada do DRF.
 * O cliente gerado cria um tipo `PaginatedXList` por entidade; este genérico
 * cobre os usos `{ count, next, previous, results }` na camada de serviços.
 */
export interface PaginatedResponse<T> {
  count: number;
  next?: string | null;
  previous?: string | null;
  results: T[];
}

/**
 * Aliases de corpo de requisição usados nos componentes (convenção Create/Update).
 * O cliente gerado expõe um único `XRequest` por entidade; mapeamos os nomes
 * Create/Update para ele.
 */
import type { TarefaRequest, CustoRequest, RiscoRequest } from '~/lib/api-client';

export type TarefaCreate = TarefaRequest;
export type TarefaUpdate = TarefaRequest;
export type CustoCreate = CustoRequest;
export type CustoUpdate = CustoRequest;
export type RiscoCreate = RiscoRequest;
export type RiscoUpdate = RiscoRequest;
