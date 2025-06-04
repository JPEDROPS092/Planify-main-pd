// Importa o composable de autenticação personalizado
import { useAuth } from '@/composables/useAuth';

/**
 * Middleware de autenticação centralizado
 * Este middleware:
 * 1. Protege rotas que requerem autenticação
 * 2. Impede usuários autenticados de acessar páginas de login/registro
 */
export default defineNuxtRouteMiddleware((to, from) => {
  // Verificar se estamos no lado do cliente para acessar localStorage
  if (process.server) {
    // No SSR, vamos permitir a navegação e deixar o cliente decidir os redirecionamentos
    return;
  }

  // Usar diretamente o composable para evitar problemas com o plugin
  const { isAuthenticated } = useAuth();

  /**
   * Definição de rotas protegidas
   * Estas rotas só podem ser acessadas por usuários autenticados
   */
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

  /**
   * Definição de rotas de autenticação
   * Estas rotas só podem ser acessadas por usuários NÃO autenticados
   */
  const authRoutes = [
    '/auth/login',
    '/auth/registro',
    '/auth/esqueci-senha',
    '/auth/reset-password',
    '/login',
    '/registro'
  ];

  /**
   * Definição de rotas públicas
   * Estas rotas estão acessíveis independente do estado de autenticação
   */
  const publicRoutes = [
    '/', // Página inicial
  ];

  /**
   * Verifica se a rota atual é protegida
   * Utiliza `startsWith` para considerar rotas filhas
   */
  const isProtectedRoute = protectedRoutes.some((route) =>
    to.path.startsWith(route)
  );

  /**
   * Verifica se a rota é uma página de autenticação
   */
  const isAuthRoute = authRoutes.includes(to.path);

  /**
   * Verifica se a rota é explicitamente pública
   */
  const isPublicRoute = publicRoutes.includes(to.path);

  /**
   * CASO 1: Usuário não autenticado tentando acessar rota protegida
   * Redireciona para a tela de login, mantendo a rota original na query.
   */
  if (!isAuthenticated.value && isProtectedRoute) {
    console.log(
      'Redirecionando para login: usuário não autenticado em rota protegida'
    );
    return navigateTo({
      path: '/auth/login',
      query: { redirect: to.fullPath }
    });
  }

  /**
   * CASO 2: Usuário autenticado tentando acessar página de autenticação
   * Redireciona para o dashboard, pois já está logado
   */
  if (isAuthenticated.value && isAuthRoute) {
    console.log(
      'Redirecionando para dashboard: usuário autenticado tentando acessar página de login/registro'
    );
    return navigateTo('/dashboard');
  }

  /**
   * Verificação adicional baseada em metadados da rota
   */
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    const query = { redirect: to.fullPath };
    return navigateTo({ path: '/auth/login', query });
  }

  // Caso contrário, o middleware permite o acesso à rota normalmente
});
