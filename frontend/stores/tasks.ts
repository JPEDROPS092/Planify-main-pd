// frontend/stores/tasks.ts
import { defineStore } from 'pinia';
import { useTaskService } from '~/services/api';
import type { Tarefa, TarefaList, TarefaRequest } from '~/services/api/types';

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    tasks: [] as TarefaList[],
    currentTask: null as Tarefa | null,
    loading: false,
    error: null as Error | null,
    totalItems: 0,
    currentPage: 1,
    totalPages: 1,
    itemsPerPage: 10
  }),
  
  getters: {
    getTasks: (state) => state.tasks,
    isLoading: (state) => state.loading,
    getError: (state) => state.error,
    getCurrentTask: (state) => state.currentTask,
    getTaskById: (state) => (id: number) => state.tasks.find(task => task.id === id)
  },
  
  actions: {
    async fetchTasks(params: any = {}) {
      this.loading = true;
      this.error = null;
      
      try {
        const { listTarefas } = useTaskService();
        const response = await listTarefas({
          page: params.page || this.currentPage,
          ordering: params.ordering || '-data_criacao',
          status: params.status || undefined,
          prioridade: params.prioridade || undefined,
          projeto: params.projeto || undefined,
          search: params.search || undefined
        });
        
        this.tasks = response.results;
        this.totalItems = response.count;
        this.totalPages = Math.ceil(response.count / this.itemsPerPage);
        this.currentPage = params.page || this.currentPage;
        
        return response;
      } catch (error: any) {
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async fetchTaskById(id: number) {
      this.loading = true;
      this.error = null;
      
      try {
        const { retrieveTarefa } = useTaskService();
        const task = await retrieveTarefa(id);
        this.currentTask = task;
        return task;
      } catch (error: any) {
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async createTask(taskData: TarefaRequest) {
      this.loading = true;
      this.error = null;
      
      try {
        const { createTarefa } = useTaskService();
        const task = await createTarefa(taskData);
        
        // Update local state
        await this.fetchTasks({ page: this.currentPage });
        
        return task;
      } catch (error: any) {
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async updateTask(id: number, taskData: Partial<TarefaRequest>) {
      this.loading = true;
      this.error = null;
      
      try {
        const { updateTarefa } = useTaskService();
        const task = await updateTarefa(id, taskData);
        
        // Update local state
        const index = this.tasks.findIndex(t => t.id === id);
        if (index !== -1) {
          this.tasks[index] = { ...this.tasks[index], ...task };
        }
        
        if (this.currentTask && this.currentTask.id === id) {
          this.currentTask = { ...this.currentTask, ...task };
        }
        
        return task;
      } catch (error: any) {
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    async deleteTask(id: number) {
      this.loading = true;
      this.error = null;
      
      try {
        const { destroyTarefa } = useTaskService();
        await destroyTarefa(id);
        
        // Update local state
        this.tasks = this.tasks.filter(task => task.id !== id);
        
        if (this.currentTask && this.currentTask.id === id) {
          this.currentTask = null;
        }
        
        return true;
      } catch (error: any) {
        this.error = error;
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    changePage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        this.fetchTasks({ page });
      }
    }
  }
});
