// Service para gerenciar riscos usando a API Fetch do Nuxt
export const useRiskService = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // Buscar riscos com filtros
  const getRisks = async (filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}risks/`, {
        params: filters,
      });
    } catch (error) {
      console.error("Erro ao buscar riscos:", error);
      throw error;
    }
  };

  // Buscar risco específico
  const getRiskById = async (id: number) => {
    try {
      return await $fetch(`${apiBase}risks/${id}/`);
    } catch (error) {
      console.error("Erro ao buscar risco:", error);
      throw error;
    }
  };

  // Criar novo risco
  const createRisk = async (riskData: any) => {
    try {
      return await $fetch(`${apiBase}risks/`, {
        method: "POST",
        body: riskData,
      });
    } catch (error) {
      console.error("Erro ao criar risco:", error);
      throw error;
    }
  };

  // Atualizar risco
  const updateRisk = async (id: number, riskData: any) => {
    try {
      return await $fetch(`${apiBase}risks/${id}/`, {
        method: "PUT",
        body: riskData,
      });
    } catch (error) {
      console.error("Erro ao atualizar risco:", error);
      throw error;
    }
  };

  // Atualizar parcialmente risco
  const partialUpdateRisk = async (id: number, riskData: any) => {
    try {
      return await $fetch(`${apiBase}risks/${id}/`, {
        method: "PATCH",
        body: riskData,
      });
    } catch (error) {
      console.error("Erro ao atualizar risco:", error);
      throw error;
    }
  };

  // Deletar risco
  const deleteRisk = async (id: number) => {
    try {
      return await $fetch(`${apiBase}risks/${id}/`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao deletar risco:", error);
      throw error;
    }
  };

  return {
    getRisks,
    getRiskById,
    createRisk,
    updateRisk,
    partialUpdateRisk,
    deleteRisk,
  };
};
