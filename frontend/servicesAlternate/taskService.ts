import { useApiClients } from '../composables/useApiClients';
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

const tarefas = [
  {
    id: "T001",
    titulo: "Implementar autenticação de usuário",
    projeto: "App de Produtividade",
    sprint: "Sprint 1",
    status: "Em Andamento",
    prioridade: "Alta",
    data_termino: "2025-07-15",
    criado_por: "Alice Silva",
    atribuicoes: ["Bob Santos", "Alice Silva"]
  },
  {
    id: "T002",
    titulo: "Criar mockups da interface",
    projeto: "Site Institucional",
    sprint: "Sprint 2",
    status: "Pendente",
    prioridade: "Média",
    data_termino: "2025-07-20",
    criado_por: "Carlos Souza",
    atribuicoes: ["Diana Lima"]
  },
  {
    id: "T003",
    titulo: "Corrigir bug de layout no rodapé",
    projeto: "App de Produtividade",
    sprint: "Sprint 1",
    status: "Concluído",
    prioridade: "Baixa",
    data_termino: "2025-07-01",
    criado_por: "Bob Santos",
    atribuicoes: ["Carlos Souza"]
  }
];

const paginatedTarefas = {
    count: 3,
    next: "sei lá",
    previous: "num sei",
    results: tarefas,
};

