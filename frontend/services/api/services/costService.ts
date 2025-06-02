/**
 * Cost Service
 * Provides composable functions for cost management in Vue components
 * Refactored to use the new API structure
 */
import { ref, computed } from 'vue';
import * as costsApi from '../endpoints/costs';
import type { Cost, CostResponse, CostCategory, CostCategoryResponse, BudgetSummary } from '../endpoints/costs';
import { useApiService } from '~/stores/composables/useApiService';
import { useAuth } from '~/stores/composables/useAuth';

export const useCostService = () => {
  const { handleApiError, withLoading } = useApiService();
  const { user } = useAuth();
  
  // State
  const costs = ref<CostResponse[]>([]);
  const categories = ref<CostCategoryResponse[]>([]);
  const budgetSummary = ref<BudgetSummary | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  
  // Fetch costs with optional filtering
  const fetchCosts = async (params: Record<string, any> = {}) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await costsApi.listCosts(params);
      costs.value = response.results;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch a specific cost by ID
  const fetchCost = async (id: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await costsApi.retrieveCost(id);
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Create a new cost
  const createCost = async (data: Cost) => {
    return withLoading(async () => {
      try {
        // Ensure the user ID is set if not provided
        if (!data.created_by && user.value) {
          data.created_by = user.value.id;
        }
        
        const response = await costsApi.createCost(data);
        costs.value = [response, ...costs.value];
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Criando registro de custo...',
      successMessage: 'Custo registrado com sucesso!'
    });
  };
  
  // Update an existing cost
  const updateCost = async (id: number, data: Partial<Cost>) => {
    return withLoading(async () => {
      try {
        const response = await costsApi.updateCost(id, data);
        
        // Update in the local array if present
        const index = costs.value.findIndex(c => c.id === id);
        if (index !== -1) {
          costs.value[index] = response;
        }
        
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Atualizando custo...',
      successMessage: 'Custo atualizado com sucesso!'
    });
  };
  
  // Delete a cost
  const deleteCost = async (id: number) => {
    return withLoading(async () => {
      try {
        await costsApi.destroyCost(id);
        
        // Remove from the local array if present
        costs.value = costs.value.filter(c => c.id !== id);
        
        return true;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Excluindo custo...',
      successMessage: 'Custo excluído com sucesso!'
    });
  };
  
  // Fetch cost categories
  const fetchCategories = async (params: Record<string, any> = {}) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await costsApi.listCostCategories(params);
      categories.value = response;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Create a new cost category
  const createCategory = async (data: CostCategory) => {
    return withLoading(async () => {
      try {
        const response = await costsApi.createCostCategory(data);
        categories.value = [...categories.value, response];
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Criando categoria de custo...',
      successMessage: 'Categoria criada com sucesso!'
    });
  };
  
  // Update an existing category
  const updateCategory = async (id: number, data: Partial<CostCategory>) => {
    return withLoading(async () => {
      try {
        const response = await costsApi.updateCostCategory(id, data);
        
        // Update in the local array if present
        const index = categories.value.findIndex(c => c.id === id);
        if (index !== -1) {
          categories.value[index] = response;
        }
        
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Atualizando categoria...',
      successMessage: 'Categoria atualizada com sucesso!'
    });
  };
  
  // Delete a category
  const deleteCategory = async (id: number) => {
    return withLoading(async () => {
      try {
        await costsApi.destroyCostCategory(id);
        
        // Remove from the local array if present
        categories.value = categories.value.filter(c => c.id !== id);
        
        return true;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Excluindo categoria...',
      successMessage: 'Categoria excluída com sucesso!'
    });
  };
  
  // Get budget summary for a project
  const fetchBudgetSummary = async (projectId: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await costsApi.getProjectBudgetSummary(projectId);
      budgetSummary.value = response;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Calculate total cost
  const totalCost = computed(() => {
    return costs.value.reduce((sum, cost) => sum + cost.amount, 0);
  });
  
  // Group costs by category
  const costsByCategory = computed(() => {
    const grouped: Record<string, { total: number, items: CostResponse[] }> = {};
    
    costs.value.forEach(cost => {
      const category = cost.category || 'OUTROS';
      
      if (!grouped[category]) {
        grouped[category] = { total: 0, items: [] };
      }
      
      grouped[category].total += cost.amount;
      grouped[category].items.push(cost);
    });
    
    return grouped;
  });
  
  // Costs per month for charts
  const costsPerMonth = computed(() => {
    const monthData: Record<string, number> = {};
    
    costs.value.forEach(cost => {
      if (!cost.date) return;
      
      const date = new Date(cost.date);
      const month = date.toLocaleString('pt-BR', { month: 'long', year: 'numeric' });
      
      if (!monthData[month]) {
        monthData[month] = 0;
      }
      
      monthData[month] += cost.amount;
    });
    
    return monthData;
  });
  
  return {
    // State
    costs,
    categories,
    budgetSummary,
    isLoading,
    error,
    
    // Computed
    totalCost,
    costsByCategory,
    costsPerMonth,
    
    // Methods
    fetchCosts,
    fetchCost,
    createCost,
    updateCost,
    deleteCost,
    fetchCategories,
    createCategory,
    updateCategory, 
    deleteCategory,
    fetchBudgetSummary
  };
};
