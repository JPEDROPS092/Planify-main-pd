import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Custo } from '~/services/api/types';

/**
 * Store para gerenciamento de custos com cache
 * Implementa cache de dados para reduzir chamadas à API e melhorar performance
 */
export const useCostStore = defineStore('costs', () => {
  // Estado
  const costs = ref<Custo[]>([]);
  const costDetails = ref<Record<number, Custo>>({});
  const lastFetched = ref<Record<string, number>>({
    list: 0,
    details: {}
  });
  const isFetching = ref(false);

  // Cache válido por 5 minutos (300000ms)
  const CACHE_DURATION = 300000;

  // Getters
  const getCosts = computed(() => costs.value);
  
  const getCostById = computed(() => (id: number) => {
    return costDetails.value[id];
  });

  const isCacheValid = computed(() => (key: string) => {
    const now = Date.now();
    if (key === 'list') {
      return lastFetched.value.list > 0 && 
             (now - lastFetched.value.list) < CACHE_DURATION;
    }
    
    // Para detalhes de custo específico
    if (key.startsWith('detail-')) {
      const id = key.replace('detail-', '');
      return lastFetched.value.details[id] && 
             (now - lastFetched.value.details[id]) < CACHE_DURATION;
    }
    
    return false;
  });

  // Actions
  function setCosts(newCosts: Custo[]) {
    costs.value = newCosts;
    lastFetched.value.list = Date.now();
  }

  function setCostDetail(id: number, cost: Custo) {
    costDetails.value[id] = cost;
    lastFetched.value.details[id] = Date.now();
  }

  function updateCost(id: number, updatedCost: Custo) {
    // Atualizar nos detalhes
    if (costDetails.value[id]) {
      costDetails.value[id] = { ...updatedCost };
      lastFetched.value.details[id] = Date.now();
    }
    
    // Atualizar na lista se existir
    const index = costs.value.findIndex(c => c.id === id);
    if (index !== -1) {
      costs.value[index] = { ...updatedCost };
      lastFetched.value.list = Date.now();
    }
  }

  function addCost(newCost: Custo) {
    // Adicionar à lista se existir
    if (costs.value.length > 0) {
      costs.value = [newCost, ...costs.value];
      lastFetched.value.list = Date.now();
    }
    
    // Adicionar aos detalhes
    if (newCost.id) {
      costDetails.value[newCost.id] = newCost;
      lastFetched.value.details[newCost.id] = Date.now();
    }
  }

  function removeCost(id: number) {
    // Remover da lista
    costs.value = costs.value.filter(c => c.id !== id);
    
    // Remover dos detalhes
    if (costDetails.value[id]) {
      delete costDetails.value[id];
      delete lastFetched.value.details[id];
    }
    
    // Atualizar timestamp
    lastFetched.value.list = Date.now();
  }

  function setFetching(value: boolean) {
    isFetching.value = value;
  }

  function clearCache() {
    costs.value = [];
    costDetails.value = {};
    lastFetched.value = {
      list: 0,
      details: {}
    };
  }

  return {
    // Estado
    costs,
    costDetails,
    lastFetched,
    isFetching,
    
    // Getters
    getCosts,
    getCostById,
    isCacheValid,
    
    // Actions
    setCosts,
    setCostDetail,
    updateCost,
    addCost,
    removeCost,
    setFetching,
    clearCache
  };
});
