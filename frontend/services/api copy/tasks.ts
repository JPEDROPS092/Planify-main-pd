/**
 * Serviço de tarefas
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient, useAuth } from './auth'
import { createFormData } from './config'
import { useState, computed } from '#imports'
import type {
  Tarefa,
  TarefaRequest,
  TarefaList,
  PaginatedResponse
} from './types'

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient()
}

/**
 * Listar tarefas
 * @param params Parâmetros de paginação e filtro
 */
export async function listTarefas(params?: {
  ordering?: string;
  page?: number;
  prioridade?: string;
  projeto?: number;
  responsavel?: number;
  search?: string;
  sprint?: number;
  status?: string;
}): Promise<PaginatedResponse<TarefaList>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.prioridade) queryParams.append('prioridade', params.prioridade)
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString())
  if (params?.responsavel) queryParams.append('responsavel', params.responsavel.toString())
  if (params?.search) queryParams.append('search', params.search)
  if (params?.sprint) queryParams.append('sprint', params.sprint.toString())
  if (params?.status) queryParams.append('status', params.status)
  
  const queryString = queryParams.toString()
  const url = `/api/tasks/tarefas/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<TarefaList>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova tarefa
 * @param payload Dados da tarefa
 */
export async function createTarefa(payload: TarefaRequest): Promise<Tarefa> {
  return getApi()<Tarefa>('/api/tasks/tarefas/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma tarefa
 * @param id ID da tarefa
 */
export async function retrieveTarefa(id: number): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma tarefa
 * @param id ID da tarefa
 * @param payload Dados da tarefa
 */
export async function updateTarefa(id: number, payload: TarefaRequest): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma tarefa
 * @param id ID da tarefa
 * @param payload Dados parciais da tarefa
 */
export async function partialUpdateTarefa(id: number, payload: Partial<TarefaRequest>): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma tarefa
 * @param id ID da tarefa
 */
export async function destroyTarefa(id: number): Promise<void> {
  return getApi()<void>(`/api/tasks/tarefas/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Associar uma tarefa a uma sprint
 * @param id ID da tarefa
 * @param payload Dados da associação
 */
export async function associarSprintTarefa(id: number, payload: { sprint: number }): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/associar_sprint/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Remover uma tarefa de uma sprint
 * @param id ID da tarefa
 */
export async function removerSprintTarefa(id: number): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/remover_sprint/`, {
    method: 'POST'
  })
}

/**
 * Atualizar o status de uma tarefa
 * @param id ID da tarefa
 * @param payload Novo status
 */
export async function atualizarStatusTarefa(id: number, payload: { status: string }): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/atualizar_status/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Registrar horas trabalhadas em uma tarefa
 * @param id ID da tarefa
 * @param payload Dados das horas trabalhadas
 */
export async function registrarHorasTarefa(id: number, payload: { horas: number; descricao?: string }): Promise<Tarefa> {
  return getApi()<Tarefa>(`/api/tasks/tarefas/${id}/registrar_horas/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Listar atribuições de tarefas
 * @param params Parâmetros de paginação e filtro
 */
