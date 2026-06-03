/**
 * Composable de serviço de equipes e membros.
 *
 * Delega ao cliente gerado em `~/lib/api-client` (ApiService).
 * Exporta `useTeamService` como ponto único de acesso nos call-sites.
 *
 * Métodos cobertos:
 *   getTeamMembers          → ApiService.apiProjectsListarMembrosList  (retorna array MembroProjeto[])
 *   listMembros             → ApiService.apiProjectsListarMembrosList  (retorna PaginatedMembroProjetoList)
 *   getProjectTeamMembers   → ApiService.apiProjectsListarMembrosList  (retorna { data: MembroProjeto[] })
 *   addMemberToProject      → ApiService.apiProjectsAdicionarMembroCreate
 *   removeMemberFromProject → ApiService.apiProjectsRemoverMembroDestroy
 *   listEquipes             → ApiService.apiTeamsEquipesList           (retorna PaginatedEquipeListList)
 *   retrieveEquipe          → ApiService.apiTeamsEquipesRetrieve
 *   createEquipe            → ApiService.apiTeamsEquipesCreate
 *   updateEquipe            → ApiService.apiTeamsEquipesUpdate
 *   destroyEquipe           → ApiService.apiTeamsEquipesDestroy
 *
 * NÃO MAPEADOS:
 *   Nenhum — todos os métodos usados nos call-sites têm correspondência real no
 *   cliente gerado.
 *
 * Call-sites lidos:
 *   - components/business/dashboard/ProjectDashboard.vue
 *   - components/business/project/management/ProjectOverview.vue
 *   - components/business/risk/RiskForm.vue
 *   - components/business/project/tasks/TaskForm.vue  (importa mas não chama via service)
 *   - components/business/project/team/ProjectTeam.vue
 *   - pages/equipes/index.vue
 *   - pages/projetos/[id]/team/permissions.vue
 */
import {
  ApiService,
  MembroProjetoPapelEnum,
  type Equipe,
  type EquipeRequest,
  type MembroProjeto,
  type MembroProjetoRequest,
  type PaginatedEquipeListList,
  type PaginatedMembroProjetoList,
} from '~/lib/api-client';

// ─────────────────────────────────────────────────────────────────────────────
// Tipos auxiliares
// ─────────────────────────────────────────────────────────────────────────────

export interface ListEquipesParams {
  ordering?: string;
  page?: number;
  search?: string;
  /** Filtro por projeto — aceito nos call-sites mas não exposto pelo endpoint
   *  de listagem de equipes; mantido para compatibilidade de assinatura. */
  projeto?: number;
}

