/**
 * Serviço de projetos
 * Refatorado para usar o novo sistema de API
 * Mantém cache via Pinia e suporte para feedback visual
 */
import { ref } from 'vue';
import { useApiService } from '~/stores/composables/useApiService';
import { useAuth } from '~/stores/composables/useAuth';
import * as projectsApi from '../services/api/endpoints/projects';
// Importando defineStore para criar a store localmente
import { defineStore } from 'pinia';

// Definindo store de projetos localmente para evitar dependência externa
const useProjectStore = defineStore('projects', () => {
  const projects = ref([]);
  const isLoading = ref(false);

  function setProjects(newProjects) {
    projects.value = newProjects;
  }

  function addProject(project) {
    projects.value.push(project);
  }

  function updateProjectInStore(id, updatedProject) {
    const index = projects.value.findIndex(p => p.id === id);
    if (index !== -1) {
      projects.value[index] = { ...projects.value[index], ...updatedProject };
    }
  }

  function removeProject(id) {
    projects.value = projects.value.filter(p => p.id !== id);
  }

  return {
    projects,
    isLoading,
    setProjects,
    addProject,
    updateProjectInStore,
    removeProject
  };
});

// Composable para gerenciamento de projetos
export const useProjectService = () => {
  const { user, isAuthenticated } = useAuth();
  const { handleApiError, withLoading } = useApiService();
  const projectStore = useProjectStore();

  const projects = ref([]);
  const currentProject = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  // Função para buscar todos os projetos
  const fetchProjects = async (params = {}, useCache = true) => {
    // Verificar se podemos usar o cache
    if (useCache && !params?.page && !params?.search && projectStore.isProjectsCacheValid) {
      return {
        results: projectStore.projects,
        count: projectStore.projects.length,
        data: projectStore.projects
      };
    }

    isLoading.value = true;
    error.value = null;
    projectStore.setFetching(true);

    try {
      // Se o usuário estiver logado e não houver filtro de gerente, adicionar o usuário como gerente
      if (user.value && !params.owner_id && isAuthenticated.value) {
        params = { ...params, owner_id: user.value.id };
      }

      const response = await projectsApi.listProjects(params);

      // Armazenar no cache apenas se não houver filtros específicos
      if (!params?.search && !params?.page) {
        projectStore.setProjects(response.results || []);
      }

      projects.value = response.results;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
      projectStore.setFetching(false);
    }
  };

  // Função para buscar um projeto específico
  const fetchProject = async (id, useCache = true) => {
    // Verificar se podemos usar o cache
    if (useCache && projectStore.isProjectDetailCacheValid(id)) {
      const cachedProject = projectStore.projectDetails[id];
      currentProject.value = cachedProject;
      return cachedProject;
    }

    isLoading.value = true;
    error.value = null;
    projectStore.setFetching(true);

    try {
      const project = await projectsApi.retrieveProject(id);
      currentProject.value = project;

      // Armazenar no cache
      projectStore.setProjectDetail(project);

      return project;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
      projectStore.setFetching(false);
    }
  };

  // Função para criar um novo projeto
  const createProject = async (projectData) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Associar o usuário logado como gerente se não for especificado
      if (!projectData.owner_id && user.value) {
        projectData.owner_id = user.value.id;
      }

      const newProject = await withLoading(async () => {
        return await projectsApi.createProject(projectData);
      }, {
        loadingMessage: 'Criando projeto...',
        successMessage: 'Projeto criado com sucesso!'
      });

      // Atualizar o cache
      projectStore.setProjectDetail(newProject);
      projectStore.clearCache(); // Limpar o cache da lista para forçar uma nova busca

      return newProject;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Função para atualizar um projeto
  const updateProject = async (id, projectData) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Verificar permissão - apenas o gerente pode atualizar o projeto
      const canEdit = await isProjectManager(id);
      if (!canEdit) {
        throw new Error('Você não tem permissão para editar este projeto');
      }

      const updatedProject = await withLoading(async () => {
        return await projectsApi.updateProject(id, projectData);
      }, {
        loadingMessage: 'Atualizando projeto...',
        successMessage: 'Projeto atualizado com sucesso!'
      });

      // Atualizar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = updatedProject;
      }

      // Atualizar o cache
      projectStore.setProjectDetail(updatedProject);

      return updatedProject;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Função para atualizar parcialmente um projeto
  const partialUpdateProject = async (id, projectData) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Verificar permissão - apenas o gerente pode atualizar o projeto
      const canEdit = await isProjectManager(id);
      if (!canEdit) {
        throw new Error('Você não tem permissão para editar este projeto');
      }

      const updatedProject = await withLoading(async () => {
        return await projectsApi.updateProject(id, projectData);
      }, {
        loadingMessage: 'Atualizando projeto...',
        successMessage: 'Projeto atualizado com sucesso!'
      });

      // Atualizar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = updatedProject;
      }

      // Atualizar o cache
      projectStore.setProjectDetail(updatedProject);

      return updatedProject;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Função para excluir um projeto
  const deleteProject = async (id) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Verificar permissão - apenas o gerente pode excluir o projeto
      const canDelete = await isProjectManager(id);
      if (!canDelete) {
        throw new Error('Você não tem permissão para excluir este projeto');
      }

      await withLoading(async () => {
        await projectsApi.destroyProject(id);
      }, {
        loadingMessage: 'Excluindo projeto...',
        successMessage: 'Projeto excluído com sucesso!'
      });

      // Limpar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = null;
      }

      // Remover do cache
      projectStore.removeProject(id);

      return true;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Função para verificar se o usuário é gerente do projeto
  const isProjectManager = async (projectId) => {
    if (!user.value) return false;

    // Se o projeto atual estiver carregado, verificar se o usuário é o gerente
    if (currentProject.value && currentProject.value.id === projectId) {
      return currentProject.value.owner_id === user.value.id;
    }

    // Caso contrário, buscar o projeto para verificar
    try {
      const project = await fetchProject(projectId);
      return project.owner_id === user.value.id;
    } catch (err) {
      return false;
    }
  };

  // Exportar projeto
  const exportProject = async (id, format = 'pdf') => {
    isLoading.value = true;
    error.value = null;

    try {
      const blob = await withLoading(async () => {
        return await projectsApi.exportProject(id, format);
      }, {
        loadingMessage: `Exportando projeto como ${format.toUpperCase()}...`,
        successMessage: 'Projeto exportado com sucesso!'
      });

      // Criar URL para download
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `projeto_${id}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      return true;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    projects,
    currentProject,
    isLoading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    partialUpdateProject,
    deleteProject,
    exportProject,
    isProjectManager,
    // Função para limpar o cache
    clearProjectCache: () => {
      projectStore.clearCache();
    },
  };
};
