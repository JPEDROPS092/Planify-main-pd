// frontend/stores/tasks.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
// Ex: import type { Tarefa } from '~/services/utils/types';

export const useTasksStore = defineStore('tasks', () => {
  // State
  const tasks = ref<any[]>([]); // Substituir 'any' pelo tipo Tarefa[]
  const currentTask = ref<any | null>(null); // Substituir 'any' pelo tipo Tarefa | null
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Actions
  async function fetchTasksForProject(projectId: number | string) {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar tarefas de um projeto
      console.warn(`fetchTasksForProject(${projectId}): Mock implementation.`);
      // tasks.value = [{ id: 1, titulo: 'Tarefa Mock 1', projeto: projectId }];
    } catch (e:any) {
      error.value = e.message || `Falha ao buscar tarefas para o projeto ${projectId}.`;
    } finally {
      isLoading.value = false;
    }
  }

  // TODO: Adicionar actions para CRUD (create, update, delete) e outras operações (ex: mudar status)

  return {
    tasks,
    currentTask,
    isLoading,
    error,
    fetchTasksForProject,
  };
});
