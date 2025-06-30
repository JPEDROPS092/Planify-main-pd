// Service para gerenciar alertas usando a API Fetch do Nuxt
export const useAlertService = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // Buscar alertas com filtros
  const getAlerts = async (filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/`, {
        params: filters,
      });
    } catch (error) {
      console.error("Erro ao buscar alertas:", error);
      throw error;
    }
  };

  // Buscar alerta específico
  const getAlertById = async (id: number) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/${id}/`);
    } catch (error) {
      console.error("Erro ao buscar alerta:", error);
      throw error;
    }
  };

  // Criar novo alerta
  const createAlert = async (alertData: any) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/`, {
        method: "POST",
        body: alertData,
      });
    } catch (error) {
      console.error("Erro ao criar alerta:", error);
      throw error;
    }
  };

  // Atualizar alerta
  const updateAlert = async (id: number, alertData: any) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/${id}/`, {
        method: "PUT",
        body: alertData,
      });
    } catch (error) {
      console.error("Erro ao atualizar alerta:", error);
      throw error;
    }
  };

  // Atualizar parcialmente alerta
  const partialUpdateAlert = async (id: number, alertData: any) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/${id}/`, {
        method: "PATCH",
        body: alertData,
      });
    } catch (error) {
      console.error("Erro ao atualizar alerta:", error);
      throw error;
    }
  };

  // Deletar alerta
  const deleteAlert = async (id: number) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/${id}/`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao deletar alerta:", error);
      throw error;
    }
  };

  // Resolver alerta (marca como resolvido)
  const resolveAlert = async (id: number) => {
    try {
      return await $fetch(`${apiBase}costs/alertas/${id}/resolver/`, {
        method: "POST",
      });
    } catch (error) {
      console.error("Erro ao resolver alerta:", error);
      throw error;
    }
  };

  return {
    getAlerts,
    getAlertById,
    createAlert,
    updateAlert,
    partialUpdateAlert,
    deleteAlert,
    resolveAlert,
  };
};
