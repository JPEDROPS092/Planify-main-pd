/**
 * Middleware para redirecionar usuários autenticados para o dashboard
 * Deve ser usado em páginas de login e registro
 */
export default defineNuxtRouteMiddleware(() => {
  const { isAuthenticated, isLoadingUser } = useAuth()
  
  // Se ainda está carregando, aguarda
  if (isLoadingUser.value) {
    return
  }
  
  // Se está autenticado, redireciona para dashboard
  if (isAuthenticated.value) {
    return navigateTo('/dashboard')
  }
})
