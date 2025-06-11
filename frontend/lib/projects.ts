// frontend/lib/projects.ts
import { 
  ApiService, 
  ProjetosService, 
  type Projeto, 
  type ProjetoRequest, 
  type PatchedProjetoRequest,
  type PaginatedProjetoListList,
  type MetricasProjeto,
  type MembroProjetoRequest
} from '~/lib/api-client';

/**
 * Biblioteca de funções para gerenciar projetos
 */
export const projectsLib = {
  /**
   * Buscar lista de projetos com paginação e filtros
   */
  async fetchProjects(params: { 
    page?: number, 
    ordering?: string,
    status?: string,
    search?: string,
    prioridade?: string
  } = {}) {
    try {
      const response = await ApiService.apiProjectsList(
        params.ordering || '-data_criacao',
        params.page || 1,
        params.search,
        params.status
      ) as PaginatedProjetoListList;
      
      return {
        projects: response.results || [],
        pagination: {
          count: response.count || 0,
          currentPage: params.page || 1,
          totalPages: Math.ceil((response.count || 0) / 10)
        }
      };
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Buscar um projeto específico pelo ID
   */
  async fetchProjectById(id: number) {
    try {
      return await ApiService.apiProjectsRetrieve(id);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Criar um novo projeto
   */
  async createProject(projectData: ProjetoRequest) {
    try {
      return await ApiService.apiProjectsCreate(projectData);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Atualizar um projeto existente
   */
  async updateProject(id: number, projectData: ProjetoRequest) {
    try {
      return await ApiService.apiProjectsUpdate(id, projectData);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Atualizar parcialmente um projeto
   */
  async patchProject(id: number, projectData: PatchedProjetoRequest) {
    try {
      return await ApiService.apiProjectsPartialUpdate(id, projectData);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Excluir um projeto
   */
  async deleteProject(id: number) {
    try {
      await ApiService.apiProjectsDestroy(id);
      return true;
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Buscar métricas de um projeto específico
   */
  async fetchProjectMetrics(id: number) {
    try {
      return await ProjetosService.metricasProjetoRetrieve(id);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Adicionar um membro ao projeto
   */
  async addProjectMember(projectId: number, memberData: MembroProjetoRequest) {
    try {
      return await ApiService.apiProjectsAdicionarMembroCreate(projectId, memberData);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Listar membros de um projeto
   */
  async fetchProjectMembers(projectId: number, params: { page?: number, ordering?: string } = {}) {
    try {
      return await ApiService.apiProjectsListarMembrosList(
        projectId,
        params.ordering,
        params.page
      );
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Remover um membro do projeto
   */
  async removeProjectMember(projectId: number, userId: number) {
    try {
      await ApiService.apiProjectsRemoverMembroDestroy(projectId, userId);
      return true;
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Arquivar um projeto
   */
  async archiveProject(projectId: number) {
    try {
      return await ApiService.apiProjectsArchiveCreate(projectId);
    } catch (err: any) {
      throw err;
    }
  },
  
  /**
   * Formatar uma data para exibição
   */
  formatDate(dateString: string) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short' }).format(date);
  },
  
  /**
   * Obter label para status do projeto
   */
  getStatusLabel(status: string) {
    const statusMap = {
      'PLANEJADO': 'Planejado',
      'EM_ANDAMENTO': 'Em Andamento',
      'CONCLUIDO': 'Concluído',
      'CANCELADO': 'Cancelado',
      'SUSPENSO': 'Suspenso',
      'ARQUIVADO': 'Arquivado'
    };
    return statusMap[status] || status;
  },
  
  /**
   * Obter label para prioridade do projeto
   */
  getPriorityLabel(priority: string) {
    const priorityMap = {
      'BAIXA': 'Baixa',
      'MEDIA': 'Média',
      'ALTA': 'Alta',
      'CRITICA': 'Crítica'
    };
    return priorityMap[priority] || priority;
  }
};
