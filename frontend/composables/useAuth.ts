// composables/useAuth.ts
import { ref, computed, readonly } from 'vue';
import type { User } from '../types/User';
import { useNotification } from './useNotification';

export const useAuth = () => {
  const { $api } = useNuxtApp();

  // Estados reativos
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Função para verificar se o usuário está autenticado
  const isAuthenticated = computed((): boolean => {
    const token = useCookie('auth-token');
    return !!token.value;
  });

  // Função para obter dados do usuário do token
  const getCurrentUser = (): User | null => {
    const userCookie = useCookie('auth-user');
    if (userCookie.value) {
      try {
        return JSON.parse(userCookie.value as string);
      } catch (e) {
        console.error('Error parsing user cookie:', e);
        return null;
      }
    }
    return null;
  };

  // Função para fazer login
  const login = async (credentials: { username: string; password: string; remember?: boolean }) => {
    isLoading.value = true;
    error.value = null;
    
    const { showSuccess, showError } = useNotification();

    try {
      const { $api } = useNuxtApp();
      
      // Fazer a chamada para a API de login usando o serviço correto
      const response = await $api.api.apiAuthTokenCreate({
        username: credentials.username,
        password: credentials.password,
      });

      // Verificar se a resposta contém os tokens
      if (response && (response.access || response.token)) {
        // Suportar diferentes formatos de resposta
        const accessToken = response.access || response.token;
        const refreshToken = response.refresh || response.refresh_token;
        
        // Configurar opções dos cookies baseado no "remember me"
        const cookieOptions = {
          maxAge: credentials.remember ? 60 * 60 * 24 * 30 : 60 * 60 * 24, // 30 dias se remember, 1 dia se não
          secure: true,
          sameSite: 'strict' as const,
          httpOnly: false, // Precisa ser false para acessar via JavaScript
        };
        
        // Salvar tokens nos cookies
        const tokenCookie = useCookie('auth-token', cookieOptions);
        const refreshTokenCookie = useCookie('refresh-token', {
          ...cookieOptions,
          maxAge: 60 * 60 * 24 * 30, // Refresh token sempre dura 30 dias
        });
        const userCookie = useCookie('auth-user', cookieOptions);

        tokenCookie.value = accessToken;
        
        if (refreshToken) {
          refreshTokenCookie.value = refreshToken;
        }
        
        // Se o response contém dados do usuário, salvá-los
        if (response.user) {
          userCookie.value = JSON.stringify(response.user);
          user.value = response.user;
        }

        // Exibir notificação de sucesso
        showSuccess('Login realizado com sucesso!');

        return { success: true, user: response.user, token: accessToken };
      } else {
        throw new Error('Token não encontrado na resposta da API');
      }
    } catch (e: any) {
      console.error('Erro no login:', e);
      
      let errorMessage = 'Erro ao fazer login';
      
      // Tratar diferentes tipos de erro de forma mais específica
      if (e.response?.data) {
        const data = e.response.data;
        
        // Erros específicos do Django REST Framework
        if (data.detail) {
          if (typeof data.detail === 'string') {
            if (data.detail.includes('No active account') || 
                data.detail.includes('Unable to log in') ||
                data.detail.includes('Invalid credentials')) {
              errorMessage = 'Credenciais inválidas. Verifique seu nome de usuário e senha.';
            } else {
              errorMessage = data.detail;
            }
          }
        } else if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
          const firstError = data.non_field_errors[0];
          if (firstError.includes('No active account') || 
              firstError.includes('Unable to log in') ||
              firstError.includes('Invalid credentials')) {
            errorMessage = 'Credenciais inválidas. Verifique seu nome de usuário e senha.';
          } else {
            errorMessage = firstError;
          }
        } else if (data.message) {
          errorMessage = data.message;
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
      } else if (e.message) {
        if (e.message.includes('Network Error') || e.message.includes('ERR_NETWORK')) {
          errorMessage = 'Erro de conexão. Verifique sua internet e tente novamente.';
        } else {
          errorMessage = e.message;
        }
      }
      
      // Exibir notificação de erro
      showError(errorMessage);
      
      error.value = errorMessage;
      return { success: false, error: errorMessage };
    } finally {
      isLoading.value = false;
    }
  };

  // Função para fazer logout
  const logout = async () => {
    const { showSuccess } = useNotification();
    
    const tokenCookie = useCookie('auth-token');
    const refreshTokenCookie = useCookie('refresh-token');
    const userCookie = useCookie('auth-user');
    
    // Limpar todos os cookies relacionados à autenticação
    tokenCookie.value = null;
    refreshTokenCookie.value = null;
    userCookie.value = null;
    user.value = null;
    
    // Exibir notificação de sucesso
    showSuccess('Logout realizado com sucesso!');
    
    // Redirecionar para a página de login
    await navigateTo('/auth/login');
  };

  // Função para renovar o token
  const refreshToken = async () => {
    try {
      const { $api } = useNuxtApp();
      const refreshTokenCookie = useCookie('refresh-token');
      
      if (!refreshTokenCookie.value) {
        throw new Error('No refresh token available');
      }

      // Usar o endpoint correto para refresh
      const response = await $api.api.apiAuthTokenRefreshCreate({
        refresh: refreshTokenCookie.value,
      });

      if (response && response.access) {
        const tokenCookie = useCookie('auth-token');
        tokenCookie.value = response.access;
        
        // Se um novo refresh token foi fornecido, atualizá-lo também
        if (response.refresh) {
          refreshTokenCookie.value = response.refresh;
        }
        
        return { success: true, token: response.access };
      } else {
        throw new Error('Token de acesso não encontrado na resposta');
      }
    } catch (e: any) {
      console.error('Erro ao renovar token:', e);
      
      // Se não conseguir renovar o token, fazer logout
      await logout();
      
      let errorMessage = 'Erro ao renovar token de acesso';
      if (e.response?.data?.detail) {
        errorMessage = e.response.data.detail;
      } else if (e.message) {
        errorMessage = e.message;
      }
      
      return { success: false, error: errorMessage };
    }
  };

  // Função para verificar autenticação (útil para middleware)
  const checkAuth = async () => {
    if (isAuthenticated.value) {
      const currentUser = getCurrentUser();
      if (currentUser) {
        user.value = currentUser;
        return true;
      }
      
      // Se não temos dados do usuário no cookie, buscar da API
      try {
        const { $api } = useNuxtApp();
        const userData = await $api.autenticaO.apiAuthUsersMeRetrieve();
        
        if (userData) {
          const userCookie = useCookie('auth-user');
          userCookie.value = JSON.stringify(userData);
          user.value = userData;
          return true;
        }
      } catch (e) {
        console.error('Erro ao buscar dados do usuário:', e);
        // Se falhar, fazer logout
        await logout();
        return false;
      }
    }
    return false;
  };

  // Função para registrar usuário
  const register = async (userData: {
    username: string;
    email: string;
    full_name: string;
    password: string;
  }) => {
    isLoading.value = true;
    error.value = null;
    
    const { showSuccess, showError } = useNotification();

    try {
      const { $api } = useNuxtApp();
      
      // Fazer a chamada para a API de registro usando o AuthService correto
      const response = await $api.autenticaO.apiAuthUsersCreate({
        username: userData.username,
        email: userData.email,
        full_name: userData.full_name,
        password: userData.password,
      });

      if (response) {
        // Exibir notificação de sucesso
        showSuccess('Usuário registrado com sucesso!');
        
        return { 
          success: true, 
          user: response,
          message: 'Usuário registrado com sucesso!'
        };
      } else {
        throw new Error('Resposta inválida da API');
      }
    } catch (e: any) {
      console.error('Erro no registro:', e);
      
      let errorMessage = 'Erro ao registrar usuário';
      
      // Tratar diferentes tipos de erro de forma mais específica
      if (e.response?.data) {
        const data = e.response.data;
        
        if (typeof data === 'object') {
          const errorMessages: string[] = [];
          
          Object.entries(data).forEach(([key, value]) => {
            const messages = Array.isArray(value) ? value : [value];
            messages.forEach((msg: string) => {
              if (key === 'username' && msg.includes('already exists')) {
                errorMessages.push('Este nome de usuário já está em uso.');
              } else if (key === 'email' && msg.includes('already exists')) {
                errorMessages.push('Este e-mail já está cadastrado.');
              } else {
                errorMessages.push(msg);
              }
            });
          });
          
          if (errorMessages.length > 0) {
            errorMessage = errorMessages.join('\n');
          }
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
      } else if (e.message) {
        errorMessage = e.message;
      }
      
      // Exibir notificação de erro
      showError(errorMessage);
      
      error.value = errorMessage;
      return { success: false, error: errorMessage };
    } finally {
      isLoading.value = false;
    }
  };

  // Função para atualizar perfil do usuário
  const updateProfile = async (profileData: {
    full_name?: string;
    email?: string;
    username?: string;
  }) => {
    isLoading.value = true;
    error.value = null;
    
    const { showSuccess, showError } = useNotification();

    try {
      const { $api } = useNuxtApp();
      
      // Usar o endpoint para atualizar o perfil do usuário atual
      const response = await $api.api.apiAuthUsersMePartialUpdate({
        ...profileData,
      });

      if (response) {
        // Atualizar o cookie do usuário
        const userCookie = useCookie('auth-user');
        userCookie.value = JSON.stringify(response);
        user.value = response;

        // Exibir notificação de sucesso
        showSuccess('Perfil atualizado com sucesso!');

        return { success: true, user: response };
      } else {
        throw new Error('Resposta inválida da API');
      }
    } catch (e: any) {
      console.error('Erro ao atualizar perfil:', e);
      
      let errorMessage = 'Erro ao atualizar perfil';
      
      if (e.response?.data) {
        const data = e.response.data;
        
        if (typeof data === 'object') {
          const errorMessages: string[] = [];
          
          Object.entries(data).forEach(([key, value]) => {
            const messages = Array.isArray(value) ? value : [value];
            
            messages.forEach((msg: string) => {
              if (msg.includes('already exists')) {
                if (key === 'username') {
                  errorMessages.push('Este nome de usuário já está em uso.');
                } else if (key === 'email') {
                  errorMessages.push('Este e-mail já está cadastrado.');
                } else {
                  errorMessages.push(msg);
                }
              } else {
                errorMessages.push(msg);
              }
            });
          });
          
          if (errorMessages.length > 0) {
            errorMessage = errorMessages.join('\n');
          }
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
      } else if (e.message) {
        errorMessage = e.message;
      }
      
      // Exibir notificação de erro
      showError(errorMessage);
      
      error.value = errorMessage;
      return { success: false, error: errorMessage };
    } finally {
      isLoading.value = false;
    }
  };

  // Inicializar o estado do usuário se autenticado (apenas no cliente)
  if (typeof window !== 'undefined' && isAuthenticated.value) {
    user.value = getCurrentUser();
  }

  return {
    // Estados
    user: readonly(user),
    isLoading: readonly(isLoading),
    error: readonly(error),
    isAuthenticated,

    // Métodos
    login,
    logout,
    register,
    checkAuth,
    getCurrentUser,
    updateProfile,
    refreshToken,
  };
};
