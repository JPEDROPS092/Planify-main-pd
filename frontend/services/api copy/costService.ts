/**
 * Serviço de custos - adaptador para o novo sistema de API
 */
import { ref } from 'vue'
import * as costsApi from '~/services/api/costs'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'

export const useCostService = () => {
  const { user, hasPermission } = useAuth()
  const { handleApiError, withLoading } = useApiService()
  
  const costs = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Carregar todos os custos
  const fetchCosts = async (projectId = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      if (projectId) {
        costs.value = await costsApi.listCostsByProject(projectId)
      } else {
        costs.value = await costsApi.listCosts()
      }
      return costs.value
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter um custo pelo ID
  const getCost = async (costId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const cost = await costsApi.retrieveCost(costId)
      return cost
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Criar um novo custo
  const createCost = async (costData) => {
    return withLoading(async () => {
      try {
        // Associar automaticamente o usuário atual como criador se não estiver definido
        if (!costData.created_by) {
          costData.created_by = user.value?.id
        }
        
        const newCost = await costsApi.createCost(costData)
        costs.value = [...costs.value, newCost]
        return newCost
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar um custo
  const updateCost = async (costId, costData) => {
    return withLoading(async () => {
      try {
        const updatedCost = await costsApi.updateCost(costId, costData)
        
        // Atualizar a lista local
        costs.value = costs.value.map(cost => 
          cost.id === costId ? updatedCost : cost
        )
        
        return updatedCost
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Excluir um custo
  const deleteCost = async (costId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('cost', 'delete')) {
          throw new Error('Você não tem permissão para excluir este custo')
        }
        
        await costsApi.destroyCost(costId)
        
        // Remover da lista local
        costs.value = costs.value.filter(cost => cost.id !== costId)
        
        return true
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Buscar resumo de custos por projeto
  const getCostSummary = async (projectId) => {
    return withLoading(async () => {
      try {
        const summary = await costsApi.getCostSummary(projectId)
        return summary
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Adicionar um pagamento a um custo
  const addCostPayment = async (costId, paymentData) => {
    return withLoading(async () => {
      try {
        const updatedCost = await costsApi.addCostPayment(costId, paymentData)
        
        // Atualizar a lista local
        costs.value = costs.value.map(cost => 
          cost.id === costId ? updatedCost : cost
        )
        
        return updatedCost
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  return {
    costs,
    isLoading,
    error,
    fetchCosts,
    getCost,
    createCost,
    updateCost,
    deleteCost,
    getCostSummary,
    addCostPayment
  }
}
