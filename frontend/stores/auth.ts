import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { User } from "@/api/schemas";

export const useAuthStore = defineStore("auth", () => {
  // Use useCookie para persistência de token (funciona no SSR e no cliente)
  const accessToken = useCookie<string | null>("auth_token", {
    maxAge: 60 * 60 * 24 * 7, // 7 dias
    default: () => null,
    secure: true,
    sameSite: "strict",
  });

  const refreshToken = useCookie<string | null>("auth_refresh_token", {
    maxAge: 60 * 60 * 24 * 30, // 30 dias
    default: () => null,
    secure: true,
    sameSite: "strict",
  });

  const user = ref<User | null>(null);

  // Computed para verificar se o usuário está logado
  const isLoggedIn = computed(() => !!accessToken.value && !!user.value);

  // Mantendo compatibilidade com código existente
  const isAuthenticated = computed(() => isLoggedIn.value);

  /**
   * Define os tokens de acesso e refresh
   */
  function setTokens(newAccessToken: string, newRefreshToken?: string) {
    accessToken.value = newAccessToken;
    if (newRefreshToken) {
      refreshToken.value = newRefreshToken;
    }
    console.log("Tokens set in store.");
  }

  /**
   * Define os dados do usuário
   */
  function setUser(newUser: User) {
    user.value = newUser;
    console.log("User data set in store:", newUser.username);
  }

  /**
   * Busca as informações do usuário atual (mantido para compatibilidade)
   */
  async function fetchUser() {
    if (!accessToken.value) return;

    try {
      // Importação dinâmica para evitar problemas de SSR
      const { authUsersMeRetrieve } = await import("~/api/auth/auth");
      const response = await authUsersMeRetrieve();

      if (response.data) {
        user.value = response.data;
        console.log("User data fetched and set:", response.data.username);
      } else {
        throw new Error("Dados do usuário não encontrados na resposta.");
      }
    } catch (error) {
      console.error("Falha ao buscar dados do usuário:", error);
      logout();
    }
  }

  /**
   * Tenta carregar a sessão a partir dos cookies (para inicialização da app)
   */
  async function tryToLoadSession() {
    if (accessToken.value && !user.value) {
      console.log("Token encontrado, tentando carregar sessão...");
      await fetchUser();
    }
  }

  /**
   * Limpa todos os dados de autenticação
   */
  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    console.log("User logged out, tokens and user cleared.");
  }

  /**
   * Função legacy para compatibilidade (deprecated)
   * @deprecated Use setTokens e setUser separadamente
   */
  async function setAuthData(tokenData: { access: string; refresh?: string }) {
    console.warn(
      "setAuthData is deprecated. Use setTokens and setUser instead."
    );
    setTokens(tokenData.access, tokenData.refresh);
    await fetchUser();
  }

  return {
    // State
    accessToken,
    refreshToken,
    user,

    // Getters
    isLoggedIn,
    isAuthenticated, // Para compatibilidade

    // Actions
    setTokens,
    setUser,
    fetchUser,
    tryToLoadSession,
    logout,
    setAuthData, // Deprecated but kept for compatibility
  };
});
