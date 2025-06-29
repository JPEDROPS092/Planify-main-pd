/**
 * Middleware para proteger rotas que requerem autenticação
 * Verifica se o usuário está autenticado e se o token é válido
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const { isAuthenticated, isLoadingUser, verifyToken, refreshToken, logout } = useAuth()
  
  // Se ainda está carregando, aguarda
  if (isLoadingUser.value) {
    return
  }
  
  // Se não está autenticado, redireciona para login
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
  
  // Validar se token não está expirado
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      return navigateTo('/login')
    }
    
    // Verificar se token é válido
    const isValid = await verifyToken()
    
    if (!isValid) {
      // Tentar refresh do token
      try {
        await refreshToken()
      } catch (error) {
        // Se refresh falhar, fazer logout e redirecionar
        await logout()
        return navigateTo('/login')
      }
    }
  } catch (error) {
    // Em caso de erro, fazer logout e redirecionar
    await logout()
    return navigateTo('/login')
  }
})
