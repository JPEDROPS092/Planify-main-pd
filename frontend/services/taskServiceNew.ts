import { useApiClient } from '~/composables/useApiClient';
import {
  Tarefa,
  TarefaList,
  TarefaRequest,
  TarefaCreateRequest,
  PaginatedTarefaListList
} from '../api-types';

// Interfaces para parâmetros e respostas específicas
interface TaskFilters {
  atrasada?: boolean;
  data_inicio_antes_after?: string;
  data_inicio_antes_before?: string;
  data_inicio_apos_after?: string;
  data_inicio_apos_before?: string;
  data_termino_antes_after?: string;
  data_termino_antes_before?: string;
  data_termino_apos_after?: string;
  data_termino_apos_before?: string;
  descricao?: string;
  minhas_tarefas?: boolean;
  ordering?: string;
  page?: number;
  prioridade?: string;
  projeto?: number;
  responsavel?: number;
  search?: string;
  sem_responsavel?: boolean;
  sem_sprint?: boolean;
  sprint?: number;
  status?: string;
  titulo?: string;
}

interface TaskStatusUpdate {
  status: 'A_FAZER' | 'EM_ANDAMENTO' | 'FEITO' | 'BLOQUEADA' | 'CANCELADA';
  comentario?: string;
}

interface TaskComment {
  texto: string;
}

interface TaskCommentResponse {
  id: number;
  tarefa: number;
  autor: number;
  autor_nome: string;
  texto: string;
  criado_em: string;
}

interface TaskHistoryResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Array<{
    id: number;
    tarefa: number;
    status_anterior: string;
    status_anterior_display: string;
    novo_status: string;
    novo_status_display: string;
    alterado_por: number;
    alterado_por_nome: string;
    alterado_em: string;
  }>;
}

interface SprintAssociation {
  sprint_id: number | null;
}

export const useTaskService = () => {
  const apiClient = useApiClient();
  
  return {
    // CRUD básico de tarefas
    getTasks: async (params: TaskFilters = {}): Promise<PaginatedTarefaListList> => {
      const response = await apiClient.get('/api/tasks/tarefas/', { params });
      return response.data;
    },
    
    getTask: async (id: number): Promise<Tarefa> => {
      const response = await apiClient.get(`/api/tasks/tarefas/${id}/`);
      return response.data;
    },
    
    createTask: async (task: TarefaCreateRequest): Promise<Tarefa> => {
      const response = await apiClient.post('/api/tasks/tarefas/', task);
      return response.data;
    },
    
    updateTask: async (id: number, task: TarefaRequest): Promise<Tarefa> => {
      const response = await apiClient.put(`/api/tasks/tarefas/${id}/`, task);
      return response.data;
    },
    
    partialUpdateTask: async (id: number, task: Partial<TarefaRequest>): Promise<Tarefa> => {
      const response = await apiClient.patch(`/api/tasks/tarefas/${id}/`, task);
      return response.data;
    },
    
    deleteTask: async (id: number): Promise<void> => {
      await apiClient.delete(`/api/tasks/tarefas/${id}/`);
    },
    
    // Gerenciamento de status
    updateTaskStatus: async (id: number, statusData: TaskStatusUpdate): Promise<any> => {
      const response = await apiClient.post(`/api/tasks/tarefas/${id}/atualizar_status/`, statusData);
      return response.data;
    },
    
    getTaskHistory: async (id: number, params: TaskFilters = {}): Promise<TaskHistoryResponse> => {
      const response = await apiClient.get(`/api/tasks/tarefas/${id}/historico_status/`, { params });
      return response.data;
    },
    
    // Gerenciamento de comentários
    addComment: async (id: number, commentData: TaskComment): Promise<TaskCommentResponse> => {
      const response = await apiClient.post(`/api/tasks/tarefas/${id}/adicionar_comentario/`, commentData);
      return response.data;
    },
    
    // Gerenciamento de sprints
    associateToSprint: async (id: number, sprintData: SprintAssociation): Promise<Tarefa> => {
      const response = await apiClient.post(`/api/tasks/tarefas/${id}/associar_sprint/`, sprintData);
      return response.data;
    },
    
    removeFromSprint: async (id: number): Promise<Tarefa> => {
      const response = await apiClient.post(`/api/tasks/tarefas/${id}/associar_sprint/`, { sprint_id: null });
      return response.data;
    },
    
    // Métodos de filtro específicos para facilitar o uso
    getMyTasks: async (params: Omit<TaskFilters, 'minhas_tarefas'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, minhas_tarefas: true });
    },
    
    getTasksByProject: async (projectId: number, params: Omit<TaskFilters, 'projeto'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, projeto: projectId });
    },
    
    getTasksBySprint: async (sprintId: number, params: Omit<TaskFilters, 'sprint'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, sprint: sprintId });
    },
    
    getTasksByStatus: async (status: string, params: Omit<TaskFilters, 'status'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, status });
    },
    
    getTasksByPriority: async (priority: string, params: Omit<TaskFilters, 'prioridade'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, prioridade: priority });
    },
    
    getOverdueTasks: async (params: Omit<TaskFilters, 'atrasada'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, atrasada: true });
    },
    
    getTasksWithoutAssignment: async (params: Omit<TaskFilters, 'sem_responsavel'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, sem_responsavel: true });
    },
    
    getTasksWithoutSprint: async (params: Omit<TaskFilters, 'sem_sprint'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, sem_sprint: true });
    },
    
    searchTasks: async (searchTerm: string, params: Omit<TaskFilters, 'search'> = {}): Promise<PaginatedTarefaListList> => {
      return await this.getTasks({ ...params, search: searchTerm });
    },
    
    // Métodos de ações rápidas
    markAsInProgress: async (id: number, comentario?: string): Promise<any> => {
      return await this.updateTaskStatus(id, { 
        status: 'EM_ANDAMENTO', 
        comentario: comentario || 'Tarefa iniciada' 
      });
    },
    
    markAsCompleted: async (id: number, comentario?: string): Promise<any> => {
      return await this.updateTaskStatus(id, { 
        status: 'FEITO', 
        comentario: comentario || 'Tarefa concluída' 
      });
    },
    
    markAsBlocked: async (id: number, comentario?: string): Promise<any> => {
      return await this.updateTaskStatus(id, { 
        status: 'BLOQUEADA', 
        comentario: comentario || 'Tarefa bloqueada' 
      });
    },
    
    markAsCancelled: async (id: number, comentario?: string): Promise<any> => {
      return await this.updateTaskStatus(id, { 
        status: 'CANCELADA', 
        comentario: comentario || 'Tarefa cancelada' 
      });
    }
  };
};
