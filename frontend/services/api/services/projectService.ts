/**
 * Composable de serviço de projetos.
 *
 * Delega ao cliente gerado em `~/lib/api-client` (ApiService / ProjetosService).
 * Exporta `useProjectService` como ponto único de acesso nos call-sites.
 *
 * Métodos cobertos:
 *   fetchProjects        → ApiService.apiProjectsList
 *   listProjetos         → ApiService.apiProjectsList  (alias direto)
 *   getProject / getById → ApiService.apiProjectsRetrieve
 *   retrieveProjeto      → ApiService.apiProjectsRetrieve  (alias)
 *   createProjeto        → ApiService.apiProjectsCreate
 *   updateProject        → ApiService.apiProjectsUpdate
 *   updateProjeto        → ApiService.apiProjectsUpdate  (alias)
 *   patchProjeto         → ApiService.apiProjectsPartialUpdate
 *   deleteProject        → ApiService.apiProjectsDestroy
 *   archiveProject       → ApiService.apiProjectsArchiveCreate
 *   adicionarMembro      → ApiService.apiProjectsAdicionarMembroCreate
 *   listarMembros        → ApiService.apiProjectsListarMembrosList
 *   removerMembro        → ApiService.apiProjectsRemoverMembroDestroy
 *   getMetricas          → ProjetosService.metricasProjetoRetrieve
 *   listSprints          → ApiService.apiProjectsSprintsRetrieve
 *   createSprint         → ApiService.apiProjectsCriarSprintCreate
 *
 * NÃO MAPEADOS (sem endpoint real correspondente no cliente gerado):
 *   updateSprint   — backend não expõe PUT/PATCH /api/sprints/{id}/; mapeado
 *                    para apiProjectsCriarSprintCreate com aviso em comentário.
 *   destroySprint  — backend não expõe DELETE /api/sprints/{id}/; stub que
 *                    lança NotImplemented para não quebrar compilação.
 */
import {
  ApiService,
  ProjetosService,
  type Projeto,
  type ProjetoRequest,
  type PatchedProjetoRequest,
  type PaginatedProjetoListList,
  type PaginatedMembroProjetoList,
  type MembroProjeto,
  type MembroProjetoRequest,
  type MetricasProjeto,
} from '~/lib/api-client';

// ─────────────────────────────────────────────────────────────────────────────
// Tipos auxiliares usados nos call-sites
// ─────────────────────────────────────────────────────────────────────────────

export interface FetchProjectsParams {
  page?: number;
  ordering?: string;
  status?: string;
  search?: string;
  arquivado?: boolean;
  membro?: string;
  prioridade?: string;
  titulo?: string;
}

export interface ListMembrosParams {
  ordering?: string;
  page?: number;
  membro?: string;
  search?: string;
  status?: string;
}

export interface ListSprintsParams {
  /** ID do projeto — usado nos call-sites como `{ projeto: projectId }` */
  projeto?: number | string;
  ordering?: string;
  page?: number;
}

// ─────────────────────────────────────────────────────────────────────────────
// Composable
// ─────────────────────────────────────────────────────────────────────────────

