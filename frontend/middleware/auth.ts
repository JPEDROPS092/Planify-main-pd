import { useAuth } from '~/stores/composables/useAuth';

/**
 * Middleware de autenticação
 * Protege rotas que requerem autenticação
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const { $auth } = useNuxtApp();
  
  // Verificar se o usuário está autenticado usando o composable de autenticação
  const isAuthenticated = $auth.isAuthenticated;
  
  // Rotas protegidas que exigem autenticação
  const protectedRoutes = [
    '/projetos',
    '/tarefas',
    '/equipes',
    '/comunicacoes',
    '/dashboard',
    '/riscos',
    '/documentos',
    '/custos',
    '/perfil',
  ];

  // Rotas públicas que não exigem autenticação
  const publicRoutes = [
    '/auth/login',
    '/auth/registro',
    '/auth/esqueci-senha',
    '/auth/reset-password',
    '/', // Página inicial
  ];

  // Verificar se a rota atual é protegida
  const isProtectedRoute = protectedRoutes.some((route) =>
    to.path.startsWith(route)
  );
  const isPublicRoute = publicRoutes.includes(to.path) || to.path === '/';

  // Se não está autenticado e a rota é protegida, redirecionar para o login
  if (!isAuthenticated && isProtectedRoute) {
    console.log(
      'Redirecionando para login: usuário não autenticado em rota protegida'
    );
    // Preservar a rota original como parâmetro de query para redirecionamento após login
    return navigateTo({
      path: '/auth/login',
      query: { redirect: to.fullPath }
    });
  }

  // Se está autenticado e está tentando acessar uma rota pública, redirecionar para o dashboard
  if (isAuthenticated && isPublicRoute) {
    console.log(
      'Redirecionando para dashboard: usuário autenticado em rota pública'
    );
    return navigateTo('/dashboard');
  }

  // Verificação baseada em metadados de rota
  // Se a rota requer autenticação explicitamente e o usuário não está autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Armazenar a rota original para redirecionar após o login
    const query = { redirect: to.fullPath };
    return navigateTo({ path: '/auth/login', query });
  }

  // Se a rota é só para visitantes e o usuário está autenticado
  if (to.meta.guestOnly && isAuthenticated) {
    return navigateTo('/dashboard');
  }
});
