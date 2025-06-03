// filepath: /home/jpcode092/projects/Planify-main-pd/frontend/stores/composables/withLoading.ts
import { ref, } from 'vue';
import { useNotification } from './useNotification';

/**
 * Composable for handling loading states and wrapping async operations
 */
export function withLoading() {
  const loading = ref(false);
  const error = ref<Error | null>(null);

  /**
   * Executes a promise while managing loading state
   * @param fn Async function to execute
   * @param options Optional configuration
   * @returns Result of the promise
   */
  async function execute<T>(
    fn: () => Promise<T>,
    options: {
      silent?: boolean;
      loadingMessage?: string;
      successMessage?: string;
      errorMessage?: string;
      resetErrorOnStart?: boolean;
    } = {}
  ): Promise<T | undefined> {
    const {
      silent = false,
      loadingMessage = 'Carregando...',
      successMessage = 'Operação concluída com sucesso',
      errorMessage,
      resetErrorOnStart = true,
    } = options;

    if (resetErrorOnStart) {
      error.value = null;
    }

    loading.value = true;

    const notification = useNotification();
    let loadingId: string | undefined;

    if (!silent && loadingMessage) {
      loadingId = notification.loading(loadingMessage);
    }

    try {
      const result = await fn();
      
      if (!silent && successMessage) {
        if (loadingId) {
          notification.remove(loadingId);
        }
        notification.success(successMessage);
      }

      return result;
    } catch (err) {
      error.value = err as Error;

      if (!silent) {
        if (loadingId) {
          notification.remove(loadingId);
        }
        
        notification.showApiError(err);
      }
      
      console.error('Error in withLoading:', err);
    } finally {
      loading.value = false;
    }
  }

  /**
   * Wraps a component method with loading state
   * @param method The method to wrap
   * @param options Optional configuration
   * @returns A wrapped method that manages loading state
   */
  function wrapMethod<T>(
    method: (...args: any[]) => Promise<T>,
    options: {
      silent?: boolean;
      loadingMessage?: string;
      successMessage?: string;
      errorMessage?: string;
    } = {}
  ) {
    return async (...args: any[]): Promise<T | undefined> => {
      return execute(() => method(...args), options);
    };
  }

  return {
    loading,
    error,
    execute,
    wrapMethod,
  };
}

/**
 * Helper function to wrap an async operation with loading state
 * without creating a composable instance
 */
export async function executeWithLoading<T>(
  fn: () => Promise<T>,
  options: {
    withNotifications?: boolean;
    loadingMessage?: string;
    successMessage?: string;
    errorMessage?: string;
  } = {}
): Promise<T | undefined> {
  const {
    withNotifications = true,
    loadingMessage = 'Carregando...',
    successMessage = 'Operação concluída com sucesso',
    errorMessage,
  } = options;

  if (withNotifications) {
    const notification = useNotification();
    return notification.withLoading(fn(), {
      loadingMessage,
      successMessage,
      errorMessage,
    });
  } else {
    try {
      return await fn();
    } catch (error) {
      console.error('Error in executeWithLoading:', error);
      throw error;
    }
  }
}