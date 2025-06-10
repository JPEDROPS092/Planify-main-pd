/**
 * Serviço de riscos - adaptador para o novo sistema de API
 * Otimizado com cache via Pinia
 */
import { ref } from 'vue';
import { useApiService } from '~/stores/composables/useApiService';
import { useAuth } from '~/stores/composables/useAuth';
import * as risksApi from '../services/api/endpoints/risks';
// Importando defineStore para criar a store localmente
import { defineStore } from 'pinia';

export const useRiskService = () => {
  const { user, hasPermission } = useAuth();
  const { handleApiError, withLoading } = useApiService();

  const risks = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  // Definindo store de riscos localmente para evitar dependência externa
  const useRiskStore = defineStore('risks', () => {
    const risks = ref([]);
    const isLoading = ref(false);

    function setRisks(newRisks) {
      risks.value = newRisks;
    }

    function addRisk(risk) {
      risks.value.push(risk);
    }

    function updateRiskInStore(id, updatedRisk) {
      const index = risks.value.findIndex(r => r.id === id);
      if (index !== -1) {
        risks.value[index] = { ...risks.value[index], ...updatedRisk };
      }
    }

    function removeRisk(id) {
      risks.value = risks.value.filter(r => r.id !== id);
    }

    return {
      risks,
      isLoading,
      setRisks,
      addRisk,
      updateRiskInStore,
      removeRisk
    };
  });

  // Carregar todos os riscos
  const fetchRisks = async (projectId = null, useCache = true) => {
    const riskStore = useRiskStore();

    // Verificar se podemos usar o cache
    if (useCache && riskStore.isRisksCacheValid) {
      // Se temos um projectId e o cache contém riscos, filtramos pelo projeto
      if (projectId) {
        const filteredRisks = riskStore.risks.filter(risk => {
          const projetoId = typeof risk.projeto === 'object' ? risk.projeto.id : risk.projeto;
          return projetoId === projectId;
        });
        risks.value = filteredRisks;
        return filteredRisks;
      } else {
        // Se não temos projectId, retornamos todos os riscos do cache
        risks.value = riskStore.risks;
        return riskStore.risks;
      }
    }

    isLoading.value = true;
    error.value = null;
    riskStore.setFetching(true);

    try {
      let response;
      if (projectId) {
        response = await risksApi.listRiscos({ projeto: projectId });
      } else {
        response = await risksApi.listRiscos();
      }

      risks.value = response.results;

      // Armazenar no cache
      if (!projectId) { // Armazenamos apenas a lista completa
        riskStore.setRisks(response.results);
      }

      return risks.value;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
      riskStore.setFetching(false);
    }
  };

  // Obter um risco pelo ID
  const getRisk = async (riskId, useCache = true) => {
    const riskStore = useRiskStore();

    // Verificar se podemos usar o cache
    if (useCache && riskStore.isRiskDetailCacheValid(riskId)) {
      return riskStore.riskDetails[riskId];
    }

    isLoading.value = true;
    error.value = null;
    riskStore.setFetching(true);

    try {
      const risk = await risksApi.retrieveRisco(riskId);

      // Armazenar no cache
      riskStore.setRiskDetail(risk);

      return risk;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
      riskStore.setFetching(false);
    }
  };

  // Criar um novo risco
  const createRisk = async (riskData) => {
    const riskStore = useRiskStore();

    return withLoading(async () => {
      try {
        // Associar automaticamente o usuário atual como criador se não estiver definido
        if (!riskData.created_by) {
          riskData.created_by = user.value?.id;
        }

        const newRisk = await risksApi.createRisco(riskData);
        risks.value = [...risks.value, newRisk];

        // Atualizar o cache
        riskStore.setRiskDetail(newRisk);

        return newRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Atualizar um risco
  const updateRisk = async (riskId, riskData) => {
    const riskStore = useRiskStore();

    return withLoading(async () => {
      try {
        const updatedRisk = await risksApi.updateRisco(riskId, riskData);

        // Atualizar a lista local
        risks.value = risks.value.map((risk) =>
          risk.id === riskId ? updatedRisk : risk
        );

        // Atualizar o cache
        riskStore.setRiskDetail(updatedRisk);

        return updatedRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Excluir um risco
  const deleteRisk = async (riskId) => {
    const riskStore = useRiskStore();

    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('risk', 'delete')) {
          throw new Error('Você não tem permissão para excluir este risco');
        }

        await risksApi.destroyRisco(riskId);

        // Remover da lista local
        risks.value = risks.value.filter((risk) => risk.id !== riskId);

        // Remover do cache
        riskStore.removeRisk(riskId);

        return true;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Adicionar uma resposta a um risco
  const addRiskResponse = async (riskId, responseData) => {
    const riskStore = useRiskStore();

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

        // Atualizar o cache
        riskStore.setRiskDetail(updatedRisk);

        return updatedRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Atualizar status de um risco
  const updateRiskStatus = async (riskId, status) => {
    const riskStore = useRiskStore();

    return withLoading(async () => {
      try {
        const updatedRisk = await risksApi.atualizarStatusRisco(riskId, {
          status,
        });

        // Atualizar a lista local
        risks.value = risks.value.map((risk) =>
          risk.id === riskId ? updatedRisk : risk
        );

        // Atualizar o cache
        riskStore.setRiskDetail(updatedRisk);

        return updatedRisk;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    });
  };

  // Função para limpar o cache
  const clearRiskCache = () => {
    const riskStore = useRiskStore();
    riskStore.clearCache();
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
    clearRiskCache,
  };
};
