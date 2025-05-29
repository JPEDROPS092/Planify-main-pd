/**
 * Serviço de autenticação
 * Gerado a partir da especificação OpenAPI
 */
import { $fetch } from 'ofetch'
import { useNuxtApp } from '#app'
import { useState, computed } from '#imports'
import { API_CONFIG, ApiError, createFormData, getApiConfig } from './config'
import { authLogger, apiLogger } from '~/lib/logger'
import type {
  TokenObtainPairRequest,
  TokenObtainPair,
  TokenRefreshRequest,
  TokenRefresh,
  User,
  UserCreatePasswordRetypeRequest,
  UserCreatePasswordRetype,
  SetPasswordRetypeRequest,
  SendEmailResetRequest,
  SetNewPasswordRequest,
  PaginatedResponse
} from './types'

// Definir o tipo FetchOptions localmente
type FetchOptions = {
  method?: string
  body?: any
  params?: Record<string, any>
  headers?: Record<string, string>
  baseURL?: string
}

/**
 * Composable para gerenciamento de autenticação
 */
export const useAuth = () => {
  const accessToken = useState<string | null>('auth.accessToken', () => {
    return process.client ? localStorage.getItem('auth_token') : null
  })
  
  const refreshToken = useState<string | null>('auth.refreshToken', () => {
    return process.client ? localStorage.getItem('refresh_token') : null
  })
  
  const user = useState<User | null>('auth.user', () => null)
  
  const isAuthenticated = computed(() => !!accessToken.value)
  
  // Função para salvar tokens
  const saveTokens = (tokens: TokenObtainPair | TokenRefresh) => {
    accessToken.value = tokens.access
    if ('refresh' in tokens) {
      refreshToken.value = tokens.refresh
    }
    
    if (process.client) {
      localStorage.setItem('auth_token', tokens.access)
      if ('refresh' in tokens) {
        localStorage.setItem('refresh_token', tokens.refresh)
      }
    }
    
    authLogger.info('Tokens salvos com sucesso')
    authLogger.debug('Access token:', tokens.access.substring(0, 15) + '...')
  }
  
  // Função para limpar tokens
  const clearTokens = () => {
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    
    if (process.client) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
    }
    
    authLogger.info('Tokens removidos')
  }
  
  // Função para fazer login
  const login = async (credentials: TokenObtainPairRequest) => {
    authLogger.info('Tentando login para usuário:', credentials.username)
    try {
      const tokens = await createAuthToken(credentials)
      authLogger.info('Login bem-sucedido')
      saveTokens(tokens)
      await fetchCurrentUser()
      return true
    } catch (error: any) {
      authLogger.error('Falha no login:', error.message || 'Erro desconhecido')
      clearTokens()
      throw error
    }
  }
  
  // Função para fazer logout
  const logout = () => {
    authLogger.info('Realizando logout')
    clearTokens()
  }
  
  // Função para atualizar o token
  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      authLogger.error('Refresh token não disponível')
      throw new Error('Refresh token não disponível')
    }
    
    authLogger.info('Atualizando token de acesso')
    try {
      const tokens = await refreshAuthTokenCreate({ refresh: refreshToken.value })
      authLogger.info('Token atualizado com sucesso')
      saveTokens(tokens)
      return tokens
    } catch (error: any) {
      authLogger.error('Falha ao atualizar token:', error.message || 'Erro desconhecido')
      clearTokens()
      throw error
    }
  }
  
  // Função para buscar o usuário atual
  const fetchCurrentUser = async () => {
    authLogger.info('Buscando informações do usuário atual')
    try {
      user.value = await retrieveAuthUsersMe()
      authLogger.info('Informações do usuário obtidas com sucesso', user.value?.username)
      return user.value
    } catch (error: any) {
      authLogger.error('Falha ao buscar usuário atual:', error.message || 'Erro desconhecido')
      throw error
    }
  }
  
  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    login,
    logout,
    refreshAuthToken,
    fetchCurrentUser
  }
}

/**
 * Função para criar um cliente fetch configurado com autenticação
 */
