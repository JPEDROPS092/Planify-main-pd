/**
 * Serviço de riscos
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient } from './auth'
import { createFormData } from './config'
import type {
  Risco,
  RiscoRequest,
  PaginatedResponse
} from './types'

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient()
}

/**
 * Listar riscos
 * @param params Parâmetros de paginação e filtro
 */
export async function listRiscos(params?: {
  impacto?: string;
  ordering?: string;
  page?: number;
  probabilidade?: string;
  projeto?: number;
  search?: string;
  status?: string;
}): Promise<PaginatedResponse<Risco>> {
  const queryParams = new URLSearchParams()
  
  if (params?.impacto) queryParams.append('impacto', params.impacto)
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.probabilidade) queryParams.append('probabilidade', params.probabilidade)
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString())
  if (params?.search) queryParams.append('search', params.search)
  if (params?.status) queryParams.append('status', params.status)
  
  const queryString = queryParams.toString()
  const url = `/api/risks/riscos/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<Risco>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo risco
 * @param payload Dados do risco
 */
export async function createRisco(payload: RiscoRequest): Promise<Risco> {
  return getApi()<Risco>('/api/risks/riscos/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de um risco
 * @param id ID do risco
 */
export async function retrieveRisco(id: number): Promise<Risco> {
  return getApi()<Risco>(`/api/risks/riscos/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um risco
 * @param id ID do risco
 * @param payload Dados do risco
 */
export async function updateRisco(id: number, payload: RiscoRequest): Promise<Risco> {
  return getApi()<Risco>(`/api/risks/riscos/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente um risco
 * @param id ID do risco
 * @param payload Dados parciais do risco
 */
export async function partialUpdateRisco(id: number, payload: Partial<RiscoRequest>): Promise<Risco> {
  return getApi()<Risco>(`/api/risks/riscos/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um risco
 * @param id ID do risco
 */
export async function destroyRisco(id: number): Promise<void> {
  return getApi()<void>(`/api/risks/riscos/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Atualizar o status de um risco
 * @param id ID do risco
 * @param payload Novo status
 */
export async function atualizarStatusRisco(id: number, payload: { status: string }): Promise<Risco> {
  return getApi()<Risco>(`/api/risks/riscos/${id}/atualizar_status/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Excluir múltiplos riscos
 * @param payload IDs dos riscos a serem excluídos
 */
export async function excluirVariosRiscos(payload: { ids: number[] }): Promise<void> {
  return getApi()<void>('/api/risks/riscos/excluir_varios/', {
    method: 'DELETE',
    body: payload
  })
}

/**
 * Listar histórico de riscos
 * @param params Parâmetros de paginação e filtro
 */
export async function listHistorico(params?: {
  ordering?: string;
  page?: number;
  risco?: number;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.risco) queryParams.append('risco', params.risco.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/risks/historico/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET'
  })
}

/**
 * Obter detalhes de um histórico de risco
 * @param id ID do histórico
 */
export async function retrieveHistorico(id: number): Promise<any> {
  return getApi()<any>(`/api/risks/historico/${id}/`, {
    method: 'GET'
  })
}
