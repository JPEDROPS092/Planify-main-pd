// frontend/stores/projects.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
// Importará tipos relevantes de '~/services/utils/types' quando necessário
// Ex: import type { Projeto } from '~/services/utils/types';

export const useProjectsStore = defineStore('projects', () => {
  // State
  const projects = ref<any[]>([]); // Substituir 'any' pelo tipo Projeto[]
  const currentProject = ref<any | null>(null); // Substituir 'any' pelo tipo Projeto | null
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  // Ex: const activeProjects = computed(() => projects.value.filter(p => !p.arquivado));

  // Actions
  async function fetchProjects() {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar projetos
      // Ex: const data = await projectService.getAllProjects();
      // projects.value = data;
      console.warn('fetchProjects: Mock implementation. Dados de projetos não foram buscados.');
      // Simular dados
      // projects.value = [{ id: 1, nome: 'Projeto Mock 1', status: 'EM_ANDAMENTO' }];
    } catch (e:any) {
      error.value = e.message || 'Falha ao buscar projetos.';
      console.error(error.value);
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchProjectById(id: number | string) {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar projeto por ID
      // Ex: const data = await projectService.getProjectById(id);
      // currentProject.value = data;
      console.warn(`fetchProjectById(${id}): Mock implementation. Dados do projeto não foram buscados.`);
      // Simular dados
      // if (Number(id) === 1) {
      //   currentProject.value = { id: 1, nome: 'Projeto Mock 1 Detalhado', status: 'EM_ANDAMENTO', descricao: 'Detalhes...' };
      // } else {
      //   currentProject.value = null;
      // }
    } catch (e:any) {
      error.value = e.message || `Falha ao buscar projeto ${id}.`;
      console.error(error.value);
      currentProject.value = null;
    } finally {
      isLoading.value = false;
    }
  }

  // TODO: Adicionar actions para CRUD (create, update, delete)

  return {
    projects,
    currentProject,
    isLoading,
    error,
    fetchProjects,
    fetchProjectById,
    // activeProjects, (exemplo de getter)
  };
});
