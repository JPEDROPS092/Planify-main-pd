import { useAuth } from '~/composables/useAuth';

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isAuthenticated, refreshAuthToken, accessToken, checkAuth } =
    useAuth();

  // Verifica se há token no localStorage mas não no estado (caso de recarga da página)
  if (!accessToken.value && process.client) {
    const storedToken = localStorage.getItem('auth_token');
    if (storedToken) {
      // Sincronizar o token do localStorage com o estado
      accessToken.value = storedToken;

      // Verificar se o token é válido tentando obter os dados do usuário
      try {
        await checkAuth();
      } catch (error) {
        console.error('Erro ao verificar token:', error);
        try {
          // Tentar renovar o token usando o refresh token
          await refreshAuthToken();
        } catch (refreshError) {
          console.error('Erro ao renovar token:', refreshError);
        }
      }
    }
  }

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
  ];

  // Rotas públicas que não exigem autenticação
  const publicRoutes = [
    '/login',
    '/register',
    '/forgot-password',
    '/reset-password',
  ];

  // Verificar se a rota atual é protegida
  const isProtectedRoute = protectedRoutes.some((route) =>
    to.path.startsWith(route)
  );
  const isPublicRoute = publicRoutes.includes(to.path) || to.path === '/';

  // Apenas se estivermos no lado do cliente
  if (process.client) {
    // Não precisamos chamar useAuth novamente pois já temos a instância acima

    // Verificar autenticação novamente para garantir
    const isAuthValid = await checkAuth();

    console.log('Middleware de autenticação:', {
      isAuthValid,
      isAuthenticated: isAuthenticated.value,
      path: to.path,
      isProtectedRoute,
      isPublicRoute,
    });

    // Se não está autenticado e a rota é protegida, redirecionar para o login
    if (!isAuthenticated.value && isProtectedRoute) {
      console.log(
        'Redirecionando para login: usuário não autenticado em rota protegida'
      );
      return navigateTo('/login');
    }

    // Se está autenticado e está tentando acessar uma rota pública, redirecionar para o dashboard
    if (isAuthenticated.value && isPublicRoute) {
      console.log(
        'Redirecionando para dashboard: usuário autenticado em rota pública'
      );
      return navigateTo('/dashboard');
    }
  }
});
