/**
 * Serviço de autenticação do Planify
 * Fornece funções para autenticação e gerenciamento de usuários
 */
import { $fetch } from 'ofetch';
import { useNuxtApp } from '#app';
import { useState, computed } from '#imports';
import {
  API_CONFIG,
  ApiError,
  createFormData,
  getApiConfig,
  getAuthToken,
} from './config';
import type {
  TokenObtainPairRequest,
  TokenObtainPair,
  TokenRefreshRequest,
  TokenRefresh,
  User,
  UserCreatePasswordRetypeRequest,
  UserCreatePasswordRetype,
  SetPasswordRetypeRequest,
  SendEmailResetRequest,
  SetNewPasswordRequest,
  PaginatedResponse,
} from './types';

/**
 * Opções para requisições fetch
 */
type FetchOptions = {
  method?: string;
  body?: any;
  params?: Record<string, any>;
  headers?: Record<string, string>;
  baseURL?: string;
};

/**
 * Composable para gerenciamento de autenticação
 * Fornece estado reativo e métodos para autenticação do usuário
 */
export const useAuth = () => {
  // Estado reativo para o token de acesso
  const accessToken = useState<string | null>('auth.accessToken', () => {
    return process.client ? localStorage.getItem('auth_token') : null;
  });

  // Estado reativo para o token de refresh
  const refreshToken = useState<string | null>('auth.refreshToken', () => {
    return process.client ? localStorage.getItem('refresh_token') : null;
  });

  // Estado reativo para os dados do usuário
  const user = useState<User | null>('auth.user', () => null);

  // Computed para verificar se o usuário está autenticado
  const isAuthenticated = computed(() => !!accessToken.value);

  /**
   * Salva os tokens de autenticação no estado e localStorage
   * @param tokens Tokens de autenticação
   */
  const saveTokens = (tokens: TokenObtainPair | TokenRefresh) => {
    accessToken.value = tokens.access;
    if ('refresh' in tokens && tokens.refresh) {
      refreshToken.value = tokens.refresh;
    }

    if (process.client) {
      localStorage.setItem('auth_token', tokens.access);
      if ('refresh' in tokens && tokens.refresh) {
        localStorage.setItem('refresh_token', tokens.refresh);
      }
    }

    console.log('Tokens salvos com sucesso');
  };

  /**
   * Limpa os tokens de autenticação do estado e localStorage
   */
  const clearTokens = () => {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;

    if (process.client) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }

    console.log('Tokens removidos');
  };

  /**
   * Realiza o login do usuário
   * @param credentials Credenciais de login (username e password)
   * @returns true se o login foi bem-sucedido
   */
  const login = async (credentials: TokenObtainPairRequest) => {
    console.log('Tentando login para usuário:', credentials.username);
    try {
      const tokens = await createAuthToken(credentials);
      console.log('Login bem-sucedido');
      saveTokens(tokens);
      await fetchCurrentUser();
      return true;
    } catch (error: any) {
      console.error('Falha no login:', error.message || 'Erro desconhecido');
      clearTokens();
      throw error;
    }
  };

  /**
   * Realiza o logout do usuário
   */
  const logout = () => {
    console.log('Realizando logout');
    clearTokens();
  };

  // Função para atualizar o token
  const refreshAuthToken = async () => {
    if (!refreshToken.value) {
      authLogger.error('Refresh token não disponível');
      throw new Error('Refresh token não disponível');
    }

    authLogger.info('Atualizando token de acesso');
    try {
      const tokens = await refreshAuthTokenCreate({
        refresh: refreshToken.value,
      });
      authLogger.info('Token atualizado com sucesso');
      saveTokens(tokens);
      return tokens;
    } catch (error: any) {
      authLogger.error(
        'Falha ao atualizar token:',
        error.message || 'Erro desconhecido'
      );
      clearTokens();
      throw error;
    }
  };

  // Função para buscar o usuário atual
  const fetchCurrentUser = async () => {
    authLogger.info('Buscando informações do usuário atual');
    try {
      user.value = await retrieveAuthUsersMe();
      authLogger.info(
        'Informações do usuário obtidas com sucesso',
        user.value?.username
      );
      return user.value;
    } catch (error: any) {
      authLogger.error(
        'Falha ao buscar usuário atual:',
        error.message || 'Erro desconhecido'
      );
      throw error;
    }
  };

  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    login,
    logout,
    refreshAuthToken,
    fetchCurrentUser,
  };
};

