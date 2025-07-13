import { useToast } from "@/composables/useToast";

export const useApiErrorHandler = () => {
  const { toast } = useToast();

  const handleApiError = (
    error: any,
    defaultMessage: string = "Ocorreu um erro"
  ) => {
    console.error("API Error:", {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
      url: error.config?.url,
      method: error.config?.method,
    });

    let errorMessage = defaultMessage;
    let errorTitle = "Erro";

    switch (error.response?.status) {
      case 401:
        errorTitle = "Não Autorizado";
        errorMessage = "Sua sessão expirou. Faça login novamente.";
        // Clear tokens
        localStorage.removeItem("auth-token");
        sessionStorage.removeItem("auth-token");
        // Redirect to login
        navigateTo("/login");
        break;

      case 403:
        errorTitle = "Acesso Negado";
        errorMessage = "Você não tem permissão para realizar esta ação.";
        break;

      case 404:
        errorTitle = "Não Encontrado";
        errorMessage = "O recurso solicitado não foi encontrado.";
        break;

      case 422:
        errorTitle = "Dados Inválidos";
        errorMessage = "Os dados fornecidos são inválidos.";
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }
        break;

      case 500:
        errorTitle = "Erro do Servidor";
        errorMessage = "Erro interno do servidor. Tente novamente mais tarde.";
        break;

      default:
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        }
    }

    toast({
      title: errorTitle,
      description: errorMessage,
      type: "error",
    });

    return {
      message: errorMessage,
      title: errorTitle,
      status: error.response?.status,
    };
  };

  return {
    handleApiError,
  };
};
