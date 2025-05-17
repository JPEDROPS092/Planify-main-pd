import { ref, computed } from 'vue'
import { useState } from '#imports'
import { ApiError } from '~/services/api/config'
import { createAuthToken, retrieveAuthUsersMe, refreshAuthTokenCreate } from '~/services/api/auth'

export const useAuth = () => {
  // Usar useState para persistir o estado do usuário entre componentes
  const user = useState('user', () => null)
  const isAuthenticated = computed(() => !!user.value)
  const isLoading = ref(false)
  const error = ref('')
  
  // Tokens de autenticação
  const accessToken = useState<string | null>('auth.accessToken', () => {
    return process.client ? localStorage.getItem('auth_token') : null
  })
  
  const refreshToken = useState<string | null>('auth.refreshToken', () => {
    return process.client ? localStorage.getItem('refresh_token') : null
  })

  // Verificar se o usuário está autenticado
  const checkAuth = async () => {
    if (!accessToken.value) {
      user.value = null
      return false
    }

    try {
      isLoading.value = true
      
      // Usando o novo serviço de API para buscar o usuário atual
      const userData = await retrieveAuthUsersMe()
      user.value = userData
      return true
    } catch (err) {
      console.error('Erro ao verificar autenticação:', err)
      
      // Tratamento de erro específico
      if (err instanceof ApiError && (err.status === 401 || err.status === 403)) {
        if (process.client) {
          localStorage.removeItem('auth_token')
          localStorage.removeItem('refresh_token')
        }
        accessToken.value = null
        refreshToken.value = null
      }
      
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fazer login
  const login = async (credentials: { username: string; password: string }) => {
    isLoading.value = true
    error.value = ''
    
    try {
      // Usando o novo serviço de API para login
      const tokenData = await createAuthToken(credentials)
      
      // Salvar tokens
      if (process.client) {
        localStorage.setItem('auth_token', tokenData.access)
        if (tokenData.refresh) {
          localStorage.setItem('refresh_token', tokenData.refresh)
        }
      }
      
      accessToken.value = tokenData.access
      if (tokenData.refresh) {
        refreshToken.value = tokenData.refresh
      }
      
      // Buscar dados do usuário
      const userData = await retrieveAuthUsersMe()
      user.value = userData
      
      return userData
    } catch (err) {
      console.error('Erro ao fazer login:', err)
      
      if (err instanceof ApiError) {
        error.value = err.message
      } else if (err instanceof Error) {
        error.value = err.message
      } else {
        error.value = 'Ocorreu um erro ao fazer login. Por favor, tente novamente.'
      }
      
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Fazer logout
  const logout = () => {
    if (process.client) {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
    }
    accessToken.value = null
    refreshToken.value = null
    user.value = null
    navigateTo('/login')
  }
  
  // Atualizar token usando refresh token
  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      throw new Error('Refresh token não disponível')
    }
    
    try {
      const tokenData = await refreshAuthTokenCreate({ refresh: refreshToken.value })
      
      if (process.client) {
        localStorage.setItem('auth_token', tokenData.access)
      }
      
      accessToken.value = tokenData.access
      return tokenData.access
    } catch (err) {
      console.error('Erro ao atualizar token:', err)
      
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('refresh_token')
      }
      
      accessToken.value = null
      refreshToken.value = null
      user.value = null
      throw err
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
    accessToken,
    refreshToken,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    checkAuth,
    refreshAuthToken,
    getCurrentUser,
    hasPermission
  }
}
