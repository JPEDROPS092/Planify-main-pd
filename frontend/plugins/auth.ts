import { defineNuxtPlugin, navigateTo, useRoute } from '#app';
import { useAuth } from '~/composables/useAuth';

export default defineNuxtPlugin(async (nuxtApp) => {
  const { checkAuth, isAuthenticated } = useAuth();
  const route = useRoute();

  // Verificar autenticação ao iniciar a aplicação
  if (process.client) {
    try {
      await checkAuth();
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error);
    }
  }

  // Middleware global para verificar autenticação em rotas protegidas
  nuxtApp.hook('app:created', () => {
    nuxtApp.hook('page:start', async () => {
      // Rotas públicas que não precisam de autenticação
      const publicRoutes = [
        '/login',
        '/register',
        '/forgot-password',
        '/reset-password',
      ];

      // Se a rota atual não é pública e o usuário não está autenticado, redirecionar para login
      if (!publicRoutes.includes(route.path) && !isAuthenticated.value) {
        return navigateTo('/login');
      }

      // Se o usuário está autenticado e está tentando acessar uma página de autenticação, redirecionar para dashboard
      if (publicRoutes.includes(route.path) && isAuthenticated.value) {
        return navigateTo('/dashboard');
      }
    });
  });
});