export const useTaskService = () => {
  const { tasksApi } = useApiClients();
  
  return {
    // CRUD básico de tarefas
    getTasks: async (params: TaskFilters = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    getTask: async (id: number): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasRetrieve(id);
      return response.data;
    },
    
    createTask: async (task: TarefaCreateRequest): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasCreate(task as any);
      return response.data;
    },
    
    updateTask: async (id: number, task: TarefaRequest): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasUpdate(id, task);
      return response.data;
    },
    
    partialUpdateTask: async (id: number, task: Partial<TarefaRequest>): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasPartialUpdate(id, task as any);
      return response.data;
    },
    
    deleteTask: async (id: number): Promise<void> => {
      await tasksApi.tasksTarefasDestroy(id);
    },
    
    // Gerenciamento de status
    updateTaskStatus: async (id: number, statusData: TaskStatusUpdate): Promise<any> => {
      const response = await tasksApi.tasksTarefasAtualizarStatusCreate(id, statusData as any);
      return response.data;
    },
    
    getTaskHistory: async (id: number, params: TaskFilters = {}): Promise<TaskHistoryResponse> => {
      const response = await tasksApi.tasksTarefasHistoricoStatusList(
        id,
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel as any,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    // Gerenciamento de comentários
    addComment: async (id: number, commentData: TaskComment): Promise<TaskCommentResponse> => {
      const response = await tasksApi.tasksTarefasAdicionarComentarioCreate(id, commentData as any);
      return response.data;
    },
    
    // Método legado para compatibilidade com código existente
    addTaskComment: async (taskId: number, comment: string): Promise<TaskCommentResponse> => {
      const response = await tasksApi.tasksTarefasAdicionarComentarioCreate(taskId, { texto: comment } as any);
      return response.data;
    },
    
    // Gerenciamento de sprints
    associateToSprint: async (id: number, sprintData: SprintAssociation): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasAssociarSprintCreate(id, sprintData as any);
      return response.data;
    },
    
    removeFromSprint: async (id: number): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasAssociarSprintCreate(id, { sprint_id: null } as any);
      return response.data;
    },

    // Método legado para compatibilidade com código existente
    associateTaskToSprint: async (taskId: number, sprintId: number): Promise<Tarefa> => {
      const response = await tasksApi.tasksTarefasAssociarSprintCreate(taskId, { sprint_id: sprintId } as any);
      return response.data;
    },

    // Gerenciamento de responsáveis (métodos legados para compatibilidade)
    assignTaskResponsible: async (taskId: number, userId: number): Promise<Tarefa> => {
      // Note: This uses AtribuiesApi, we'll need to add it to useApiClients
      const { tasksApi } = useApiClients();
      const response = await tasksApi.tasksTarefasUpdate(taskId, { responsavel: userId } as any);
      return response.data;
    },
    
    removeTaskResponsible: async (taskId: number): Promise<Tarefa> => {
      // Usando PATCH para remover o responsável
      const response = await tasksApi.tasksTarefasUpdate(taskId, { responsavel: null } as any);
      return response.data;
    },

    // Criação em lote (método legado - precisa ser implementado no backend se necessário)
    createBulkTasks: async (data: any[]): Promise<any> => {
      // Por enquanto, criar uma por vez até o backend implementar bulk creation
      const promises = data.map(task => tasksApi.tasksTarefasCreate(task as any));
      const responses = await Promise.all(promises);
      return responses.map((response: any) => response.data);
    },
    
    // Métodos de filtro específicos para facilitar o uso
    getMyTasks: async (params: Omit<TaskFilters, 'minhas_tarefas'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        undefined,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        true,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return new Promise(paginatedTarefas);
    },
    
    getTasksByProject: async (projectId: number, params: Omit<TaskFilters, 'projeto'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        projectId,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    getTasksBySprint: async (sprintId: number, params: Omit<TaskFilters, 'sprint'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasSprintList(
        params.prioridade,
        params.responsavel,
        sprintId,
        params.status,
      );
      return response.data;
    },
    
    getTasksByStatus: async (status: string, params: Omit<TaskFilters, 'status'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        status,
        params.titulo
      );
      return response.data;
    },
    
    getTasksByPriority: async (priority: string, params: Omit<TaskFilters, 'prioridade'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        priority,
        params.projeto,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    getOverdueTasks: async (params: Omit<TaskFilters, 'atrasada'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        true,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    getTasksWithoutAssignment: async (params: Omit<TaskFilters, 'sem_responsavel'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        undefined,
        params.search,
        true,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    getTasksWithoutSprint: async (params: Omit<TaskFilters, 'sem_sprint'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel,
        params.search,
        params.sem_responsavel,
        true,
        undefined,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    searchTasks: async (searchTerm: string, params: Omit<TaskFilters, 'search'> = {}): Promise<PaginatedTarefaListList> => {
      const response = await tasksApi.tasksTarefasList(
        params.atrasada,
        params.data_inicio_antes_after,
        params.data_inicio_antes_before,
        params.data_inicio_apos_after,
        params.data_inicio_apos_before,
        params.data_termino_antes_after,
        params.data_termino_antes_before,
        params.data_termino_apos_after,
        params.data_termino_apos_before,
        params.descricao,
        params.minhas_tarefas,
        params.ordering,
        params.page,
        params.prioridade,
        params.projeto,
        params.responsavel,
        searchTerm,
        params.sem_responsavel,
        params.sem_sprint,
        params.sprint,
        params.status,
        params.titulo
      );
      return response.data;
    },
    
    // Métodos de ações rápidas
    markAsInProgress: async (id: number, comentario?: string): Promise<any> => {
      const response = await tasksApi.tasksTarefasAtualizarStatusCreate(id, { 
        status: 'EM_ANDAMENTO', 
        comentario: comentario || 'Tarefa iniciada' 
      } as any);
      return response.data;
    },
    
    markAsCompleted: async (id: number, comentario?: string): Promise<any> => {
      const response = await tasksApi.tasksTarefasAtualizarStatusCreate(id, { 
        status: 'FEITO', 
        comentario: comentario || 'Tarefa concluída' 
      } as any);
      return response.data;
    },
    
    markAsBlocked: async (id: number, comentario?: string): Promise<any> => {
      const response = await tasksApi.tasksTarefasAtualizarStatusCreate(id, { 
        status: 'BLOQUEADA', 
        comentario: comentario || 'Tarefa bloqueada' 
      } as any);
      return response.data;
    },
    
    markAsCancelled: async (id: number, comentario?: string): Promise<any> => {
      const response = await tasksApi.tasksTarefasAtualizarStatusCreate(id, { 
        status: 'CANCELADA', 
        comentario: comentario || 'Tarefa cancelada' 
      } as any);
      return response.data;
    }
  };
};
