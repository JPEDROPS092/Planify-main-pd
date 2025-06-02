/**
 * Serviço de autenticação
 * Gerencia autenticação, sessão de usuário e permissões
 */
import { useState } from '#imports';
import { navigateTo } from '#app';
import type { 
  LoginCredentials, 
  TokenResponse,
  ExtendedUserProfile,
  PasswordResetConfirmData,
  PasswordResetResponse,
  RegisterResponse,
  AuthError
} from './types';
import { useAuthEndpoints } from './endpoints';
import { AuthErrorType } from './types';

/**
 * Utilitários para manipulação de tokens de autenticação
 */
export const tokenUtils = {
  saveTokens: (access: string, refresh: string): void => {
    if (process.client) {
      localStorage.setItem('auth_token', access);
      localStorage.setItem('refresh_token', refresh);
    }
  },
  
  clearTokens: (): void => {
    if (process.client) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
  },
  
  getStoredTokens: (): { access: string | null, refresh: string | null } => {
    if (process.client) {
      return {
        access: localStorage.getItem('auth_token'),
        refresh: localStorage.getItem('refresh_token')
      };
    }
    return { access: null, refresh: null };
  }
};

/**
 * Funções de tratamento de erros
 */
export const handleAuthError = (error: any): AuthError => {
  // Determinar tipo de erro baseado na resposta da API
  if (error?.response) {
    const status = error.response.status;
    const data = error.response.data;
    
    if (status === 401) {
      if (data?.detail?.includes('expired')) {
        return { 
          type: AuthErrorType.TOKEN_EXPIRED, 
          message: 'Sua sessão expirou. Por favor, faça login novamente.',
          originalError: error 
        };
      }
      return { 
        type: AuthErrorType.INVALID_CREDENTIALS, 
        message: 'Credenciais inválidas. Verifique seu usuário e senha.',
        originalError: error 
      };
    }
    
    if (status === 403 && data?.detail?.includes('inactive')) {
      return { 
        type: AuthErrorType.USER_INACTIVE, 
        message: 'Esta conta está desativada. Entre em contato com o administrador.',
        originalError: error 
      };
    }
  }
  
  if (error?.message?.includes('Network Error')) {
    return { 
      type: AuthErrorType.NETWORK_ERROR, 
      message: 'Erro de conexão. Verifique sua internet e tente novamente.',
      originalError: error 
    };
  }
  
  return { 
    type: AuthErrorType.UNKNOWN_ERROR, 
    message: 'Ocorreu um erro inesperado. Por favor, tente novamente.',
    originalError: error 
  };
};

/**
 * Hook para gerenciar autenticação do usuário
 * @returns Métodos e estado para gerenciar autenticação
 */
