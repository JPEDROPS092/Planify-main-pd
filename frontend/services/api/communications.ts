/**
 * Serviço de comunicações
 * Gerado a partir da especificação OpenAPI
 */
import { createFetchClient } from './auth'
import { createFormData } from './config'
import type {
  ChatMensagem,
  ChatMensagemRequest,
  Notificacao,
  NotificacaoRequest,
  PaginatedResponse
} from './types'

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient()
}

/**
 * Listar mensagens de chat
 * @param params Parâmetros de paginação e filtro
 */
export async function listMensagens(params?: {
  ordering?: string;
  page?: number;
  projeto?: number;
}): Promise<PaginatedResponse<ChatMensagem>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.projeto) queryParams.append('projeto', params.projeto.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/communications/mensagens/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<ChatMensagem>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova mensagem de chat
 * @param payload Dados da mensagem
 */
export async function createMensagem(payload: ChatMensagemRequest): Promise<ChatMensagem> {
  // Se houver um anexo, usar FormData
  if (payload.anexo) {
    const formData = createFormData(payload)
    
    return getApi()<ChatMensagem>('/api/communications/mensagens/', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': undefined // O navegador definirá automaticamente com o boundary correto
      }
    })
  }
  
  return getApi()<ChatMensagem>('/api/communications/mensagens/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma mensagem de chat
 * @param id ID da mensagem
 */
export async function retrieveMensagem(id: number): Promise<ChatMensagem> {
  return getApi()<ChatMensagem>(`/api/communications/mensagens/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma mensagem de chat
 * @param id ID da mensagem
 * @param payload Dados da mensagem
 */
export async function updateMensagem(id: number, payload: ChatMensagemRequest): Promise<ChatMensagem> {
  // Se houver um anexo, usar FormData
  if (payload.anexo) {
    const formData = createFormData(payload)
    
    return getApi()<ChatMensagem>(`/api/communications/mensagens/${id}/`, {
      method: 'PUT',
      body: formData,
      headers: {
        'Content-Type': undefined // O navegador definirá automaticamente com o boundary correto
      }
    })
  }
  
  return getApi()<ChatMensagem>(`/api/communications/mensagens/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma mensagem de chat
 * @param id ID da mensagem
 * @param payload Dados parciais da mensagem
 */
export async function partialUpdateMensagem(id: number, payload: Partial<ChatMensagemRequest>): Promise<ChatMensagem> {
  // Se houver um anexo, usar FormData
  if (payload.anexo) {
    const formData = createFormData(payload)
    
    return getApi()<ChatMensagem>(`/api/communications/mensagens/${id}/`, {
      method: 'PATCH',
      body: formData,
      headers: {
        'Content-Type': undefined // O navegador definirá automaticamente com o boundary correto
      }
    })
  }
  
  return getApi()<ChatMensagem>(`/api/communications/mensagens/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma mensagem de chat
 * @param id ID da mensagem
 */
export async function destroyMensagem(id: number): Promise<void> {
  return getApi()<void>(`/api/communications/mensagens/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Marcar uma mensagem como lida
 * @param id ID da mensagem
 */
export async function marcarComoLidaMensagem(id: number): Promise<ChatMensagem> {
  return getApi()<ChatMensagem>(`/api/communications/mensagens/${id}/marcar_como_lida/`, {
    method: 'POST'
  })
}

/**
 * Obter mensagens não lidas
 */
export async function retrieveMensagensNaoLidas(): Promise<ChatMensagem[]> {
  return getApi()<ChatMensagem[]>('/api/communications/mensagens/mensagens_nao_lidas/', {
    method: 'GET'
  })
}

/**
 * Listar notificações
 * @param params Parâmetros de paginação e filtro
 */
export async function listNotificacoes(params?: {
  lida?: boolean;
  ordering?: string;
  page?: number;
  usuario?: number;
}): Promise<PaginatedResponse<Notificacao>> {
  const queryParams = new URLSearchParams()
  
  if (params?.lida !== undefined) queryParams.append('lida', params.lida.toString())
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.usuario) queryParams.append('usuario', params.usuario.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/communications/notificacoes/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<Notificacao>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova notificação
 * @param payload Dados da notificação
 */
export async function createNotificacao(payload: NotificacaoRequest): Promise<Notificacao> {
  return getApi()<Notificacao>('/api/communications/notificacoes/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma notificação
 * @param id ID da notificação
 */
export async function retrieveNotificacao(id: number): Promise<Notificacao> {
  return getApi()<Notificacao>(`/api/communications/notificacoes/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma notificação
 * @param id ID da notificação
 * @param payload Dados da notificação
 */
export async function updateNotificacao(id: number, payload: NotificacaoRequest): Promise<Notificacao> {
  return getApi()<Notificacao>(`/api/communications/notificacoes/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma notificação
 * @param id ID da notificação
 * @param payload Dados parciais da notificação
 */
export async function partialUpdateNotificacao(id: number, payload: Partial<NotificacaoRequest>): Promise<Notificacao> {
  return getApi()<Notificacao>(`/api/communications/notificacoes/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma notificação
 * @param id ID da notificação
 */
export async function destroyNotificacao(id: number): Promise<void> {
  return getApi()<void>(`/api/communications/notificacoes/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Marcar uma notificação como lida
 * @param id ID da notificação
 */
export async function marcarComoLidaNotificacao(id: number): Promise<Notificacao> {
  return getApi()<Notificacao>(`/api/communications/notificacoes/${id}/marcar_como_lida/`, {
    method: 'POST'
  })
}

/**
 * Marcar todas as notificações como lidas
 */
export async function marcarTodasComoLidasNotificacoes(): Promise<void> {
  return getApi()<void>('/api/communications/notificacoes/marcar_todas_como_lidas/', {
    method: 'POST'
  })
}

/**
 * Listar configurações de notificações
 * @param params Parâmetros de paginação e filtro
 */
export async function listConfiguracoes(params?: {
  ordering?: string;
  page?: number;
  usuario?: number;
}): Promise<PaginatedResponse<any>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.usuario) queryParams.append('usuario', params.usuario.toString())
  
  const queryString = queryParams.toString()
  const url = `/api/communications/configuracoes/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<any>>(url, {
    method: 'GET'
  })
}

/**
 * Criar uma nova configuração de notificação
 * @param payload Dados da configuração
 */
export async function createConfiguracao(payload: any): Promise<any> {
  return getApi()<any>('/api/communications/configuracoes/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de uma configuração de notificação
 * @param id ID da configuração
 */
export async function retrieveConfiguracao(id: number): Promise<any> {
  return getApi()<any>(`/api/communications/configuracoes/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar uma configuração de notificação
 * @param id ID da configuração
 * @param payload Dados da configuração
 */
export async function updateConfiguracao(id: number, payload: any): Promise<any> {
  return getApi()<any>(`/api/communications/configuracoes/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente uma configuração de notificação
 * @param id ID da configuração
 * @param payload Dados parciais da configuração
 */
export async function partialUpdateConfiguracao(id: number, payload: any): Promise<any> {
  return getApi()<any>(`/api/communications/configuracoes/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir uma configuração de notificação
 * @param id ID da configuração
 */
export async function destroyConfiguracao(id: number): Promise<void> {
  return getApi()<void>(`/api/communications/configuracoes/${id}/`, {
    method: 'DELETE'
  })
}