export const createFetchClient = () => {
  // Criamos uma função interna que só vai acessar o useAuth quando for chamada
  // e não durante a inicialização do módulo
  return async <T>(url: string, options: FetchOptions = {}): Promise<T> => {
    const method = options.method || 'GET';
    
    // Movemos a chamada do useAuth para dentro da função que será executada no contexto correto
    let token = null
    if (process.client) {
      // Em ambiente cliente, tentamos obter o token do localStorage diretamente
      token = localStorage.getItem('auth_token')
      authLogger.debug('Token obtido do localStorage:', token ? `${token.substring(0, 15)}...` : 'null')
    } else {
      // Em SSR ou quando o composable estiver disponível, usamos o useAuth
      try {
        const { accessToken } = useAuth()
        token = accessToken.value
        authLogger.debug('Token obtido do useAuth:', token ? `${token.substring(0, 15)}...` : 'null')
      } catch (e) {
        // Ignora erro se o composable não estiver disponível
        authLogger.warn('useAuth não disponível no contexto atual')
      }
    }
    
    // Obter configuração da API de forma lazy
    const apiConfig = getApiConfig()
    
    const fetchOptions: FetchOptions = {
      ...options,
      baseURL: apiConfig.baseURL,
      headers: {
        ...apiConfig.headers,
        ...options.headers
      }
    }
    
    // Adicionar token de autenticação se disponível
    if (token) {
      fetchOptions.headers = {
        ...fetchOptions.headers,
        'Authorization': `Bearer ${token}`
      }
      apiLogger.debug(`Requisição ${method} para ${url} com token de autenticação`)
      apiLogger.debug('Headers:', fetchOptions.headers)
    } else {
      apiLogger.warn(`Requisição ${method} para ${url} SEM token de autenticação`)
    }
    
    try {
      apiLogger.http(method, url);
      const response = await $fetch<T>(url, fetchOptions)
      apiLogger.http(method, url, 200);
      return response
    } catch (error: any) {
      const status = error.response?.status || 0;
      apiLogger.http(method, url, status);
      apiLogger.error(`Erro ${status} na requisição:`, error.message || 'Erro desconhecido');
      
      // Tratar erro 401 com refresh de token
      if (error.response?.status === 401 && !url.includes('/api/auth/token/refresh/')) {
        authLogger.info('Tentando refresh de token após erro 401')
        try {
          // Tentamos obter o refreshAuthToken apenas quando precisamos dele
          const { refreshAuthToken } = useAuth()
          
          try {
            authLogger.debug('Executando refreshAuthToken()')
            await refreshAuthToken()
            
            // Tentar novamente com o novo token
            // Obter o token atualizado do localStorage diretamente para evitar problemas de contexto
            const newToken = process.client ? localStorage.getItem('auth_token') : null
            authLogger.debug('Novo token após refresh:', newToken ? `${newToken.substring(0, 15)}...` : 'null')
            
            if (newToken) {
              fetchOptions.headers = {
                ...fetchOptions.headers,
                'Authorization': `Bearer ${newToken}`
              }
              
              apiLogger.info('Repetindo requisição com novo token')
              apiLogger.http(method, url);
              const retryResponse = await $fetch<T>(url, fetchOptions)
              apiLogger.http(method, url, 200);
              apiLogger.info('Requisição repetida com sucesso')
              return retryResponse
            } else {
              authLogger.error('Refresh de token não retornou um novo token')
              throw error
            }
          } catch (refreshError) {
            // Se falhar o refresh, propagar o erro original
            authLogger.error('Erro durante refresh de token:', refreshError)
            throw error
          }
        } catch (authError) {
          // Se não conseguir acessar o useAuth, propagar o erro original
          authLogger.error('Erro ao acessar useAuth para refresh:', authError)
          throw error
        }
      }
      
      // Outros erros
      if (error.response) {
        throw new ApiError(
          error.response._data?.detail || 'Erro na requisição',
          error.response.status,
          error.response._data
        )
      }
      
      throw error
    }
  }
}

// Criamos uma função lazy para obter a instância do cliente fetch apenas quando necessário
// Isso evita que o createFetchClient seja chamado durante a inicialização do módulo
const getApi = () => {
  // Lazy initialization do cliente fetch
  return createFetchClient()
}

/**
 * Obter token de autenticação
 * @param payload Credenciais de autenticação
 */
