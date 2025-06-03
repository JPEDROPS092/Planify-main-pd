/**
 * Composable para gerenciamento de custos
 * Encapsula as funções do serviço de custos
 */
import { ref, computed } from 'vue';
import { useCostService as apiCostService } from '~/services/api/services/costService';
import type { Cost, CostCategory, CostResponse } from '~/services/api/endpoints/costs'; // Adicionar tipos
import { useNotification } from './useNotification';
// import { withLoading } from './withLoading'; // Removido pois não será mais usado diretamente aqui
import { useCostStore } from '~/stores'; // Corrigido o caminho para importar de frontend/stores/index.ts

export const useCostService = () => {
  const loading = ref(false); // Ref de loading principal do composable
  const error = ref<any | null>(null); // Tipar o erro e usar este para todo o composable
  const notify = useNotification();
  
  // Usar a store Pinia para cache
  const costStore = useCostStore();
  
  // Computed para verificar se o cache está sendo usado
  const usingCache = computed(() => costStore.isCacheValid('list'));

  // const costs = ref([]); // Removido - não utilizado
  const categories = ref<CostCategoryResponse[]>([]); // Tipar categories
  // const alerts = ref([]); // Removido - não utilizado
  // const budgets = ref([]); // Removido - não utilizado
  // const isLoading = ref(false); // Removido - usar o 'loading' principal
  // const error = ref(null); // Removido - usar o 'error' principal

  /**
   * Busca custos com filtros opcionais
   * @param params Parâmetros de filtro e paginação
   * @returns Lista paginada de custos
   */
  const fetchCustos = async (params: Record<string, any> = {}, useCache = true) => {
    // Verificar se podemos usar o cache
    if (useCache && costStore.isCacheValid('list')) {
      console.log('Usando custos em cache');
      // Retornar no formato esperado, assumindo getCosts é um array
      return { results: costStore.getCosts, count: costStore.getCosts.length }; // Ajustar conforme a estrutura de getCosts
    }

    loading.value = true;
    costStore.setFetching(true);
    error.value = null; // Usar o error principal

    try {
      const response = await apiCostService().fetchCosts(params); // Corrigido: listCustos -> fetchCosts
      // Armazenar no cache
      costStore.setCosts(response.results); // Corrigido: response.data -> response.results
      return response;
    } catch (err: any) { // Tipar err
      console.error('Erro ao buscar custos:', err);
      error.value = err; // Usar o error principal
      throw err;
    } finally {
      loading.value = false; // Usar o loading principal
      costStore.setFetching(false);
    }
  };

  /**
   * Obtém detalhes de um custo pelo ID
   * @param id ID do custo
   * @returns Detalhes do custo
   */
  const getCusto = async (id: number, useCache = true) => { // Tipar id
    // Verificar se podemos usar o cache
    if (useCache && costStore.isCacheValid(`detail-${id}`)) {
      const cachedCost = costStore.getCostById(id);
      console.log(`Usando custo ${id} em cache`);
      return cachedCost ? { data: cachedCost } : undefined; // Ajustar retorno se necessário
    }

    loading.value = true;
    error.value = null; // Usar o error principal

    try {
      const response = await apiCostService().fetchCost(id); // Corrigido: retrieveCusto -> fetchCost
      // Armazenar no cache
      costStore.setCostDetail(id, response); // Corrigido: response.data -> response
      return { data: response }; // Manter consistência no formato de retorno se fetchCustos retorna { data: ... }
    } catch (err: any) { // Tipar err
      console.error(`Erro ao buscar custo ${id}:`, err);
      error.value = err; // Usar o error principal
      throw err;
    } finally {
      loading.value = false; // Usar o loading principal
    }
  };

  /**
   * Cria um novo custo
   * @param custoData Dados do custo
   * @returns Custo criado
   */
  const createCusto = async (custoData: Cost) => { // Tipar custoData
    loading.value = true;
    error.value = null;
    try {
      const response = await apiCostService().createCost(custoData); // Corrigido: createCusto -> createCost
      costStore.addCost(response); // Corrigido: response.data -> response
      // notify.success('Custo criado com sucesso!'); // Removido - apiCostService já notifica
      return response;
    } catch (err: any) {
      console.error('Erro ao criar custo (useCostService):', err);
      error.value = err;
      // notify.error('Erro ao criar custo'); // Removido - apiCostService já notifica
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Atualiza um custo existente
   * @param id ID do custo
   * @param custoData Dados do custo
   * @returns Custo atualizado
   */
  const updateCusto = async (id: number, custoData: Partial<Cost>) => { // Tipar id e custoData
    loading.value = true;
    error.value = null;
    try {
      const response = await apiCostService().updateCost(id, custoData); // Corrigido: updateCusto -> updateCost
      costStore.updateCost(id, response); // Corrigido: response.data -> response
      // notify.success('Custo atualizado com sucesso!'); // Removido
      return response;
    } catch (err: any) {
      console.error(`Erro ao atualizar custo ${id} (useCostService):`, err);
      error.value = err;
      // notify.error('Erro ao atualizar custo'); // Removido
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Atualiza parcialmente um custo
   * @param id ID do custo
   * @param custoData Dados parciais do custo
   * @returns Custo atualizado
   */
  const partialUpdateCusto = async (id: number, custoData: Partial<Cost>) => { // Tipar id e custoData
    loading.value = true;
    error.value = null;
    try {
      // Não existe partialUpdateCusto em apiCostService, updateCost lida com Partial<Cost>
      const response = await apiCostService().updateCost(id, custoData); // Corrigido: partialUpdateCusto -> updateCost
      costStore.updateCost(id, response); // Corrigido: response.data -> response
      // notify.success('Custo atualizado com sucesso!'); // Removido
      return response;
    } catch (err: any) {
      console.error(`Erro ao atualizar parcialmente custo ${id} (useCostService):`, err);
      error.value = err;
      // notify.error('Erro ao atualizar custo'); // Removido
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Exclui um custo
   * @param id ID do custo
   * @returns true se excluído com sucesso
   */
  const deleteCusto = async (id: number) => { // Tipar id
    loading.value = true;
    error.value = null;
    try {
      await apiCostService().deleteCost(id); // Corrigido: destroyCusto -> deleteCost
      costStore.removeCost(id);
      // notify.success('Custo excluído com sucesso!'); // Removido
      return true;
    } catch (err: any) {
      console.error(`Erro ao excluir custo ${id} (useCostService):`, err);
      error.value = err;
      // notify.error('Erro ao excluir custo'); // Removido
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Busca categorias de custos
   * @param params Parâmetros de filtro e paginação
   * @returns Lista paginada de categorias
   */
  const fetchCategorias = async (params: Record<string, any> = {}) => { // Tipar params
    loading.value = true;
    error.value = null;

    try {
      const response = await apiCostService().fetchCategories(params); // Corrigido: listCategorias -> fetchCategories
      categories.value = response || []; // Corrigido: response.results -> response (fetchCategories retorna array)
      return response;
    } catch (err: any) { // Tipar err
      console.error('Erro ao buscar categorias:', err);
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Obtém um resumo dos custos por categoria, status, etc.
   * @param projectId ID opcional do projeto para filtrar
   * @returns Resumo dos custos
   */
  const getResumoCustos = async (projectId: number | null = null) => { // Tipar projectId
    loading.value = true;
    error.value = null;

    try {
      // Buscar custos com filtros apropriados
      const params = projectId ? { projeto: projectId } : {};
      const response = await apiCostService().fetchCosts(params); // Corrigido: listCustos -> fetchCosts
      const custos: CostResponse[] = response.results || []; // Tipar custos

      // Calcular totais por categoria
      const totalPorCategoria: Record<string | number, { id: string | number; nome: string; total: number }> = {};
      const totalPorStatus: Record<string, number> = { // Tipar totalPorStatus
        pendente: 0,
        aprovado: 0,
        rejeitado: 0,
        // Adicionar outros status se existirem para evitar erros de tipagem no acesso
      };

      let totalGeral = 0;

      custos.forEach((custo: CostResponse) => { // Tipar custo
        // Total por categoria
        const categoriaId = typeof custo.category === 'object' && custo.category !== null // 'category' em vez de 'categoria', verificar null
          ? (custo.category as CostCategory).id // Assumir que category pode ser CostCategory
          : custo.category; // Ou é string/number diretamente
        const categoriaNome = typeof custo.category === 'object' && custo.category !== null
          ? (custo.category as CostCategory).name // 'name' em vez de 'nome'
          : custo.category || 'Sem categoria';


        if (categoriaId !== undefined && categoriaId !== null) {
            if (!totalPorCategoria[categoriaId]) {
              totalPorCategoria[categoriaId] = {
                id: categoriaId,
                nome: String(categoriaNome), // Garantir que nome seja string
                total: 0
              };
            }
            totalPorCategoria[categoriaId].total += custo.amount || 0; // 'amount' em vez de 'valor'
        }


        // Total por status
        if (custo.status && totalPorStatus.hasOwnProperty(custo.status)) { // Usar hasOwnProperty para segurança
          totalPorStatus[custo.status] += custo.amount || 0; // 'amount' em vez de 'valor'
        }

        // Total geral
        totalGeral += custo.amount || 0; // 'amount' em vez de 'valor'
      });

      return {
        totalGeral,
        totalPorCategoria: Object.values(totalPorCategoria),
        totalPorStatus,
        count: response.count
      };
    } catch (err: any) { // Tipar err
      console.error('Erro ao obter resumo de custos:', err);
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Limpar o cache manualmente
  const clearCostCache = () => {
    costStore.clearCache();
    notify.info('Cache de custos limpo');
  };

  return {
    loading,
    error,
    usingCache,
    fetchCustos,
    getCusto,
    createCusto,
    updateCusto,
    partialUpdateCusto,
    deleteCusto,
    getResumoCustos,
    fetchCategorias,
    clearCostCache
  };
};
