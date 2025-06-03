/**
 * Composable para utilização dos serviços da API
 * Fornece métodos para executar operações com feedback visual e tratamento de erros
 */
import { ApiError } from '~/services/api/client/config';
import { apiClient } from '~/services/api/services/apiClient';
import { useAuthStore } from '~/stores/modules/auth';
import { useNotification } from '~/composables/useNotification';
import { navigateTo } from '#app';
import { ref } from 'vue';

export const useApiService = () => {
  const authStore = useAuthStore();
  const notification = useNotification();
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  /**
   * Função para executar uma operação de API com tratamento de loading e erros
   * @param operation Função da API a ser executada
   * @param options Opções de configuração
   */
  const withLoading = async <T>(
    operation: () => Promise<T>,
    options: {
      loadingMessage?: string;
      successMessage?: string;
      errorMessage?: string;
      showSuccess?: boolean;
      showError?: boolean;
      redirectOnError?: string;
    } = {}
  ): Promise<T | null> => {
    const {
      loadingMessage = 'Carregando...',
      successMessage = 'Operação realizada com sucesso!',
      errorMessage = 'Ocorreu um erro ao realizar a operação.',
      showSuccess = true,
      showError = true,
      redirectOnError,
    } = options;

    let notificationId = null;
    isLoading.value = true;
    error.value = null;

    try {
      // Exibir notificação de loading
      notificationId = notification.loading(loadingMessage);

      // Executar a operação
      const result = await operation();

      // Exibir notificação de sucesso
      if (showSuccess) {
        notification.success(successMessage, { id: notificationId });
      } else if (notificationId) {
        notification.dismiss(notificationId);
      }

      return result;
    } catch (e: unknown) {
      const typedError = e as any;
      error.value = handleApiError(typedError);

      // Tratar erro de autenticação
      if (typedError instanceof ApiError && typedError.status === 401) {
        // Tentar refresh do token primeiro (já feito pelos interceptors)
        // Se ainda assim falhar, fazer logout
        authStore.logout();
        await navigateTo('/auth/login');
      }

      // Exibir notificação de erro
      if (showError) {
        const message = error.value;
        notification.error(message, { id: notificationId ?? undefined });
      } else if (notificationId) {
        notification.dismiss(notificationId);
      }

      // Redirecionar se necessário
      if (redirectOnError) {
        await navigateTo(redirectOnError);
      }

      console.error('API Error:', typedError);
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Função para tratar erros da API e retornar mensagens amigáveis
   * @param e Erro capturado
   * @returns Mensagem de erro formatada
   */
  const handleApiError = (e: unknown): string => {
    if (e instanceof ApiError) {
      return e.friendlyMessage;
    } else if (e instanceof Error) {
      return e.message;
    } else {
      return 'Ocorreu um erro inesperado. Por favor, tente novamente.';
    }
  };

  /**
   * Executa uma requisição GET com feedback visual
   * @param url URL da requisição
   * @param config Configuração da requisição
   * @param options Opções de feedback
   */
  const get = async <T>(
    url: string,
    config: any = {},
    options: any = {}
  ): Promise<T | null> => {
    return withLoading<T>(
      async () => await apiClient.get<T>(url, config),
      options
    );
  };

  /**
   * Executa uma requisição POST com feedback visual
   * @param url URL da requisição
   * @param data Dados a serem enviados
   * @param config Configuração da requisição
   * @param options Opções de feedback
   */
  const post = async <T>(
    url: string,
    data: any = {},
    config: any = {},
    options: any = {}
  ): Promise<T | null> => {
    return withLoading<T>(
      async () => await apiClient.post<T>(url, data, config),
      options
    );
  };

  /**
   * Executa uma requisição PUT com feedback visual
   * @param url URL da requisição
   * @param data Dados a serem enviados
   * @param config Configuração da requisição
   * @param options Opções de feedback
   */
  const put = async <T>(
    url: string,
    data: any = {},
    config: any = {},
    options: any = {}
  ): Promise<T | null> => {
    return withLoading<T>(
      async () => await apiClient.put<T>(url, data, config),
      options
    );
  };

  /**
   * Executa uma requisição PATCH com feedback visual
   * @param url URL da requisição
   * @param data Dados a serem enviados
   * @param config Configuração da requisição
   * @param options Opções de feedback
   */
  const patch = async <T>(
    url: string,
    data: any = {},
    config: any = {},
    options: any = {}
  ): Promise<T | null> => {
    return withLoading<T>(
      async () => await apiClient.patch<T>(url, data, config),
      options
    );
  };

  /**
   * Executa uma requisição DELETE com feedback visual
   * @param url URL da requisição
   * @param config Configuração da requisição
   * @param options Opções de feedback
   */
  const del = async <T>(
    url: string,
    config: any = {},
    options: any = {}
  ): Promise<T | null> => {
    return withLoading<T>(
      async () => await apiClient.delete<T>(url, config),
      options
    );
  };

  return {
    withLoading,
    handleApiError,
    get,
    post,
    put,
    patch,
    delete: del,
    isLoading,
    error,
    // Expor o cliente API diretamente para casos especiais
    client: apiClient
  };
};
