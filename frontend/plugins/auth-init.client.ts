import { defineNuxtPlugin } from "#imports";
import { useAuthStore } from "~/stores/auth";

export default defineNuxtPlugin(async () => {
  console.log("[auth-init.ts plugin] Tentando carregar sessão do cookie...");

  // Only run in client-side
  if (process.client) {
    const authStore = useAuthStore();

    // Try to load user data if we have a token
    if (authStore.accessToken) {
      try {
        const { authUsersMeRetrieve } = await import("~/api/auth/auth");
        const response = await authUsersMeRetrieve({
          headers: {
            Authorization: `Bearer ${authStore.accessToken}`,
          },
        });
        authStore.setUser(response.data);
        console.log("[auth-init.ts plugin] Sessão carregada com sucesso.");
      } catch (error) {
        console.error("[auth-init.ts plugin] Erro ao carregar sessão:", error);
        // If we get here, the token is invalid - clean up
        authStore.logout();
      }
    } else {
      console.log("[auth-init.ts plugin] Nenhum token encontrado.");
    }
  }
});
