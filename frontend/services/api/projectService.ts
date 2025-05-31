/**
 * Serviço de projetos - adaptador para o novo sistema de API
 */
import { ref, computed } from 'vue'
import * as projectsApi from './projects'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'

export const useProjectService = () => {
  const { user, hasPermission } = useAuth()
  const { handleApiError, withLoading } = useApiService()
  
  const projects = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Projetos filtrados para o usuário atual
  const myProjects = computed(() => {
    if (!user.value || !projects.value) return []
    return projects.value.filter(project => 
      project.members?.some(member => member.user_id === user.value.id) || 
      project.created_by === user.value.id
    )
  })
  
  // Carregar todos os projetos
  const fetchProjects = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await projectsApi.listProjetos()
      projects.value = response.results
      return projects.value
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter um projeto pelo ID
  const getProject = async (projectId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const project = await projectsApi.retrieveProjeto(projectId)
      return project
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Criar um novo projeto
  const createProject = async (projectData) => {
    return withLoading(async () => {
      try {
        // Associar automaticamente o usuário atual como criador se não estiver definido
        if (!projectData.created_by) {
          projectData.created_by = user.value?.id
        }
        
        // Garantir que o usuário atual seja membro do projeto
        if (!projectData.members || !projectData.members.some(member => member.user_id === user.value?.id)) {
          projectData.members = [
            ...(projectData.members || []),
            { user_id: user.value?.id, role: 'manager' }
          ]
        }
        
        const newProject = await projectsApi.createProjeto(projectData)
        projects.value = [...projects.value, newProject]
        return newProject
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar um projeto
  const updateProject = async (projectId, projectData) => {
    return withLoading(async () => {
      try {
        const updatedProject = await projectsApi.updateProjeto(projectId, projectData)
        
        // Atualizar a lista local
        projects.value = projects.value.map(project => 
          project.id === projectId ? updatedProject : project
        )
        
        return updatedProject
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Excluir um projeto
  const deleteProject = async (projectId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('project', 'delete')) {
          throw new Error('Você não tem permissão para excluir este projeto')
        }
        
        await projectsApi.destroyProjeto(projectId)
        
        // Remover da lista local
        projects.value = projects.value.filter(project => project.id !== projectId)
        
        return true
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Adicionar membro ao projeto
  const addProjectMember = async (projectId, memberData) => {
    return withLoading(async () => {
      try {
        const updatedProject = await projectsApi.adicionarMembroProjeto(projectId, memberData)
        
        // Atualizar a lista local
        projects.value = projects.value.map(project => 
          project.id === projectId ? updatedProject : project
        )
        
        return updatedProject
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Remover membro do projeto
  const removeProjectMember = async (projectId, memberId) => {
    return withLoading(async () => {
      try {
        await projectsApi.removerMembroProjeto(projectId, memberId)
        
        // Atualizar a lista local
        const updatedProject = await getProject(projectId)
        projects.value = projects.value.map(project => 
          project.id === projectId ? updatedProject : project
        )
        
        return updatedProject
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Obter estatísticas do projeto
  const getProjectStats = async (projectId) => {
    return withLoading(async () => {
      try {
        const stats = await projectsApi.getEstatisticasProjeto(projectId)
        return stats
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  return {
    projects,
    myProjects,
    isLoading,
    error,
    fetchProjects,
    getProject,
    createProject,
    updateProject,
    deleteProject,
    addProjectMember,
    removeProjectMember,
    getProjectStats
  }
}
