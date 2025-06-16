// composables/useApiErrorHandler.ts
import { useNotification } from './useNotification';

export const useApiErrorHandler = () => {
  const { showError, showApiError } = useNotification();

  // Function to handle API errors globally
  const handleApiError = (error: any, showNotification = true) => {
    let errorMessage = 'Ocorreu um erro inesperado';
    let errorDetail = '';

    // Handle different types of API errors
    if (error?.response) {
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          errorMessage = 'Dados inválidos';
          if (data?.detail) {
            errorDetail = data.detail;
          } else if (data?.non_field_errors) {
            errorDetail = Array.isArray(data.non_field_errors) 
              ? data.non_field_errors.join(', ')
              : data.non_field_errors;
          }
          break;
          
        case 401:
          errorMessage = 'Não autorizado';
          errorDetail = 'Faça login novamente';
          // Don't show notification for 401 as it's handled by the auth interceptor
          showNotification = false;
          break;
          
        case 403:
          errorMessage = 'Acesso negado';
          errorDetail = 'Você não tem permissão para esta ação';
          break;
          
        case 404:
          errorMessage = 'Não encontrado';
          errorDetail = 'O recurso solicitado não foi encontrado';
          break;
          
        case 422:
          errorMessage = 'Dados inválidos';
          if (data?.detail) {
            errorDetail = Array.isArray(data.detail)
              ? data.detail.map((item: any) => item.msg || item.message || item).join(', ')
              : data.detail;
          }
          break;
          
        case 500:
          errorMessage = 'Erro interno do servidor';
          errorDetail = 'Tente novamente em alguns instantes';
          break;
          
        default:
          if (data?.detail) {
            errorDetail = data.detail;
          } else if (data?.message) {
            errorDetail = data.message;
          }
      }
    } else if (error?.message) {
      errorDetail = error.message;
    }

    // Show notification if needed
    if (showNotification) {
      if (errorDetail) {
        showError(`${errorMessage}: ${errorDetail}`);
      } else {
        showError(errorMessage);
      }
    }

    return {
      message: errorMessage,
      detail: errorDetail,
      status: error?.response?.status,
      data: error?.response?.data,
    };
  };

  // Function to handle authentication errors specifically
  const handleAuthError = async (error: any) => {
    const { logout } = useAuth();
    
    if (error?.response?.status === 401) {
      // Clear auth data and redirect to login
      await logout();
      showError('Sua sessão expirou. Faça login novamente.');
    }
  };

  return {
    handleApiError,
    handleAuthError,
  };
};
