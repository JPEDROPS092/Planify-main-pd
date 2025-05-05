import { ref } from 'vue'
import axios from 'axios'

export const useAuth = () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const error = ref('')

  // Verificar se o usuário está autenticado
  const checkAuth = async () => {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      isAuthenticated.value = false
      user.value = null
      return false
    }

    try {
      const response = await axios.get('http://localhost:8001/api/auth/users/me/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      
      user.value = response.data
      isAuthenticated.value = true
      return true
    } catch (err) {
      console.error('Erro ao verificar autenticação:', err)
      localStorage.removeItem('auth_token')
      isAuthenticated.value = false
      user.value = null
      return false
    }
  }

  // Fazer login
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = ''
    
    try {
      const response = await axios.post('http://localhost:8001/api/auth/token/', {
        email,
        password
      })
      
      if (response.data.access) {
        localStorage.setItem('auth_token', response.data.access)
        await checkAuth()
        return true
      }
      return false
    } catch (err) {
      console.error('Erro ao fazer login:', err)
      error.value = 'Credenciais inválidas. Por favor, tente novamente.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Fazer logout
  const logout = () => {
    localStorage.removeItem('auth_token')
    isAuthenticated.value = false
    user.value = null
    navigateTo('/login')
  }

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    checkAuth
  }
}