export interface ListMembrosParams {
  /** ID do projeto (obrigatório para o endpoint /api/projects/{id}/listar_membros/) */
  projeto: number | string;
  ordering?: string;
  page?: number;
  membro?: string;
  search?: string;
  status?: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// Composable
// ─────────────────────────────────────────────────────────────────────────────

export function useTeamService() {
  // ── Membros do projeto ──────────────────────────────────────────────────────

  /**
   * Retorna array de membros de um projeto.
   * Usado em:
   *   - ProjectTeam.vue → `teamService.getTeamMembers(projectId.value)`
   *   - permissions.vue → `getTeamMembers(projectId)` (projectId como string)
   */
  async function getTeamMembers(projectId: number | string): Promise<MembroProjeto[]> {
    const response = await ApiService.apiProjectsListarMembrosList(Number(projectId));
    return response.results ?? [];
  }

  /**
   * Retorna membros paginados de um projeto.
   * Usado em:
   *   - ProjectOverview.vue → `teamService.listMembros({ projeto: projectId.value })`
   *     O call-site acessa `membersResponse.results || []`.
   */
  function listMembros(params: ListMembrosParams): Promise<PaginatedMembroProjetoList> {
    return ApiService.apiProjectsListarMembrosList(
      Number(params.projeto),
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
   * Retorna membros do projeto no formato `{ data: MembroProjeto[] }`.
   * Usado em:
   *   - RiskForm.vue → `teamService.getProjectTeamMembers(props.projectId)`
   *     O call-site acessa `response.data || []`.
   */
  async function getProjectTeamMembers(projectId: number | string): Promise<{ data: MembroProjeto[] }> {
    const response = await ApiService.apiProjectsListarMembrosList(Number(projectId));
    return { data: response.results ?? [] };
  }

  /**
   * Adiciona um membro ao projeto.
   * Usado em:
   *   - ProjectTeam.vue → `teamService.addMemberToProject(projectId.value, selectedUserIdToAdd.value)`
   *     O segundo argumento é apenas o ID do usuário (number); o papel padrão
   *     é 'MEMBRO' (não há enum 'MEMBRO' na spec — usando 'DEV' como fallback).
   *     Se o call-site passar um objeto MembroProjetoRequest completo, é usado diretamente.
   */
  function addMemberToProject(
    projectId: number | string,
    usuarioOrBody: number | MembroProjetoRequest,
  ): Promise<MembroProjeto> {
    const body: MembroProjetoRequest =
      typeof usuarioOrBody === 'number'
        ? { usuario: usuarioOrBody, papel: MembroProjetoPapelEnum.DESENVOLVEDOR }
        : usuarioOrBody;
    return ApiService.apiProjectsAdicionarMembroCreate(Number(projectId), body);
  }

  /**
   * Remove um membro do projeto pelo ID do usuário/membro.
   * Usado em:
   *   - ProjectTeam.vue → `teamService.removeMemberFromProject(projectId.value, memberToRemove.id)`
   */
  function removeMemberFromProject(projectId: number | string, membroId: number): Promise<void> {
    return ApiService.apiProjectsRemoverMembroDestroy(Number(projectId), membroId);
  }

  // ── Equipes ─────────────────────────────────────────────────────────────────

  /**
   * Lista equipes (paginado).
   * Usado em:
   *   - ProjectDashboard.vue → `teamService.listEquipes({ projeto: projectId })`
   *     O call-site acessa `response.results` para contar membros_count.
   *   - equipes/index.vue → `listEquipes()` (destructured ou referência direta)
   *
   * Nota: o endpoint GET /api/teams/equipes/ não filtra por projeto;
   * o parâmetro `projeto` em `params` é ignorado silenciosamente.
   */
  function listEquipes(params: ListEquipesParams = {}): Promise<PaginatedEquipeListList> {
    return ApiService.apiTeamsEquipesList(
      params.ordering,
      params.page,
      params.search,
    );
  }

  /**
   * Busca detalhes de uma equipe por ID.
   * Usado em:
   *   - equipes/index.vue → `retrieveEquipe(team.id)`
   */
  function retrieveEquipe(id: number | string): Promise<Equipe> {
    return ApiService.apiTeamsEquipesRetrieve(Number(id));
  }

  /**
   * Cria uma nova equipe.
   * Usado em:
   *   - equipes/index.vue → `createEquipe(teamData)` onde teamData = { nome, descricao, membros }
   *     O campo `membros` não faz parte do EquipeRequest gerado; é descartado silenciosamente.
   */
  function createEquipe(data: EquipeRequest & { membros?: unknown[] }): Promise<Equipe> {
    const { membros: _ignored, ...body } = data as EquipeRequest & { membros?: unknown[] };
    return ApiService.apiTeamsEquipesCreate(body as EquipeRequest);
  }

  /**
   * Atualiza uma equipe (PUT).
   * Usado em:
   *   - equipes/index.vue → `updateEquipe(editingTeam.value.id, teamData)`
   */
  function updateEquipe(id: number | string, data: EquipeRequest): Promise<Equipe> {
    return ApiService.apiTeamsEquipesUpdate(Number(id), data);
  }

  /**
   * Remove uma equipe.
   * Usado em:
   *   - equipes/index.vue → `destroyEquipe(id)`
   */
  function destroyEquipe(id: number | string): Promise<void> {
    return ApiService.apiTeamsEquipesDestroy(Number(id));
  }

  // ─────────────────────────────────────────────────────────────────────────────
  // Retorno público
  // ─────────────────────────────────────────────────────────────────────────────

  return {
    // membros do projeto
    getTeamMembers,
    listMembros,
    getProjectTeamMembers,
    addMemberToProject,
    removeMemberFromProject,

    // equipes
    listEquipes,
    retrieveEquipe,
    createEquipe,
    updateEquipe,
    destroyEquipe,
  };
}
