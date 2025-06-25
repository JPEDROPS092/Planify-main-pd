export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated, isLoading } = useAuth()
  
  // Se ainda está carregando, aguardar
  if (isLoading.value) {
    return
  }
  
  // Se não está autenticado, redirecionar para landing page
  if (!isAuthenticated.value) {
    return navigateTo('/')
  }
})
