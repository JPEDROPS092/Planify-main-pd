/**
 * useRiskService
 *
 * Composable de serviço para riscos. Delega integralmente ao cliente gerado
 * em `~/lib/api-client` (ApiService). NÃO configura transporte — isso já é
 * feito pelo plugin `plugins/api.ts`.
 *
 * Métodos exportados (rastreados nos call-sites):
 *
 * | Método composable        | Gerado (ApiService)                   | Call-sites                                              |
 * |--------------------------|---------------------------------------|---------------------------------------------------------|
 * | listRiscos(params?)      | apiRisksRiscosList(...)               | index.vue, ProjectStatistics.vue, ProjectDashboard.vue  |
 * | getRisks(projectId)      | apiRisksRiscosList(projeto=id)        | risks.vue (reports)                                     |
 * | getByProject(projectId)  | apiRisksRiscosList(projeto=id)        | ProjectRisks.vue                                        |
 * | retrieveRisco(id)        | apiRisksRiscosRetrieve(id)            | index.vue                                               |
 * | createRisco(data)        | apiRisksRiscosCreate(data)            | index.vue, RiskForm.vue (via .createRisco)              |
 * | create(data)             | apiRisksRiscosCreate(data)            | ProjectRisks.vue (via .create)                          |
 * | updateRisco(id, data)    | apiRisksRiscosUpdate(id, data)        | index.vue, RiskForm.vue (via .updateRisco)              |
 * | update(id, data)         | apiRisksRiscosUpdate(id, data)        | ProjectRisks.vue (via .update)                          |
 * | destroyRisco(id)         | apiRisksRiscosDestroy(id)             | index.vue                                               |
 * | remove(id)               | apiRisksRiscosDestroy(id)             | ProjectRisks.vue (via .remove)                          |
 */

import { ApiService } from '~/lib/api-client';
import type {
  Risco,
  RiscoRequest,
  PatchedRiscoRequest,
  PaginatedRiscoListList,
  RiscoList,
} from '~/lib/api-client';

// ---------------------------------------------------------------------------
// Tipo do objeto de parâmetros aceito por listRiscos
// ---------------------------------------------------------------------------
export interface ListRiscosParams {
  impacto?: 'ALTO' | 'BAIXO' | 'MEDIO';
  ordering?: string;
  page?: number;
  probabilidade?: 'ALTA' | 'BAIXA' | 'MEDIA';
  projeto?: number;
  responsavelMitigacao?: number;
  search?: string;
  status?: 'ACEITO' | 'ELIMINADO' | 'EM_ANALISE' | 'IDENTIFICADO' | 'MITIGADO';
}

