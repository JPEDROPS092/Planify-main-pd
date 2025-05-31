/**
 * Serviço de projetos
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient } from './auth'
import { createFormData } from './config'
import { useState, computed } from '#imports'
import { useAuth } from './auth'
import type {
  Projeto,
  ProjetoRequest,
  ProjetoList,
  PaginatedResponse
} from './types'

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient()
}

/**
 * Composable para gerenciamento de projetos
 */
export const useProjectService = () => {
  const { user, isAuthenticated } = useAuth()
  const projects = useState<Projeto[]>('projects', () => [])
  const currentProject = useState<Projeto | null>('currentProject', () => null)
  const isLoading = useState<boolean>('projects.loading', () => false)
  const error = useState<string | null>('projects.error', () => null)
  
  // Função para buscar todos os projetos
  const fetchProjects = async (params?: {
    arquivado?: boolean;
    gerente?: number;
    ordering?: string;
    page?: number;
    search?: string;
    status?: string;
  }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await listProjetos(params)
      return response
    } catch (err: any) {
      error.value = err.message || 'Erro ao buscar projetos'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para buscar um projeto específico
  const fetchProject = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const project = await retrieveProjeto(id)
      currentProject.value = project
      return project
    } catch (err: any) {
      error.value = err.message || `Erro ao buscar projeto ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para criar um novo projeto
  const createProject = async (projectData: ProjetoRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      // Associar o usuário logado como gerente se não for especificado
      if (!projectData.gerente && user.value) {
        projectData.gerente = user.value.id
      }
      
      const newProject = await createProjeto(projectData)
      return newProject
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar projeto'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar um projeto
  const updateProject = async (id: number, projectData: ProjetoRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedProject = await updateProjeto(id, projectData)
      
      // Atualizar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = updatedProject
      }
      
      return updatedProject
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar projeto ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar parcialmente um projeto
  const partialUpdateProject = async (id: number, projectData: Partial<ProjetoRequest>) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedProject = await partialUpdateProjeto(id, projectData)
      
      // Atualizar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = updatedProject
      }
      
      return updatedProject
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar projeto ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para excluir um projeto
  const deleteProject = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await destroyProjeto(id)
      
      // Limpar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = null
      }
      
      return true
    } catch (err: any) {
      error.value = err.message || `Erro ao excluir projeto ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para arquivar/desarquivar um projeto
  const archiveProject = async (id: number, arquivado: boolean) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedProject = await archiveProjeto(id, { arquivado })
      
      // Atualizar o projeto atual se estiver sendo visualizado
      if (currentProject.value && currentProject.value.id === id) {
        currentProject.value = updatedProject
      }
      
      return updatedProject
    } catch (err: any) {
      error.value = err.message || `Erro ao ${arquivado ? 'arquivar' : 'desarquivar'} projeto ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para verificar se o usuário é gerente do projeto
  const isProjectManager = (projectId: number) => {
    if (!user.value) return false
    
    // Se o projeto atual estiver carregado, verificar se o usuário é o gerente
    if (currentProject.value && currentProject.value.id === projectId) {
      return currentProject.value.gerente === user.value.id
    }
    
    // Caso contrário, buscar o projeto para verificar
    return fetchProject(projectId).then(project => {
      return project.gerente === user.value?.id
    }).catch(() => false)
  }
  
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
    archiveProject,
    isProjectManager
  }
}

/**
 * Listar projetos
 * @param params Parâmetros de paginação e filtro
 */
export async function listProjetos(params?: {
  arquivado?: boolean;
  gerente?: number;
  ordering?: string;
  page?: number;
  search?: string;
  status?: string;
}): Promise<PaginatedResponse<ProjetoList>> {
  const queryParams = new URLSearchParams()
  
  if (params?.arquivado !== undefined) queryParams.append('arquivado', params.arquivado.toString())
  if (params?.gerente) queryParams.append('gerente', params.gerente.toString())
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.search) queryParams.append('search', params.search)
  if (params?.status) queryParams.append('status', params.status)
  
  const queryString = queryParams.toString()
  const url = `/api/projects/projetos/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<ProjetoList>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo projeto
 * @param payload Dados do projeto
 */
export async function createProjeto(payload: ProjetoRequest): Promise<Projeto> {
  return getApi()<Projeto>('/api/projects/projetos/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de um projeto
 * @param id ID do projeto
 */
export async function retrieveProjeto(id: number): Promise<Projeto> {
  return getApi()<Projeto>(`/api/projects/projetos/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um projeto
 * @param id ID do projeto
 * @param payload Dados do projeto
 */
export async function updateProjeto(id: number, payload: ProjetoRequest): Promise<Projeto> {
  return getApi()<Projeto>(`/api/projects/projetos/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente um projeto
 * @param id ID do projeto
 * @param payload Dados parciais do projeto
 */
export async function partialUpdateProjeto(id: number, payload: Partial<ProjetoRequest>): Promise<Projeto> {
  return getApi()<Projeto>(`/api/projects/projetos/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um projeto
 * @param id ID do projeto
 */
export async function destroyProjeto(id: number): Promise<void> {
  return getApi()<void>(`/api/projects/projetos/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Arquivar ou desarquivar um projeto
 * @param id ID do projeto
 * @param payload Dados para arquivar/desarquivar
 */
export async function archiveProjeto(id: number, payload: { arquivado: boolean }): Promise<Projeto> {
  return getApi()<Projeto>(`/api/projects/projetos/${id}/archive/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Listar sprints
 * @param params Parâmetros de paginação e filtro
 */
export async function listSprints(params?: {
  ordering?: string;
  page?: number;
  projeto?: number;
  search?: string;
  status?: string;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString())
  if (params?.search) queryParams.append('search', params.search)
  if (params?.status) queryParams.append('status', params.status)
  
  const queryString = queryParams.toString()
  const url = `/api/projects/sprints/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova sprint
 * @param payload Dados da sprint
 */
export async function createSprint(payload: any): Promise<any> {
  return getApi()<any>('/api/projects/sprints/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma sprint
 * @param id ID da sprint
 */
export async function retrieveSprint(id: number): Promise<any> {
  return getApi()<any>(`/api/projects/sprints/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma sprint
 * @param id ID da sprint
 * @param payload Dados da sprint
 */
export async function updateSprint(id: number, payload: any): Promise<any> {
  return getApi()<any>(`/api/projects/sprints/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma sprint
 * @param id ID da sprint
 * @param payload Dados parciais da sprint
 */
export async function partialUpdateSprint(id: number, payload: any): Promise<any> {
  return getApi()<any>(`/api/projects/sprints/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma sprint
 * @param id ID da sprint
 */
export async function destroySprint(id: number): Promise<void> {
  return getApi()<void>(`/api/projects/sprints/${id}/`, {
    method: 'DELETE'
  })
}
