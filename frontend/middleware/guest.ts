import { useAuth } from '~/composables/useAuth';

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { isAuthenticated, fetchUser } = useAuth();

  // Garante que o estado do usuário seja verificado
  if (!isAuthenticated.value) {
    await fetchUser();
  }

  // Se o usuário estiver autenticado, redireciona para o dashboard
  if (isAuthenticated.value) {
    return navigateTo('/dashboard');
  }
});
