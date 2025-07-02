import { defineStore } from "pinia";
import { ref, computed } from "vue";
import type { User } from "@/api/schemas";

export const useAuthStore = defineStore("auth", () => {
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
  const isLoggedIn = computed(() => !!accessToken.value && !!user.value);
  const isAuthenticated = computed(() => isLoggedIn.value);

  function setTokens(newAccessToken: string, newRefreshToken?: string) {
    accessToken.value = newAccessToken;
    if (newRefreshToken) {
      refreshToken.value = newRefreshToken;
    }
    console.log("[auth.ts] Tokens definidos na store");
  }

  function setUser(newUser: User | null) {
    user.value = newUser;
    console.log(
      `[auth.ts] Dados do usuário definidos na store: ${
        newUser?.username || "null"
      }`
    );
  }

  function logout() {
    console.log("[auth.ts] Realizando logout, limpando dados da sessão");
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
  }

  async function initialize() {
    console.log("[auth.ts] Iniciando inicialização da store de autenticação");

    if (!accessToken.value) {
      console.log("[auth.ts] Nenhum token encontrado, pulando inicialização");
      return;
    }

    if (user.value) {
      console.log("[auth.ts] Usuário já está carregado, pulando inicialização");
      return;
    }

    console.log("[auth.ts] Token encontrado. Buscando dados do usuário...");
    try {
      const { authUsersMeRetrieve } = await import("~/api/auth/auth");
      const response = await authUsersMeRetrieve();
      setUser(response.data);
      console.log("[auth.ts] Dados do usuário carregados com sucesso");
    } catch (error) {
      console.error("[auth.ts] Erro ao carregar dados do usuário:", error);
      logout();
    }
  }

  return {
    // State
    accessToken,
    refreshToken,
    user,

    // Getters
    isLoggedIn,
    isAuthenticated,

    // Actions
    setTokens,
    setUser,
    initialize,
    logout,
  };
});
