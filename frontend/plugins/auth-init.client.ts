import { defineNuxtPlugin } from "#imports";
import { useAuthStore } from "@/stores/auth";

export default defineNuxtPlugin(async (nuxtApp) => {
  console.log(
    "[auth-init.ts plugin] Rodando plugin de inicialização de autenticação..."
  );

  // Aguarda a conclusão da store antes de permitir que a aplicação continue
  const authStore = useAuthStore();
  await authStore.initialize();

  console.log("[auth-init.ts plugin] Inicialização de autenticação concluída");

  // Expõe algumas funções úteis para o resto da aplicação
  return {
    provide: {
      auth: {
        // Funções que podem ser úteis em outros lugares da aplicação
        login: async (token: string, refreshToken?: string) => {
          authStore.setTokens(token, refreshToken);
          await authStore.initialize();
        },
        logout: () => {
          authStore.logout();
        },
      },
    },
  };
});
