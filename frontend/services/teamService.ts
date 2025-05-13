import { useApiService } from './api'
import { useAuth } from '~/composables/useAuth'
import { useProjectService } from './projectService'

export interface TeamMember {
  id?: number
  user: number
  role: string
  joined_at?: string
}

export interface Team {
  id?: number
  name: string
  description: string
  project: number
  members: TeamMember[]
  created_by?: number
  created_at?: string
  updated_at?: string
}

export const useTeamService = () => {
  const api = useApiService()
  const { getCurrentUser } = useAuth()
  const projectService = useProjectService()
  const endpoint = '/api/teams/'

  // Listar todas as equipes
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Listar equipes do usuário atual
  const getUserTeams = async () => {
    try {
      const currentUser = await getCurrentUser()
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      const response = await api.get(`${endpoint}user-teams/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter uma equipe específica
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar uma nova equipe
  const create = async (team: Team) => {
    try {
      // Obter o usuário atual
      const currentUser = await getCurrentUser()
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Definir o usuário atual como criador da equipe
      team.created_by = currentUser.id
      
      // Verificar se o usuário tem permissão para criar equipe no projeto
      const projectDetails = await projectService.getById(team.project)
      const isManager = projectDetails.manager === currentUser.id
      
      if (!isManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para criar equipes neste projeto')
      }
      
      // Garantir que o usuário atual seja adicionado como membro da equipe com papel de gerente
      if (!team.members) team.members = []
      
      // Verificar se o usuário já está na equipe
      const userAlreadyInTeam = team.members.some(member => member.user === currentUser.id)
      
      if (!userAlreadyInTeam) {
        team.members.push({
          user: currentUser.id,
          role: 'manager'
        })
      }
      
      const response = await api.post(endpoint, team)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar uma equipe existente
  const update = async (id: number, team: Team) => {
    try {
      // Verificar permissões antes de atualizar
      const currentUser = await getCurrentUser()
      const existingTeam = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para atualizar a equipe
      const projectDetails = await projectService.getById(existingTeam.project)
      const isProjectManager = projectDetails.manager === currentUser.id
      
      // Verificar se o usuário é gerente da equipe
      const isTeamManager = existingTeam.members.some(
        member => member.user === currentUser.id && member.role === 'manager'
      )
      
      if (!isProjectManager && !isTeamManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para atualizar esta equipe')
      }
      
      const response = await api.put(`${endpoint}${id}/`, team)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente uma equipe
  const patch = async (id: number, partialTeam: Partial<Team>) => {
    try {
      // Verificar permissões antes de atualizar parcialmente
      const currentUser = await getCurrentUser()
      const existingTeam = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para atualizar a equipe
      const projectDetails = await projectService.getById(existingTeam.project)
      const isProjectManager = projectDetails.manager === currentUser.id
      
      // Verificar se o usuário é gerente da equipe
      const isTeamManager = existingTeam.members.some(
        member => member.user === currentUser.id && member.role === 'manager'
      )
      
      if (!isProjectManager && !isTeamManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para atualizar esta equipe')
      }
      
      const response = await api.patch(`${endpoint}${id}/`, partialTeam)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Excluir uma equipe
  const remove = async (id: number) => {
    try {
      // Verificar permissões antes de excluir
      const currentUser = await getCurrentUser()
      const existingTeam = await getById(id)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para excluir a equipe
      const projectDetails = await projectService.getById(existingTeam.project)
      const isProjectManager = projectDetails.manager === currentUser.id
      
      if (!isProjectManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para excluir esta equipe')
      }
      
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Adicionar membro à equipe
  const addMember = async (teamId: number, userId: number, role: string = 'member') => {
    try {
      // Verificar permissões antes de adicionar membro
      const currentUser = await getCurrentUser()
      const existingTeam = await getById(teamId)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para adicionar membros à equipe
      const projectDetails = await projectService.getById(existingTeam.project)
      const isProjectManager = projectDetails.manager === currentUser.id
      
      // Verificar se o usuário é gerente da equipe
      const isTeamManager = existingTeam.members.some(
        member => member.user === currentUser.id && member.role === 'manager'
      )
      
      if (!isProjectManager && !isTeamManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para adicionar membros a esta equipe')
      }
      
      // Verificar se o usuário já está na equipe
      const userAlreadyInTeam = existingTeam.members.some(member => member.user === userId)
      
      if (userAlreadyInTeam) {
        throw new Error('Este usuário já é membro da equipe')
      }
      
      const response = await api.post(`${endpoint}${teamId}/members/`, {
        user: userId,
        role: role
      })
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Remover membro da equipe
  const removeMember = async (teamId: number, memberId: number) => {
    try {
      // Verificar permissões antes de remover membro
      const currentUser = await getCurrentUser()
      const existingTeam = await getById(teamId)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para remover membros da equipe
      const projectDetails = await projectService.getById(existingTeam.project)
      const isProjectManager = projectDetails.manager === currentUser.id
      
      // Verificar se o usuário é gerente da equipe
      const isTeamManager = existingTeam.members.some(
        member => member.user === currentUser.id && member.role === 'manager'
      )
      
      if (!isProjectManager && !isTeamManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para remover membros desta equipe')
      }
      
      // Verificar se está tentando remover o último gerente
      const memberToRemove = existingTeam.members.find(member => member.id === memberId)
      if (memberToRemove && memberToRemove.role === 'manager') {
        const managerCount = existingTeam.members.filter(member => member.role === 'manager').length
        if (managerCount <= 1) {
          throw new Error('Não é possível remover o último gerente da equipe')
        }
      }
      
      await api.delete(`${endpoint}${teamId}/members/${memberId}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Obter equipes por projeto
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

  // Atualizar papel de um membro na equipe
  const updateMemberRole = async (teamId: number, memberId: number, role: string) => {
    try {
      // Verificar permissões antes de atualizar papel
      const currentUser = await getCurrentUser()
      const existingTeam = await getById(teamId)
      
      if (!currentUser) throw new Error('Usuário não autenticado')
      
      // Verificar se o usuário tem permissão para atualizar papéis na equipe
      const projectDetails = await projectService.getById(existingTeam.project)
      const isProjectManager = projectDetails.manager === currentUser.id
      
      // Verificar se o usuário é gerente da equipe
      const isTeamManager = existingTeam.members.some(
        member => member.user === currentUser.id && member.role === 'manager'
      )
      
      if (!isProjectManager && !isTeamManager && !currentUser.is_staff) {
        throw new Error('Você não tem permissão para atualizar papéis nesta equipe')
      }
      
      // Verificar se está tentando rebaixar o último gerente
      const memberToUpdate = existingTeam.members.find(member => member.id === memberId)
      if (memberToUpdate && memberToUpdate.role === 'manager' && role !== 'manager') {
        const managerCount = existingTeam.members.filter(member => member.role === 'manager').length
        if (managerCount <= 1) {
          throw new Error('Não é possível rebaixar o último gerente da equipe')
        }
      }
      
      const response = await api.patch(`${endpoint}${teamId}/members/${memberId}/`, {
        role: role
      })
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    getAll,
    getUserTeams,
    getById,
    create,
    update,
    patch,
    remove,
    addMember,
    removeMember,
    getByProject,
    updateMemberRole
  }
}
