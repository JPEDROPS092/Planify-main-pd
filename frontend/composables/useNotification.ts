// composables/useNotification.ts
import { ref, h, render } from 'vue';

type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface NotificationOptions {
  title?: string;
  duration?: number;
  persistent?: boolean;
}

interface Notification {
  id: string;
  type: NotificationType;
  message: string;
  title?: string;
  duration: number;
  persistent: boolean;
  timestamp: number;
}

export const useNotification = () => {
  const notifications = ref<Notification[]>([]);
  const nextId = ref(0);

  // Função para gerar ID único
  const generateId = (): string => {
    return `notification-${Date.now()}-${++nextId.value}`;
  };

  // Função para criar uma notificação
  const createNotification = (
    type: NotificationType,
    message: string,
    options: NotificationOptions = {}
  ): string => {
    const {
      title,
      duration = type === 'error' ? 5000 : 3000,
      persistent = false,
    } = options;

    const notification: Notification = {
      id: generateId(),
      type,
      message,
      title,
      duration,
      persistent,
      timestamp: Date.now(),
    };

    notifications.value.push(notification);

    // Auto remover notificação se não for persistente
    if (!persistent && duration > 0) {
      setTimeout(() => {
        removeNotification(notification.id);
      }, duration);
    }

    return notification.id;
  };

  // Função para remover notificação
  const removeNotification = (id: string) => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index > -1) {
      notifications.value.splice(index, 1);
    }
  };

  // Função para limpar todas as notificações
  const clearAll = () => {
    notifications.value = [];
  };

  // Métodos específicos para cada tipo
  const success = (message: string, options?: NotificationOptions) => {
    return createNotification('success', message, options);
  };

  const error = (message: string, options?: NotificationOptions) => {
    return createNotification('error', message, options);
  };

  const warning = (message: string, options?: NotificationOptions) => {
    return createNotification('warning', message, options);
  };

  const info = (message: string, options?: NotificationOptions) => {
    return createNotification('info', message, options);
  };

  // Função especializada para erros de API
  const showApiError = (error: any, defaultMessage = 'Ocorreu um erro inesperado') => {
    let message = defaultMessage;

    if (typeof error === 'string') {
      message = error;
    } else if (error?.response?.data?.message) {
      message = error.response.data.message;
    } else if (error?.response?.data?.error) {
      message = error.response.data.error;
    } else if (error?.message) {
      message = error.message;
    } else if (error?.data?.message) {
      message = error.data.message;
    }

    return createNotification('error', message, { duration: 5000 });
  };

  // Função para mostrar toast simples (compatibilidade)
  const toast = {
    success: (message: string) => success(message),
    error: (message: string) => error(message),
    warning: (message: string) => warning(message),
    info: (message: string) => info(message),
  };

  return {
    // Estado
    notifications: readonly(notifications),

    // Métodos principais
    success,
    error,
    warning,
    info,

    // Aliases para compatibilidade (destructuring aliases)
    showSuccess: success,
    showError: error,
    showWarning: warning,
    showInfo: info,

    // Métodos especiais
    showApiError,
    toast,

    // Utilitários
    removeNotification,
    clearAll,
    createNotification,
  };
};

// Composable global para notificações (singleton pattern)
let globalNotificationInstance: ReturnType<typeof useNotification> | null = null;

export const useGlobalNotification = () => {
  if (!globalNotificationInstance) {
    globalNotificationInstance = useNotification();
  }
  return globalNotificationInstance;
};