export async function createAuthToken(payload: TokenObtainPairRequest): Promise<TokenObtainPair> {
  return getApi()<TokenObtainPair>('/api/auth/token/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Atualizar token de autenticação
 * @param payload Token de refresh
 */
export async function refreshAuthTokenCreate(payload: TokenRefreshRequest): Promise<TokenRefresh> {
  return getApi()<TokenRefresh>('/api/auth/token/refresh/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Listar usuários
 * @param params Parâmetros de paginação e filtro
 */
export async function listAuthUsers(params?: {
  ordering?: string;
  page?: number;
  search?: string;
}): Promise<PaginatedResponse<User>> {
  const queryParams = new URLSearchParams()
  
  if (params?.ordering) queryParams.append('ordering', params.ordering)
  if (params?.page) queryParams.append('page', params.page.toString())
  if (params?.search) queryParams.append('search', params.search)
  
  const queryString = queryParams.toString()
  const url = `/api/auth/users/${queryString ? `?${queryString}` : ''}`
  
  return getApi()<PaginatedResponse<User>>(url, {
    method: 'GET'
  })
}

/**
 * Criar um novo usuário
 * @param payload Dados do usuário
 */
export async function createAuthUser(payload: UserCreatePasswordRetypeRequest): Promise<UserCreatePasswordRetype> {
  return getApi()<UserCreatePasswordRetype>('/api/auth/users/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Obter detalhes de um usuário
 * @param id ID do usuário
 */
export async function retrieveAuthUser(id: number): Promise<User> {
  return getApi()<User>(`/api/auth/users/${id}/`, {
    method: 'GET'
  })
}

/**
 * Atualizar um usuário
 * @param id ID do usuário
 * @param payload Dados do usuário
 */
export async function updateAuthUser(id: number, payload: any): Promise<User> {
  return getApi()<User>(`/api/auth/users/${id}/`, {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente um usuário
 * @param id ID do usuário
 * @param payload Dados parciais do usuário
 */
export async function partialUpdateAuthUser(id: number, payload: any): Promise<User> {
  return getApi()<User>(`/api/auth/users/${id}/`, {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Excluir um usuário
 * @param id ID do usuário
 */
export async function destroyAuthUser(id: number): Promise<void> {
  return getApi()<void>(`/api/auth/users/${id}/`, {
    method: 'DELETE'
  })
}

/**
 * Obter o usuário atual
 */
export async function retrieveAuthUsersMe(): Promise<User> {
  return getApi()<User>('/api/auth/users/me/', {
    method: 'GET'
  })
}

/**
 * Atualizar o usuário atual
 * @param payload Dados do usuário
 */
export async function updateAuthUsersMe(payload: any): Promise<User> {
  return getApi()<User>('/api/auth/users/me/', {
    method: 'PUT',
    body: payload
  })
}

/**
 * Atualizar parcialmente o usuário atual
 * @param payload Dados parciais do usuário
 */
export async function partialUpdateAuthUsersMe(payload: any): Promise<User> {
  return getApi()<User>('/api/auth/users/me/', {
    method: 'PATCH',
    body: payload
  })
}

/**
 * Alterar a senha do usuário atual
 * @param payload Nova senha e confirmação
 */
export async function createAuthUsersSetPassword(payload: SetPasswordRetypeRequest): Promise<void> {
  return getApi()<void>('/api/auth/users/set_password/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Solicitar redefinição de senha
 * @param payload Email do usuário
 */
export async function createAuthUsersResetPassword(payload: SendEmailResetRequest): Promise<void> {
  return getApi()<void>('/api/auth/users/reset_password/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Confirmar redefinição de senha
 * @param payload Nova senha e token
 */
export async function createAuthUsersResetPasswordConfirm(payload: SetNewPasswordRequest): Promise<void> {
  return getApi()<void>('/api/auth/users/reset_password_confirm/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Ativar conta de usuário
 * @param payload UID e token de ativação
 */
export function createAuthUsersActivation(payload: { uid: string; token: string }): Promise<void> {
  return getApi()<void>('/api/auth/users/activation/', {
    method: 'POST',
    body: payload
  })
}

/**
 * Composable para gerenciamento de usuários
 */
export const useUserService = () => {
  const { user: currentUser, isAuthenticated } = useAuth()
  const users = useState<User[]>('users', () => [])
  const isLoading = useState<boolean>('users.loading', () => false)
  const error = useState<string | null>('users.error', () => null)
  
  // Função para buscar todos os usuários
  const fetchUsers = async (params?: {
    ordering?: string;
    page?: number;
    search?: string;
  }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await listAuthUsers(params)
      users.value = response.results
      return response
    } catch (err: any) {
      error.value = err.message || 'Erro ao buscar usuários'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para buscar um usuário específico
  const fetchUser = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const user = await retrieveAuthUser(id)
      return user
    } catch (err: any) {
      error.value = err.message || `Erro ao buscar usuário ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para criar um novo usuário
  const createUser = async (userData: UserCreatePasswordRetypeRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      const newUser = await createAuthUser(userData)
      return newUser
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar usuário'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar um usuário
  const updateUser = async (id: number, userData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedUser = await updateAuthUser(id, userData)
      return updatedUser
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar usuário ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar parcialmente um usuário
  const partialUpdateUser = async (id: number, userData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedUser = await partialUpdateAuthUser(id, userData)
      return updatedUser
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar usuário ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para excluir um usuário
  const deleteUser = async (id: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      await destroyAuthUser(id)
      return true
    } catch (err: any) {
      error.value = err.message || `Erro ao excluir usuário ${id}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para buscar o usuário atual
  const fetchCurrentUser = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const user = await retrieveAuthUsersMe()
      return user
    } catch (err: any) {
      error.value = err.message || 'Erro ao buscar usuário atual'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Função para atualizar o usuário atual
  const updateCurrentUser = async (userData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedUser = await updateAuthUsersMe(userData)
      return updatedUser
    } catch (err: any) {
      error.value = err.message || 'Erro ao atualizar usuário atual'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    users,
    currentUser,
    isLoading,
    error,
    fetchUsers,
    fetchUser,
    createUser,
    updateUser,
    partialUpdateUser,
    deleteUser,
    fetchCurrentUser,
    updateCurrentUser
  }
}
