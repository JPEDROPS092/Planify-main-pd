import { useAuthStore } from "@/stores/auth";
import { useAuthJwtCreateCreate, authUsersMeRetrieve } from "@/api/auth/auth";
import type { TokenObtainPairRequest } from "@/api/schemas";
import { computed } from "vue";
import { useRouter } from "vue-router";

interface LoginVariables {
  data: TokenObtainPairRequest;
  redirectTo?: string;
}

/**
 * Composable para orquestrar o fluxo de autenticação.
 * Otimizado para SPA (Single Page Application).
 */
export function useAuth() {
  const authStore = useAuthStore();
  const router = useRouter();

  // 1. Login mutation with explicit navigation handling
  const loginMutation = useAuthJwtCreateCreate({
    mutation: {
      onSuccess: async (response, variables: LoginVariables) => {
        console.log("Login API call successful. Response:", response);

        // Extract the new access token from the response
        const newAccessToken = response.data.access;

        // Save tokens in store
        authStore.setTokens(newAccessToken, response.data.refresh);

        try {
          // Fetch user info with explicit token
          const userResponse = await authUsersMeRetrieve({
            headers: {
              Authorization: `Bearer ${newAccessToken}`,
            },
          });
          authStore.setUser(userResponse.data);
          console.log(
            "User data fetched and set in store:",
            userResponse.data.username
          );

          // Navigate using Nuxt's built-in navigation utility
          const targetPath = variables.redirectTo || "/dashboard";
          await router.replace(targetPath);
        } catch (fetchError) {
          console.error("Failed to fetch user after login:", fetchError);
          // Logout to avoid inconsistent state if user fetch fails
          authStore.logout();
        }
      },
      onError: (error) => {
        console.error("Login mutation failed:", error);
      },
    },
  });

  /**
   * Login function that components will call to start the login process.
   */
  const login = (credentials: TokenObtainPairRequest, redirectTo?: string) => {
    return loginMutation.mutate({
      data: credentials,
      redirectTo,
    } as LoginVariables);
  };

  const logout = async () => {
    authStore.logout();
    // Use router.replace instead of navigateTo
    await router.replace("/login");
  };

  return {
    // Auth state from store
    user: authStore.user,
    isAuthenticated: authStore.isAuthenticated,

    // Functions
    login,
    logout,

    // Login mutation state
    isLoading: computed(() => loginMutation.isPending.value),
    isError: computed(() => loginMutation.isError.value),
    error: computed(() => loginMutation.error.value),
  };
}