// ---------------------------------------------------------------------------
// Composable
// ---------------------------------------------------------------------------
export function useRiskService() {
  /**
   * Lista riscos com filtros opcionais.
   * Retorna a resposta paginada gerada (PaginatedRiscoListList).
   *
   * Usado em:
   *   - pages/riscos/index.vue           → listRiscos(params)
   *   - ProjectStatistics.vue            → riskService.listRiscos({ projeto })
   *   - ProjectDashboard.vue             → riskService.listRiscos({ projeto })
   */
  async function listRiscos(params: ListRiscosParams = {}): Promise<PaginatedRiscoListList> {
    return ApiService.apiRisksRiscosList(
      params.impacto,
      params.ordering,
      params.page,
      params.probabilidade,
      params.projeto,
      params.responsavelMitigacao,
      params.search,
      params.status,
    );
  }

  /**
   * Retorna os riscos de um projeto como array (resultados da primeira página).
   * Alias de listRiscos filtrando por projeto — compatível com call-sites que
   * esperam um array direto (risks.vue) ou { results } (ProjectRisks.vue).
   *
   * Usado em:
   *   - pages/projetos/[id]/reports/risks.vue  → getRisks(projectId) → array
   */
  async function getRisks(projectId: number): Promise<RiscoList[]> {
    const response = await ApiService.apiRisksRiscosList(
      undefined, // impacto
      undefined, // ordering
      undefined, // page
      undefined, // probabilidade
      projectId, // projeto
    );
    return response.results ?? [];
  }

  /**
   * Retorna os riscos de um projeto.
   * Retorna a resposta paginada completa para que o caller possa lidar com
   * `Array.isArray(result)` ou `result.results`.
   *
   * Usado em:
   *   - ProjectRisks.vue  → riskService.getByProject(projectId)
   */
  async function getByProject(projectId: number): Promise<PaginatedRiscoListList> {
    return ApiService.apiRisksRiscosList(
      undefined, // impacto
      undefined, // ordering
      undefined, // page
      undefined, // probabilidade
      projectId, // projeto
    );
  }

  /**
   * Recupera um risco pelo ID.
   *
   * Usado em:
   *   - pages/riscos/index.vue  → retrieveRisco(id)
   */
  async function retrieveRisco(id: number): Promise<Risco> {
    return ApiService.apiRisksRiscosRetrieve(id);
  }

  /**
   * Cria um novo risco.
   * Retorna `{ data: Risco }` para compatibilidade com RiskForm.vue que acessa
   * `response.data.id`.
   *
   * Usado em:
   *   - pages/riscos/index.vue         → createRisco(riskData)
   *   - RiskForm.vue                   → riskService.createRisco(riskData) → .data.id
   */
  async function createRisco(data: RiscoRequest): Promise<{ data: Risco }> {
    const risco = await ApiService.apiRisksRiscosCreate(data);
    return { data: risco };
  }

  /**
   * Alias de createRisco com assinatura directa.
   *
   * Usado em:
   *   - ProjectRisks.vue  → riskService.create(payload)
   */
  async function create(data: RiscoRequest): Promise<Risco> {
    return ApiService.apiRisksRiscosCreate(data);
  }

  /**
   * Atualiza um risco existente (PUT completo).
   * Retorna `{ data: Risco }` para compatibilidade com RiskForm.vue.
   *
   * Usado em:
   *   - pages/riscos/index.vue  → updateRisco(id, riskData)
   *   - RiskForm.vue            → riskService.updateRisco(id, riskData) → .data
   */
  async function updateRisco(id: number, data: RiscoRequest): Promise<{ data: Risco }> {
    const risco = await ApiService.apiRisksRiscosUpdate(id, data);
    return { data: risco };
  }

  /**
   * Alias de updateRisco com assinatura directa.
   *
   * Usado em:
   *   - ProjectRisks.vue  → riskService.update(id, formData)
   */
  async function update(id: number, data: RiscoRequest | PatchedRiscoRequest): Promise<Risco> {
    // Se o payload for parcial usamos PATCH, caso contrário PUT.
    // ProjectRisks.vue passa `RiskUpdate` (potencialmente parcial), por isso
    // delegamos ao PATCH que aceita campos opcionais.
    return ApiService.apiRisksRiscosPartialUpdate(id, data as PatchedRiscoRequest);
  }

  /**
   * Remove um risco pelo ID.
   *
   * Usado em:
   *   - pages/riscos/index.vue  → destroyRisco(id)
   */
  async function destroyRisco(id: number): Promise<void> {
    return ApiService.apiRisksRiscosDestroy(id);
  }

  /**
   * Alias de destroyRisco.
   *
   * Usado em:
   *   - ProjectRisks.vue  → riskService.remove(riskId)
   */
  async function remove(id: number): Promise<void> {
    return ApiService.apiRisksRiscosDestroy(id);
  }

  return {
    // Nomes usados no call-site index.vue (desestruturação implícita ou direta)
    listRiscos,
    retrieveRisco,
    createRisco,
    updateRisco,
    destroyRisco,

    // Nomes usados em risks.vue (reports)
    getRisks,

    // Nomes usados em ProjectRisks.vue
    getByProject,
    create,
    update,
    remove,
  };
}