export async function listAtribuicoes(params?: {
  ordering?: string;
  page?: number;
  tarefa?: number;
  usuario?: number;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.tarefa) queryParams.append('tarefa', params.tarefa.toString())
  if (params?.usuario) queryParams.append('usuario', params.usuario.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/tasks/atribuicoes/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova atribuição de tarefa
 * @param payload Dados da atribuição
 */
export async function createAtribuicao(payload: { tarefa: number; usuario: number }): Promise<any> {
  return getApi()<any>('/api/tasks/atribuicoes/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma atribuição de tarefa
 * @param id ID da atribuição
 */
export async function retrieveAtribuicao(id: number): Promise<any> {
  return getApi()<any>(`/api/tasks/atribuicoes/${id}/`, {
    method: 'GET'
  })
}

/**
 * Excluir uma atribuição de tarefa
 * @param id ID da atribuição
 */
export async function destroyAtribuicao(id: number): Promise<void> {
  return getApi()<void>(`/api/tasks/atribuicoes/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Listar comentários de tarefas
 * @param params Parâmetros de paginação e filtro
 */
export async function listComentarios(params?: {
  ordering?: string;
  page?: number;
  tarefa?: number;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.tarefa) queryParams.append('tarefa', params.tarefa.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/tasks/comentarios/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo comentário de tarefa
 * @param payload Dados do comentário
 */
export async function createComentario(payload: { tarefa: number; texto: string }): Promise<any> {
  return getApi()<any>('/api/tasks/comentarios/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de um comentário de tarefa
 * @param id ID do comentário
 */
export async function retrieveComentario(id: number): Promise<any> {
  return getApi()<any>(`/api/tasks/comentarios/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um comentário de tarefa
 * @param id ID do comentário
 * @param payload Dados do comentário
 */
export async function updateComentario(id: number, payload: { texto: string }): Promise<any> {
  return getApi()<any>(`/api/tasks/comentarios/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente um comentário de tarefa
 * @param id ID do comentário
 * @param payload Dados parciais do comentário
 */
export async function partialUpdateComentario(id: number, payload: { texto?: string }): Promise<any> {
  return getApi()<any>(`/api/tasks/comentarios/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um comentário de tarefa
 * @param id ID do comentário
 */
export async function destroyComentario(id: number): Promise<void> {
  return getApi()<void>(`/api/tasks/comentarios/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Composable para gerenciamento de tarefas
 */
export const useTaskService = () => {
  const { user, isAuthenticated } = useAuth()
  const tasks = useState<Tarefa[]>('tasks', () => [])
  const currentTask = useState<Tarefa | null>('currentTask', () => null)
  const isLoading = useState<boolean>('tasks.loading', () => false)
  const error = useState<string | null>('tasks.error', () => null)
  
  // Função para buscar todas as tarefas
  const fetchTasks = async (params?: {
    ordering?: string;
    page?: number;
    prioridade?: string;
    projeto?: number;
    responsavel?: number;
    search?: string;
    sprint?: number;
    status?: string;
  }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await listTarefas(params)
      return response
    } catch (err: any) {
      error.value = err.message || 'Erro ao buscar tarefas'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para buscar uma tarefa específica
  const fetchTask = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const task = await retrieveTarefa(id)
      currentTask.value = task
      return task
    } catch (err: any) {
      error.value = err.message || `Erro ao buscar tarefa ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para criar uma nova tarefa
  const createTask = async (taskData: TarefaRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      // Associar o usuário logado como criador se não for especificado
      if (!taskData.criado_por && user.value) {
        taskData.criado_por = user.value.id
      }
      
      const newTask = await createTarefa(taskData)
      return newTask
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar tarefa'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar uma tarefa
  const updateTask = async (id: number, taskData: TarefaRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedTask = await updateTarefa(id, taskData)
      
      // Atualizar a tarefa atual se estiver sendo visualizada
      if (currentTask.value && currentTask.value.id === id) {
        currentTask.value = updatedTask
      }
      
      return updatedTask
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar tarefa ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar parcialmente uma tarefa
  const partialUpdateTask = async (id: number, taskData: Partial<TarefaRequest>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedTask = await partialUpdateTarefa(id, taskData)
      
      // Atualizar a tarefa atual se estiver sendo visualizada
      if (currentTask.value && currentTask.value.id === id) {
        currentTask.value = updatedTask
      }
      
      return updatedTask
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar tarefa ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para excluir uma tarefa
  const deleteTask = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await destroyTarefa(id)
      
      // Limpar a tarefa atual se estiver sendo visualizada
      if (currentTask.value && currentTask.value.id === id) {
        currentTask.value = null
      }
      
      return true
    } catch (err: any) {
      error.value = err.message || `Erro ao excluir tarefa ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar o status de uma tarefa
  const updateTaskStatus = async (id: number, status: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedTask = await atualizarStatusTarefa(id, { status })
      
      // Atualizar a tarefa atual se estiver sendo visualizada
      if (currentTask.value && currentTask.value.id === id) {
        currentTask.value = updatedTask
      }
      
      return updatedTask
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar status da tarefa ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para registrar horas trabalhadas em uma tarefa
  const registerTaskHours = async (id: number, horas: number, descricao?: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedTask = await registrarHorasTarefa(id, { horas, descricao })
      
      // Atualizar a tarefa atual se estiver sendo visualizada
      if (currentTask.value && currentTask.value.id === id) {
        currentTask.value = updatedTask
      }
      
      return updatedTask
    } catch (err: any) {
      error.value = err.message || `Erro ao registrar horas na tarefa ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    tasks,
    currentTask,
    isLoading,
    error,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    partialUpdateTask,
    deleteTask,
    updateTaskStatus,
    registerTaskHours
  }
}
