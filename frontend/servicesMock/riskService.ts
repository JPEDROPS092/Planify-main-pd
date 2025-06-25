import { useApiClient } from '~/composables/useApiClient';

export const useRiskService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de riscos de um projeto
   * @param projectId ID do projeto
   * @param params Parâmetros de paginação e filtros
   */
  const getProjectRisks = async (projectId: number, params = {}) => {
    const response = await apiClient.get(`risks/riscos/`, { 
      params: { 
        projeto_id: projectId,
        ...params 
      } 
    });
    return response.data;
  };

  /**
   * Obtém um risco específico pelo ID
   * @param id ID do risco
   */
  const getRisk = async (id: number) => {
    const response = await apiClient.get(`risks/riscos/${id}/`);
    return response.data;
  };

  /**
   * Cria um novo risco
   * @param data Dados do risco
   */
  const createRisk = async (data: any) => {
    const response = await apiClient.post('risks/riscos/', data);
    return response.data;
  };

  /**
   * Atualiza um risco existente
   * @param id ID do risco
   * @param data Dados do risco
   */
  const updateRisk = async (id: number, data: any) => {
    const response = await apiClient.patch(`risks/riscos/${id}/`, data);
    return response.data;
  };

  /**
   * Exclui um risco
   * @param id ID do risco
   */
  const deleteRisk = async (id: number) => {
    const response = await apiClient.delete(`risks/riscos/${id}/`);
    return response.data;
  };

  /**
   * Obtém o histórico de um risco
   * @param riskId ID do risco
   * @param params Parâmetros de paginação e filtros
   */
  const getRiskHistory = async (riskId: number, params = {}) => {
    const response = await apiClient.get(`risks/riscos/${riskId}/historico/`, { params });
    return response.data;
  };

  return {
    getProjectRisks,
    getRisk,
    createRisk,
    updateRisk,
    deleteRisk,
    getRiskHistory
  };
};
