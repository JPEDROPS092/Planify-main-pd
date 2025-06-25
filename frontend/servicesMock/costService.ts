import { useApiClient } from '~/composables/useApiClient';

export const useCostService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de custos
   * @param params Parâmetros de paginação e filtros
   */
  const getCosts = async (params = {}) => {
    const response = await apiClient.get('costs/custos/', { params });
    return response.data;
  };

  /**
   * Obtém um custo específico pelo ID
   * @param id ID do custo
   */
  const getCost = async (id: number) => {
    const response = await apiClient.get(`costs/custos/${id}/`);
    return response.data;
  };

  /**
   * Cria um novo custo
   * @param data Dados do custo
   */
  const createCost = async (data: any) => {
    const response = await apiClient.post('costs/custos/', data);
    return response.data;
  };

  /**
   * Atualiza um custo existente
   * @param id ID do custo
   * @param data Dados do custo
   */
  const updateCost = async (id: number, data: any) => {
    const response = await apiClient.patch(`costs/custos/${id}/`, data);
    return response.data;
  };

  /**
   * Exclui um custo
   * @param id ID do custo
   */
  const deleteCost = async (id: number) => {
    const response = await apiClient.delete(`costs/custos/${id}/`);
    return response.data;
  };

  /**
   * Obtém o orçamento de um projeto
   * @param projectId ID do projeto
   */
  const getProjectBudget = async (projectId: number) => {
    const response = await apiClient.get(`costs/orcamento-projeto/${projectId}/`);
    return response.data;
  };

  /**
   * Cria ou atualiza o orçamento de um projeto
   * @param projectId ID do projeto
   * @param data Dados do orçamento
   */
  const updateProjectBudget = async (projectId: number, data: any) => {
    const response = await apiClient.post(`costs/orcamento-projeto/`, {
      projeto_id: projectId,
      ...data
    });
    return response.data;
  };

  /**
   * Obtém o orçamento de uma tarefa
   * @param taskId ID da tarefa
   */
  const getTaskBudget = async (taskId: number) => {
    const response = await apiClient.get(`costs/orcamento-tarefa/${taskId}/`);
    return response.data;
  };

  /**
   * Cria ou atualiza o orçamento de uma tarefa
   * @param taskId ID da tarefa
   * @param data Dados do orçamento
   */
  const updateTaskBudget = async (taskId: number, data: any) => {
    const response = await apiClient.post(`costs/orcamento-tarefa/`, {
      tarefa_id: taskId,
      ...data
    });
    return response.data;
  };

  return {
    getCosts,
    getCost,
    createCost,
    updateCost,
    deleteCost,
    getProjectBudget,
    updateProjectBudget,
    getTaskBudget,
    updateTaskBudget
  };
};
