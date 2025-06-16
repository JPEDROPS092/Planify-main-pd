// plugins/auth.ts
export default defineNuxtPlugin(() => {
  // Plugin de autenticação robusto
  const { $api } = useNuxtApp();
  
  // Função para verificar se o usuário está autenticado
  const isAuthenticated = (): boolean => {
    const token = useCookie('auth-token');
    return !!token.value;
  };

  // Função para obter dados do usuário do token (se necessário)
  const getCurrentUser = () => {
    const userCookie = useCookie('auth-user');
    return userCookie.value ? JSON.parse(userCookie.value as string) : null;
  };

  // Função para fazer logout
  const logout = async () => {
    const tokenCookie = useCookie('auth-token');
    const userCookie = useCookie('auth-user');
    
    tokenCookie.value = null;
    userCookie.value = null;
    
    // Redirecionar para a página de login
    await navigateTo('/auth/login');
  };

  // Middleware de autenticação para verificar rotas protegidas
  addRouteMiddleware('auth', (to) => {
    if (!isAuthenticated() && !to.path.startsWith('/auth')) {
      return navigateTo('/auth/login');
    }
  });

  return {
    provide: {
      auth: {
        isAuthenticated,
        getCurrentUser,
        logout,
      }
    }
  };
});
