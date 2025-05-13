import { useApiService } from './api'
import { useAuth } from '~/composables/useAuth'

export interface Project {
  id?: number
  name: string
  description: string
  start_date: string
  end_date: string
  status: string
  budget?: number
  manager?: number
  team_members?: number[]
  created_by?: number
  created_at?: string
  updated_at?: string
}

export const useProjectService = () => {
  const api = useApiService()
  const { getCurrentUser } = useAuth()
  const endpoint = '/api/projects/'

  // Listar todos os projetos
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Listar projetos do usuário atual (como gerente ou membro)
  const getUserProjects = async () => {
    try {
      const currentUser = await getCurrentUser()
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      const params = {
        user: currentUser.id,
        role__in: 'manager,member'
      }
      
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter um projeto específico
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar um novo projeto
  const create = async (project: Project) => {
    try {
      // Garantir que o usuário atual seja adicionado como criador e membro da equipe
      const currentUser = await getCurrentUser()
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Definir o usuário atual como criador do projeto
      project.created_by = currentUser.id
      
      // Garantir que o usuário atual seja adicionado como membro da equipe
      if (!project.team_members) project.team_members = []
      if (!project.team_members.includes(currentUser.id)) {
        project.team_members.push(currentUser.id)
      }
      
      // Se não houver gerente definido, definir o usuário atual como gerente
      if (!project.manager) {
        project.manager = currentUser.id
      }
      
      const response = await api.post(endpoint, project)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar um projeto existente
  const update = async (id: number, project: Project) => {
    try {
      const response = await api.put(`${endpoint}${id}/`, project)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente um projeto
  const patch = async (id: number, partialProject: Partial<Project>) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, partialProject)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Excluir um projeto
  const remove = async (id: number) => {
    try {
      // Verificar se o usuário tem permissão para excluir o projeto
      const currentUser = await getCurrentUser()
      const project = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      if (project.manager !== currentUser.id && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para excluir este projeto')
      }
      
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Obter estatísticas do projeto
  const getStatistics = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/statistics/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Adicionar membro à equipe do projeto
  const addTeamMember = async (projectId: number, userId: number, role: string = 'member') => {
    try {
      const response = await api.post(`${endpoint}${projectId}/members/`, {
        user: userId,
        role: role
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Remover membro da equipe do projeto
  const removeTeamMember = async (projectId: number, userId: number) => {
    try {
      await api.delete(`${endpoint}${projectId}/members/${userId}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  return {
    getAll,
    getUserProjects,
    getById,
    create,
    update,
    patch,
    remove,
    getStatistics,
    addTeamMember,
    removeTeamMember
  }
}
