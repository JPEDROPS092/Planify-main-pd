/**
 * Serviço de documentos
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient } from './auth'
import { createFormData } from './config'
import type {
  Documento,
  DocumentoRequest,
  PaginatedResponse
} from './types'

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient()
}

/**
 * Listar documentos
 * @param params Parâmetros de paginação e filtro
 */
export async function listDocumentos(params?: {
  ordering?: string;
  page?: number;
  projeto?: number;
  search?: string;
  tarefa?: number;
  tipo?: string;
}): Promise<PaginatedResponse<Documento>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString())
  if (params?.search) queryParams.append('search', params.search)
  if (params?.tarefa) queryParams.append('tarefa', params.tarefa.toString())
  if (params?.tipo) queryParams.append('tipo', params.tipo)
  
  const queryString = queryParams.toString()
  const url = `/api/documents/documentos/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<Documento>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo documento
 * @param payload Dados do documento
 */
export async function createDocumento(payload: DocumentoRequest): Promise<Documento> {
  // Usar FormData para envio de arquivo
  const formData = createFormData(payload)
  
  return getApi()<Documento>('/api/documents/documentos/', {
    method: 'POST',
    body: formData,
    headers: {
      'Content-Type': undefined // O navegador definirá automaticamente com o boundary correto
    }
  })
}

/**
 * Obter detalhes de um documento
 * @param id ID do documento
 */
export async function retrieveDocumento(id: number): Promise<Documento> {
  return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um documento
 * @param id ID do documento
 * @param payload Dados do documento
 */
export async function updateDocumento(id: number, payload: DocumentoRequest): Promise<Documento> {
  // Usar FormData para envio de arquivo
  const formData = createFormData(payload)
  
  return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
    method: 'PUT',
    body: formData,
    headers: {
      'Content-Type': undefined // O navegador definirá automaticamente com o boundary correto
    }
  })
}

/**
 * Atualizar parcialmente um documento
 * @param id ID do documento
 * @param payload Dados parciais do documento
 */
export async function partialUpdateDocumento(id: number, payload: Partial<DocumentoRequest>): Promise<Documento> {
  // Se houver um arquivo, usar FormData
  if (payload.arquivo) {
    const formData = createFormData(payload)
    
    return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
      method: 'PATCH',
      body: formData,
      headers: {
        'Content-Type': undefined // O navegador definirá automaticamente com o boundary correto
      }
    })
  }
  
  return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um documento
 * @param id ID do documento
 */
export async function destroyDocumento(id: number): Promise<void> {
  return getApi()<void>(`/api/documents/documentos/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Associar um documento a uma tarefa
 * @param id ID do documento
 * @param payload Dados da associação
 */
export async function associarTarefaDocumento(id: number, payload: { tarefa: number }): Promise<Documento> {
  return getApi()<Documento>(`/api/documents/documentos/${id}/associar_tarefa/`, {
    method: 'POST',
    body: payload
  })
}

/**
 * Remover a associação de um documento a uma tarefa
 * @param id ID do documento
 */
export async function removerTarefaDocumento(id: number): Promise<Documento> {
  return getApi()<Documento>(`/api/documents/documentos/${id}/remover_tarefa/`, {
    method: 'POST'
  })
}

/**
 * Listar comentários de documentos
 * @param params Parâmetros de paginação e filtro
 */
export async function listComentarios(params?: {
  documento?: number;
  ordering?: string;
  page?: number;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams()
  
  if (params?.documento) queryParams.append('documento', params.documento.toString())
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/documents/comentarios/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo comentário de documento
 * @param payload Dados do comentário
 */
export async function createComentario(payload: { documento: number; texto: string }): Promise<any> {
  return getApi()<any>('/api/documents/comentarios/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de um comentário de documento
 * @param id ID do comentário
 */
export async function retrieveComentario(id: number): Promise<any> {
  return getApi()<any>(`/api/documents/comentarios/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um comentário de documento
 * @param id ID do comentário
 * @param payload Dados do comentário
 */
export async function updateComentario(id: number, payload: { texto: string }): Promise<any> {
  return getApi()<any>(`/api/documents/comentarios/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente um comentário de documento
 * @param id ID do comentário
 * @param payload Dados parciais do comentário
 */
export async function partialUpdateComentario(id: number, payload: { texto?: string }): Promise<any> {
  return getApi()<any>(`/api/documents/comentarios/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um comentário de documento
 * @param id ID do comentário
 */
export async function destroyComentario(id: number): Promise<void> {
  return getApi()<void>(`/api/documents/comentarios/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Download de um documento
 * @param id ID do documento
 * @returns URL do documento para download
 */
export async function downloadDocumento(id: number): Promise<string> {
  // Obter o token de acesso do localStorage
  const accessToken = localStorage.getItem('auth_token')
  
  // Construir a URL do documento com o token de acesso
  const baseURL = window.location.origin
  const downloadURL = `${baseURL}/api/documents/documentos/${id}/download/`
  
  // Retornar a URL para download
  return downloadURL
}
