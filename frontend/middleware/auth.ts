import { useAuth } from '~/composables/useAuth'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Rotas protegidas que exigem autenticação
  const protectedRoutes = [
    '/projetos', 
    '/tarefas', 
    '/equipes', 
    '/comunicacoes', 
    '/dashboard',
    '/riscos',
    '/documentos',
    '/custos'
  ]
  
  // Rotas públicas que não exigem autenticação
  const publicRoutes = [
    '/login',
    '/register',
    '/forgot-password',
    '/reset-password'
  ]
  
  // Verificar se a rota atual é protegida
  const isProtectedRoute = protectedRoutes.some(route => to.path.startsWith(route))
  const isPublicRoute = publicRoutes.includes(to.path) || to.path === '/'
  
  // Se estamos no lado do cliente
  if (process.client) {
    const { isAuthenticated, checkAuth } = useAuth()
    
    // Verificar autenticação
    await checkAuth()
    
    // Se não está autenticado e a rota é protegida, redirecionar para o login
    if (!isAuthenticated.value && isProtectedRoute) {
      return navigateTo('/login')
    }
    
    // Se está autenticado e está tentando acessar uma rota pública, redirecionar para o dashboard
    if (isAuthenticated.value && isPublicRoute) {
      return navigateTo('/dashboard')
    }
  }
})
