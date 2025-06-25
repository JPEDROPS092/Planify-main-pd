import type { ProjetoRequest, Projeto } from '~/api-types/api';

export const useProjectService = () => {
  const { projectsApi } = useApiClients();

  /**
   * Obtém a lista de projetos com filtros avançados
   * @param params Parâmetros de paginação e filtros
   */
  const getProjects = async (params: {
    page?: number;
    search?: string;
    status?: string;
    prioridade?: string;
    arquivado?: boolean;
    atrasado?: boolean;
    titulo?: string;
    descricao?: string;
    membro?: string;
    data_inicio_antes_after?: string;
    data_inicio_antes_before?: string;
    data_inicio_apos_after?: string;
    data_inicio_apos_before?: string;
    data_fim_antes_after?: string;
    data_fim_antes_before?: string;
    data_fim_apos_after?: string;
    data_fim_apos_before?: string;
    ordering?: string;
  } = {}) => {
    const response = await projectsApi.projectsList(params);
    return response.data;
  };

  /**
   * Obtém os projetos do usuário atual com filtros
   * @param params Parâmetros de filtros
   */
  const getMyProjects = async (params: {
    page?: number;
    search?: string;
    status?: string;
    prioridade?: string;
    arquivado?: boolean;
    atrasado?: boolean;
    titulo?: string;
    descricao?: string;
    membro?: string;
    data_inicio_antes_after?: string;
    data_inicio_antes_before?: string;
    data_inicio_apos_after?: string;
    data_inicio_apos_before?: string;
    data_fim_antes_after?: string;
    data_fim_antes_before?: string;
    data_fim_apos_after?: string;
    data_fim_apos_before?: string;
    ordering?: string;
  } = {}) => {
    const response = await projectsApi.projectsMyProjectsList(params);
    return response.data;
  };

  /**
   * Obtém um projeto específico pelo ID
   * @param id ID do projeto
   */
  const getProject = async (id: number) => {
    const response = await projectsApi.projectsRetrieve(id);
    return response.data;
  };

  /**
   * Cria um novo projeto
   * @param data Dados do projeto
   */
  const createProject = async (data: ProjetoRequest) => {
    const response = await projectsApi.projectsCreate({ projetoRequest: data });
    return response.data;
  };

  /**
   * Atualiza um projeto completamente
   * @param id ID do projeto
   * @param data Dados do projeto
   */
  const updateProject = async (id: number, data: ProjetoRequest) => {
    const response = await projectsApi.projectsUpdate(id, { projetoRequest: data });
    return response.data;
  };

  /**
   * Atualiza um projeto parcialmente
   * @param id ID do projeto
   * @param data Dados parciais do projeto
   */
  const patchProject = async (id: number, data: Partial<ProjetoRequest>) => {
    const response = await projectsApi.projectsPartialUpdate(id, { patchedProjetoRequest: data });
    return response.data;
  };

  /**
   * Exclui um projeto
   * @param id ID do projeto
   */
  const deleteProject = async (id: number) => {
    const response = await projectsApi.projectsDestroy(id);
    return response.data;
  };

  /**
   * Adiciona um membro ao projeto
   * @param id ID do projeto
   * @param data Dados do membro (usuario e papel)
   */
  const addProjectMember = async (id: number, data: { usuario: number; papel: string }) => {
    const response = await projectsApi.projectsAdicionarMembroCreate(id, data);
    return response.data;
  };

  /**
   * Remove um membro do projeto
   * @param id ID do projeto
   * @param membroId ID do membro a ser removido
   */
  const removeProjectMember = async (id: number, membroId: number) => {
    const response = await projectsApi.projectsRemoverMembroDestroy(id, { membroId });
    return response.data;
  };

  /**
   * Lista membros do projeto
   * @param id ID do projeto
   * @param params Parâmetros de filtros
   */
  const getProjectMembers = async (id: number, params: {
    page?: number;
    search?: string;
    ordering?: string;
  } = {}) => {
    const response = await projectsApi.projectsListarMembrosList(id, params);
    return response.data;
  };

  /**
   * Arquiva ou desarquiva um projeto
   * @param id ID do projeto
   * @param data Dados do projeto para arquivamento
   */
  const archiveProject = async (id: number, data: ProjetoRequest) => {
    const response = await projectsApi.projectsArchiveCreate(id, { projetoRequest: data });
    return response.data;
  };

  /**
   * Cria uma sprint no projeto
   * @param id ID do projeto
   * @param data Dados da sprint
   */
  const createProjectSprint = async (id: number, data: ProjetoRequest) => {
    const response = await projectsApi.projectsCriarSprintCreate(id, { projetoRequest: data });
    return response.data;
  };

  /**
   * Lista sprints do projeto
   * @param id ID do projeto
   */
  const getProjectSprints = async (id: number) => {
    const response = await projectsApi.projectsSprintsRetrieve(id);
    return response.data;
  };

  /**
   * Obtém dados do dashboard do projeto
   * @param projetoId ID do projeto
   */
  const getProjectDashboard = async (projetoId: number) => {
    const response = await projectsApi.projectsDashboardRetrieve(projetoId, { projetoId });
    return response.data;
  };

  /**
   * Obtém dados do kanban do projeto
   * @param projetoId ID do projeto
   */
  const getProjectKanban = async (projetoId: number) => {
    const response = await projectsApi.projectsKanbanRetrieve(projetoId);
    return response.data;
  };

  /**
   * Atualiza o kanban do projeto
   * @param projetoId ID do projeto
   * @param data Dados do kanban
   */
  const updateProjectKanban = async (projetoId: number, data: any) => {
    const response = await projectsApi.projectsKanbanPartialUpdate(projetoId, data);
    return response.data;
  };

  /**
   * Obtém dados do gantt do projeto
   * @param projetoId ID do projeto
   */
  const getProjectGantt = async (projetoId: number) => {
    const response = await projectsApi.projectsGanttRetrieve(projetoId, { projetoId });
    return response.data;
  };

  /**
   * Cria uma tarefa no projeto
   * @param projetoId ID do projeto
   * @param data Dados da tarefa
   */
  const createProjectTask = async (projetoId: number, data: {
    titulo: string;
    descricao?: string;
    data_inicio?: string;
    data_fim?: string;
    prioridade?: string;
    status?: string;
    responsaveis?: number[];
  }) => {
    const response = await projectsApi.projectsTarefasCriarCreate(projetoId, { projetoId, ...data });
    return response.data;
  };

  /**
   * Cria múltiplas tarefas no projeto
   * @param projetoId ID do projeto
   * @param data Dados das tarefas
   */
  const createMultipleProjectTasks = async (projetoId: number, data: {
    tarefas: Array<{
      titulo: string;
      descricao?: string;
      data_inicio?: string;
      data_fim?: string;
      prioridade?: string;
      status?: string;
      responsaveis?: number[];
    }>;
  }) => {
    const response = await projectsApi.projectsTarefasCriarMultiplasCreate(projetoId, { projetoId, ...data });
    return response.data;
  };

  /**
   * Exporta dados do projeto
   * @param projetoId ID do projeto
   * @param options Opções de exportação
   */
  const exportProject = async (projetoId: number, options: {
    format?: 'csv' | 'json';
    include_project?: boolean;
    include_tasks?: boolean;
    include_team?: boolean;
    include_risks?: boolean;
    include_costs?: boolean;
  } = {}) => {
    const response = await projectsApi.projectsExportarRetrieve(projetoId, {
      format: options.format || 'csv',
      includeProject: options.include_project !== false,
      includeTasks: options.include_tasks !== false,
      includeTeam: options.include_team || false,
      includeRisks: options.include_risks || false,
      includeCosts: options.include_costs || false,
    });
    return response.data;
  };

  /**
   * Obtém métricas detalhadas do projeto
   * @param id ID do projeto
   */
  const getProjectMetrics = async (id: number) => {
    const response = await projectsApi.projectsMetricsRetrieve(id);
    return response.data;
  };

  /**
   * Obtém histórico de status do projeto
   * @param id ID do projeto
   */
  const getProjectStatusHistory = async (id: number) => {
    const response = await projectsApi.projectsHistoricoStatusRetrieve(id);
    return response.data;
  };

  /**
   * Exporta dados básicos do projeto (método alternativo)
   * @param id ID do projeto
   */
  const exportProjectData = async (id: number) => {
    const response = await projectsApi.projectsExportProjectRetrieve(id);
    return response.data;
  };

  return {
    // Operações básicas CRUD
    getProjects,
    getMyProjects,
    getProject,
    createProject,
    updateProject,
    patchProject,
    deleteProject,
    
    // Gerenciamento de membros
    addProjectMember,
    removeProjectMember,
    getProjectMembers,
    
    // Operações especiais
    archiveProject,
    createProjectSprint,
    getProjectSprints,
    
    // Visualizações
    getProjectDashboard,
    getProjectKanban,
    updateProjectKanban,
    getProjectGantt,
    
    // Tarefas
    createProjectTask,
    createMultipleProjectTasks,
    
    // Relatórios e métricas
    exportProject,
    exportProjectData,
    getProjectMetrics,
    getProjectStatusHistory,
  };
};
