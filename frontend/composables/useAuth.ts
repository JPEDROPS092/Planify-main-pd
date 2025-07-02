// filepath: composables/useAuth.ts

import { useAuthStore } from "@/stores/auth";
import {
  useAuthJwtCreateCreate /* REMOVA authUsersMeRetrieve daqui */,
} from "@/api/auth/auth";
import type { TokenObtainPairRequest, User } from "@/api/schemas";
import { computed } from "vue";
// IMPORTANTE: Importe a sua instância do Axios
import { axiosInstance } from "@/lib/axios-instance";

export function useAuth() {
  const authStore = useAuthStore();
  const router = useRouter(); // use... do Nuxt são auto-importados
  const route = useRoute();

  const loginMutation = useAuthJwtCreateCreate({
    mutation: {
      onSuccess: async (response) => {
        const newAccessToken = response.data.access;
        authStore.setTokens(newAccessToken, response.data.refresh);

        try {
          console.log(
            "[useAuth] Buscando dados do usuário com o novo token..."
          );

          // ===================== A CORREÇÃO ESTÁ AQUI =====================
          // Em vez de usar authUsersMeRetrieve(), chame o axiosInstance diretamente.
          // Isso nos dá controle total sobre a requisição e evita qualquer
          // lógica interna do Orval que possa estar causando o problema do 'signal'.
          const userResponse = await axiosInstance.get<User>(
            "/api/auth/users/me/",
            {
              headers: {
                Authorization: `Bearer ${newAccessToken}`,
              },
            }
          );
          // =================================================================

          authStore.setUser(userResponse.data);
          console.log(
            "[useAuth] Dados do usuário salvos:",
            userResponse.data.username
          );

          const redirectPath = route.query.redirect?.toString() || "/dashboard";
          await navigateTo(redirectPath);
        } catch (fetchError) {
          console.error(
            "[useAuth] Falha ao buscar dados do usuário após login:",
            fetchError
          );
          authStore.logout();
        }
      },
      onError: (error) => {
        console.error("[useAuth] Falha na mutação de login:", error);
      },
    },
  });

  const login = (credentials: TokenObtainPairRequest) => {
    loginMutation.mutate({ data: credentials });
  };

  const logout = async () => {
    authStore.logout();
    await navigateTo("/login");
  };

  return {
    login,
    logout,
    isLoading: computed(() => loginMutation.isPending.value),
    isError: computed(() => loginMutation.isError.value),
    error: computed(() => loginMutation.error.value),
  };
}
