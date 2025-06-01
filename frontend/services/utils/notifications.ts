/**
 * Serviço de notificações
 * Gerencia notificações e feedback visual para o usuário
 */
import { ref, computed } from 'vue';

export type NotificationType = 'success' | 'error' | 'warning' | 'info' | 'loading';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  timeout?: number;
  icon?: string;
  closable?: boolean;
}

// Estado global para notificações
const notifications = ref<Notification[]>([]);

/**
 * Hook para gerenciar notificações
 * @returns Métodos e estado para gerenciar notificações
 */
export const useNotification = () => {
  /**
   * Adiciona uma nova notificação
   * @param notification Dados da notificação
   * @returns ID da notificação criada
   */
  const addNotification = (notification: Omit<Notification, 'id'>): string => {
    const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const newNotification: Notification = {
      id,
      closable: true,
      timeout: notification.type === 'loading' ? 0 : 5000,
      ...notification
    };
    
    notifications.value.push(newNotification);
    
    // Remover automaticamente após o timeout (se não for loading)
    if (newNotification.timeout && newNotification.timeout > 0) {
      setTimeout(() => {
        removeNotification(id);
      }, newNotification.timeout);
    }
    
    return id;
  };
  
  /**
   * Remove uma notificação pelo ID
   * @param id ID da notificação a remover
   */
  const removeNotification = (id: string): void => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  };
  
  /**
   * Atualiza uma notificação existente
   * @param id ID da notificação
   * @param updates Atualizações a aplicar
   */
  const updateNotification = (id: string, updates: Partial<Notification>): void => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value[index] = {
        ...notifications.value[index],
        ...updates
      };
      
      // Se o tipo mudou de loading para outro tipo, definir timeout
      if (
        notifications.value[index].type !== 'loading' &&
        updates.type &&
        updates.type !== 'loading'
      ) {
        setTimeout(() => {
          removeNotification(id);
        }, notifications.value[index].timeout || 5000);
      }
    }
  };
  
  /**
   * Exibe uma notificação de sucesso
   * @param message Mensagem da notificação
   * @param title Título opcional
   * @returns ID da notificação
   */
  const showSuccess = (message: string, title: string = 'Sucesso'): string => {
    return addNotification({
      type: 'success',
      title,
      message,
      icon: 'check-circle'
    });
  };
  
  /**
   * Exibe uma notificação de erro
   * @param message Mensagem da notificação
   * @param title Título opcional
   * @returns ID da notificação
   */
  const showError = (message: string, title: string = 'Erro'): string => {
    return addNotification({
      type: 'error',
      title,
      message,
      icon: 'x-circle'
    });
  };
  
  /**
   * Exibe uma notificação de aviso
   * @param message Mensagem da notificação
   * @param title Título opcional
   * @returns ID da notificação
   */
  const showWarning = (message: string, title: string = 'Aviso'): string => {
    return addNotification({
      type: 'warning',
      title,
      message,
      icon: 'alert-triangle'
    });
  };
  
  /**
   * Exibe uma notificação informativa
   * @param message Mensagem da notificação
   * @param title Título opcional
   * @returns ID da notificação
   */
  const showInfo = (message: string, title: string = 'Informação'): string => {
    return addNotification({
      type: 'info',
      title,
      message,
      icon: 'info'
    });
  };
  
  /**
   * Exibe uma notificação de carregamento
   * @param message Mensagem da notificação
   * @param title Título opcional
   * @returns ID da notificação
   */
  const showLoading = (message: string, title: string = 'Carregando'): string => {
    return addNotification({
      type: 'loading',
      title,
      message,
      icon: 'loader',
      closable: false
    });
  };
  
  /**
   * Exibe uma notificação de erro para erros de API
   * @param error Erro da API
   * @returns ID da notificação
   */
  const showApiError = (error: any): string => {
    let message = 'Ocorreu um erro inesperado.';
    let title = 'Erro';
    
    if (error.status) {
      title = `Erro ${error.status}`;
      message = error.friendlyMessage || error.message || message;
    } else if (error.message) {
      message = error.message;
    }
    
    return showError(message, title);
  };
  
  /**
   * Envolve uma promessa com notificações de carregamento, sucesso e erro
   * @param promise Promessa a envolver
   * @param options Opções de configuração
   * @returns Promessa original com notificações
   */
  const withLoading = async <T>(
    promise: Promise<T>,
    options: {
      loadingMessage?: string;
      successMessage?: string;
      errorMessage?: string;
    } = {}
  ): Promise<T> => {
    const loadingId = showLoading(
      options.loadingMessage || 'Processando sua solicitação...'
    );
    
    try {
      const result = await promise;
      
      // Atualizar notificação para sucesso
      if (options.successMessage) {
        updateNotification(loadingId, {
          type: 'success',
          title: 'Sucesso',
          message: options.successMessage,
          icon: 'check-circle'
        });
      } else {
        removeNotification(loadingId);
      }
      
      return result;
    } catch (error) {
      // Atualizar notificação para erro
      updateNotification(loadingId, {
        type: 'error',
        title: 'Erro',
        message: options.errorMessage || (error as any).message || 'Ocorreu um erro inesperado.',
        icon: 'x-circle'
      });
      
      throw error;
    }
  };
  
  return {
    // Estado
    notifications: computed(() => notifications.value),
    
    // Métodos básicos
    addNotification,
    removeNotification,
    updateNotification,
    
    // Métodos de conveniência
    showSuccess,
    showError,
    showWarning,
    showInfo,
    showLoading,
    showApiError,
    withLoading
  };
};
