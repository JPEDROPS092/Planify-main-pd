// frontend/stores/composables/useNotification.ts
import { ref } from 'vue';

export interface NotificationMessage {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'loading';
  title?: string; // Adicionado título opcional
  message: string;
  duration?: number; // Duration in ms, undefined or 0 for persistent
  autoClose?: boolean; // Adicionado autoClose opcional
}

// Reactive state for notifications
// This state is defined outside the composable function to be a singleton.
const notifications = ref<NotificationMessage[]>([]);

let idCounter = 0;

/**
 * Composable for managing and displaying notifications.
 */
export function useNotification() {
  const generateId = (): string => {
    idCounter += 1;
    return `notification-${idCounter}`;
  };

  /**
   * Adds a new notification.
   * @param message The message content.
   * @param type The type of notification.
   * @param options Optional parameters like duration or an existing ID to update.
   * @returns The ID of the notification.
   */
  const addNotification = (
    message: string,
    type: NotificationMessage['type'],
    options: { title?: string; duration?: number; id?: string; autoClose?: boolean } = {}
  ): string => {
    const id = options.id || generateId();
    
    // Remove existing notification with the same ID if updating
    if (options.id) {
      notifications.value = notifications.value.filter(n => n.id !== options.id);
    }

    const newNotification: NotificationMessage = {
      id,
      type,
      title: options.title,
      message,
      duration: options.duration,
      // Ensure autoClose is explicitly boolean or undefined.
      // If autoClose is provided in options, use it. Otherwise, default to true if duration is positive, false otherwise.
      autoClose: typeof options.autoClose === 'boolean' ? options.autoClose : (options.duration && options.duration > 0 ? true : false)
    };

    // For loading type, if autoClose is not explicitly set to true, default it to false (persistent)
    if (type === 'loading' && typeof options.autoClose !== 'boolean') {
        newNotification.autoClose = false;
    }
    // If duration is 0 or undefined for loading, ensure autoClose is false unless specified.
    if (type === 'loading' && (!newNotification.duration || newNotification.duration <=0) && typeof options.autoClose !== 'boolean' ) {
        newNotification.autoClose = false;
    }


    notifications.value.push(newNotification);
    console.log(`[Notification Mock] ${type.toUpperCase()}: ${options.title ? '['+options.title+'] ' : ''}${message} (ID: ${id})`);

    // Auto-dismiss after duration if specified and autoClose is true
    if (newNotification.autoClose && newNotification.duration && newNotification.duration > 0) {
      setTimeout(() => dismiss(id), newNotification.duration);
    }
    return id;
  };

  /**
   * Dismisses a notification by its ID.
   * @param id The ID of the notification to dismiss.
   */
  const dismiss = (id: string): void => {
    notifications.value = notifications.value.filter(n => n.id !== id);
    console.log(`[Notification Mock] Dismissed: (ID: ${id})`);
  };

  // Shortcut methods, agora podem aceitar title e autoClose
  const info = (message: string, options: { title?: string; duration?: number; id?: string; autoClose?: boolean; position?: string } = {}) => 
    addNotification(message, 'info', options);
  const success = (message: string, options: { title?: string; duration?: number; id?: string; autoClose?: boolean; position?: string } = {}) =>
    addNotification(message, 'success', options);
  const warning = (message: string, options: { title?: string; duration?: number; id?: string; autoClose?: boolean; position?: string } = {}) =>
    addNotification(message, 'warning', options);
  const error = (message: string, options: { title?: string; duration?: number; id?: string; autoClose?: boolean; position?: string } = {}) => {
    // For login errors, set a longer duration by default
    const isAuthError = options.title?.includes('Autenticação') || 
                         message.includes('login') || 
                         message.includes('senha') || 
                         message.includes('usuário') ||
                         message.includes('credenciais');
                         
    if (isAuthError && !options.duration) {
      options.duration = 8000; // Longer duration (8 seconds) for auth errors
      
      // Store the error in localStorage for persistent display
      if (process.client) {
        localStorage.setItem('last_auth_error', JSON.stringify({
          message,
          title: options.title || 'Erro de Autenticação'
        }));
        
        // Clear the error after 30 seconds
        setTimeout(() => {
          localStorage.removeItem('last_auth_error');
        }, 30000);
      }
    }
    
    return addNotification(message, 'error', options);
  }
  const loading = (message: string, options: { title?: string; duration?: number; id?: string; autoClose?: boolean } = {}): string => {
    // Loading notifications are typically persistent unless a duration and autoClose:true is specified.
    // Default duration 0 means persistent. Default autoClose for loading is false.
    const autoCloseDefault = options.duration && options.duration > 0 ? true : false;
    // Retornar o ID da notificação
    return addNotification(message, 'loading', { 
      ...options, 
      duration: options.duration || 0, // Default to 0 for persistent if not specified
      autoClose: options.autoClose ?? autoCloseDefault // If autoClose not in options, derive from duration (true if duration > 0)
    });
  }

  /**
   * Utilitário para envolver uma promessa com notificações de carregamento, sucesso e erro.
   * @param promise A promessa a ser executada
   * @param options Opções de configuração das notificações
   * @returns A promessa original com tratamento de notificações
   */
  const withLoading = async <T>(
    promise: Promise<T>,
    options: {
      loadingMessage: string;
      successMessage?: string;
      errorMessage?: string;
      loadingTitle?: string;
      successTitle?: string;
      errorTitle?: string;
      successDuration?: number;
      errorDuration?: number;
    }
  ): Promise<T> => {
    // Exibir notificação de carregamento
    const loadingId = loading(options.loadingMessage, { title: options.loadingTitle });
    
    try {
      // Executar a promessa
      const result = await promise;
      
      // Remover notificação de carregamento
      dismiss(loadingId);
      
      // Exibir notificação de sucesso, se houver mensagem
      if (options.successMessage) {
        success(options.successMessage, {
          title: options.successTitle,
          duration: options.successDuration || 3000
        });
      }
      
      return result;
    } catch (err) {
      // Remover notificação de carregamento
      dismiss(loadingId);
      
      // Determinar mensagem de erro
      const errorMsg = options.errorMessage || 
        (err instanceof Error ? err.message : 'Ocorreu um erro inesperado');
      
      // Exibir notificação de erro
      error(errorMsg, {
        title: options.errorTitle,
        duration: options.errorDuration || 5000
      });
      
      // Re-lançar o erro para tratamento adicional, se necessário
      throw err;
    }
  };

  return {
    notifications, // The reactive list of notifications for UI to bind to
    addNotification,
    dismiss,
    info,
    success,
    warning,
    error,
    loading,
    withLoading,
  };
}
