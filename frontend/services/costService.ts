// Service para gerenciar custos usando a API Fetch do Nuxt
export const useCostService = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // Buscar custos com filtros
  const getCosts = async (filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}costs/`, {
        params: filters,
      });
    } catch (error) {
      console.error("Erro ao buscar custos:", error);
      throw error;
    }
  };

  // Buscar custo específico
  const getCostById = async (id: number) => {
    try {
      return await $fetch(`${apiBase}costs/${id}/`);
    } catch (error) {
      console.error("Erro ao buscar custo:", error);
      throw error;
    }
  };

  // Criar novo custo
  const createCost = async (costData: any) => {
    try {
      return await $fetch(`${apiBase}costs/`, {
        method: "POST",
        body: costData,
      });
    } catch (error) {
      console.error("Erro ao criar custo:", error);
      throw error;
    }
  };

  // Atualizar custo
  const updateCost = async (id: number, costData: any) => {
    try {
      return await $fetch(`${apiBase}costs/${id}/`, {
        method: "PUT",
        body: costData,
      });
    } catch (error) {
      console.error("Erro ao atualizar custo:", error);
      throw error;
    }
  };

  // Atualizar parcialmente custo
  const partialUpdateCost = async (id: number, costData: any) => {
    try {
      return await $fetch(`${apiBase}costs/${id}/`, {
        method: "PATCH",
        body: costData,
      });
    } catch (error) {
      console.error("Erro ao atualizar custo:", error);
      throw error;
    }
  };

  // Deletar custo
  const deleteCost = async (id: number) => {
    try {
      return await $fetch(`${apiBase}costs/${id}/`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao deletar custo:", error);
      throw error;
    }
  };

  // Buscar relatório de custos
  const getCostReport = async (filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}costs/report/`, {
        params: filters,
      });
    } catch (error) {
      console.error("Erro ao buscar relatório de custos:", error);
      throw error;
    }
  };

  // Buscar custos por projeto
  const getCostsByProject = async (projectId: number, filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}costs/`, {
        params: { projeto: projectId, ...filters },
      });
    } catch (error) {
      console.error("Erro ao buscar custos por projeto:", error);
      throw error;
    }
  };

  return {
    getCosts,
    getCostById,
    createCost,
    updateCost,
    partialUpdateCost,
    deleteCost,
    getCostReport,
    getCostsByProject,
  };
};
