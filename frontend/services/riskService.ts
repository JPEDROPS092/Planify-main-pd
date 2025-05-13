import { useApiService } from './api'

export interface Risk {
  id?: number
  title: string
  description: string
  project: number
  probability: string
  impact: string
  status: string
  mitigation_plan: string
  contingency_plan?: string
  owner?: number
  identified_at: string
  resolved_at?: string
  created_at?: string
  updated_at?: string
}

export const useRiskService = () => {
  const api = useApiService()
  const endpoint = '/api/risks/'

  // Listar todos os riscos
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter um risco específico
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar um novo risco
  const create = async (risk: Risk) => {
    try {
      const response = await api.post(endpoint, risk)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar um risco existente
  const update = async (id: number, risk: Risk) => {
    try {
      const response = await api.put(`${endpoint}${id}/`, risk)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente um risco
  const patch = async (id: number, partialRisk: Partial<Risk>) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, partialRisk)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Excluir um risco
  const remove = async (id: number) => {
    try {
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Marcar risco como resolvido
  const markAsResolved = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { 
        status: 'RESOLVIDO',
        resolved_at: new Date().toISOString()
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter riscos por projeto
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

  // Obter análise de riscos do projeto
  const getProjectRiskAnalysis = async (projectId: number) => {
    try {
      const response = await api.get(`/api/projects/${projectId}/risk-analysis/`)
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
    markAsResolved,
    getByProject,
    getProjectRiskAnalysis
  }
}
