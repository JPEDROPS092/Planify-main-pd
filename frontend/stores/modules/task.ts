import { defineStore } from 'pinia';

interface Task {
  id: number;
  titulo: string;
  descricao?: string;
  data_inicio: string;
  data_fim?: string;
  status: string;
  prioridade: string;
  projeto: number | object;
  responsavel: number | object;
  criado_por?: number | object;
  [key: string]: any;
}

interface TaskState {
  tasks: Task[];
  taskDetails: Record<number, Task>;
  lastFetch: number;
  lastDetailsFetch: Record<number, number>;
  isFetching: boolean;
  cacheTTL: number; // Tempo de vida do cache em milissegundos
}

export const useTaskStore = defineStore('task', {
  state: (): TaskState => ({
    tasks: [],
    taskDetails: {},
    lastFetch: 0,
    lastDetailsFetch: {},
    isFetching: false,
    cacheTTL: 5 * 60 * 1000, // 5 minutos em milissegundos
  }),

  getters: {
    /**
     * Verifica se o cache da lista de tarefas é válido
     */
    isTasksCacheValid(): boolean {
      return (
        this.tasks.length > 0 &&
        Date.now() - this.lastFetch < this.cacheTTL
      );
    },

    /**
     * Verifica se o cache de uma tarefa específica é válido
     */
    isTaskDetailCacheValid(): (id: number) => boolean {
      return (id: number) => {
        return (
          !!this.taskDetails[id] &&
          !!this.lastDetailsFetch[id] &&
          Date.now() - this.lastDetailsFetch[id] < this.cacheTTL
        );
      };
    },
  },

  actions: {
    /**
     * Adiciona ou atualiza a lista de tarefas no cache
     */
    setTasks(tasks: Task[]) {
      this.tasks = tasks;
      this.lastFetch = Date.now();
    },

    /**
     * Adiciona ou atualiza uma tarefa específica no cache
     */
    setTaskDetail(task: Task) {
      if (!task || !task.id) return;
      
      this.taskDetails[task.id] = { ...task };
      this.lastDetailsFetch[task.id] = Date.now();
      
      // Atualiza também na lista se existir
      const index = this.tasks.findIndex(t => t.id === task.id);
      if (index !== -1) {
        this.tasks[index] = { ...task };
      }
    },

    /**
     * Remove uma tarefa do cache
     */
    removeTask(id: number) {
      if (!id) return;
      
      // Remove da lista
      this.tasks = this.tasks.filter(t => t.id !== id);
      
      // Remove dos detalhes
      if (this.taskDetails[id]) {
        delete this.taskDetails[id];
      }
      
      // Remove do registro de timestamp
      if (this.lastDetailsFetch[id]) {
        delete this.lastDetailsFetch[id];
      }
    },

    /**
     * Limpa todo o cache de tarefas
     */
    clearCache() {
      this.tasks = [];
      this.taskDetails = {};
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
