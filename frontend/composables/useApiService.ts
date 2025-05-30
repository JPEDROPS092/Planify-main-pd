/**
 * Composable para utilização dos serviços da API
 */
import { ApiError } from '~/services/api/config'
import { useAuth } from '~/composables/useAuth'
import { useNotification } from '~/composables/useNotification'

export const useApiService = () => {
  const auth = useAuth()
  const notification = useNotification()
  
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
    } = {}
  ): Promise<T | null> => {
    const {
      loadingMessage = 'Carregando...',
      successMessage = 'Operação realizada com sucesso!',
      errorMessage = 'Ocorreu um erro ao realizar a operação.',
      showSuccess = true,
      showError = true
    } = options
    
    let notificationId = null
    
    try {
      // Exibir notificação de loading
      notificationId = notification.loading(loadingMessage)
      
      // Executar a operação
      const result = await operation()
      
      // Exibir notificação de sucesso
      if (showSuccess) {
        notification.success(successMessage, { id: notificationId })
      } else if (notificationId) {
        notification.dismiss(notificationId)
      }
      
      return result
    } catch (error) {
      // Tratar erro de autenticação
      if (error instanceof ApiError && error.status === 401) {
        // Se o erro persistir mesmo após a tentativa de refresh do token
        auth.logout()
        navigateTo('/login')
      }
      
      // Exibir notificação de erro
      if (showError) {
        const message = error instanceof ApiError 
          ? error.friendlyMessage 
          : errorMessage
        
        notification.error(message, { id: notificationId })
      } else if (notificationId) {
        notification.dismiss(notificationId)
      }
      
      console.error('API Error:', error)
      return null
    }
  }
  
  /**
   * Função para tratar erros da API e retornar mensagens amigáveis
   * @param error Erro capturado
   * @returns Mensagem de erro formatada
   */
  const handleApiError = (error: any): string => {
    if (error instanceof ApiError) {
      return error.friendlyMessage
    } else if (error instanceof Error) {
      return error.message
    } else {
      return 'Ocorreu um erro inesperado. Por favor, tente novamente.'
    }
  }
  
  return {
    withLoading,
    handleApiError
  }
}
