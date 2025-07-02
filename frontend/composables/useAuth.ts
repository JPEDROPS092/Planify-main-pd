import { useAuthStore } from "~/stores/auth";
import { useAuthJwtCreateCreate, authUsersMeRetrieve } from "~/api/auth/auth";
import type { TokenObtainPairRequest } from "~/api/schemas";
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";

export function useAuth() {
  const authStore = useAuthStore();
  const router = useRouter();
  const route = useRoute();

  // Login mutation com tratamento explícito da navegação
  const loginMutation = useAuthJwtCreateCreate({
    mutation: {
      onSuccess: async (response) => {
        console.log(
          "[useAuth] Login bem-sucedido. Resposta da API:",
          response.data
        );

        // 1. Extrair o novo token de acesso DIRETAMENTE da resposta
        const newAccessToken = response.data.access;

        // 2. Salvar os tokens na store para uso futuro
        authStore.setTokens(newAccessToken, response.data.refresh);

        try {
          console.log(
            "[useAuth] Buscando dados do usuário com o novo token..."
          );
          // 3. Fazer a chamada para /me/ passando o novo token MANUALMENTE
          // Isso ignora o interceptor para esta chamada específica
          const userResponse = await authUsersMeRetrieve({
            headers: {
              Authorization: `Bearer ${newAccessToken}`,
            },
          });

          // 4. Salvar os dados do usuário na store
          authStore.setUser(userResponse.data);
          console.log(
            "[useAuth] Dados do usuário salvos na store:",
            userResponse.data.username
          );

          // 5. Redirecionar para a página alvo ou dashboard
          const redirectPath = route.query.redirect?.toString() || "/dashboard";
          await router.replace(redirectPath);
          console.log("[useAuth] Redirecionando para:", redirectPath);
        } catch (fetchError) {
          console.error(
            "[useAuth] Falha ao buscar dados do usuário após login:",
            fetchError
          );
          // Fazer logout para evitar estado inconsistente
          authStore.logout();
        }
      },
      onError: (error) => {
        console.error("[useAuth] Falha na mutação de login:", error);
      },
    },
  });

  /**
   * Função de login que os componentes chamarão para iniciar o processo
   */
  const login = (credentials: TokenObtainPairRequest) => {
    return loginMutation.mutate({ data: credentials });
  };

  const logout = async () => {
    authStore.logout();
    await router.replace("/login");
  };

  return {
    // Estado de autenticação da store
    user: computed(() => authStore.user),
    isAuthenticated: computed(() => authStore.isAuthenticated),

    // Funções
    login,
    logout,

    // Estado da mutação de login
    isLoading: computed(() => loginMutation.isPending.value),
    isError: computed(() => loginMutation.isError.value),
    error: computed(() => loginMutation.error.value),
  };
}
