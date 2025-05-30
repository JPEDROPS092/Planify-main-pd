/**
 * Serviço de equipes - adaptador para o novo sistema de API
 */
import { ref, computed } from 'vue'
import * as teamsApi from '~/services/api/teams'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'

export const useTeamService = () => {
  const { user, hasPermission } = useAuth()
  const { handleApiError, withLoading } = useApiService()
  
  const teams = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Equipes filtradas para o usuário atual
  const myTeams = computed(() => {
    if (!user.value || !teams.value) return []
    return teams.value.filter(team => 
      team.members.some(member => member.user_id === user.value.id)
    )
  })
  
  // Carregar todas as equipes
  const fetchTeams = async (projectId = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      if (projectId) {
        teams.value = await teamsApi.listTeamsByProject(projectId)
      } else {
        teams.value = await teamsApi.listTeams()
      }
      return teams.value
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter uma equipe pelo ID
  const getTeam = async (teamId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const team = await teamsApi.retrieveTeam(teamId)
      return team
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Criar uma nova equipe
  const createTeam = async (teamData) => {
    return withLoading(async () => {
      try {
        // Associar automaticamente o usuário atual como membro se ele não for incluído
        if (!teamData.members || !teamData.members.some(member => member.user_id === user.value?.id)) {
          teamData.members = [
            ...(teamData.members || []),
            { user_id: user.value?.id, role: 'manager' }
          ]
        }
        
        const newTeam = await teamsApi.createTeam(teamData)
        teams.value = [...teams.value, newTeam]
        return newTeam
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar uma equipe
  const updateTeam = async (teamId, teamData) => {
    return withLoading(async () => {
      try {
        const updatedTeam = await teamsApi.updateTeam(teamId, teamData)
        
        // Atualizar a lista local
        teams.value = teams.value.map(team => 
          team.id === teamId ? updatedTeam : team
        )
        
        return updatedTeam
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Excluir uma equipe
  const deleteTeam = async (teamId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('team', 'delete')) {
          throw new Error('Você não tem permissão para excluir esta equipe')
        }
        
        await teamsApi.destroyTeam(teamId)
        
        // Remover da lista local
        teams.value = teams.value.filter(team => team.id !== teamId)
        
        return true
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Adicionar membro à equipe
  const addTeamMember = async (teamId, memberData) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('team', 'update')) {
          throw new Error('Você não tem permissão para adicionar membros a esta equipe')
        }
        
        const team = await getTeam(teamId)
        
        // Verificar se o usuário já é membro
        if (team.members.some(member => member.user_id === memberData.user_id)) {
          throw new Error('Este usuário já é membro da equipe')
        }
        
        // Adicionar membro
        const updatedTeam = await teamsApi.addTeamMember(teamId, memberData)
        
        // Atualizar a lista local
        teams.value = teams.value.map(team => 
          team.id === teamId ? updatedTeam : team
        )
        
        return updatedTeam
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Remover membro da equipe
  const removeTeamMember = async (teamId, memberId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('team', 'update')) {
          throw new Error('Você não tem permissão para remover membros desta equipe')
        }
        
        await teamsApi.removeTeamMember(teamId, memberId)
        
        // Atualizar a lista local
        const team = await getTeam(teamId)
        teams.value = teams.value.map(t => 
          t.id === teamId ? team : t
        )
        
        return team
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  return {
    teams,
    myTeams,
    isLoading,
    error,
    fetchTeams,
    getTeam,
    createTeam,
    updateTeam,
    deleteTeam,
    addTeamMember,
    removeTeamMember
  }
}