export const useAuthService = () => {
  const accessToken = useState<string | null>('auth.accessToken');
  const refreshToken = useState<string | null>('auth.refreshToken');
  const user = useState<ExtendedUserProfile | null>('auth.user');
  const isAuthenticated = useState<boolean>('auth.isAuthenticated', () => !!accessToken.value);
  const isLoading = useState<boolean>('auth.isLoading', () => false);
  const lastError = useState<AuthError | null>('auth.lastError', () => null);
  
  // Obter endpoints de autenticação usando o novo composable
  const authEndpoints = useAuthEndpoints();

  /**
   * Realiza login do usuário
   * @param credentials Credenciais de login (username e password)
   * @returns Dados do usuário autenticado
   */
  const login = async (credentials: LoginCredentials): Promise<ExtendedUserProfile> => {
    isLoading.value = true;
    lastError.value = null;
    
    try {
      // Obter tokens de autenticação
      const tokenResponse = await authEndpoints.createAuthToken(credentials);
      
      // Armazenar tokens
      accessToken.value = tokenResponse.access;
      refreshToken.value = tokenResponse.refresh;
      
      // Salvar no localStorage
      tokenUtils.saveTokens(tokenResponse.access, tokenResponse.refresh);
      
      // Obter dados do usuário
      const userData = await authEndpoints.retrieveAuthUsersMe();
      user.value = userData;
      isAuthenticated.value = true;
      
      return userData;
    } catch (error) {
      const authError = handleAuthError(error);
      lastError.value = authError;
      console.error('Erro ao realizar login:', authError.message, authError.originalError);
      throw authError;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Realiza logout do usuário
   * @param redirectPath Caminho opcional para redirecionar após logout (padrão: '/login')
   */
  const logout = (redirectPath: string = '/auth/login'): void => {
    // Limpar tokens e dados do usuário
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    isAuthenticated.value = false;
    lastError.value = null;
    
    // Remover do localStorage
    tokenUtils.clearTokens();
    
    // Redirecionar para a página especificada
    navigateTo(redirectPath);
  };

  /**
   * Verifica se o usuário está autenticado
   * @returns Verdadeiro se o usuário estiver autenticado
   */
  const checkAuth = async (): Promise<boolean> => {
    // Se já temos o usuário, retornar verdadeiro
    if (user.value && accessToken.value) {
      isAuthenticated.value = true;
      return true;
    }
    
    // Verificar se temos token no localStorage
    const { access, refresh } = tokenUtils.getStoredTokens();
    
    if (access) {
      accessToken.value = access;
      if (refresh) refreshToken.value = refresh;
      
      try {
        // Tentar obter dados do usuário com o token
        const userData = await authEndpoints.retrieveAuthUsersMe();
        user.value = userData;
        isAuthenticated.value = true;
        return true;
      } catch (error) {
        // Se o token for inválido, tentar refresh
        if (refresh) {
          try {
            const newTokens = await authEndpoints.refreshAuthToken({ refresh });
            accessToken.value = newTokens.access;
            refreshToken.value = newTokens.refresh;
            
            tokenUtils.saveTokens(newTokens.access, newTokens.refresh);
            
            // Tentar novamente com o novo token
            const userData = await authEndpoints.retrieveAuthUsersMe();
            user.value = userData;
            isAuthenticated.value = true;
            return true;
          } catch (refreshError) {
            // Se falhar, limpar tudo
            logout('/auth/login');
            lastError.value = handleAuthError(refreshError);
            return false;
          }
        } else {
          logout('/auth/login');
          lastError.value = handleAuthError(error);
          return false;
        }
      }
    }
    
    isAuthenticated.value = false;
    return false;
  };

  /**
   * Verifica se o usuário tem uma permissão específica
   * @param permission Nome da permissão a verificar
   * @returns Verdadeiro se o usuário tiver a permissão
   */
  const hasPermission = (permission: string): boolean => {
    if (!user.value || !user.value.permissions) return false;
    return user.value.permissions.includes(permission);
  };

  /**
   * Verifica se o usuário pertence a um grupo específico
   * @param groupName Nome do grupo a verificar
   * @returns Verdadeiro se o usuário pertencer ao grupo
   */
  const isInGroup = (groupName: string): boolean => {
    if (!user.value || !user.value.groups) return false;
    return user.value.groups.some((group: { name: string }) => group.name === groupName);
  };

  /**
   * Registra um novo usuário
   * @param userData Dados do novo usuário
   * @returns Dados do usuário criado
   */
  const register = async (userData: Partial<ExtendedUserProfile>): Promise<RegisterResponse> => {
    isLoading.value = true;
    lastError.value = null;
    
    try {
      const newUser = await authEndpoints.registerUser(userData);
      return {
        id: newUser.id!,
        username: newUser.username!,
        email: newUser.email!
      };
    } catch (error) {
      const authError = handleAuthError(error);
      lastError.value = authError;
      console.error('Erro ao registrar usuário:', authError.message, authError.originalError);
      throw authError;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Solicita redefinição de senha
   * @param email Email do usuário
   * @returns Resposta da solicitação
   */
  const requestPasswordResetEmail = async (email: string): Promise<PasswordResetResponse> => {
    isLoading.value = true;
    lastError.value = null;
    
    try {
      return await authEndpoints.requestPasswordReset(email);
    } catch (error) {
      const authError = handleAuthError(error);
      lastError.value = authError;
      console.error('Erro ao solicitar redefinição de senha:', authError.message, authError.originalError);
      throw authError;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Confirma redefinição de senha
   * @param data Dados para redefinição (token, uid, nova senha)
   * @returns Resposta da confirmação
   */
  const confirmPasswordResetToken = async (data: PasswordResetConfirmData): Promise<PasswordResetResponse> => {
    isLoading.value = true;
    lastError.value = null;
    
    try {
      return await authEndpoints.confirmPasswordReset(data);
    } catch (error) {
      const authError = handleAuthError(error);
      lastError.value = authError;
      console.error('Erro ao confirmar redefinição de senha:', authError.message, authError.originalError);
      throw authError;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Atualiza o token de acesso
   * @returns Novo token de acesso
   */
  const refreshAccessToken = async (): Promise<TokenResponse | null> => {
    if (!refreshToken.value) return null;
    
    try {
      const tokens = await authEndpoints.refreshAuthToken({ refresh: refreshToken.value });
      accessToken.value = tokens.access;
      refreshToken.value = tokens.refresh;
      
      tokenUtils.saveTokens(tokens.access, tokens.refresh);
      return tokens;
    } catch (error) {
      const authError = handleAuthError(error);
      lastError.value = authError;
      console.error('Erro ao atualizar token:', authError.message, authError.originalError);
      logout('/auth/login');
      return null;
    }
  };

  /**
   * Exclui a conta do usuário atual
   * @returns Promise que resolve quando a conta for excluída com sucesso
   */
  const deleteAccount = async (): Promise<void> => {
    if (!user.value || !user.value.id) {
      throw new Error('Usuário não está autenticado');
    }
    
    isLoading.value = true;
    lastError.value = null;
    
    try {
      // Excluir a conta do usuário
      await authEndpoints.destroyAuthUser(user.value.id);
      
      // Fazer logout após exclusão
      logout('/auth/login');
    } catch (error) {
      const authError = handleAuthError(error);
      lastError.value = authError;
      console.error('Erro ao excluir conta:', authError.message, authError.originalError);
      throw authError;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    // Estado
    user,
    isAuthenticated,
    isLoading,
    accessToken,
    refreshToken,
    lastError,
    
    // Métodos
    login,
    logout,
    checkAuth,
    hasPermission,
    isInGroup,
    register,
    requestPasswordReset: requestPasswordResetEmail,
    confirmPasswordReset: confirmPasswordResetToken,
    refreshAccessToken,
    deleteAccount
  };
};