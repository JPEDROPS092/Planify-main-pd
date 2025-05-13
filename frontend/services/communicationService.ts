import { useApiService } from './api'

export interface Communication {
  id?: number
  title: string
  content: string
  sender: number
  recipients: number[]
  project?: number
  status: string
  priority: string
  created_at?: string
  updated_at?: string
}

export const useCommunicationService = () => {
  const api = useApiService()
  const endpoint = '/api/communications/'

  // Listar todas as comunicações
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter uma comunicação específica
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar uma nova comunicação
  const create = async (communication: Communication) => {
    try {
      const response = await api.post(endpoint, communication)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar uma comunicação existente
  const update = async (id: number, communication: Communication) => {
    try {
      const response = await api.put(`${endpoint}${id}/`, communication)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente uma comunicação
  const patch = async (id: number, partialCommunication: Partial<Communication>) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, partialCommunication)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Excluir uma comunicação
  const remove = async (id: number) => {
    try {
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Marcar comunicação como lida
  const markAsRead = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { status: 'LIDA' })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter comunicações não lidas
  const getUnread = async () => {
    try {
      const response = await api.get(`${endpoint}`, { 
        params: { status: 'NAO_LIDA' } 
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter comunicações por projeto
  const getByProject = async (projectId: number) => {
    try {
      const response = await api.get(`${endpoint}`, { 
        params: { project: projectId } 
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    getAll,
    getById,
    create,
    update,
    patch,
    remove,
    markAsRead,
    getUnread,
    getByProject
  }
}
