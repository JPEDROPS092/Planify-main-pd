import { useApiService } from './api'
import { useAuth } from '~/composables/useAuth'
import { useProjectService } from './projectService'

export interface Task {
  id?: number
  title: string
  description: string
  project: number
  assigned_to?: number
  assigned_by?: number
  status: string
  priority: string
  due_date: string
  estimated_hours?: number
  completed_at?: string
  created_at?: string
  updated_at?: string
}

export const useTaskService = () => {
  const api = useApiService()
  const { getCurrentUser } = useAuth()
  const projectService = useProjectService()
  const endpoint = '/api/tasks/'

  // Listar todas as tarefas
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Listar tarefas do usuário atual (atribuídas a ele)
  const getUserTasks = async (params = {}) => {
    try {
      const currentUser = await getCurrentUser()
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      const response = await api.get(endpoint, { 
        params: { 
          assigned_to: currentUser.id,
          ...params
        } 
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter uma tarefa específica
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar uma nova tarefa
  const create = async (task: Task) => {
    try {
      // Obter o usuário atual
      const currentUser = await getCurrentUser()
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Definir o usuário atual como criador da tarefa
      task.assigned_by = currentUser.id
      
      // Se não houver responsável definido, definir o usuário atual como responsável
      if (!task.assigned_to) {
        task.assigned_to = currentUser.id
      }
      
      // Verificar se o responsável pertence à equipe do projeto
      const projectDetails = await projectService.getById(task.project)
      if (task.assigned_to && 
          projectDetails.team_members && 
          !projectDetails.team_members.includes(task.assigned_to)) {
        throw new Error('O responsável deve fazer parte da equipe do projeto')
      }
      
      const response = await api.post(endpoint, task)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar uma tarefa existente
  const update = async (id: number, task: Task) => {
    try {
      // Verificar permissões antes de atualizar
      const currentUser = await getCurrentUser()
      const existingTask = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para atualizar a tarefa
      const projectDetails = await projectService.getById(existingTask.project)
      const isManager = projectDetails.manager === currentUser.id
      const isAssigned = existingTask.assigned_to === currentUser.id
      const isCreator = existingTask.assigned_by === currentUser.id
      
      if (!isManager && !isAssigned && !isCreator && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para atualizar esta tarefa')
      }
      
      const response = await api.put(`${endpoint}${id}/`, task)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente uma tarefa
  const patch = async (id: number, partialTask: Partial<Task>) => {
    try {
      // Verificar permissões antes de atualizar parcialmente
      const currentUser = await getCurrentUser()
      const existingTask = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para atualizar a tarefa
      const projectDetails = await projectService.getById(existingTask.project)
      const isManager = projectDetails.manager === currentUser.id
      const isAssigned = existingTask.assigned_to === currentUser.id
      const isCreator = existingTask.assigned_by === currentUser.id
      
      if (!isManager && !isAssigned && !isCreator && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para atualizar esta tarefa')
      }
      
      const response = await api.patch(`${endpoint}${id}/`, partialTask)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Excluir uma tarefa
  const remove = async (id: number) => {
    try {
      // Verificar permissões antes de excluir
      const currentUser = await getCurrentUser()
      const existingTask = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para excluir a tarefa
      const projectDetails = await projectService.getById(existingTask.project)
      const isManager = projectDetails.manager === currentUser.id
      const isCreator = existingTask.assigned_by === currentUser.id
      
      if (!isManager && !isCreator && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para excluir esta tarefa')
      }
      
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Obter tarefas por projeto
  const getByProject = async (projectId: number, params = {}) => {
    try {
      const response = await api.get(`${endpoint}`, { 
        params: { 
          project: projectId,
          ...params
        } 
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Marcar tarefa como concluída
  const markAsCompleted = async (id: number) => {
    try {
      // Verificar permissões antes de marcar como concluída
      const currentUser = await getCurrentUser()
      const existingTask = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para marcar a tarefa como concluída
      const isAssigned = existingTask.assigned_to === currentUser.id
      const projectDetails = await projectService.getById(existingTask.project)
      const isManager = projectDetails.manager === currentUser.id
      
      if (!isManager && !isAssigned && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para marcar esta tarefa como concluída')
      }
      
      const response = await api.patch(`${endpoint}${id}/`, { 
        status: 'CONCLUIDA',
        completed_at: new Date().toISOString()
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atribuir tarefa a um usuário
  const assignTask = async (id: number, userId: number) => {
    try {
      // Verificar permissões antes de atribuir
      const currentUser = await getCurrentUser()
      const existingTask = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para atribuir a tarefa
      const projectDetails = await projectService.getById(existingTask.project)
      const isManager = projectDetails.manager === currentUser.id
      const isCreator = existingTask.assigned_by === currentUser.id
      
      if (!isManager && !isCreator && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para atribuir esta tarefa')
      }
      
      // Verificar se o usuário atribuído pertence à equipe do projeto
      if (projectDetails.team_members && !projectDetails.team_members.includes(userId)) {
        throw new Error('O responsável deve fazer parte da equipe do projeto')
      }
      
      const response = await api.patch(`${endpoint}${id}/`, { 
        assigned_to: userId
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    getAll,
    getUserTasks,
    getById,
    create,
    update,
    patch,
    remove,
    getByProject,
    markAsCompleted,
    assignTask
  }
}
