import { defineStore } from 'pinia';

interface Project {
  id: number;
  nome: string;
  descricao?: string;
  data_inicio: string;
  data_fim?: string;
  status: string;
  responsavel: number | object;
  criado_por?: number | object;
  [key: string]: any;
}

interface ProjectState {
  projects: Project[];
  projectDetails: Record<number, Project>;
  lastFetch: number;
  lastDetailsFetch: Record<number, number>;
  isFetching: boolean;
  cacheTTL: number; // Tempo de vida do cache em milissegundos
}

export const useProjectStore = defineStore('project', {
  state: (): ProjectState => ({
    projects: [],
    projectDetails: {},
    lastFetch: 0,
    lastDetailsFetch: {},
    isFetching: false,
    cacheTTL: 5 * 60 * 1000, // 5 minutos em milissegundos
  }),

  getters: {
    /**
     * Verifica se o cache da lista de projetos é válido
     */
    isProjectsCacheValid(): boolean {
      return (
        this.projects.length > 0 &&
        Date.now() - this.lastFetch < this.cacheTTL
      );
    },

    /**
     * Verifica se o cache de um projeto específico é válido
     */
    isProjectDetailCacheValid(): (id: number) => boolean {
      return (id: number) => {
        return (
          !!this.projectDetails[id] &&
          !!this.lastDetailsFetch[id] &&
          Date.now() - this.lastDetailsFetch[id] < this.cacheTTL
        );
      };
    },
  },

  actions: {
    /**
     * Adiciona ou atualiza a lista de projetos no cache
     */
    setProjects(projects: Project[]) {
      this.projects = projects;
      this.lastFetch = Date.now();
    },

    /**
     * Adiciona ou atualiza um projeto específico no cache
     */
    setProjectDetail(project: Project) {
      if (!project || !project.id) return;
      
      this.projectDetails[project.id] = { ...project };
      this.lastDetailsFetch[project.id] = Date.now();
      
      // Atualiza também na lista se existir
      const index = this.projects.findIndex(p => p.id === project.id);
      if (index !== -1) {
        this.projects[index] = { ...project };
      }
    },

    /**
     * Remove um projeto do cache
     */
    removeProject(id: number) {
      if (!id) return;
      
      // Remove da lista
      this.projects = this.projects.filter(p => p.id !== id);
      
      // Remove dos detalhes
      if (this.projectDetails[id]) {
        delete this.projectDetails[id];
      }
      
      // Remove do registro de timestamp
      if (this.lastDetailsFetch[id]) {
        delete this.lastDetailsFetch[id];
      }
    },

    /**
     * Limpa todo o cache de projetos
     */
    clearCache() {
      this.projects = [];
      this.projectDetails = {};
      this.lastFetch = 0;
      this.lastDetailsFetch = {};
    },

    /**
     * Atualiza o status de carregamento
     */
    setFetching(status: boolean) {
      this.isFetching = status;
    },
  },
});
