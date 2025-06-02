/**
 * Tipos específicos para autenticação
 */
import type { 
  ExtendedUserProfile, 
  TokenResponse, 
  LoginCredentials,
  TokenRefresh,
  TokenObtainPair
} from '~/services/utils/types';

// Tipos de erro de autenticação
export enum AuthErrorType {
  INVALID_CREDENTIALS = 'invalid_credentials',
  TOKEN_EXPIRED = 'token_expired',
  USER_INACTIVE = 'user_inactive',
  NETWORK_ERROR = 'network_error',
  UNKNOWN_ERROR = 'unknown_error'
}

// Interface para erros de autenticação
export interface AuthError {
  type: AuthErrorType;
  message: string;
  originalError?: any;
}

// Interfaces para resposta de redefinição de senha
export interface PasswordResetResponse {
  message: string;
  success: boolean;
}

// Interface para resposta de registro
export interface RegisterResponse {
  id: number;
  username: string;
  email: string;
}

// Interface para dados de confirmação de redefinição de senha
export interface PasswordResetConfirmData {
  uid: string;
  token: string;
  new_password: string;
}

// Re-exportar tipos do utils/types.ts para facilitar importação
export type { 
  ExtendedUserProfile, 
  TokenResponse, 
  LoginCredentials,
  TokenRefresh,
  TokenObtainPair
};