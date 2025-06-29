/**
 * Middleware para redirecionar usuários autenticados para o dashboard
 * Deve ser usado em páginas de login e registro
 */
export default defineNuxtRouteMiddleware(() => {
  const { isAuthenticated } = useAuth()
  
  // Verificar no lado cliente apenas
  if (typeof window === 'undefined') {
    return
  }
  
  // Se está autenticado, redireciona para dashboard
  if (isAuthenticated.value) {
    return navigateTo('/dashboard')
  }
})
