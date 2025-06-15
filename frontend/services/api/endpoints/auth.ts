/**
 * Endpoints de autenticação para o Planify
 * Centraliza todas as chamadas de API relacionadas à autenticação
 */
import { apiClient } from '../services/apiClient';
import type { 
  TokenObtainPair, 
  TokenRefresh, 
  LoginCredentials, 
  ExtendedUserProfile,
} from '~/services/utils/types';

/**
 * Obtém token de acesso a partir das credenciais de login
 * @param credentials Credenciais de login (username/email e senha)
 * @returns Tokens de acesso e refresh
 */
export const createAuthToken = async (credentials: LoginCredentials): Promise<TokenObtainPair> => {
  console.log('Making auth request to Django backend with:', { username: credentials.username, password: '******' });
  
  // Updated to match the correct Django backend URL pattern
  return await apiClient.post<TokenObtainPair>('/api/auth/token/', credentials);
};

/**
 * Atualiza o token de acesso usando o token de refresh
 * @param data Objeto contendo o token de refresh
 * @returns Novo token de acesso (e possivelmente novo token de refresh)
 */
export const refreshAuthToken = async (data: { refresh: string }): Promise<TokenRefresh> => {
  // Updated to match the correct Django backend URL pattern
  return await apiClient.post<TokenRefresh>('/api/auth/token/refresh/', data);
};

/**
 * Obtém os dados do usuário autenticado
 * @returns Perfil completo do usuário
 */
export const retrieveAuthUsersMe = async (): Promise<ExtendedUserProfile> => {
  // Updated to match correct endpoint for retrieving user profile
  return await apiClient.get<ExtendedUserProfile>('/api/users/me/');
};

/**
 * Registra um novo usuário
 * @param userData Dados do usuário a ser registrado
 * @returns Perfil do usuário criado
 */
export const registerUser = async (userData: Partial<ExtendedUserProfile>): Promise<ExtendedUserProfile> => {
  // Updated to match correct endpoint for user registration
  return await apiClient.post<ExtendedUserProfile>('/api/users/', userData);
};

/**
 * Solicita redefinição de senha
 * @param email Email do usuário
 * @returns Resposta da API
 */
export const requestPasswordReset = async (email: string): Promise<any> => {
  // Updated to match correct endpoint for password reset request
  return await apiClient.post('/api/users/reset_password/', { email });
};

/**
 * Confirma a redefinição de senha
 * @param data Dados para redefinição (uid, token, nova senha)
 * @returns Resposta da API
 */
export const confirmPasswordReset = async (data: { uid: string; token: string; new_password: string }): Promise<any> => {
  // Updated to match correct endpoint for password reset confirmation
  return await apiClient.post('/api/users/reset_password_confirm/', data);
};
