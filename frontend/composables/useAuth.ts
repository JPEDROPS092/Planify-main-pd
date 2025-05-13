import { ref, computed } from 'vue'
import axios from 'axios'
import { useApiService, ApiError } from '~/services/api'
import { useState } from '#imports'

export const useAuth = () => {
  // Usar useState para persistir o estado do usuário entre componentes
  const user = useState('user', () => null)
  const isAuthenticated = computed(() => !!user.value)
  const isLoading = ref(false)
  const error = ref('')
  
  // Usar o serviço de API
  const apiService = useApiService()

  // Verificar se o usuário está autenticado
  const checkAuth = async () => {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      isAuthenticated.value = false
      user.value = null
      return false
    }

    try {
      isLoading.value = true
      
      // Usando o serviço de API para verificar autenticação
      const userData = await apiService.checkAuth()
      user.value = userData
      return true
    } catch (err) {
      console.error('Erro ao verificar autenticação:', err)
      
      // Tratamento de erro específico
      if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
        localStorage.removeItem('auth_token')
      }
      
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fazer login
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = ''
    
    try {
      // Usando o serviço de API para login
      const success = await apiService.login(email, password)
      
      if (success) {
        await checkAuth()
        return true
      }
      return false
    } catch (err) {
      console.error('Erro ao fazer login:', err)
      
      // Tratamento de erro específico
      if (err instanceof ApiError) {
        if (err.status === 401) {
          error.value = 'Credenciais inválidas. Por favor, verifique seu email e senha.'
        } else if (err.status === 400) {
          // Extrair mensagens de erro do backend se disponíveis
          if (err.data && typeof err.data === 'object') {
            const errorMessages = Object.values(err.data)
              .flat()
              .filter(msg => typeof msg === 'string')
              .join('. ')
            
            error.value = errorMessages || 'Dados de login inválidos. Por favor, verifique as informações.'
          } else {
            error.value = 'Dados de login inválidos. Por favor, verifique as informações.'
          }
        } else {
          error.value = err.friendlyMessage
        }
      } else {
        error.value = 'Credenciais inválidas. Por favor, tente novamente.'
      }
      
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fazer logout
  const logout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('refresh_token')
    user.value = null
    navigateTo('/login')
  }
  
  // Atualizar token usando refresh token
  const refreshToken = async () => {
    try {
      return await apiService.refreshToken()
    } catch (err) {
      console.error('Erro ao atualizar token:', err)
      return false
    }
  }

  // Obter o usuário atual
  const getCurrentUser = () => {
    if (user.value) return user.value;
    return checkAuth().then(() => user.value);
  }
  
  // Verificar se o usuário tem permissão para acessar um recurso
  const hasPermission = (resource, action) => {
    if (!user.value) return false;
    
    // Administradores têm acesso a tudo
    if (user.value.is_staff) return true;
    
    // Verificações específicas por tipo de recurso
    switch (resource) {
      case 'project':
        // Verificar se o usuário é gerente ou membro do projeto
        return action === 'view' || user.value.role === 'manager';
      case 'task':
        // Qualquer um pode ver tarefas, apenas gerentes podem deletar
        return action !== 'delete' || user.value.role === 'manager';
      default:
        return false;
    }
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    checkAuth,
    refreshToken,
    getCurrentUser,
    hasPermission
  }
}
