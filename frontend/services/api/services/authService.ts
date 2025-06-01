/**
 * Serviço de autenticação
 * Gerencia autenticação, sessão de usuário e permissões
 */
import { useState, navigateTo } from '#imports';
import { authEndpoints, LoginCredentials, UserProfile } from '../endpoints/auth';

/**
 * Hook para gerenciar autenticação do usuário
 * @returns Métodos e estado para gerenciar autenticação
 */
export const useAuthService = () => {
  const accessToken = useState<string | null>('auth.accessToken');
  const refreshToken = useState<string | null>('auth.refreshToken');
  const user = useState<UserProfile | null>('auth.user');
  const isAuthenticated = useState<boolean>('auth.isAuthenticated', () => !!accessToken.value);
  const isLoading = useState<boolean>('auth.isLoading', () => false);

  /**
   * Realiza login do usuário
   * @param credentials Credenciais de login (username e password)
   * @returns Dados do usuário autenticado
   */
  const login = async (credentials: LoginCredentials) => {
    isLoading.value = true;
    try {
      // Obter tokens de autenticação
      const tokenResponse = await authEndpoints.createAuthToken(credentials);
      
      // Armazenar tokens
      accessToken.value = tokenResponse.access;
      refreshToken.value = tokenResponse.refresh;
      
      if (process.client) {
        localStorage.setItem('auth_token', tokenResponse.access);
        localStorage.setItem('refresh_token', tokenResponse.refresh);
      }
      
      // Obter dados do usuário
      const userData = await authEndpoints.retrieveCurrentUser();
      user.value = userData;
      isAuthenticated.value = true;
      
      return userData;
    } catch (error) {
      console.error('Erro ao realizar login:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Realiza logout do usuário
   */
  const logout = () => {
    // Limpar tokens e dados do usuário
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    isAuthenticated.value = false;
    
    if (process.client) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
    
    // Redirecionar para a página de login
    navigateTo('/login');
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
    if (process.client) {
      const token = localStorage.getItem('auth_token');
      const refresh = localStorage.getItem('refresh_token');
      
      if (token) {
        accessToken.value = token;
        if (refresh) refreshToken.value = refresh;
        
        try {
          // Tentar obter dados do usuário com o token
          const userData = await authEndpoints.retrieveCurrentUser();
          user.value = userData;
          isAuthenticated.value = true;
          return true;
        } catch (error) {
          // Se o token for inválido, tentar refresh
          if (refresh) {
            try {
              const newTokens = await authEndpoints.refreshAuthToken({ refresh });
              accessToken.value = newTokens.access;
              if (newTokens.refresh) refreshToken.value = newTokens.refresh;
              
              localStorage.setItem('auth_token', newTokens.access);
              if (newTokens.refresh) localStorage.setItem('refresh_token', newTokens.refresh);
              
              // Tentar novamente com o novo token
              const userData = await authEndpoints.retrieveCurrentUser();
              user.value = userData;
              isAuthenticated.value = true;
              return true;
            } catch (refreshError) {
              // Se falhar, limpar tudo
              logout();
              return false;
            }
          } else {
            logout();
            return false;
          }
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
   * @param group Nome do grupo a verificar
   * @returns Verdadeiro se o usuário pertencer ao grupo
   */
  const isInGroup = (group: string): boolean => {
    if (!user.value || !user.value.groups) return false;
    return user.value.groups.includes(group);
  };

  /**
   * Registra um novo usuário
   * @param userData Dados do novo usuário
   * @returns Dados do usuário criado
   */
  const register = async (userData: Partial<UserProfile>) => {
    isLoading.value = true;
    try {
      const newUser = await authEndpoints.registerUser(userData);
      return newUser;
    } catch (error) {
      console.error('Erro ao registrar usuário:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Solicita redefinição de senha
   * @param email Email do usuário
   * @returns Mensagem de confirmação
   */
  const requestPasswordReset = async (email: string) => {
    isLoading.value = true;
    try {
      return await authEndpoints.requestPasswordReset(email);
    } catch (error) {
      console.error('Erro ao solicitar redefinição de senha:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Confirma redefinição de senha
   * @param data Dados para redefinição (token, uid, nova senha)
   * @returns Mensagem de confirmação
   */
  const confirmPasswordReset = async (data: { uid: string; token: string; new_password: string }) => {
    isLoading.value = true;
    try {
      return await authEndpoints.confirmPasswordReset(data);
    } catch (error) {
      console.error('Erro ao confirmar redefinição de senha:', error);
      throw error;
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
    
    // Métodos
    login,
    logout,
    checkAuth,
    hasPermission,
    isInGroup,
    register,
    requestPasswordReset,
    confirmPasswordReset
  };
};
