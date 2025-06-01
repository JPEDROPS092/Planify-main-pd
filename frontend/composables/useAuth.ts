import { ref, computed } from 'vue';
import { useState } from '#imports';
import { ApiError } from '~/services/api/config';
import {
  createAuthToken,
  retrieveAuthUsersMe,
  refreshAuthTokenCreate,
} from '~/services/api/auth';

export const useAuth = () => {
  // Usar useState para persistir o estado do usuário entre componentes
  const user = useState('user', () => null);
  const isAuthenticated = computed(() => !!user.value);
  const isLoading = ref(false);
  const error = ref('');

  // Tokens de autenticação
  const accessToken = useState<string | null>('auth.accessToken', () => {
    return process.client ? localStorage.getItem('auth_token') : null;
  });

  const refreshToken = useState<string | null>('auth.refreshToken', () => {
    return process.client ? localStorage.getItem('refresh_token') : null;
  });

  // Verificar se o usuário está autenticado
  const checkAuth = async () => {
    if (!accessToken.value) {
      user.value = null;
      return false;
    }

    try {
      isLoading.value = true;

      // Usando o novo serviço de API para buscar o usuário atual
      const userData = await retrieveAuthUsersMe();
      user.value = userData;
      return true;
    } catch (err) {
      console.error('Erro ao verificar autenticação inicial:', err);

      // Tratamento de erro específico
      if (
        err instanceof ApiError &&
        (err.status === 401 || err.status === 403)
      ) {
        console.log('Token de acesso inválido/expirado, tentando refresh...');
        try {
          await refreshAuthToken(); // Tenta atualizar o token
          // Se o refresh funcionou, o accessToken.value foi atualizado.
          // Tentar buscar o usuário novamente.
          console.log(
            'Refresh bem-sucedido, tentando buscar usuário novamente...'
          );
          const userDataAfterRefresh = await retrieveAuthUsersMe();
          user.value = userDataAfterRefresh;
          return true; // Autenticação bem-sucedida após refresh
        } catch (refreshErr) {
          console.error(
            'Falha ao atualizar token durante checkAuth:',
            refreshErr
          );
          // Se o refresh falhar, aí sim limpar tudo e deslogar
          if (process.client) {
            localStorage.removeItem('auth_token');
            localStorage.removeItem('refresh_token');
          }
          accessToken.value = null;
          refreshToken.value = null; // Garante que refreshToken também seja limpo
          user.value = null;
          return false;
        }
      } else {
        // Se o erro não for 401/403, ou se não for ApiError, apenas desloga
        console.error(
          'Erro não relacionado a token inválido durante checkAuth, deslogando:',
          err
        );
        if (process.client) {
          localStorage.removeItem('auth_token');
          localStorage.removeItem('refresh_token');
        }
        accessToken.value = null;
        refreshToken.value = null;
        user.value = null;
        return false;
      }
    } finally {
      isLoading.value = false;
    }
  };

  // Fazer login
  const login = async (credentials: { username: string; password: string }) => {
    isLoading.value = true;
    error.value = '';

    try {
      // Usando o novo serviço de API para login
      const tokenData = await createAuthToken(credentials);

      // Salvar tokens
      if (process.client) {
        localStorage.setItem('auth_token', tokenData.access);
        if (tokenData.refresh) {
          localStorage.setItem('refresh_token', tokenData.refresh);
        }
      }

      accessToken.value = tokenData.access;
      if (tokenData.refresh) {
        refreshToken.value = tokenData.refresh;
      }

      // Buscar dados do usuário
      const userData = await retrieveAuthUsersMe();
      user.value = userData;

      return userData;
    } catch (err) {
      console.error('Erro ao fazer login:', err);

      if (err instanceof ApiError) {
        if (err.status === 400 || err.status === 401) {
          error.value =
            'Usuário ou senha inválidos. Verifique seus dados e tente novamente.';
        } else if (err.status === 403) {
          if (
            err.data &&
            err.data.detail &&
            err.data.detail.includes('locked')
          ) {
            error.value =
              'Sua conta foi bloqueada devido a múltiplas tentativas de login inválidas. Entre em contato com um administrador.';
          } else {
            error.value =
              'Acesso negado. Você não tem permissão para acessar este recurso.';
          }
        } else if (err.status >= 500) {
          error.value =
            'Ocorreu um erro no servidor. Por favor, tente novamente mais tarde.';
        } else {
          error.value =
            err.data?.detail ||
            err.message ||
            'Ocorreu um erro ao tentar fazer login. Por favor, tente novamente.';
        }
      } else if (err instanceof Error) {
        error.value = err.message;
      } else {
        error.value =
          'Ocorreu um erro desconhecido ao fazer login. Por favor, tente novamente.';
      }

      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Fazer logout
  const logout = () => {
    if (process.client) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    navigateTo('/login');
  };

  // Atualizar token usando refresh token
  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      console.warn('Refresh token não disponível, redirecionando para login');
      if (process.client) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
      }
      accessToken.value = null;
      refreshToken.value = null;
      user.value = null;
      throw new Error('Refresh token não disponível');
    }

    try {
      console.log('Tentando atualizar token com refresh token');
      const tokenData = await refreshAuthTokenCreate({
        refresh: refreshToken.value,
      });

      if (process.client) {
        localStorage.setItem('auth_token', tokenData.access);
        // Se um novo refresh token for fornecido, atualize-o também
        if (tokenData.refresh) {
          localStorage.setItem('refresh_token', tokenData.refresh);
          refreshToken.value = tokenData.refresh;
        }
      }

      accessToken.value = tokenData.access;
      console.log('Token atualizado com sucesso');
      return tokenData.access;
    } catch (err) {
      console.error('Erro ao atualizar token:', err);

      // Limpar dados de autenticação
      if (process.client) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
      }

      accessToken.value = null;
      refreshToken.value = null;
      user.value = null;

      // Se estivermos em uma rota protegida, redirecione para o login
      const route = useRoute();
      const protectedRoutes = [
        '/projetos',
        '/tarefas',
        '/equipes',
        '/comunicacoes',
        '/dashboard',
        '/riscos',
        '/documentos',
        '/custos',
      ];

      const isProtectedRoute = protectedRoutes.some((path) =>
        route.path.startsWith(path)
      );
      if (isProtectedRoute && process.client) {
        console.log('Redirecionando para login após falha no refresh token');
        navigateTo('/login');
      }

      throw err;
    }
  };

  // Obter o usuário atual
  const getCurrentUser = () => {
    if (user.value) return user.value;
    return checkAuth().then(() => user.value);
  };

  // Verificar se o usuário tem permissão para acessar um recurso
  const hasPermission = (resource, action) => {
    if (!user.value) return false;

    // Administradores têm acesso a tudo
    if (user.value.is_staff) return true;

    // Verificações específicas por tipo de recurso
    switch (resource) {
      case 'project':
        // Verificar se o usuário é gerente ou membro do projeto
        return action === 'view' || user.value.role === 'manager';
      case 'task':
        // Qualquer um pode ver tarefas, apenas gerentes podem deletar
        return action !== 'delete' || user.value.role === 'manager';
      default:
        return false;
    }
  };

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    checkAuth,
    refreshAuthToken,
    getCurrentUser,
    hasPermission,
  };
};
