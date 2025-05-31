/**
 * Serviço de equipes
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient } from './auth'
import { createFormData } from './config'
import { listAuthUsers } from './auth'
import type {
  Equipe,
  EquipeRequest,
  MembroEquipe,
  MembroEquipeRequest,
  PermissaoEquipe,
  PermissaoEquipeRequest,
  PaginatedResponse,
  User
} from './types'

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient()
}

/**
 * Listar equipes
 * @param params Parâmetros de paginação e filtro
 */
export async function listEquipes(params?: {
  ordering?: string;
  page?: number;
  projeto?: number;
  search?: string;
}): Promise<PaginatedResponse<Equipe>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString())
  if (params?.search) queryParams.append('search', params.search)
  
  const queryString = queryParams.toString()
  const url = `/api/teams/equipes/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<Equipe>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova equipe
 * @param payload Dados da equipe
 */
export async function createEquipe(payload: EquipeRequest): Promise<Equipe> {
  return getApi()<Equipe>('/api/teams/equipes/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma equipe
 * @param id ID da equipe
 */
export async function retrieveEquipe(id: number): Promise<Equipe> {
  return getApi()<Equipe>(`/api/teams/equipes/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma equipe
 * @param id ID da equipe
 * @param payload Dados da equipe
 */
export async function updateEquipe(id: number, payload: EquipeRequest): Promise<Equipe> {
  return getApi()<Equipe>(`/api/teams/equipes/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma equipe
 * @param id ID da equipe
 * @param payload Dados parciais da equipe
 */
export async function partialUpdateEquipe(id: number, payload: Partial<EquipeRequest>): Promise<Equipe> {
  return getApi()<Equipe>(`/api/teams/equipes/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma equipe
 * @param id ID da equipe
 */
export async function destroyEquipe(id: number): Promise<void> {
  return getApi()<void>(`/api/teams/equipes/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Adicionar membro a uma equipe
 * @param id ID da equipe
 * @param payload Dados do membro
 */
export async function adicionarMembroEquipe(id: number, payload: { usuario: number; papel: string }): Promise<MembroEquipe> {
  return getApi()<MembroEquipe>(`/api/teams/equipes/${id}/adicionar_membro/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Remover membro de uma equipe
 * @param id ID da equipe
 * @param payload ID do membro
 */
export async function removerMembroEquipe(id: number, payload: { membro_id: number }): Promise<void> {
  return getApi()<void>(`/api/teams/equipes/${id}/remover_membro/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Atualizar papel de um membro da equipe
 * @param id ID da equipe
 * @param payload Dados do membro
 */
export async function atualizarPapelMembroEquipe(id: number, payload: { membro_id: number; papel: string }): Promise<MembroEquipe> {
  return getApi()<MembroEquipe>(`/api/teams/equipes/${id}/atualizar_papel_membro/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Listar membros de equipe
 * @param params Parâmetros de paginação e filtro
 */
export async function listMembros(params?: {
  equipe?: number;
  ordering?: string;
  page?: number;
  papel?: string;
  usuario?: number;
}): Promise<PaginatedResponse<MembroEquipe>> {
  const queryParams = new URLSearchParams()
  
  if (params?.equipe) queryParams.append('equipe', params.equipe.toString())
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.papel) queryParams.append('papel', params.papel)
  if (params?.usuario) queryParams.append('usuario', params.usuario.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/teams/membros/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<MembroEquipe>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo membro de equipe
 * @param payload Dados do membro
 */
export async function createMembro(payload: MembroEquipeRequest): Promise<MembroEquipe> {
  return getApi()<MembroEquipe>('/api/teams/membros/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de um membro de equipe
 * @param id ID do membro
 */
export async function retrieveMembro(id: number): Promise<MembroEquipe> {
  return getApi()<MembroEquipe>(`/api/teams/membros/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um membro de equipe
 * @param id ID do membro
 * @param payload Dados do membro
 */
export async function updateMembro(id: number, payload: MembroEquipeRequest): Promise<MembroEquipe> {
  return getApi()<MembroEquipe>(`/api/teams/membros/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente um membro de equipe
 * @param id ID do membro
 * @param payload Dados parciais do membro
 */
export async function partialUpdateMembro(id: number, payload: Partial<MembroEquipeRequest>): Promise<MembroEquipe> {
  return getApi()<MembroEquipe>(`/api/teams/membros/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um membro de equipe
 * @param id ID do membro
 */
export async function destroyMembro(id: number): Promise<void> {
  return getApi()<void>(`/api/teams/membros/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Listar permissões de equipe
 * @param params Parâmetros de paginação e filtro
 */
export async function listPermissoes(params?: {
  equipe?: number;
  modulo?: string;
  ordering?: string;
  page?: number;
  papel?: string;
  permissao?: string;
}): Promise<PaginatedResponse<PermissaoEquipe>> {
  const queryParams = new URLSearchParams()
  
  if (params?.equipe) queryParams.append('equipe', params.equipe.toString())
  if (params?.modulo) queryParams.append('modulo', params.modulo)
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.papel) queryParams.append('papel', params.papel)
  if (params?.permissao) queryParams.append('permissao', params.permissao)
  
  const queryString = queryParams.toString()
  const url = `/api/teams/permissoes/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<PermissaoEquipe>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova permissão de equipe
 * @param payload Dados da permissão
 */
export async function createPermissao(payload: PermissaoEquipeRequest): Promise<PermissaoEquipe> {
  return getApi()<PermissaoEquipe>('/api/teams/permissoes/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma permissão de equipe
 * @param id ID da permissão
 */
export async function retrievePermissao(id: number): Promise<PermissaoEquipe> {
  return getApi()<PermissaoEquipe>(`/api/teams/permissoes/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma permissão de equipe
 * @param id ID da permissão
 * @param payload Dados da permissão
 */
export async function updatePermissao(id: number, payload: PermissaoEquipeRequest): Promise<PermissaoEquipe> {
  return getApi()<PermissaoEquipe>(`/api/teams/permissoes/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma permissão de equipe
 * @param id ID da permissão
 * @param payload Dados parciais da permissão
 */
export async function partialUpdatePermissao(id: number, payload: Partial<PermissaoEquipeRequest>): Promise<PermissaoEquipe> {
  return getApi()<PermissaoEquipe>(`/api/teams/permissoes/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma permissão de equipe
 * @param id ID da permissão
 */
export async function destroyPermissao(id: number): Promise<void> {
  return getApi()<void>(`/api/teams/permissoes/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Listar usuários
 * @param params Parâmetros de paginação e filtro
 */
export async function listUsuarios(params?: {
  ordering?: string;
  page?: number;
  search?: string;
}): Promise<PaginatedResponse<User>> {
  return listAuthUsers(params)
}
