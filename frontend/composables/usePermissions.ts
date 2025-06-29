import { computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { useAuth } from './useAuth'

export interface Permission {
  id: number
  name: string
  codename: string
  content_type: string
}

export interface UserPermissions {
  permissions: Permission[]
  groups: string[]
  is_superuser: boolean
  is_staff: boolean
}

export const usePermissions = () => {
  const { user, isAuthenticated } = useAuth()

  // Query para buscar permissões do usuário
  const { data: userPermissions, isLoading } = useQuery({
    queryKey: ['user-permissions'],
    queryFn: async (): Promise<UserPermissions> => {
      const response = await $fetch('/api/users/admin/users/permissions/')
      return response
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000, // Cache por 5 minutos
  })

  // Função para verificar se o usuário tem uma permissão específica
  const hasPermission = (permission: string): boolean => {
    if (!userPermissions.value) return false
    
    // Super usuários têm todas as permissões
    if (userPermissions.value.is_superuser) return true
    
    // Verificar se tem a permissão específica
    return userPermissions.value.permissions.some(
      p => p.codename === permission || p.name === permission
    )
  }

  // Função para verificar múltiplas permissões (AND)
  const hasAllPermissions = (permissions: string[]): boolean => {
    return permissions.every(permission => hasPermission(permission))
  }

  // Função para verificar se tem pelo menos uma das permissões (OR)
  const hasAnyPermission = (permissions: string[]): boolean => {
    return permissions.some(permission => hasPermission(permission))
  }

  // Função para verificar se é admin
  const isAdmin = computed(() => {
    return userPermissions.value?.is_staff || userPermissions.value?.is_superuser || false
  })

  // Função para verificar se pertence a um grupo
  const hasGroup = (groupName: string): boolean => {
    if (!userPermissions.value) return false
    return userPermissions.value.groups.includes(groupName)
  }

  // Permissões específicas do sistema
  const canViewUsers = computed(() => hasPermission('view_user'))
  const canCreateUsers = computed(() => hasPermission('add_user'))
  const canEditUsers = computed(() => hasPermission('change_user'))
  const canDeleteUsers = computed(() => hasPermission('delete_user'))

  const canViewProjects = computed(() => hasPermission('view_projeto'))
  const canCreateProjects = computed(() => hasPermission('add_projeto'))
  const canEditProjects = computed(() => hasPermission('change_projeto'))
  const canDeleteProjects = computed(() => hasPermission('delete_projeto'))

  const canViewTasks = computed(() => hasPermission('view_tarefa'))
  const canCreateTasks = computed(() => hasPermission('add_tarefa'))
  const canEditTasks = computed(() => hasPermission('change_tarefa'))
  const canDeleteTasks = computed(() => hasPermission('delete_tarefa'))

  const canViewTeams = computed(() => hasPermission('view_equipe'))
  const canCreateTeams = computed(() => hasPermission('add_equipe'))
  const canEditTeams = computed(() => hasPermission('change_equipe'))
  const canDeleteTeams = computed(() => hasPermission('delete_equipe'))

  const canViewDocuments = computed(() => hasPermission('view_documento'))
  const canCreateDocuments = computed(() => hasPermission('add_documento'))
  const canEditDocuments = computed(() => hasPermission('change_documento'))
  const canDeleteDocuments = computed(() => hasPermission('delete_documento'))

  const canViewCosts = computed(() => hasPermission('view_custo'))
  const canCreateCosts = computed(() => hasPermission('add_custo'))
  const canEditCosts = computed(() => hasPermission('change_custo'))
  const canDeleteCosts = computed(() => hasPermission('delete_custo'))

  const canViewRisks = computed(() => hasPermission('view_risco'))
  const canCreateRisks = computed(() => hasPermission('add_risco'))
  const canEditRisks = computed(() => hasPermission('change_risco'))
  const canDeleteRisks = computed(() => hasPermission('delete_risco'))

  return {
    // Estado
    userPermissions,
    isLoading,
    isAdmin,

    // Funções de verificação
    hasPermission,
    hasAllPermissions,
    hasAnyPermission,
    hasGroup,

    // Permissões específicas
    canViewUsers,
    canCreateUsers,
    canEditUsers,
    canDeleteUsers,

    canViewProjects,
    canCreateProjects,
    canEditProjects,
    canDeleteProjects,

    canViewTasks,
    canCreateTasks,
    canEditTasks,
    canDeleteTasks,

    canViewTeams,
    canCreateTeams,
    canEditTeams,
    canDeleteTeams,

    canViewDocuments,
    canCreateDocuments,
    canEditDocuments,
    canDeleteDocuments,

    canViewCosts,
    canCreateCosts,
    canEditCosts,
    canDeleteCosts,

    canViewRisks,
    canCreateRisks,
    canEditRisks,
    canDeleteRisks,
  }
}