export function useProjectService() {
  // ── Lista de projetos ───────────────────────────────────────────────────────

  /**
   * Busca lista paginada de projetos.
   * Usado em: stores/projects.ts, pages/custos/index.vue,
   *           pages/comunicacoes/index.vue.
   */
  function fetchProjects(params: FetchProjectsParams = {}): Promise<PaginatedProjetoListList> {
    return ApiService.apiProjectsList(
      params.arquivado,
      /* atrasado */ undefined,
      /* dataFimAntesAfter */ undefined,
      /* dataFimAntesBefore */ undefined,
      /* dataFimAposAfter */ undefined,
      /* dataFimAposBefore */ undefined,
      /* dataInicioAntesAfter */ undefined,
      /* dataInicioAntesBefore */ undefined,
      /* dataInicioAposAfter */ undefined,
      /* dataInicioAposBefore */ undefined,
      /* descricao */ undefined,
      params.membro,
      params.ordering,
      params.page,
      params.prioridade,
      params.search,
      params.status,
      params.titulo,
    );
  }

  /**
   * Alias de `fetchProjects` para call-sites que o importam pelo nome
   * `listProjetos` (pages/tarefas, pages/documentos, pages/riscos).
   */
  function listProjetos(params: FetchProjectsParams = {}): Promise<PaginatedProjetoListList> {
    return fetchProjects(params);
  }

  // ── Projeto individual ──────────────────────────────────────────────────────

  /**
   * Obtém detalhes de um projeto por ID.
   * Usado como: `getProject(id)` — pages/projetos/[id]/index.vue,
   *             pages/projetos/[id]/settings/index.vue, etc.
   * O ID pode chegar como string (route.params) ou number.
   */
  function getProject(id: number | string): Promise<Projeto> {
    return ApiService.apiProjectsRetrieve(Number(id));
  }

  /**
   * Alias de `getProject` — usado em: components/business/project/resources/ProjectCosts.vue.
   */
  function getById(id: number | string): Promise<Projeto> {
    return getProject(id);
  }

  /**
   * Alias de `getProject` — usado em: pages/projetos/[id].vue,
   * components/business/project/management/ProjectOverview.vue,
   * components/business/project/management/ProjectStatistics.vue,
   * components/business/dashboard/ProjectDashboard.vue, gantt.vue, kanban.vue.
   */
  function retrieveProjeto(id: number | string): Promise<Projeto> {
    return getProject(id);
  }

  // ── Criar projeto ───────────────────────────────────────────────────────────

  /**
   * Cria um novo projeto.
   * Usado em: pages/projetos/novo.vue, components/shared/forms/project/ProjectForm.vue.
   */
  function createProjeto(data: ProjetoRequest): Promise<Projeto> {
    return ApiService.apiProjectsCreate(data);
  }

  // ── Atualizar projeto ───────────────────────────────────────────────────────

  /**
   * Atualiza todos os campos de um projeto (PUT).
   * Usado como `updateProject(id, data)` em:
   *   pages/projetos/[id]/settings/index.vue.
   */
  function updateProject(id: number | string, data: ProjetoRequest): Promise<Projeto> {
    return ApiService.apiProjectsUpdate(Number(id), data);
  }

  /**
   * Alias de `updateProject` — usado em:
   *   components/shared/forms/project/ProjectForm.vue (`updateProjeto`).
   */
  function updateProjeto(id: number | string, data: ProjetoRequest): Promise<Projeto> {
    return updateProject(id, data);
  }

  /**
   * Atualiza parcialmente um projeto (PATCH).
   */
  function patchProjeto(id: number | string, data: PatchedProjetoRequest): Promise<Projeto> {
    return ApiService.apiProjectsPartialUpdate(Number(id), data);
  }

  // ── Excluir projeto ─────────────────────────────────────────────────────────

  /**
   * Remove um projeto.
   */
  function deleteProject(id: number | string): Promise<void> {
    return ApiService.apiProjectsDestroy(Number(id));
  }

  // ── Arquivar projeto ────────────────────────────────────────────────────────

  /**
   * Arquiva ou desarquiva um projeto.
   * Usado em: stores/projects.ts (`archiveProject`).
   * O endpoint exige um body ProjetoRequest; passar objeto vazio é suficiente
   * para o toggle no backend.
   */
  function archiveProject(id: number | string, data: ProjetoRequest = {} as ProjetoRequest): Promise<Projeto> {
    return ApiService.apiProjectsArchiveCreate(Number(id), data);
  }

  // ── Membros do projeto ──────────────────────────────────────────────────────

  /**
   * Adiciona um membro ao projeto.
   * Usado em: stores/projects.ts (`addProjectMember`).
   */
  function adicionarMembro(id: number | string, data: MembroProjetoRequest): Promise<MembroProjeto> {
    return ApiService.apiProjectsAdicionarMembroCreate(Number(id), data);
  }

  /**
   * Lista membros do projeto.
   * Usado em: stores/projects.ts (`fetchProjectMembers`).
   */
  function listarMembros(
    id: number | string,
    params: ListMembrosParams = {},
  ): Promise<PaginatedMembroProjetoList> {
    return ApiService.apiProjectsListarMembrosList(
      Number(id),
      /* arquivado */ undefined,
      /* atrasado */ undefined,
      /* dataFimAntesAfter */ undefined,
      /* dataFimAntesBefore */ undefined,
      /* dataFimAposAfter */ undefined,
      /* dataFimAposBefore */ undefined,
      /* dataInicioAntesAfter */ undefined,
      /* dataInicioAntesBefore */ undefined,
      /* dataInicioAposAfter */ undefined,
      /* dataInicioAposBefore */ undefined,
      /* descricao */ undefined,
      params.membro,
      params.ordering,
      params.page,
      /* prioridade */ undefined,
      params.search,
      params.status,
      /* titulo */ undefined,
    );
  }

  /**
   * Remove um membro do projeto pelo ID do usuário.
   * Usado em: stores/projects.ts (`removeProjectMember`).
   */
  function removerMembro(projectId: number | string, membroId: number): Promise<void> {
    return ApiService.apiProjectsRemoverMembroDestroy(Number(projectId), membroId);
  }

  // ── Métricas ────────────────────────────────────────────────────────────────

  /**
   * Busca métricas detalhadas do projeto.
   * Usado em: stores/projects.ts (`fetchProjectMetrics`).
   */
  function getMetricas(id: number | string): Promise<MetricasProjeto> {
    return ProjetosService.metricasProjetoRetrieve(Number(id));
  }

  // ── Sprints ─────────────────────────────────────────────────────────────────

  /**
   * Lista sprints do projeto.
   * Usado em: components/business/project/planning/SprintManagement.vue
   *   → `projectService.listSprints({ projeto: props.projectId, ordering: 'start_date' })`
   *
   * O endpoint gerado é GET /api/projects/{id}/sprints/ e retorna `Projeto`
   * (envelope contendo lista de sprints). O call-site acessa `.results`.
   *
   * Como o call-site passa `{ projeto: id }` (não o id como argumento posicional),
   * aceitamos `params.projeto` como o ID do projeto.
   */
  function listSprints(params: ListSprintsParams = {}): Promise<any> {
    const projectId = Number(params.projeto);
    return ApiService.apiProjectsSprintsRetrieve(projectId);
  }

  /**
   * Cria uma nova sprint no projeto.
   * Usado em: SprintManagement.vue → `projectService.createSprint({ nome, descricao, data_inicio, data_fim, projeto })`
   *
   * O endpoint POST /api/projects/{id}/criar_sprint/ extrai o projeto do path.
   * O `projeto` dentro do body é redundante mas seguimos a convenção.
   */
  function createSprint(data: ProjetoRequest & { projeto?: number | string }): Promise<Projeto> {
    const projectId = Number(data.projeto);
    return ApiService.apiProjectsCriarSprintCreate(projectId, data as ProjetoRequest);
  }

  /**
   * Atualiza uma sprint existente.
   *
   * NÃO MAPEADO: o cliente gerado não expõe um endpoint dedicado
   * PUT/PATCH /api/sprints/{id}/. Este método é chamado em SprintManagement.vue
   * mas não tem correspondência direta no backend gerado.
   *
   * Estratégia conservadora: lança erro informativo em runtime para que o
   * desenvolvedor perceba a ausência do endpoint sem silenciar a falha.
   */
  function updateSprint(sprintId: number | string, _data: Record<string, any>): Promise<never> {
    return Promise.reject(
      new Error(
        `[useProjectService] updateSprint(${sprintId}): endpoint PUT/PATCH /api/sprints/{id}/ não está disponível no cliente gerado. ` +
        'Adicione o endpoint ao backend ou use apiProjectsCriarSprintCreate para recriar a sprint.',
      ),
    );
  }

  /**
   * Exclui uma sprint.
   *
   * NÃO MAPEADO: o cliente gerado não expõe DELETE /api/sprints/{id}/.
   * Mesmo tratamento conservador de `updateSprint`.
   */
  function destroySprint(sprintId: number | string): Promise<never> {
    return Promise.reject(
      new Error(
        `[useProjectService] destroySprint(${sprintId}): endpoint DELETE /api/sprints/{id}/ não está disponível no cliente gerado.`,
      ),
    );
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // Retorno público
  // ─────────────────────────────────────────────────────────────────────────────

  return {
    // lista
    fetchProjects,
    listProjetos,

    // individual
    getProject,
    getById,
    retrieveProjeto,

    // CRUD
    createProjeto,
    updateProject,
    updateProjeto,
    patchProjeto,
    deleteProject,

    // arquivar
    archiveProject,

    // membros
    adicionarMembro,
    listarMembros,
    removerMembro,

    // métricas
    getMetricas,

    // sprints
    listSprints,
    createSprint,
    updateSprint,   // não-mapeado — rejeita com erro informativo
    destroySprint,  // não-mapeado — rejeita com erro informativo
  };
}
