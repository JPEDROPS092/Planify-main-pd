/**
 * Serviço de usuários do Planify
 * Fornece funções para gerenciamento de usuários
 */
import { ref, computed } from 'vue'
import { useState } from '#imports'
import { 
  listAuthUsers, 
  retrieveAuthUser, 
  createAuthUser, 
  updateAuthUser, 
  partialUpdateAuthUser, 
  destroyAuthUser, 
  retrieveAuthUsersMe, 
  updateAuthUsersMe, 
  createAuthUsersSetPassword 
} from './auth'
import { useAuth } from './auth'
import type { 
  User, 
  UserCreatePasswordRetypeRequest, 
  SetPasswordRetypeRequest 
} from './types'

/**
 * Busca usuários com filtros opcionais
 * @param params Parâmetros de filtro e paginação
 * @returns Lista paginada de usuários
 */
export async function searchUsers(params?: {
  search?: string;
  ordering?: string;
  page?: number;
}) {
  return listAuthUsers(params)
}

/**
 * Composable para gerenciamento de usuários
 * Fornece estado reativo e métodos para gerenciar usuários
 */
export const useUserService = () => {
  const { user } = useAuth()
  
  const users = ref<User[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  /**
   * Carrega todos os usuários
   * @param params Parâmetros de filtro e paginação
   * @returns Lista de usuários
   */
  const fetchUsers = async (params?: { search?: string }) => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await listAuthUsers(params)
      users.value = response.results
      return users.value
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar usuários'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Obtém um usuário pelo ID
   * @param userId ID do usuário
   * @returns Dados do usuário
   */
  const getUser = async (userId: number) => {
    isLoading.value = true
    error.value = null
    
    try {
      const userData = await retrieveAuthUser(userId)
      return userData
    } catch (err: any) {
      error.value = err.message || `Erro ao carregar usuário #${userId}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Obtém o usuário atual
   * @returns Dados do usuário atual
   */
  const getCurrentUser = async () => {
    if (user.value) return user.value
    
    isLoading.value = true
    error.value = null
    
    try {
      const userData = await retrieveAuthUsersMe()
      user.value = userData
      return userData
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar usuário atual'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Cria um novo usuário
   * @param userData Dados do usuário
   * @returns Usuário criado
   */
  const createUser = async (userData: UserCreatePasswordRetypeRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      const newUser = await createAuthUser(userData)
      users.value = [...users.value, newUser]
      return newUser
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar usuário'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Atualiza um usuário
   * @param userId ID do usuário
   * @param userData Dados do usuário
   * @returns Usuário atualizado
   */
  const updateUser = async (userId: number, userData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedUser = await updateAuthUser(userId, userData)
      
      // Atualizar a lista local
      users.value = users.value.map(u => 
        u.id === userId ? updatedUser : u
      )
      
      // Atualizar o usuário atual se for o mesmo
      if (user.value && user.value.id === userId) {
        user.value = updatedUser
      }
      
      return updatedUser
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar usuário #${userId}`
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Atualiza o perfil do usuário atual
   * @param userData Dados do perfil
   * @returns Usuário atualizado
   */
  const updateProfile = async (userData: any) => {
    isLoading.value = true
    error.value = null
    
    try {
      const updatedUser = await updateAuthUsersMe(userData)
      user.value = updatedUser
      return updatedUser
    } catch (err: any) {
      error.value = err.message || 'Erro ao atualizar perfil'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Altera a senha do usuário atual
   * @param passwordData Dados da senha
   * @returns true se a senha foi alterada com sucesso
   */
  const updatePassword = async (passwordData: SetPasswordRetypeRequest) => {
    isLoading.value = true
    error.value = null
    
    try {
      await createAuthUsersSetPassword(passwordData)
      return true
    } catch (err: any) {
      error.value = err.message || 'Erro ao alterar senha'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    users,
    isLoading,
    error,
    fetchUsers,
    getUser,
    getCurrentUser,
    createUser,
    updateUser,
    updateProfile,
    updatePassword
  }
}