/**
 * Função para criar um cliente fetch configurado com autenticação
 */
export const createFetchClient = () => {
  // Criamos uma função interna que só vai acessar o useAuth quando for chamada
  // e não durante a inicialização do módulo
  return async <T>(url: string, options: FetchOptions = {}): Promise<T> => {
    const { method = 'GET', body, headers = {}, baseURL } = options;

    // Obter configurações da API
    const apiConfig = getApiConfig();

    // Configurar headers
    const mergedHeaders = {
      ...API_CONFIG.headers,
      ...headers,
    };

    // Adicionar token de autenticação se disponível
    const token = getAuthToken();
    if (token) {
      mergedHeaders.Authorization = `Bearer ${token}`;
    }

    // Configurar URL base
    const finalBaseURL = baseURL || apiConfig.baseURL;

    // Configurar opções finais
    const fetchOptions: any = {
      method,
      headers: mergedHeaders,
    };

    // Adicionar body se existir
    if (body !== undefined) {
      fetchOptions.body = body;
    }

    // Converter body para JSON se não for FormData
    if (fetchOptions.body && !(fetchOptions.body instanceof FormData)) {
      fetchOptions.body = JSON.stringify(fetchOptions.body);
    }

    try {
      console.debug(`Requisitando ${method} ${finalBaseURL}${url}`);

      // Fazer a requisição
      const response = await $fetch<T>(url, {
        baseURL: finalBaseURL,
        ...fetchOptions,
      });

      console.debug('Resposta recebida com sucesso');
      return response;
    } catch (error: any) {
      console.error(
        `Erro na requisição ${method} ${finalBaseURL}${url}:`,
        error
      );

      // Tratar erro de token expirado
      if (error.response?.status === 401) {
        console.warn('Token expirado, tentando refresh');

        // Tentar atualizar o token
        const refreshToken = useState<string | null>('auth.refreshToken');
        const accessToken = useState<string | null>('auth.accessToken');

        if (refreshToken.value) {
          try {
            console.info('Tentando refresh do token');

            // Chamar a API de refresh
            const tokens = await refreshAuthTokenCreate({
              refresh: refreshToken.value,
            });

            // Atualizar tokens
            accessToken.value = tokens.access;
            if (tokens.refresh) {
              refreshToken.value = tokens.refresh;
            }

            // Atualizar localStorage
            if (process.client) {
              localStorage.setItem('auth_token', tokens.access);
              if (tokens.refresh) {
                localStorage.setItem('refresh_token', tokens.refresh);
              }
            }

            console.info('Token atualizado com sucesso');

            // Atualizar o header de autorização
            mergedHeaders.Authorization = `Bearer ${tokens.access}`;

            // Tentar a requisição novamente
            console.debug(
              `Repetindo requisição ${method} ${finalBaseURL}${url}`
            );

            const response = await $fetch<T>(url, {
              baseURL: finalBaseURL,
              ...fetchOptions,
              headers: mergedHeaders,
            });

            console.debug('Resposta recebida com sucesso após refresh');
            return response;
          } catch (refreshError) {
            console.error('Falha ao atualizar token:', refreshError);

            // Limpar tokens
            accessToken.value = null;
            refreshToken.value = null;

            if (process.client) {
              localStorage.removeItem('auth_token');
              localStorage.removeItem('refresh_token');
            }

            // Propagar o erro original
            throw new ApiError(
              'Sessão expirada. Por favor, faça login novamente.',
              401,
              error.response?.data
            );
          }
        }
      }

      // Converter erro para ApiError
      if (error.response) {
        throw new ApiError(
          error.response._data?.detail || error.message || 'Erro na requisição',
          error.response.status,
          error.response._data
        );
      }

      throw new ApiError(error.message || 'Erro na requisição', 500, null);
    }
  };
};

// Criamos uma função lazy para obter a instância do cliente fetch apenas quando necessário
// Isso evita que o createFetchClient seja chamado durante a inicialização do módulo
const getApi = () => {
  // Lazy initialization do cliente fetch
  return createFetchClient();
};

