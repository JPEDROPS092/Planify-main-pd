/**
 * Serviço de riscos - adaptador para o novo sistema de API
 */
import { ref } from 'vue';
import * as risksApi from './risks';
import { useApiService } from '~/composables/useApiService';
import { useAuth } from '~/composables/useAuth';

export const useRiskService = () => {
  const { user, hasPermission } = useAuth();
  const { handleApiError, withLoading } = useApiService();

  const risks = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  // Carregar todos os riscos
  const fetchRisks = async (projectId = null) => {
    isLoading.value = true;
    error.value = null;

    try {
      if (projectId) {
        const response = await risksApi.listRiscos({ projeto: projectId });
        risks.value = response.results;
      } else {
        const response = await risksApi.listRiscos();
        risks.value = response.results;
      }
      return risks.value;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Obter um risco pelo ID
  const getRisk = async (riskId) => {
    isLoading.value = true;
    error.value = null;

    try {
      const risk = await risksApi.retrieveRisco(riskId);
      return risk;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Criar um novo risco
  const createRisk = async (riskData) => {
    return withLoading(async () => {
      try {
        // Associar automaticamente o usuário atual como criador se não estiver definido
        if (!riskData.created_by) {
          riskData.created_by = user.value?.id;
        }

        const newRisk = await risksApi.createRisco(riskData);
        risks.value = [...risks.value, newRisk];
        return newRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Atualizar um risco
  const updateRisk = async (riskId, riskData) => {
    return withLoading(async () => {
      try {
        const updatedRisk = await risksApi.updateRisco(riskId, riskData);

        // Atualizar a lista local
        risks.value = risks.value.map((risk) =>
          risk.id === riskId ? updatedRisk : risk
        );

        return updatedRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Excluir um risco
  const deleteRisk = async (riskId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('risk', 'delete')) {
          throw new Error('Você não tem permissão para excluir este risco');
        }

        await risksApi.destroyRisco(riskId);

        // Remover da lista local
        risks.value = risks.value.filter((risk) => risk.id !== riskId);

        return true;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Adicionar uma resposta a um risco
  const addRiskResponse = async (riskId, responseData) => {
    return withLoading(async () => {
      try {
        const updatedRisk = await risksApi.adicionarRespostaRisco(
          riskId,
          responseData
        );

        // Atualizar a lista local
        risks.value = risks.value.map((risk) =>
          risk.id === riskId ? updatedRisk : risk
        );

        return updatedRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Atualizar status de um risco
  const updateRiskStatus = async (riskId, status) => {
    return withLoading(async () => {
      try {
        const updatedRisk = await risksApi.atualizarStatusRisco(riskId, {
          status,
        });

        // Atualizar a lista local
        risks.value = risks.value.map((risk) =>
          risk.id === riskId ? updatedRisk : risk
        );

        return updatedRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  return {
    risks,
    isLoading,
    error,
    fetchRisks,
    getRisk,
    createRisk,
    updateRisk,
    deleteRisk,
    addRiskResponse,
    updateRiskStatus,
  };
};
