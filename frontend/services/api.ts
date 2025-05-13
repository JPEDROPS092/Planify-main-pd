import { useNuxtApp } from '#app'

/**
 * Classe para gerenciar erros da API
 */
export class ApiError extends Error {
  status: number
  data: any
  
  constructor(message: string, status: number, data: any = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
  
  /**
   * Retorna uma mensagem amigável baseada no status HTTP
   */
  get friendlyMessage(): string {
    switch (this.status) {
      case 400:
        return 'Dados inválidos. Por favor, verifique as informações enviadas.'
      case 401:
        return 'Sessão expirada ou não autenticado. Por favor, faça login novamente.'
      case 403:
        return 'Você não tem permissão para acessar este recurso.'
      case 404:
        return 'O recurso solicitado não foi encontrado.'
      case 422:
        return 'Não foi possível processar a solicitação. Verifique os dados enviados.'
      case 429:
        return 'Muitas requisições. Por favor, aguarde um momento e tente novamente.'
      case 500:
      case 502:
      case 503:
      case 504:
        return 'Erro no servidor. Por favor, tente novamente mais tarde.'
      default:
        return this.message || 'Ocorreu um erro inesperado. Por favor, tente novamente.'
    }
  }
}

/**
 * Serviço para gerenciar requisições à API
 */
export const useApiService = () => {
  const { $api } = useNuxtApp()
  
  return {
    // Métodos HTTP básicos
    get: async (url: string, params = {}) => {
      try {
        const response = await $api.get(url, { params })
        return response.data
      } catch (error: any) {
        if (error.response) {
          throw new ApiError(
            error.response.data?.detail || 'Erro na requisição',
            error.response.status,
            error.response.data
          )
        }
        throw error
      }
    },
    
    post: async (url: string, data = {}) => {
      try {
        const response = await $api.post(url, data)
        return response.data
      } catch (error: any) {
        if (error.response) {
          throw new ApiError(
            error.response.data?.detail || 'Erro na requisição',
            error.response.status,
            error.response.data
          )
        }
        throw error
      }
    },
    
    put: async (url: string, data = {}, config = {}) => {
      try {
        const response = await $api.put(url, data, config)
        return response.data
      } catch (error: any) {
        if (error.response) {
          throw new ApiError(
            error.response.data?.detail || 'Erro na requisição',
            error.response.status,
            error.response.data
          )
        }
        throw error
      }
    },
    
    patch: async (url: string, data = {}) => {
      try {
        const response = await $api.patch(url, data)
        return response.data
      } catch (error: any) {
        if (error.response) {
          throw new ApiError(
            error.response.data?.detail || 'Erro na requisição',
            error.response.status,
            error.response.data
          )
        }
        throw error
      }
    },
    
    delete: async (url: string) => {
      try {
        const response = await $api.delete(url)
        return response.data
      } catch (error: any) {
        if (error.response) {
          throw new ApiError(
            error.response.data?.detail || 'Erro na requisição',
            error.response.status,
            error.response.data
          )
        }
        throw error
      }
    },
    
    // Métodos específicos para autenticação
    login: async (email: string, password: string) => {
      try {
        const response = await $api.post('/api/auth/token/', { email, password })
        if (response.data.access) {
          localStorage.setItem('auth_token', response.data.access)
          if (response.data.refresh) {
            localStorage.setItem('refresh_token', response.data.refresh)
          }
          return true
        }
        return false
      } catch (error) {
        throw error
      }
    },
    
    // Método para verificar autenticação
    checkAuth: async () => {
      try {
        const response = await $api.get('/api/auth/users/me/')
        return response.data
      } catch (error) {
        throw error
      }
    }
  }
}
