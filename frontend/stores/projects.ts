// frontend/stores/projects.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
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

export const useProjectStore = defineStore('projects', {
  state: () => ({
    projects: [] as Projeto[],
    currentProject: null as Projeto | null,
    projectMetrics: null as MetricasProjeto | null,
    loading: false,
    error: null as string | null,
    pagination: {
      count: 0,
      currentPage: 1,
      itemsPerPage: 10,
      totalPages: 0
    }
  }),
  
  getters: {
    getProjectById: (state) => (id: number) => {
      return state.projects.find(project => project.id === id) || null;
    },
    filteredProjects: (state) => (filters: { status?: string, search?: string, priority?: string }) => {
      let filtered = [...state.projects];
      
      if (filters.status) {
        filtered = filtered.filter(project => project.status === filters.status);
      }
      
      if (filters.priority) {
        filtered = filtered.filter(project => project.prioridade === filters.priority);
      }
      
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        filtered = filtered.filter(project => 
          project.nome?.toLowerCase().includes(searchLower) || 
          project.descricao?.toLowerCase().includes(searchLower)
        );
      }
      
      return filtered;
    }
  },
  
  actions: {
    // Buscar lista de projetos com paginação e filtros
    async fetchProjects(params: { 
      page?: number, 
      ordering?: string,
      status?: string,
      search?: string
    } = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await ApiService.apiProjectsList(
          params.ordering || '-data_criacao',
          params.page || 1,
          params.search,
          params.status
        ) as PaginatedProjetoListList;
        
        this.projects = response.results || [];
        this.pagination.count = response.count || 0;
        this.pagination.currentPage = params.page || 1;
        this.pagination.totalPages = Math.ceil((response.count || 0) / this.pagination.itemsPerPage);
        
        return response;
      } catch (err: any) {
        this.error = err.message || 'Erro ao buscar projetos';
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Buscar um projeto específico pelo ID
    async fetchProjectById(id: number) {
      this.loading = true;
      this.error = null;
      
      try {
        const project = await ApiService.apiProjectsRetrieve(id);
        this.currentProject = project;
        
        // Atualiza o projeto na lista se já existir
        const index = this.projects.findIndex(p => p.id === id);
        if (index !== -1) {
          this.projects[index] = project;
        }
        
        return project;
      } catch (err: any) {
        this.error = err.message || `Erro ao buscar projeto com ID ${id}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Criar um novo projeto
    async createProject(projectData: ProjetoRequest) {
      this.loading = true;
      this.error = null;
      
      try {
        const newProject = await ApiService.apiProjectsCreate(projectData);
        this.projects.unshift(newProject); // Adiciona no início da lista
        return newProject;
      } catch (err: any) {
        this.error = err.message || 'Erro ao criar projeto';
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Atualizar um projeto existente
    async updateProject(id: number, projectData: ProjetoRequest) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedProject = await ApiService.apiProjectsUpdate(id, projectData);
        
        // Atualiza o projeto na lista
        const index = this.projects.findIndex(p => p.id === id);
        if (index !== -1) {
          this.projects[index] = updatedProject;
        }
        
        // Atualiza o projeto atual se estiver selecionado
        if (this.currentProject && this.currentProject.id === id) {
          this.currentProject = updatedProject;
        }
        
        return updatedProject;
      } catch (err: any) {
        this.error = err.message || `Erro ao atualizar projeto com ID ${id}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Atualizar parcialmente um projeto
    async patchProject(id: number, projectData: PatchedProjetoRequest) {
      this.loading = true;
      this.error = null;
      
      try {
        const updatedProject = await ApiService.apiProjectsPartialUpdate(id, projectData);
        
        // Atualiza o projeto na lista
        const index = this.projects.findIndex(p => p.id === id);
        if (index !== -1) {
          this.projects[index] = updatedProject;
        }
        
        // Atualiza o projeto atual se estiver selecionado
        if (this.currentProject && this.currentProject.id === id) {
          this.currentProject = updatedProject;
        }
        
        return updatedProject;
      } catch (err: any) {
        this.error = err.message || `Erro ao atualizar parcialmente projeto com ID ${id}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Excluir um projeto
    async deleteProject(id: number) {
      this.loading = true;
      this.error = null;
      
      try {
        await ApiService.apiProjectsDestroy(id);
        
        // Remove o projeto da lista
        this.projects = this.projects.filter(p => p.id !== id);
        
        // Limpa o projeto atual se for o mesmo
        if (this.currentProject && this.currentProject.id === id) {
          this.currentProject = null;
        }
        
        return true;
      } catch (err: any) {
        this.error = err.message || `Erro ao excluir projeto com ID ${id}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Buscar métricas de um projeto específico
    async fetchProjectMetrics(id: number) {
      this.loading = true;
      this.error = null;
      
      try {
        const metrics = await ProjetosService.metricasProjetoRetrieve(id);
        this.projectMetrics = metrics;
        return metrics;
      } catch (err: any) {
        this.error = err.message || `Erro ao buscar métricas do projeto com ID ${id}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Adicionar um membro ao projeto
    async addProjectMember(projectId: number, memberData: MembroProjetoRequest) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await ApiService.apiProjectsAdicionarMembroCreate(projectId, memberData);
        return response;
      } catch (err: any) {
        this.error = err.message || `Erro ao adicionar membro ao projeto com ID ${projectId}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Listar membros de um projeto
    async fetchProjectMembers(projectId: number, params: { page?: number, ordering?: string } = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await ApiService.apiProjectsListarMembrosList(
          projectId,
          params.ordering,
          params.page
        );
        return response;
      } catch (err: any) {
        this.error = err.message || `Erro ao buscar membros do projeto com ID ${projectId}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Remover um membro do projeto
    async removeProjectMember(projectId: number, userId: number) {
      this.loading = true;
      this.error = null;
      
      try {
        await ApiService.apiProjectsRemoverMembroDestroy(projectId, userId);
        return true;
      } catch (err: any) {
        this.error = err.message || `Erro ao remover membro do projeto com ID ${projectId}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Arquivar um projeto
    async archiveProject(projectId: number) {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await ApiService.apiProjectsArchiveCreate(projectId);
        
        // Atualiza o projeto na lista
        const index = this.projects.findIndex(p => p.id === projectId);
        if (index !== -1) {
          this.projects[index] = response;
        }
        
        // Atualiza o projeto atual se estiver selecionado
        if (this.currentProject && this.currentProject.id === projectId) {
          this.currentProject = response;
        }
        
        return response;
      } catch (err: any) {
        this.error = err.message || `Erro ao arquivar projeto com ID ${projectId}`;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    
    // Limpar o estado da store
    clearState() {
      this.projects = [];
      this.currentProject = null;
      this.projectMetrics = null;
      this.error = null;
      this.pagination = {
        count: 0,
        currentPage: 1,
        itemsPerPage: 10,
        totalPages: 0
      };
    }
  }
});
