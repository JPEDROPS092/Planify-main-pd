// frontend/stores/costs.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
// Ex: import type { Custo } from '~/services/utils/types';

export const useCostsStore = defineStore('costs', () => {
  // State
  const costs = ref<any[]>([]); // Substituir 'any' pelo tipo Custo[]
  const currentCost = ref<any | null>(null); // Substituir 'any' pelo tipo Custo | null
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Actions
  async function fetchCostsForProject(projectId: number | string) {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar custos de um projeto
      console.warn(`fetchCostsForProject(${projectId}): Mock implementation.`);
      // costs.value = [{ id: 1, descricao: 'Custo Mock 1', valor: '100.00', projeto: projectId }];
    } catch (e:any) {
      error.value = e.message || `Falha ao buscar custos para o projeto ${projectId}.`;
    } finally {
      isLoading.value = false;
    }
  }
  
  // TODO: Adicionar actions para CRUD 

  return {
    costs,
    currentCost,
    isLoading,
    error,
    fetchCostsForProject,
  };
});
