/**
 * Plugin para interceptar requisições HTTP e adicionar token de autenticação
 * Também trata refresh automático de tokens quando necessário
 */

export default defineNuxtPlugin(() => {
  const { refreshToken, logout } = useAuth()

  // Configurar interceptor para requisições HTTP
  if (typeof window !== 'undefined') {
    // Interceptar fetch nativo
    const originalFetch = window.fetch
    
    window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
      const token = localStorage.getItem('access_token')
      
      // Adicionar token se disponível
      if (token && init?.headers) {
        const headers = new Headers(init.headers)
        headers.set('Authorization', `Bearer ${token}`)
        init = { ...init, headers }
      } else if (token) {
        init = {
          ...init,
          headers: {
            ...init?.headers,
            'Authorization': `Bearer ${token}`
          }
        }
      }
      
      try {
        const response = await originalFetch(input, init)
        
        // Se response for 401, tentar refresh do token
        if (response.status === 401 && token) {
          try {
            await refreshToken()
            
            // Repetir requisição com novo token
            const newToken = localStorage.getItem('access_token')
            if (newToken && init) {
              const headers = new Headers(init.headers)
              headers.set('Authorization', `Bearer ${newToken}`)
              return originalFetch(input, { ...init, headers })
            }
          } catch (refreshError) {
            // Se refresh falhar, fazer logout
            await logout()
            throw refreshError
          }
        }
        
        return response
      } catch (error) {
        throw error
      }
    }
  }
})
