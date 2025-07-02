import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware((to) => {
  const authStore = useAuthStore(); // Use a store, a fonte da verdade

  // Lista de rotas que NÃO requerem autenticação
  const publicPages = ["/", "/login", "/register"];

  const isAuthRequired = !publicPages.includes(to.path);

  // Se a rota requer autenticação e o usuário não está logado, redirecione
  if (isAuthRequired && !authStore.isLoggedIn) {
    // Adicionar um console.log aqui ajuda a debugar
    console.log(
      `[Auth Middleware] Bloqueado. Redirecionando para /login. Tentou acessar: ${to.path}`
    );

    // Preserve a rota de destino para redirecionamento após login
    const redirectQuery =
      to.path !== "/login" ? `?redirect=${encodeURIComponent(to.path)}` : "";
    return navigateTo(`/login${redirectQuery}`);
  }
});
