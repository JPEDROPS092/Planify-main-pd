/**
 * Middleware para proteger rotas que requerem autenticação
 * Verifica se o usuário está autenticado e se o token é válido
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const { isAuthenticated, checkAuthStatus } = useAuth()
  
  // Verificar no lado cliente apenas
  if (typeof window === 'undefined') {
    return
  }
  
  // Se não está autenticado, redireciona para login
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
  
  // Verificar status de autenticação (inclui verificação e refresh automático)
  try {
    const isValid = await checkAuthStatus()
    
    if (!isValid) {
      return navigateTo('/login')
    }
  } catch (error) {
    console.error('Auth check failed:', error)
    return navigateTo('/login')
  }
})
