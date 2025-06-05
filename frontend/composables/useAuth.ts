// frontend/stores/composables/useAuth.ts
import { ref, computed } from 'vue';
import { useState } from '#app'; // Importar useState para estado global
import type { ExtendedUserProfile, LoginCredentials, TokenObtainPair } from '~/services/utils/types';
// Importar o serviço de API para operações com feedback visual
import { useApiService } from '~/composables/useApiService';
// Importar as funções reais da API de autenticação
import {
  createAuthToken,
  retrieveAuthUsersMe,
  refreshAuthToken as apiRefreshAuthToken,
  requestPasswordReset as apiRequestPasswordReset,
  confirmPasswordReset as apiConfirmPasswordReset,
  registerUser as apiRegisterUser
} from '~/services/api/endpoints/auth'; // Renomeado para evitar conflito
import { ApiError } from '~/services/api/client/config'; // Para tratamento de erros da API

/**
 * Composable para gerenciar o estado de autenticação e interações.
 */
export function useAuth() {
  // Estado reativo local para o composable
  const user = ref<ExtendedUserProfile | null>(null);
  const localAccessToken = ref<string | null>(null);
  const localRefreshToken = ref<string | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Estado global para o token de acesso, compartilhado com o interceptor da API e outras partes do app.
  // O valor inicial é null.
  // Tentativa de carregar do localStorage se estiver no cliente para a inicialização do useState
  const globalAccessToken = useState<string | null>('auth.accessToken', () => {
    if (process.client) {
      return localStorage.getItem('accessToken');
    }
    return null;
  });

  /**
   * Indica se o usuário está atualmente autenticado.
   * Baseia-se na presença de um token de acesso (priorizando o global) e dados do usuário.
   */
  const isAuthenticated = computed(() => !!globalAccessToken.value && !!user.value);

  /**
   * Retorna o papel/função do usuário (se disponível)
   */
  const userRole = computed(() => user.value?.role || null);

  /**
   * Checa se o input é um email
   */
  const isEmail = (input: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(input);
  };

  /**
   * Realiza o login do usuário utilizando a API.
   */
  const login = async (credentials: LoginCredentials): Promise<{ user: ExtendedUserProfile | null; accessToken: string | null; success: boolean }> => {
    isLoading.value = true;
    error.value = null;
    const api = useApiService();
    console.log('useAuth().login() - Attempting API login.');

    try {
      // Determinar se o input é um email ou username
      const isEmailInput = isEmail(credentials.username);
      
      // Criar objeto de credenciais para a API
      const loginData = {
        username: credentials.username,
        password: credentials.password,
        // Adicionar flag indicando se é email ou username
        is_email: isEmailInput
      };

      // Log request for debugging (without password)
      console.log('Login request to:', '/api/auth/token/', 
        { username: loginData.username, password: '******', is_email: loginData.is_email });

      // Obter token com feedback visual
      const tokenData = await api.withLoading<TokenObtainPair>(
        async () => await createAuthToken(loginData),
        {
          loadingMessage: 'Realizando login...',
          showSuccess: false,
          showError: false
        }
      );

      if (!tokenData) {
        throw new Error('Falha ao obter token de acesso');
      }

      // Log successful token response (without showing actual token)
      console.log('Token obtained successfully, fetching user data');

      // Armazenar tokens
      localAccessToken.value = tokenData.access;
      localRefreshToken.value = tokenData.refresh;
      globalAccessToken.value = tokenData.access;

      // Obter dados do usuário
      const userData = await api.withLoading<ExtendedUserProfile>(
        async () => await retrieveAuthUsersMe(),
        {
          loadingMessage: 'Carregando dados do usuário...',
          showSuccess: false,
          showError: false
        }
      );

      if (!userData) {
        throw new Error('Falha ao obter dados do usuário');
      }

      user.value = userData;

      // Persistir tokens no localStorage
      if (process.client) {
        if (localAccessToken.value) {
          localStorage.setItem('accessToken', localAccessToken.value);
        }
        if (localRefreshToken.value) {
          localStorage.setItem('refreshToken', localRefreshToken.value);
        }
        // Store remember me preference if provided
        if (credentials.remember) {
          localStorage.setItem('rememberMe', 'true');
        } else {
          localStorage.removeItem('rememberMe');
        }
      }
      
      console.log('Login successful, user data fetched:', user.value?.username);
      
      // Após login bem-sucedido, redirecionar para a página de dashboard
      if (process.client) {
        // Usar o router do Nuxt para redirecionar
        const router = useRouter();
        // Verificar se há um parâmetro redirect na URL
        const route = useRoute();
        const redirectPath = route.query.redirect as string || '/dashboard';
        router.push(redirectPath);
      }
      
      return { user: user.value, accessToken: localAccessToken.value, success: true };

    } catch (e: unknown) {
      const apiError = e as ApiError;
      console.error('Erro no login via API:', apiError.message, apiError.data);
      
      // Enhanced error handling for common Django REST auth errors
      let errorMessage = apiError.friendlyMessage || 'Falha no login. Verifique suas credenciais.';
      
      // Extract specific error messages from Django response formats
      if (apiError.data) {
        if (apiError.data.detail) {
          errorMessage = apiError.data.detail;
        } else if (apiError.data.non_field_errors && Array.isArray(apiError.data.non_field_errors)) {
          errorMessage = apiError.data.non_field_errors[0];
        }
      }
      
      error.value = errorMessage;
      
      // Limpar estado em caso de falha
      user.value = null;
      localAccessToken.value = null;
      localRefreshToken.value = null;
      globalAccessToken.value = null;
      if (process.client) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
      return { user: null, accessToken: null, success: false };
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Realiza o logout do usuário.
   */
  const logout = (): void => {
    console.log('useAuth().logout() - Logging out.'); // Mudado de warn para log
    user.value = null;
    localAccessToken.value = null;
    localRefreshToken.value = null;
    globalAccessToken.value = null; // Limpa o estado global
    if (process.client) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    }
    // Opcional: redirecionar para login após logout, se desejado em todos os casos.
    // Geralmente, o redirecionamento é tratado pelo middleware de rota.
    // if (process.client) navigateTo('/login');
  };

  /**
   * Verifica o estado de autenticação ao carregar a aplicação, utilizando a API.
   */
  const checkAuth = async (): Promise<void> => {
    console.log('useAuth().checkAuth() - Checking auth state.');
    isLoading.value = true;

    // No cliente, tentar carregar tokens do localStorage se `globalAccessToken` (do useState) for nulo.
    // `globalAccessToken` já tenta carregar na inicialização do useState.
    // Esta lógica aqui serve mais para sincronizar localRefreshToken se globalAccessToken foi encontrado.
    if (process.client) {
        if (globalAccessToken.value && !localAccessToken.value) {
            localAccessToken.value = globalAccessToken.value; // Sincroniza local com global
        }
        if (globalAccessToken.value && !localRefreshToken.value) {
            const storedRefreshToken = localStorage.getItem('refreshToken');
            if (storedRefreshToken) {
                localRefreshToken.value = storedRefreshToken;
            }
        }
    }


    if (globalAccessToken.value) {
      // Se temos um token global, tentamos buscar o usuário
      // Sincronizar localAccessToken com globalAccessToken, caso ainda não esteja.
      if (!localAccessToken.value) {
          localAccessToken.value = globalAccessToken.value;
      }

      try {
        // Evitar buscar usuário se já estiver carregado e o token é o mesmo
        // (Esta condição pode precisar de ajuste se o usuário pode mudar sem mudar o token)
        if (!user.value) {
            const userData = await retrieveAuthUsersMe(); // Usa o globalAccessToken implicitamente pelo interceptor
            user.value = userData;
            console.log('User data fetched successfully by checkAuth:', user.value?.username);
        }
      } catch (e) {
        const apiError = e as ApiError;
        console.warn('checkAuth: Failed to retrieve user with current token.', apiError.message);
        // Se retrieveAuthUsersMe falhar (ex: token inválido/expirado), limpar tudo.
        logout(); // Limpa tokens e usuário
      }
    } else {
      // Nenhum token global encontrado, garantir que o estado local esteja limpo.
      if (user.value || localAccessToken.value || localRefreshToken.value) {
        console.log('checkAuth: No global token, ensuring clean local state.');
        // Chamar logout() apenas se houver algo para limpar, para evitar logs desnecessários.
        user.value = null;
        localAccessToken.value = null;
        localRefreshToken.value = null;
      }
    }
    isLoading.value = false;
  };

  /**
   * Atualiza o token de acesso usando o token de refresh via API.
   */
  const refreshUserToken = async (): Promise<string | null> => {
    console.log('useAuth().refreshUserToken() - Attempting API token refresh.');
    // Priorizar refresh token do localStorage se o local for nulo mas existir no storage
    if (process.client && !localRefreshToken.value) {
        const storedRefreshToken = localStorage.getItem('refreshToken');
        if (storedRefreshToken) {
            localRefreshToken.value = storedRefreshToken;
        }
    }

    if (!localRefreshToken.value) {
      error.value = 'Nenhum token de atualização disponível.';
      isLoading.value = false;
      console.error(error.value);
      logout(); // Se não pode dar refresh, melhor deslogar
      return null;
    }
    
    isLoading.value = true; // Mover para depois da verificação do refresh token
    error.value = null;

    try {
      // Usar o apiService para obter o token com feedback visual
      const tokenData = await apiService.withLoading(
        async () => await apiRefreshAuthToken({ refresh: localRefreshToken.value }),
        {
          loadingMessage: 'Atualizando token...',
          showSuccess: false,
          showError: false,
        }
      );

      if (!tokenData) {
        error.value = 'Falha ao atualizar token';
        return null;
      }

      localAccessToken.value = tokenData.access;
      globalAccessToken.value = tokenData.access;
      if (tokenData.refresh) {
          localRefreshToken.value = tokenData.refresh;
      }

      if (process.client) {
        if (localAccessToken.value) {
            localStorage.setItem('accessToken', localAccessToken.value);
        }
        if (localRefreshToken.value && tokenData.refresh) { // Salva o novo refresh token se ele foi atualizado
            localStorage.setItem('refreshToken', localRefreshToken.value);
        }
      }
      console.log('Token de acesso atualizado com sucesso via API.');
      return localAccessToken.value;
    } catch (e: unknown) {
      const apiError = e as ApiError;
      console.error('Erro ao atualizar token via API:', apiError.message, apiError.data);
      error.value = apiError.friendlyMessage || 'Falha ao atualizar a sessão.';
      logout();
      return null;
    } finally {
      isLoading.value = false;
    }
  };


  /**
   * Solicita recuperação de senha para o e-mail fornecido.
   */
  const requestPasswordReset = async (email: string): Promise<{ success: boolean; message: string }> => {
    isLoading.value = true;
    error.value = null;
    const api = useApiService();

    try {
      await apiRequestPasswordReset(email);
      console.log('Solicitação de recuperação de senha enviada com sucesso');
      return { success: true, message: 'Enviamos instruções para recuperar sua senha. Por favor, verifique seu e-mail.' };
    } catch (e: unknown) {
      const apiError = e as ApiError;
      console.error('Erro ao solicitar recuperação de senha:', apiError.message, apiError.data);
      const friendlyMsg = apiError.friendlyMessage || 'Não foi possível processar sua solicitação. Verifique o e-mail informado.';
      error.value = friendlyMsg;
      return { success: false, message: friendlyMsg };
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Redefine a senha do usuário usando o token recebido por e-mail.
   */
  const resetPassword = async (data: { email: string; token: string; password: string; password_confirmation: string }): Promise<{ success: boolean; message: string }> => {
    isLoading.value = true;
    error.value = null;
    const api = useApiService();

    try {
      const apiData = {
        uid: btoa(data.email),
        token: data.token,
        new_password: data.password
      };

      await api.withLoading(
        async () => await apiConfirmPasswordReset(apiData),
        {
          loadingMessage: 'Redefinindo senha...',
          successMessage: 'Senha redefinida com sucesso!',
          errorMessage: 'Erro ao redefinir senha. Verifique o token e tente novamente.',
          showSuccess: true
        }
      );
      
      console.log('Senha redefinida com sucesso');
      return { success: true, message: 'Sua senha foi redefinida com sucesso. Você já pode fazer login com sua nova senha.' };
    } catch (e: unknown) {
      const apiError = e as ApiError;
      console.error('Erro ao redefinir senha:', apiError.message, apiError.data);
      const friendlyMsg = apiError.friendlyMessage || 'Não foi possível redefinir sua senha. O token pode ser inválido ou ter expirado.';
      error.value = friendlyMsg;
      return { success: false, message: friendlyMsg };
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Registra um novo usuário.
   */
  const register = async (userData: Partial<ExtendedUserProfile>): Promise<{ success: boolean; user?: ExtendedUserProfile; message: string; errors?: any }> => { // Ajustado tipo de retorno
    isLoading.value = true;
    error.value = null;

    try {
      const responseUser = await apiRegisterUser(userData);
      console.log('Usuário registrado com sucesso:', responseUser.username);
      return { success: true, user: responseUser, message: 'Cadastro realizado com sucesso! Você já pode fazer login.' };
    } catch (e: unknown) {
      const apiError = e as ApiError;
      console.error('Erro ao registrar usuário:', apiError.message, apiError.data);
      const friendlyMsg = apiError.friendlyMessage || 'Não foi possível completar o cadastro. Verifique os dados informados.';
      error.value = friendlyMsg;
      return { success: false, message: friendlyMsg, errors: apiError.data };
    } finally {
      isLoading.value = false;
    }
  };

  return {
    user, // ref
    // Não exponha localAccessToken e localRefreshToken diretamente se globalAccessToken é a fonte da verdade.
    // Apenas o globalAccessToken deve ser a referência para o token de acesso atual.
    // accessToken: globalAccessToken, // Expor o globalAccessToken (useState)
    isAuthenticated, // computed
    userRole, // computed - added for dashboard
    login,
    logout,
    checkAuth,
    refreshUserToken,
    requestPasswordReset,
    resetPassword,
    register,
    isLoading, // ref
    error, // ref
    // Adicionar explicitamente o globalAccessToken para que possa ser observado se necessário
    // ou usado por interceptors
    _globalAccessToken: globalAccessToken // Renomeado para indicar uso interno/avançado
  };
}