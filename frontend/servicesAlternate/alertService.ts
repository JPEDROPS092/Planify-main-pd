import { useApiClient } from '~/composables/useApiClient';

const alerta = {
  id: 101,
  tipo: "atraso_tarefa",
  tipo_display: "Atraso de Tarefa",
  projeto: 1, // Corresponds to Project ID 1 (Planify)
  projeto_nome: "Planify - Task Management App",
  tarefa: 501, // Example Task ID
  tarefa_titulo: "Implementar autenticação de usuário",
  percentual: 0.85, // 85% do tempo limite excedido ou do progresso esperado
  mensagem: "A tarefa 'Implementar autenticação de usuário' está 5 dias atrasada.",
  status: "aberto",
  status_display: "Aberto",
  data_criacao: "2025-06-20T09:30:00Z",
  data_resolucao: null, // Still open, so no resolution date
  resolvido_por: null,
  resolvido_por_nome: null,
};

export const useAlertService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de alertas
   * @param params Parâmetros de paginação e filtros
   */
  const getAlerts = async (params = {}) => {
    const response = {data: alerta};
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
