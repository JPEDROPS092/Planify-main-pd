/**
 * Serviço de usuários - adaptador para o novo sistema de API
 */
import { ref } from 'vue'
import * as authApi from '~/services/api/auth'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'

export const useUserService = () => {
  const { handleApiError, withLoading } = useApiService()
  const { user } = useAuth()
  
  const users = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Carregar todos os usuários
  const fetchUsers = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      users.value = await authApi.listUsers()
      return users.value
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter um usuário pelo ID
  const getUser = async (userId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const userInfo = await authApi.retrieveUser(userId)
      return userInfo
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter o usuário atual
  const getCurrentUser = () => {
    if (user.value) {
      return user.value
    }
    
    // Se não houver usuário no estado, tenta buscar
    return withLoading(async () => {
      try {
        const currentUser = await authApi.retrieveAuthUsersMe()
        return currentUser
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Buscar usuários por nome (para componentes de autocompletar)
  const searchUsers = async (query) => {
    return withLoading(async () => {
      try {
        const results = await authApi.searchUsers(query)
        return results
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar perfil do usuário
  const updateProfile = async (userData) => {
    return withLoading(async () => {
      try {
        const updatedUser = await authApi.updateUserProfile(user.value.id, userData)
        return updatedUser
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar senha do usuário
  const updatePassword = async (passwordData) => {
    return withLoading(async () => {
      try {
        await authApi.updateUserPassword(passwordData)
        return true
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  return {
    users,
    isLoading,
    error,
    fetchUsers,
    getUser,
    getCurrentUser,
    searchUsers,
    updateProfile,
    updatePassword
  }
}
