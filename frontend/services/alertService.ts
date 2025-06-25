import { useApiClient } from '~/composables/useApiClient';

export const useAlertService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de alertas
   * @param params Parâmetros de paginação e filtros
   */
  const getAlerts = async (params = {}) => {
    const response = await apiClient.get('costs/alertas/', { params });
    return response.data;
  };

  /**
   * Obtém um alerta específico pelo ID
   * @param id ID do alerta
   */
  const getAlert = async (id: number) => {
    const response = await apiClient.get(`costs/alertas/${id}/`);
    return response.data;
  };

  /**
   * Cria um novo alerta
   * @param data Dados do alerta
   */
  const createAlert = async (data: any) => {
    const response = await apiClient.post('costs/alertas/', data);
    return response.data;
  };

  /**
   * Atualiza um alerta existente
   * @param id ID do alerta
   * @param data Dados do alerta
   */
  const updateAlert = async (id: number, data: any) => {
    const response = await apiClient.patch(`costs/alertas/${id}/`, data);
    return response.data;
  };

  /**
   * Exclui um alerta
   * @param id ID do alerta
   */
  const deleteAlert = async (id: number) => {
    const response = await apiClient.delete(`costs/alertas/${id}/`);
    return response.data;
  };

  /**
   * Marca um alerta como resolvido
   * @param id ID do alerta
   */
  const resolveAlert = async (id: number) => {
    const response = await apiClient.patch(`costs/alertas/${id}/`, {
      status: 'RESOLVIDO'
    });
    return response.data;
  };

  /**
   * Marca um alerta como em andamento
   * @param id ID do alerta
   */
  const startAlert = async (id: number) => {
    const response = await apiClient.patch(`costs/alertas/${id}/`, {
      status: 'EM_ANDAMENTO'
    });
    return response.data;
  };

  return {
    getAlerts,
    getAlert,
    createAlert,
    updateAlert,
    deleteAlert,
    resolveAlert,
    startAlert
  };
};
