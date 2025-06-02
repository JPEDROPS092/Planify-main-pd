/**
 * Endpoints de autenticação
 * Define funções para interagir com a API de autenticação
 */
import { useApiClient } from '../client';
import type { 
  LoginCredentials, 
  TokenResponse, 
  ExtendedUserProfile,
  PasswordResetConfirmData,
  PasswordResetResponse
} from './types';

/**
 * Composable que fornece funções de endpoints de autenticação
 */
export const useAuthEndpoints = () => {
  const apiClient = useApiClient();

  /**
   * Cria um token de autenticação (login)
   */
  const createAuthToken = async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/api/auth/token/', credentials);
    return response.data;
  };

  /**
   * Atualiza o token de acesso usando o token de refresh
   */
  const refreshAuthToken = async (data: { refresh: string }): Promise<TokenResponse> => {
    const response = await apiClient.post<TokenResponse>('/api/auth/token/refresh/', data);
    return response.data;
  };

  /**
   * Obtém os dados do usuário autenticado
   */
  const retrieveAuthUsersMe = async (): Promise<ExtendedUserProfile> => {
    const response = await apiClient.get<ExtendedUserProfile>('/api/auth/users/me/');
    return response.data;
  };

  /**
   * Registra um novo usuário
   */
  const registerUser = async (userData: Partial<ExtendedUserProfile>): Promise<ExtendedUserProfile> => {
    const response = await apiClient.post<ExtendedUserProfile>('/api/auth/users/', userData);
    return response.data;
  };

  /**
   * Solicita redefinição de senha
   */
  const requestPasswordReset = async (email: string): Promise<PasswordResetResponse> => {
    const response = await apiClient.post<PasswordResetResponse>('/api/auth/users/reset_password/', { email });
    return response.data;
  };

  /**
   * Confirma redefinição de senha
   */
  const confirmPasswordReset = async (data: PasswordResetConfirmData): Promise<PasswordResetResponse> => {
    const response = await apiClient.post<PasswordResetResponse>('/api/auth/users/reset_password_confirm/', data);
    return response.data;
  };

  /**
   * Exclui a conta do usuário
   */
  const destroyAuthUser = async (userId: number): Promise<void> => {
    await apiClient.delete(`/api/auth/users/${userId}/`);
  };

  return {
    createAuthToken,
    refreshAuthToken,
    retrieveAuthUsersMe,
    registerUser,
    requestPasswordReset,
    confirmPasswordReset,
    destroyAuthUser
  };
};