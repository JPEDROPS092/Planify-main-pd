/**
 * Serviço de usuários - adaptador para o novo sistema de API
 */
import { ref } from 'vue'
import * as authApi from './auth'
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
      const response = await authApi.listUsuarios()
      users.value = response.results
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
      const userInfo = await authApi.retrieveUsuario(userId)
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
        const currentUser = await authApi.retrieveUsuarioAtual()
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
        const results = await authApi.buscarUsuarios(query)
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
        const updatedUser = await authApi.atualizarPerfilUsuario(user.value.id, userData)
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
        await authApi.atualizarSenhaUsuario(passwordData)
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
