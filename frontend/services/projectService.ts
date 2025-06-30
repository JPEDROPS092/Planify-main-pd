// Service para gerenciar projetos usando a API Fetch do Nuxt
export const useProjectService = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // Buscar projetos com filtros
  const getProjects = async (filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}projects/`, {
        params: filters,
      });
    } catch (error) {
      console.error("Erro ao buscar projetos:", error);
      throw error;
    }
  };

  // Buscar projeto específico
  const getProjectById = async (id: number) => {
    try {
      return await $fetch(`${apiBase}projects/${id}/`);
    } catch (error) {
      console.error("Erro ao buscar projeto:", error);
      throw error;
    }
  };

  // Criar novo projeto
  const createProject = async (projectData: any) => {
    try {
      return await $fetch(`${apiBase}projects/`, {
        method: "POST",
        body: projectData,
      });
    } catch (error) {
      console.error("Erro ao criar projeto:", error);
      throw error;
    }
  };

  // Atualizar projeto
  const updateProject = async (id: number, projectData: any) => {
    try {
      return await $fetch(`${apiBase}projects/${id}/`, {
        method: "PUT",
        body: projectData,
      });
    } catch (error) {
      console.error("Erro ao atualizar projeto:", error);
      throw error;
    }
  };

  // Atualizar parcialmente projeto
  const partialUpdateProject = async (id: number, projectData: any) => {
    try {
      return await $fetch(`${apiBase}projects/${id}/`, {
        method: "PATCH",
        body: projectData,
      });
    } catch (error) {
      console.error("Erro ao atualizar projeto:", error);
      throw error;
    }
  };

  // Deletar projeto
  const deleteProject = async (id: number) => {
    try {
      return await $fetch(`${apiBase}projects/${id}/`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao deletar projeto:", error);
      throw error;
    }
  };

  // Buscar estatísticas do projeto
  const getProjectStats = async (id: number) => {
    try {
      return await $fetch(`${apiBase}projects/${id}/stats/`);
    } catch (error) {
      console.error("Erro ao buscar estatísticas do projeto:", error);
      throw error;
    }
  };

  // Buscar membros do projeto
  const getProjectMembers = async (id: number) => {
    try {
      return await $fetch(`${apiBase}projects/${id}/members/`);
    } catch (error) {
      console.error("Erro ao buscar membros do projeto:", error);
      throw error;
    }
  };

  return {
    getProjects,
    getProjectById,
    createProject,
    updateProject,
    partialUpdateProject,
    deleteProject,
    getProjectStats,
    getProjectMembers,
  };
};
