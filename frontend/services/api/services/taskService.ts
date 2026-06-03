/**
 * useTaskService
 *
 * Composable Nuxt que delega toda a comunicação com /api/tasks/tarefas/*
 * ao cliente gerado (ApiService). Não configura transporte nem estado global;
 * mantém exatamente os nomes de método usados nos call-sites.
 */
import { ApiService } from '~/lib/api-client';
import type {
  Tarefa,
  TarefaList,
  TarefaRequest,
  PatchedTarefaRequest,
  PaginatedTarefaListList,
} from '~/lib/api-client';

// --------------------------------------------------------------------------
// Tipo de parâmetros para listagem, alinhado com ApiService.apiTasksTarefasList
// --------------------------------------------------------------------------
export interface ListTarefasParams {
  atrasada?: boolean;
  dataInicioAntesAfter?: string;
  dataInicioAntesBefore?: string;
  dataInicioAposAfter?: string;
  dataInicioAposBefore?: string;
  dataTerminoAntesAfter?: string;
  dataTerminoAntesBefore?: string;
  dataTerminoAposAfter?: string;
  dataTerminoAposBefore?: string;
  descricao?: string;
  minhasTarefas?: boolean;
  ordering?: string;
  page?: number;
  prioridade?: string;
  projeto?: number;
  responsavel?: number;
  search?: string;
  semResponsavel?: boolean;
  semSprint?: boolean;
  sprint?: number;
  status?: string;
  titulo?: string;
}

