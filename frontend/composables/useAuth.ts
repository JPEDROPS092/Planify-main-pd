import { useQueryClient } from '@tanstack/vue-query'
import { computed } from 'vue'
import { useToast } from './useToast'
import { 
  useAuthJwtCreateCreate, 
  useAuthJwtRefreshCreate, 
  useAuthJwtVerifyCreate,
  useAuthUsersCreate,
  useAuthUsersMeRetrieve 
} from './api/auth/auth'

export const useAuth = () => {
  const queryClient = useQueryClient()
  const { toast } = useToast()
  
  // Estado de autenticação reativo
  const isAuthenticated = computed(() => {
    if (typeof window === 'undefined') return false
    return !!localStorage.getItem('access_token')
  })

  // Query para buscar dados do usuário atual usando Orval
  const { 
    data: user, 
    isLoading: isLoadingUser, 
    error: userError 
  } = useAuthUsersMeRetrieve({
    query: {
      enabled: isAuthenticated,
      staleTime: 5 * 60 * 1000, // 5 minutos
      gcTime: 10 * 60 * 1000, // 10 minutos
      retry: false
    }
  })

  // Mutation para login usando Orval
  const loginMutation = useAuthJwtCreateCreate({
    mutation: {
      onSuccess: (response) => {
        const { access, refresh } = response.data
        
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        
        // Invalidar queries para buscar dados do usuário
        queryClient.invalidateQueries({ queryKey: ['api', 'auth', 'users', 'me'] })
        
        toast({
          title: 'Login realizado com sucesso!',
          description: 'Bem-vindo ao Planify!',
          type: 'success'
        })
      },
      onError: (error: any) => {
        console.error('Login error:', error)
        toast({
          title: 'Erro ao fazer login',
          description: 'Credenciais inválidas. Por favor, verifique seus dados.',
          type: 'error'
        })
      }
    }
  })

  // Mutation para registro usando Orval
  const registerMutation = useAuthUsersCreate({
    mutation: {
      onSuccess: () => {
        toast({
          title: 'Conta criada com sucesso!',
          description: 'Você pode fazer login agora.',
          type: 'success'
        })
      },
      onError: (error: any) => {
        console.error('Registration error:', error)
        
        if (error?.response?.data) {
          const errorData = error.response.data
          
          if (errorData.username) {
            toast({
              title: 'Erro no nome de usuário',
              description: Array.isArray(errorData.username) ? errorData.username.join(', ') : errorData.username,
              type: 'error'
            })
          } else if (errorData.email) {
            toast({
              title: 'Erro no email',
              description: Array.isArray(errorData.email) ? errorData.email.join(', ') : errorData.email,
              type: 'error'
            })
          } else if (errorData.password) {
            toast({
              title: 'Erro na senha',
              description: Array.isArray(errorData.password) ? errorData.password.join(', ') : errorData.password,
              type: 'error'
            })
          } else if (errorData.non_field_errors) {
            toast({
              title: 'Erro de validação',
              description: errorData.non_field_errors.join(', '),
              type: 'error'
            })
          } else {
            toast({
              title: 'Erro ao criar conta',
              description: 'Verifique os dados informados e tente novamente.',
              type: 'error'
            })
          }
        } else {
          toast({
            title: 'Erro ao criar conta',
            description: 'Ocorreu um erro inesperado. Tente novamente.',
            type: 'error'
          })
        }
      }
    }
  })

  // Mutation para refresh do token usando Orval
  const refreshMutation = useAuthJwtRefreshCreate({
    mutation: {
      onSuccess: (response) => {
        localStorage.setItem('access_token', response.data.access)
        // Invalidar queries do usuário para refetch com novo token
        queryClient.invalidateQueries({ queryKey: ['api', 'auth', 'users', 'me'] })
      },
      onError: () => {
        logout() // Se refresh falhar, fazer logout
      }
    }
  })

  // Mutation para verificar token usando Orval
  const verifyMutation = useAuthJwtVerifyCreate()

  // Função de login
  const login = async (credentials: { username: string; password: string }) => {
    return loginMutation.mutateAsync({ data: credentials })
  }

  // Função de registro
  const register = async (userData: any) => {
    return registerMutation.mutateAsync({ data: userData })
  }

  // Função de logout
  const logout = async () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    
    // Limpar cache do Vue Query
    queryClient.clear()
    
    // Redirecionar para login usando window.location se necessário
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
    
    toast({
      title: 'Logout realizado com sucesso!',
      type: 'success'
    })
  }

  // Função para refresh do token
  const refreshToken = async () => {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) throw new Error('No refresh token')
    
    return refreshMutation.mutateAsync({ data: { refresh } })
  }

  // Verificar se token é válido
  const verifyToken = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return false

    try {
      await verifyMutation.mutateAsync({ data: { token } })
      return true
    } catch {
      return false
    }
  }

  // Verificar status de autenticação com retry automático
  const checkAuthStatus = async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return false

    try {
      // Verificar se token atual é válido
      await verifyMutation.mutateAsync({ data: { token } })
      return true
    } catch (error) {
      // Token inválido, tentar refresh
      try {
        await refreshToken()
        return true
      } catch (refreshError) {
        await logout()
        return false
      }
    }
  }

  return {
    // Estado
    user,
    isAuthenticated,
    isLoadingUser,
    userError,
    
    // Loading states das mutations
    isLoggingIn: computed(() => loginMutation.isPending),
    isRegistering: computed(() => registerMutation.isPending),
    isRefreshing: computed(() => refreshMutation.isPending),
    
    // Funções principais
    login,
    register,
    logout,
    refreshToken,
    verifyToken,
    checkAuthStatus
  }
}
