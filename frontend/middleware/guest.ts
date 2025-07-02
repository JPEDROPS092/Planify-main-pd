import { useAuthStore } from "@/stores/auth";

export default defineNuxtRouteMiddleware((to, from) => {
  // 1. Instancie a store Pinia.
  //    Não é necessário chamar `useAuthStore()` dentro do defineNuxtRouteMiddleware,
  //    pode ser fora se for um middleware global. Mas aqui dentro é mais seguro.
  const authStore = useAuthStore();

  // 2. Verifique o estado `isLoggedIn` da store.
  //    Acessamos diretamente a propriedade computada.
  if (authStore.isLoggedIn) {
    // Se o usuário já está autenticado, redirecione-o do /login para o /dashboard.
    console.log(
      "[Guest Middleware] Usuário autenticado tentando acessar uma página de convidado. Redirecionando para /dashboard."
    );
    return navigateTo("/dashboard");
  }

  // Se não estiver autenticado, não faz nada e permite o acesso à página de convidado.
});
