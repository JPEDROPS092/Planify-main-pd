import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from "axios";

// Importe APENAS o hook para buscar o usuário. O de login não é mais necessário aqui.
import { useAuthUsersMeRetrieve } from "~/api/auth/auth";
import type { User, TokenObtainPair } from "~/api/schemas";

export const useAuthStore = defineStore("auth", () => {
  // --- STATE (sem mudanças) ---
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const user = ref<User | null>(null);

  // --- GETTERS (sem mudanças) ---
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);

  // --- ACTIONS ---

  /**
   * Nova ação para definir os dados de autenticação e buscar o usuário.
   * Esta função será chamada pelo componente de login após uma chamada de API bem-sucedida.
   */
  async function setAuthData(tokenData: TokenObtainPair) {
    accessToken.value = tokenData.access;
    refreshToken.value = tokenData.refresh ?? null; // Usa ?? para o caso de refresh ser opcional

    if (process.client) {
      localStorage.setItem("accessToken", tokenData.access);
      if (tokenData.refresh) {
        localStorage.setItem("refreshToken", tokenData.refresh);
      }
    }

    // Após salvar os tokens, busque os dados do usuário.
    await fetchUser();
  }

  async function fetchUser() {
    if (!accessToken.value) return;
    const { refetch } = useAuthUsersMeRetrieve({
      query: { enabled: false, retry: false },
    });

    try {
      const response = await refetch();
      if (response.data?.value) {
        user.value = response.data.value.data;
      } else {
        throw new Error("Dados do usuário não encontrados na resposta.");
      }
    } catch (error) {
      console.error("Falha ao buscar dados do usuário:", error);
      await logout();
    }
  }

  // ... (tryToLoadSession, logout, _clearSession permanecem iguais) ...
  async function tryToLoadSession() {
    /* ...código existente... */
  }
  async function _clearSession() {
    /* ...código existente... */
  }
  async function logout() {
    /* ...código existente... */
  }

  return {
    accessToken,
    user,
    isAuthenticated,
    // Remova a exportação do 'login' antigo e exporte a nova função
    setAuthData,
    logout,
    fetchUser,
    tryToLoadSession,
  };
});
