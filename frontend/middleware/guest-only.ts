/**
 * Middleware para rotas de visitantes
 * Redireciona usuários autenticados para o dashboard
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const { $auth } = useNuxtApp();
  
  // Verificar se o usuário está autenticado usando o composable de autenticação
  const isAuthenticated = $auth.isAuthenticated;
  
  // Lista de rotas públicas que são apenas para visitantes
  const guestOnlyRoutes = [
    '/auth/login',
    '/auth/registro',
    '/auth/esqueci-senha',
    '/auth/reset-password'
  ];
  
  // Se o usuário está autenticado e a rota é apenas para visitantes, redirecionar para o dashboard
  if (isAuthenticated && (to.meta.guestOnly || guestOnlyRoutes.includes(to.path))) {
    return navigateTo('/dashboard');
  }
});