// --------------------------------------------------------------------------
// Composable
// --------------------------------------------------------------------------
export function useTaskService() {
  /**
   * Listar tarefas com filtros opcionais.
   * → ApiService.apiTasksTarefasList(...)
   */
  function listTarefas(params: ListTarefasParams = {}): Promise<PaginatedTarefaListList> {
    return ApiService.apiTasksTarefasList(
      params.atrasada,
      params.dataInicioAntesAfter,
      params.dataInicioAntesBefore,
      params.dataInicioAposAfter,
      params.dataInicioAposBefore,
      params.dataTerminoAntesAfter,
      params.dataTerminoAntesBefore,
      params.dataTerminoAposAfter,
      params.dataTerminoAposBefore,
      params.descricao,
      params.minhasTarefas,
      params.ordering,
      params.page,
      params.prioridade,
      params.projeto,
      params.responsavel,
      params.search,
      params.semResponsavel,
      params.semSprint,
      params.sprint,
      params.status,
      params.titulo,
    );
  }

  /**
   * Alias de listTarefas usado por DraggableTaskList.
   * Aceita { projeto, ... } e retorna a resposta paginada.
   * → ApiService.apiTasksTarefasList(...)
   */
  function fetchTasks(params: ListTarefasParams = {}): Promise<PaginatedTarefaListList> {
    return listTarefas(params);
  }

  /**
   * Listar todas as tarefas de um projeto e retornar o array de resultados.
   * Usado por pages/projetos/[id]/reports/tasks.vue via getTasks(projectId).
   * → ApiService.apiTasksTarefasList(... projeto=projectId ...)
   */
  async function getTasks(projectId: number | string): Promise<TarefaList[]> {
    const response = await ApiService.apiTasksTarefasList(
      undefined, // atrasada
      undefined, undefined, undefined, undefined,
      undefined, undefined, undefined, undefined,
      undefined, // descricao
      undefined, // minhasTarefas
      undefined, // ordering
      undefined, // page
      undefined, // prioridade
      Number(projectId), // projeto
    );
    return response.results ?? [];
  }

  /**
   * Listar tarefas filtradas por projeto (retorna a resposta paginada completa).
   * Usado por ProjectTasks.vue via getByProject(projectId).
   * → ApiService.apiTasksTarefasList(... projeto=projectId ...)
   */
  function getByProject(projectId: number | string): Promise<PaginatedTarefaListList> {
    return listTarefas({ projeto: Number(projectId) });
  }

  /**
   * Buscar uma tarefa pelo ID.
   * → ApiService.apiTasksTarefasRetrieve(id)
   */
  function retrieveTarefa(id: number): Promise<Tarefa> {
    return ApiService.apiTasksTarefasRetrieve(id);
  }

  /**
   * Criar uma nova tarefa.
   * → ApiService.apiTasksTarefasCreate(body)
   */
  function createTarefa(body: TarefaRequest): Promise<Tarefa> {
    return ApiService.apiTasksTarefasCreate(body);
  }

  /**
   * Alias de createTarefa usado por ProjectTasks.vue.
   * → ApiService.apiTasksTarefasCreate(body)
   */
  function create(body: TarefaRequest): Promise<Tarefa> {
    return ApiService.apiTasksTarefasCreate(body);
  }

  /**
   * Atualizar completamente uma tarefa (PUT).
   * → ApiService.apiTasksTarefasUpdate(id, body)
   */
  function updateTarefa(id: number, body: TarefaRequest | Partial<TarefaRequest>): Promise<Tarefa> {
    return ApiService.apiTasksTarefasUpdate(id, body as TarefaRequest);
  }

  /**
   * Alias de updateTarefa usado por ProjectTasks.vue e KanbanBoard.vue.
   * → ApiService.apiTasksTarefasUpdate(id, body)
   */
  function update(id: number, body: TarefaRequest | Partial<TarefaRequest>): Promise<Tarefa> {
    return ApiService.apiTasksTarefasUpdate(id, body as TarefaRequest);
  }

  /**
   * Alias de updateTarefa usado por KanbanBoard.vue como updateTask.
   * → ApiService.apiTasksTarefasUpdate(id, body)
   */
  function updateTask(id: number, body: TarefaRequest | Partial<TarefaRequest>): Promise<Tarefa> {
    return ApiService.apiTasksTarefasUpdate(id, body as TarefaRequest);
  }

  /**
   * Atualizar parcialmente uma tarefa (PATCH).
   * → ApiService.apiTasksTarefasPartialUpdate(id, body)
   */
  function partialUpdateTarefa(id: number, body?: PatchedTarefaRequest): Promise<Tarefa> {
    return ApiService.apiTasksTarefasPartialUpdate(id, body);
  }

  /**
   * Excluir uma tarefa.
   * → ApiService.apiTasksTarefasDestroy(id)
   */
  function destroyTarefa(id: number): Promise<void> {
    return ApiService.apiTasksTarefasDestroy(id);
  }

  /**
   * Alias de destroyTarefa usado por ProjectTasks.vue.
   * → ApiService.apiTasksTarefasDestroy(id)
   */
  function remove(id: number): Promise<void> {
    return ApiService.apiTasksTarefasDestroy(id);
  }

  /**
   * Associar tarefa a uma sprint.
   * Usado em SprintManagement.vue (código comentado: taskService.associateWithSprint).
   * → ApiService.apiTasksTarefasAssociarSprintCreate(id, { sprint_id })
   */
  function associateWithSprint(taskId: number, sprintId: number): Promise<Tarefa> {
    return ApiService.apiTasksTarefasAssociarSprintCreate(taskId, { sprint_id: sprintId });
  }

  /**
   * Remover tarefa de uma sprint (passa sprint_id: null).
   * Usado em SprintManagement.vue (código comentado: taskService.removeFromSprint).
   * → ApiService.apiTasksTarefasAssociarSprintCreate(id, { sprint_id: null })
   */
  function removeFromSprint(taskId: number): Promise<Tarefa> {
    return ApiService.apiTasksTarefasAssociarSprintCreate(taskId, { sprint_id: null });
  }

  /**
   * Atualizar o status de uma tarefa com registro no histórico.
   * → ApiService.apiTasksTarefasAtualizarStatusCreate(id, { status, comentario? })
   */
  function atualizarStatus(
    id: number,
    status: string,
    comentario?: string,
  ): Promise<Tarefa> {
    return ApiService.apiTasksTarefasAtualizarStatusCreate(id, { status, comentario });
  }

  /**
   * Adicionar um comentário a uma tarefa.
   * → ApiService.apiTasksTarefasAdicionarComentarioCreate(id, { texto })
   */
  function adicionarComentario(
    id: number,
    texto: string,
  ) {
    return ApiService.apiTasksTarefasAdicionarComentarioCreate(id, { texto });
  }

  return {
    // Listagem
    listTarefas,
    fetchTasks,
    getTasks,
    getByProject,
    // Retrieve
    retrieveTarefa,
    // Create
    createTarefa,
    create,
    // Update (full)
    updateTarefa,
    update,
    updateTask,
    // Partial update
    partialUpdateTarefa,
    // Delete
    destroyTarefa,
    remove,
    // Sprint
    associateWithSprint,
    removeFromSprint,
    // Actions
    atualizarStatus,
    adicionarComentario,
  };
}
