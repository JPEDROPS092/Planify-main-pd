/**
 * Cost Service
 *
 * Delega ao cliente gerado `~/lib/api-client` (ApiService).
 * O transporte (base URL / token) é configurado pelo plugin `plugins/api.ts`;
 * este arquivo não toca em OpenAPI.
 */
import { ApiService } from '~/lib/api-client';
import type {
  Custo,
  CustoRequest,
  PatchedCustoRequest,
  PaginatedCustoListList,
  CustoList,
} from '~/lib/api-client';

// ---------------------------------------------------------------------------
// Parâmetros de listagem (subset dos query-params suportados pela API)
// ---------------------------------------------------------------------------
export interface ListCustosParams {
  /** Filtra por ID de projeto */
  projeto?: number;
  /** Filtra por ID de tarefa */
  tarefa?: number;
  /** Filtra por ID de categoria */
  categoria?: number;
  /** Filtra por data (YYYY-MM-DD) */
  data?: string;
  /** Termo de busca textual */
  search?: string;
  /** Paginação */
  page?: number;
  /** Ordenação */
  ordering?: string;
  /** Tipo de custo */
  tipo?: 'FIXO' | 'RECORRENTE' | 'VARIAVEL';
  /** Passthrough para campos extras vindos de call-sites legados (ex.: status) */
  [key: string]: unknown;
}

// ---------------------------------------------------------------------------
// Composable
// ---------------------------------------------------------------------------
export function useCostService() {
  /**
   * Lista custos com filtros opcionais.
   *
   * Call-sites:
   *  - pages/custos/index.vue  → fetchCustos({ page, search, categoria, status, projeto })
   *  - pages/projetos/[id]/reports/costs.vue → fetchCustos(projectId)  [argumento posicional]
   *  - ProjectStatistics.vue  → listCustos({ projeto })
   *  - ProjectOverview.vue    → listCustos({ projeto })
   *
   * Suporte duplo: aceita tanto um objeto de parâmetros quanto um `number`
   * (ID de projeto direto), para compatibilidade com o call-site de costs.vue.
   *
   * Retorna: PaginatedCustoListList  ({ count, next, previous, results: CustoList[] })
   */
  async function fetchCustos(
    paramsOrProjectId?: ListCustosParams | number,
  ): Promise<PaginatedCustoListList> {
    let params: ListCustosParams = {};

    if (typeof paramsOrProjectId === 'number') {
      params = { projeto: paramsOrProjectId };
    } else if (paramsOrProjectId) {
      params = paramsOrProjectId;
    }

    return ApiService.apiCostsCustosList(
      params.categoria as number | undefined,
      params.data as string | undefined,
      params.ordering as string | undefined,
      params.page as number | undefined,
      params.projeto as number | undefined,
      params.search as string | undefined,
      params.tarefa as number | undefined,
      params.tipo as 'FIXO' | 'RECORRENTE' | 'VARIAVEL' | undefined,
    );
  }

  /** Alias de fetchCustos — usado em ProjectStatistics e ProjectOverview. */
  const listCustos = fetchCustos;

  /**
   * Retorna a lista de custos de um projeto específico.
   * Retorna PaginatedCustoListList (compatível com consumo via .results).
   *
   * Call-site: ProjectCosts.vue → costService.getByProject(projectId)
   */
  async function getByProject(
    projectId: number,
  ): Promise<PaginatedCustoListList> {
    return ApiService.apiCostsCustosList(
      undefined, // categoria
      undefined, // data
      undefined, // ordering
      undefined, // page
      projectId, // projeto
      undefined, // search
      undefined, // tarefa
      undefined, // tipo
    );
  }

  /**
   * Busca um custo pelo ID.
   *
   * Call-site: pages/custos/index.vue → getCusto(id) (alias retrieveCusto)
   */
  async function getCusto(id: number): Promise<Custo> {
    return ApiService.apiCostsCustosRetrieve(id);
  }

  /**
   * Cria um novo custo.
   *
   * Call-sites:
   *  - pages/custos/index.vue   → createCusto(custoData)
   *  - ProjectCosts.vue         → costService.create(payload)
   *  - CostForm.vue             → createCost(costData)
   */
  async function createCusto(data: CustoRequest): Promise<Custo> {
    return ApiService.apiCostsCustosCreate(data);
  }

  /** Alias de createCusto — usado em ProjectCosts.vue e CostForm.vue. */
  const create = createCusto;
  const createCost = createCusto;

  /**
   * Atualiza um custo existente (PUT completo).
   *
   * Call-sites:
   *  - pages/custos/index.vue  → updateCusto(id, data)
   *  - ProjectCosts.vue        → costService.update(id, data)
   *  - CostForm.vue            → updateCost(id, data)
   */
  async function updateCusto(id: number, data: CustoRequest): Promise<Custo> {
    return ApiService.apiCostsCustosUpdate(id, data);
  }

  /** Alias de updateCusto — usado em ProjectCosts.vue e CostForm.vue. */
  const update = updateCusto;
  const updateCost = updateCusto;

  /**
   * Atualização parcial de um custo (PATCH).
   * Disponível para uso futuro; não aparece diretamente nos call-sites actuais.
   */
  async function patchCusto(
    id: number,
    data: PatchedCustoRequest,
  ): Promise<Custo> {
    return ApiService.apiCostsCustosPartialUpdate(id, data);
  }

  /**
   * Remove um custo pelo ID.
   *
   * Call-sites:
   *  - pages/custos/index.vue  → destroyCusto(id)
   *  - ProjectCosts.vue        → costService.remove(costId)
   */
  async function deleteCusto(id: number): Promise<void> {
    return ApiService.apiCostsCustosDestroy(id);
  }

  /** Alias de deleteCusto — usado em ProjectCosts.vue. */
  const remove = deleteCusto;

  /**
   * Retorna dados resumidos do dashboard financeiro.
   *
   * Call-site: pages/custos/index.vue → getResumoCustos (desestruturado mas
   * não chamado na versão atual; mapeado para o endpoint mais próximo).
   */
  async function getResumoCustos(): Promise<Custo> {
    return ApiService.apiCostsCustosDashboardRetrieve();
  }

  return {
    // Listagem
    fetchCustos,
    listCustos,
    getByProject,
    // CRUD
    getCusto,
    createCusto,
    create,
    createCost,
    updateCusto,
    update,
    updateCost,
    patchCusto,
    deleteCusto,
    remove,
    // Relatório / resumo
    getResumoCustos,
  };
}
