export default defineNuxtRouteMiddleware((to, from) => {
  // Se estamos no lado do cliente
  if (process.client) {
    // Verificar se o token existe
    const token = localStorage.getItem('auth_token')
    
    // Se não existe token e a rota requer autenticação, redirecionar para o login
    if (!token && (to.path.startsWith('/projetos') || 
                  to.path.startsWith('/tarefas') || 
                  to.path.startsWith('/equipes') || 
                  to.path.startsWith('/comunicacoes') || 
                  to.path.startsWith('/dashboard'))) {
      return navigateTo('/login')
    }
    
    // Se o usuário está autenticado e está tentando acessar a página inicial, redirecionar para o dashboard
    if (token && (to.path === '/' || to.path === '/login')) {
      return navigateTo('/dashboard')
    }
  }
})
