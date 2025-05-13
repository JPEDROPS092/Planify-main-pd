import { ref, reactive } from 'vue'
import { ApiError } from '~/services/api'

export type NotificationType = 'success' | 'error' | 'warning' | 'info' | 'loading'

export interface Notification {
  id: string
  type: NotificationType
  message: string
  title?: string
  duration?: number
  autoClose?: boolean
  icon?: string
  progress?: number
}

// Estado global para notificações
const notifications = reactive<Notification[]>([])

// Estado para rastrear notificações de loading
const loadingNotifications = reactive<Record<string, string>>({})

export const useNotification = () => {
  // Adicionar uma nova notificação
  const notify = (
    type: NotificationType,
    message: string,
    options: { 
      title?: string; 
      duration?: number; 
      autoClose?: boolean;
      icon?: string;
      progress?: number;
    } = {}
  ) => {
    const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    
    const notification: Notification = {
      id,
      type,
      message,
      title: options.title,
      duration: options.duration ?? (type === 'error' ? 8000 : 5000),
      autoClose: options.autoClose ?? (type !== 'loading'),
      icon: options.icon,
      progress: options.progress
    }
    
    // Para notificações do tipo loading, armazenar o ID para referência futura
    if (type === 'loading') {
      loadingNotifications[message] = id
    }
    
    notifications.push(notification)
    
    // Remover automaticamente após a duração, se autoClose for true
    if (notification.autoClose && notification.duration) {
      setTimeout(() => {
        remove(id)
      }, notification.duration)
    }
    
    return id
  }
  
  // Remover uma notificação pelo ID
  const remove = (id: string) => {
    const index = notifications.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.splice(index, 1)
    }
  }
  
  // Limpar todas as notificações
  const clear = () => {
    notifications.splice(0, notifications.length)
  }
  
  // Métodos de conveniência para diferentes tipos de notificações
  const success = (message: string, options = {}) => notify('success', message, { 
    icon: 'check-circle', 
    ...options 
  })
  
  const error = (message: string, options = {}) => notify('error', message, { 
    icon: 'alert-circle', 
    ...options 
  })
  
  const warning = (message: string, options = {}) => notify('warning', message, { 
    icon: 'alert-triangle', 
    ...options 
  })
  
  const info = (message: string, options = {}) => notify('info', message, { 
    icon: 'info', 
    ...options 
  })
  
  const loading = (message: string, options = {}) => notify('loading', message, { 
    icon: 'loader', 
    autoClose: false, 
    ...options 
  })
  
  // Atualizar notificação de loading para sucesso
  const loadingSuccess = (loadingMessage: string, successMessage: string, options = {}) => {
    const loadingId = loadingNotifications[loadingMessage]
    if (loadingId) {
      // Remover a notificação de loading
      remove(loadingId)
      // Remover da lista de loadings
      delete loadingNotifications[loadingMessage]
      // Criar notificação de sucesso
      return success(successMessage, options)
    }
    // Se não encontrar o loading, apenas criar uma notificação de sucesso
    return success(successMessage, options)
  }
  
  // Atualizar notificação de loading para erro
  const loadingError = (loadingMessage: string, errorMessage: string, options = {}) => {
    const loadingId = loadingNotifications[loadingMessage]
    if (loadingId) {
      // Remover a notificação de loading
      remove(loadingId)
      // Remover da lista de loadings
      delete loadingNotifications[loadingMessage]
      // Criar notificação de erro
      return error(errorMessage, options)
    }
    // Se não encontrar o loading, apenas criar uma notificação de erro
    return error(errorMessage, options)
  }
  
  // Método para exibir erros da API
  const showApiError = (err: any) => {
    // Verificar se é um erro da API
    if (err instanceof ApiError) {
      error(err.friendlyMessage || 'Ocorreu um erro na requisição', {
        title: `Erro ${err.status || ''}`,
        duration: 8000
      })
    } else if (err && err.message) {
      // Erro genérico com mensagem
      error(err.message, {
        title: 'Erro',
        duration: 8000
      })
    } else {
      // Fallback para erro desconhecido
      error('Ocorreu um erro inesperado. Por favor, tente novamente.', {
        title: 'Erro',
        duration: 8000
      })
    }
  }
  
  // Método para envolver uma promessa com notificações de loading/sucesso/erro
  const withLoading = async <T>(
    promise: Promise<T>, 
    options: {
      loadingMessage: string;
      successMessage: string;
      errorMessage?: string;
    }
  ): Promise<T> => {
    const loadingId = loading(options.loadingMessage)
    
    try {
      const result = await promise
      remove(loadingId)
      success(options.successMessage)
      return result
    } catch (err) {
      remove(loadingId)
      const errorMsg = options.errorMessage || 
        (err instanceof ApiError ? err.friendlyMessage : 'Ocorreu um erro inesperado')
      showApiError(err)
      throw err
    }
  }

  return {
    notifications,
    notify,
    success,
    error,
    warning,
    info,
    loading,
    loadingSuccess,
    loadingError,
    remove,
    clear,
    showApiError,
    withLoading
  }
}