/**
 * Obter token de autenticação
 * @param payload Credenciais de autenticação
 */
export async function createAuthToken(
  payload: TokenObtainPairRequest
): Promise<TokenObtainPair> {
  return getApi()<TokenObtainPair>('/api/auth/token/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Atualizar token de autenticação
 * @param payload Token de refresh
 */
export async function refreshAuthTokenCreate(
  payload: TokenRefreshRequest
): Promise<TokenRefresh> {
  return getApi()<TokenRefresh>('/api/auth/token/refresh/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Listar usuários
 * @param params Parâmetros de paginação e filtro
 */
export async function listAuthUsers(params?: {
  ordering?: string;
  page?: number;
  search?: string;
}): Promise<PaginatedResponse<User>> {
  const queryParams = new URLSearchParams();

  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.search) queryParams.append('search', params.search);

  const queryString = queryParams.toString();
  const url = `/api/auth/users/${queryString ? `?${queryString}` : ''}`;

  return getApi()<PaginatedResponse<User>>(url, {
    method: 'GET',
  });
}

/**
 * Criar um novo usuário
 * @param payload Dados do usuário
 */
export async function createAuthUser(
  payload: UserCreatePasswordRetypeRequest
): Promise<UserCreatePasswordRetype> {
  return getApi()<UserCreatePasswordRetype>('/api/auth/users/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Obter detalhes de um usuário
 * @param id ID do usuário
 */
export async function retrieveAuthUser(id: number): Promise<User> {
  return getApi()<User>(`/api/auth/users/${id}/`, {
    method: 'GET',
  });
}

/**
 * Atualizar um usuário
 * @param id ID do usuário
 * @param payload Dados do usuário
 */
export async function updateAuthUser(id: number, payload: any): Promise<User> {
  return getApi()<User>(`/api/auth/users/${id}/`, {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Atualizar parcialmente um usuário
 * @param id ID do usuário
 * @param payload Dados parciais do usuário
 */
export async function partialUpdateAuthUser(
  id: number,
  payload: any
): Promise<User> {
  return getApi()<User>(`/api/auth/users/${id}/`, {
    method: 'PATCH',
    body: payload,
  });
}

/**
 * Excluir um usuário
 * @param id ID do usuário
 */
export async function destroyAuthUser(id: number): Promise<void> {
  return getApi()<void>(`/api/auth/users/${id}/`, {
    method: 'DELETE',
  });
}

/**
 * Obter o usuário atual
 */
export async function retrieveAuthUsersMe(): Promise<User> {
  return getApi()<User>('/api/auth/users/me/', {
    method: 'GET',
  });
}

/**
 * Atualizar o usuário atual
 * @param payload Dados do usuário
 */
export async function updateAuthUsersMe(payload: any): Promise<User> {
  return getApi()<User>('/api/auth/users/me/', {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Atualizar parcialmente o usuário atual
 * @param payload Dados parciais do usuário
 */
export async function partialUpdateAuthUsersMe(payload: any): Promise<User> {
  return getApi()<User>('/api/auth/users/me/', {
    method: 'PATCH',
    body: payload,
  });
}

/**
 * Alterar a senha do usuário atual
 * @param payload Nova senha e confirmação
 */
export async function createAuthUsersSetPassword(
  payload: SetPasswordRetypeRequest
): Promise<void> {
  return getApi()<void>('/api/auth/users/set_password/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Solicitar redefinição de senha
 * @param payload Email do usuário
 */
export async function createAuthUsersResetPassword(
  payload: SendEmailResetRequest
): Promise<void> {
  return getApi()<void>('/api/auth/users/reset_password/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Confirmar redefinição de senha
 * @param payload Nova senha e token
 */
export async function createAuthUsersResetPasswordConfirm(
  payload: SetNewPasswordRequest
): Promise<void> {
  return getApi()<void>('/api/auth/users/reset_password_confirm/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Ativar conta de usuário
 * @param payload UID e token de ativação
 */
export function createAuthUsersActivation(payload: {
  uid: string;
  token: string;
}): Promise<void> {
  return getApi()<void>('/api/auth/users/activation/', {
    method: 'POST',
    body: payload,
  });
}
