// frontend/stores/auth.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { ExtendedUserProfile, LoginCredentials, TokenObtainPair } from '~/services/utils/types';
import { ThemePreferenceEnum } from '~/services/utils/types'; // Assuming this is still needed for mock/default user
// Atualizar o caminho de importação para as funções da API de autenticação
import {
  createAuthToken,
  retrieveAuthUsersMe,
  refreshAuthToken as apiRefreshAuthToken
} from '~/lib/api-client/services/AuthService';
import { ApiError } from '~/lib/api-client/services/AuthService';
import { useState } from '#app'; // For global state synchronization if needed outside Pinia

// It's good practice for Pinia store IDs to be unique.
export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<ExtendedUserProfile | null>(null);
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // For synchronization with Nuxt's global state if other parts of the app (like API client interceptors)
  // rely on useState directly. This ensures Pinia and useState are in sync.
  const globalNuxtAccessToken = useState<string | null>('auth.accessToken', () => null);

  // Getters (computed properties)
  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);
  const userFullName = computed(() => {
    if (user.value) {
      return `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim() || user.value.username;
    }
    return 'Convidado';
  });
  const userRole = computed(() => user.value?.role || null); // Assuming 'role' is part of ExtendedUserProfile

  // Actions
  async function login(credentials: LoginCredentials): Promise<boolean> {
    isLoading.value = true;
    error.value = null;
    try {
      const tokenData: TokenObtainPair = await createAuthToken(credentials);
      accessToken.value = tokenData.access;
      refreshToken.value = tokenData.refresh;
      globalNuxtAccessToken.value = tokenData.access; // Sync with Nuxt's useState

      const userData: ExtendedUserProfile = await retrieveAuthUsersMe();
      user.value = userData;

      if (process.client) {
        localStorage.setItem('accessToken', accessToken.value);
        if (refreshToken.value) {
          localStorage.setItem('refreshToken', refreshToken.value);
        }
      }
      return true;
    } catch (e: unknown) {
      const apiError = e as ApiError;
      error.value = apiError.friendlyMessage || 'Falha no login.';
      _clearAuthData(); // Helper to clear data
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  function logout(): void {
    _clearAuthData();
    if (process.client) {
      // Potentially notify other tabs/windows, or call an API endpoint for server-side session invalidation
    }
    // No redirect here; redirection should be handled by middleware or page logic.
  }

  async function checkAuthStatus(): Promise<void> {
    isLoading.value = true;
    // Try to load from Nuxt's global state first (e.g. if set by SSR or previous client interaction)
    if (globalNuxtAccessToken.value && !accessToken.value) {
        accessToken.value = globalNuxtAccessToken.value;
        if(process.client && !refreshToken.value) {
            refreshToken.value = localStorage.getItem('refreshToken');
        }
    }

    // Then try localStorage if still no token in Pinia state
    if (process.client && !accessToken.value) {
      const storedAccessToken = localStorage.getItem('accessToken');
      if (storedAccessToken) {
        accessToken.value = storedAccessToken;
        globalNuxtAccessToken.value = storedAccessToken; // Sync
        refreshToken.value = localStorage.getItem('refreshToken');
      }
    }

    if (accessToken.value) {
      try {
        // If user data is not already in store, fetch it
        if (!user.value) {
            const userData = await retrieveAuthUsersMe();
            user.value = userData;
        }
      } catch (e) {
        // If fetching user fails (e.g., token expired), clear auth data
        _clearAuthData();
      }
    } else {
        // No token found, ensure everything is cleared
        _clearAuthData();
    }
    isLoading.value = false;
  }

  async function refreshAccessToken(): Promise<boolean> {
    if (!refreshToken.value) {
      error.value = 'Sessão expirada. Por favor, faça login novamente.';
      _clearAuthData(); // No refresh token means session is truly lost
      return false;
    }
    isLoading.value = true;
    error.value = null;
    try {
      const tokenData = await apiRefreshAuthToken({ refresh: refreshToken.value });
      accessToken.value = tokenData.access;
      globalNuxtAccessToken.value = tokenData.access; // Sync

      // API might return a new refresh token
      if (tokenData.refresh) {
        refreshToken.value = tokenData.refresh;
      }

      if (process.client) {
        localStorage.setItem('accessToken', accessToken.value);
        if (refreshToken.value) {
          localStorage.setItem('refreshToken', refreshToken.value);
        }
      }
      return true;
    } catch (e) {
      error.value = 'Sua sessão expirou. Por favor, faça login novamente.';
      _clearAuthData(); // Refresh failed, clear session
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  // Helper function to clear all auth-related data
  function _clearAuthData(): void {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    globalNuxtAccessToken.value = null; // Clear Nuxt's useState
    if (process.client) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    isAuthenticated,
    userFullName,
    userRole,
    login,
    logout,
    checkAuthStatus,
    refreshAccessToken,
  };
});
