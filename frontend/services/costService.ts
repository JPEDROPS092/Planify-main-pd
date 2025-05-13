import { useApiService } from './api'

export interface Cost {
  id?: number
  title: string
  description: string
  project: number
  amount: number
  category: string
  date: string
  status: string
  responsible?: number
  receipt?: string
  created_at?: string
  updated_at?: string
}

export const useCostService = () => {
  const api = useApiService()
  const endpoint = '/api/costs/'

  // Listar todos os custos
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter um custo específico
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar um novo custo
  const create = async (cost: Cost) => {
    try {
      // Se houver um arquivo de recibo, usamos FormData
      if (cost.receipt && typeof cost.receipt !== 'string') {
        const formData = new FormData()
        Object.keys(cost).forEach(key => {
          if (key === 'receipt') {
            formData.append(key, cost[key])
          } else {
            formData.append(key, cost[key])
          }
        })
        
        const response = await api.post(endpoint, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.post(endpoint, cost)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Atualizar um custo existente
  const update = async (id: number, cost: Cost) => {
    try {
      // Se houver um arquivo de recibo, usamos FormData
      if (cost.receipt && typeof cost.receipt !== 'string') {
        const formData = new FormData()
        Object.keys(cost).forEach(key => {
          if (key === 'receipt') {
            formData.append(key, cost[key])
          } else {
            formData.append(key, cost[key])
          }
        })
        
        const response = await api.put(`${endpoint}${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.put(`${endpoint}${id}/`, cost)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente um custo
  const patch = async (id: number, partialCost: Partial<Cost>) => {
    try {
      // Se houver um arquivo de recibo, usamos FormData
      if (partialCost.receipt && typeof partialCost.receipt !== 'string') {
        const formData = new FormData()
        Object.keys(partialCost).forEach(key => {
          if (key === 'receipt') {
            formData.append(key, partialCost[key])
          } else {
            formData.append(key, partialCost[key])
          }
        })
        
        const response = await api.patch(`${endpoint}${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.patch(`${endpoint}${id}/`, partialCost)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Excluir um custo
  const remove = async (id: number) => {
    try {
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Aprovar um custo
  const approve = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { status: 'APROVADO' })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Rejeitar um custo
  const reject = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { status: 'REJEITADO' })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter custos por projeto
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

  // Obter resumo de custos por projeto
  const getProjectCostSummary = async (projectId: number) => {
    try {
      const response = await api.get(`/api/projects/${projectId}/cost-summary/`)
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
    approve,
    reject,
    getByProject,
    getProjectCostSummary
  }
}
