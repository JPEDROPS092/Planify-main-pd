/**
 * Composable para gerenciamento de custos
 * Encapsula as funções do serviço de custos
 */
import { ref, computed } from 'vue';
import { useCostService as apiCostService } from '~/services/api/services/costService';
import { useNotification } from './useNotification';
import { withLoading } from './withLoading';
import { useCostStore } from '~/stores/costStore';

export const useCostService = () => {
  const loading = ref(false);
  const error = ref(null);
  const notify = useNotification();
  
  // Usar a store Pinia para cache
  const costStore = useCostStore();
  
  // Computed para verificar se o cache está sendo usado
  const usingCache = computed(() => costStore.isCacheValid('list'));

  const costs = ref([]);
  const categories = ref([]);
  const alerts = ref([]);
  const budgets = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  /**
   * Busca custos com filtros opcionais
   * @param params Parâmetros de filtro e paginação
   * @returns Lista paginada de custos
   */
  const fetchCustos = async (params = {}, useCache = true) => {
    // Verificar se podemos usar o cache
    if (useCache && costStore.isCacheValid('list')) {
      console.log('Usando custos em cache');
      return { data: costStore.getCosts };
    }

    loading.value = true;
    costStore.setFetching(true);
    error.value = null;

    try {
      const response = await apiCostService().listCustos(params);
      // Armazenar no cache
      costStore.setCosts(response.data);
      return response;
    } catch (err) {
      console.error('Erro ao buscar custos:', err);
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
      costStore.setFetching(false);
    }
  };

  /**
   * Obtém detalhes de um custo pelo ID
   * @param id ID do custo
   * @returns Detalhes do custo
   */
  const getCusto = async (id, useCache = true) => {
    // Verificar se podemos usar o cache
    if (useCache && costStore.isCacheValid(`detail-${id}`)) {
      console.log(`Usando custo ${id} em cache`);
      return { data: costStore.getCostById(id) };
    }

    loading.value = true;
    error.value = null;

    try {
      const response = await apiCostService().retrieveCusto(id);
      // Armazenar no cache
      costStore.setCostDetail(id, response.data);
      return response;
    } catch (err) {
      console.error(`Erro ao buscar custo ${id}:`, err);
      error.value = err;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  /**
   * Cria um novo custo
   * @param custoData Dados do custo
   * @returns Custo criado
   */
  const createCusto = async (custoData) => {
    return withLoading(
      async () => {
        try {
          const response = await apiCostService().createCusto(custoData);
          // Atualizar o cache
          costStore.addCost(response.data);
          notify.success('Custo criado com sucesso!');
          return response;
        } catch (err) {
          console.error('Erro ao criar custo:', err);
          notify.error('Erro ao criar custo');
          throw err;
        }
      },
      { loading }
    );
  };

  /**
   * Atualiza um custo existente
   * @param id ID do custo
   * @param custoData Dados do custo
   * @returns Custo atualizado
   */
  const updateCusto = async (id, custoData) => {
    return withLoading(
      async () => {
        try {
          const response = await apiCostService().updateCusto(id, custoData);
          // Atualizar o cache
          costStore.updateCost(id, response.data);
          notify.success('Custo atualizado com sucesso!');
          return response;
        } catch (err) {
          console.error(`Erro ao atualizar custo ${id}:`, err);
          notify.error('Erro ao atualizar custo');
          throw err;
        }
      },
      { loading }
    );
  };

  /**
   * Atualiza parcialmente um custo
   * @param id ID do custo
   * @param custoData Dados parciais do custo
   * @returns Custo atualizado
   */
  const partialUpdateCusto = async (id, custoData) => {
    return withLoading(
      async () => {
        try {
          const response = await apiCostService().partialUpdateCusto(id, custoData);
          // Atualizar o cache
          costStore.updateCost(id, response.data);
          notify.success('Custo atualizado com sucesso!');
          return response;
        } catch (err) {
          console.error(`Erro ao atualizar custo ${id}:`, err);
          notify.error('Erro ao atualizar custo');
          throw err;
        }
      },
      { loading }
    );
  };

  /**
   * Exclui um custo
   * @param id ID do custo
   * @returns true se excluído com sucesso
   */
  const deleteCusto = async (id) => {
    return withLoading(
      async () => {
        try {
          await apiCostService().destroyCusto(id);
          // Atualizar o cache
          costStore.removeCost(id);
          notify.success('Custo excluído com sucesso!');
          return true;
        } catch (err) {
          console.error(`Erro ao excluir custo ${id}:`, err);
          notify.error('Erro ao excluir custo');
          throw err;
        }
      },
      { loading }
    );
  };

  /**
   * Busca categorias de custos
   * @param params Parâmetros de filtro e paginação
   * @returns Lista paginada de categorias
   */
  const fetchCategorias = async (params = {}) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await apiCostService().listCategorias(params);
      categories.value = response.results || [];
      return response;
    } catch (err) {
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
  const getResumoCustos = async (projectId = null) => {
    loading.value = true;
    error.value = null;

    try {
      // Buscar custos com filtros apropriados
      const params = projectId ? { projeto: projectId } : {};
      const response = await apiCostService().listCustos(params);
      const custos = response.results || [];

      // Calcular totais por categoria
      const totalPorCategoria = {};
      const totalPorStatus = {
        pendente: 0,
        aprovado: 0,
        rejeitado: 0,
      };

      let totalGeral = 0;

      custos.forEach(custo => {
        // Total por categoria
        const categoriaId = typeof custo.categoria === 'object' 
          ? custo.categoria.id 
          : custo.categoria;
        const categoriaNome = typeof custo.categoria === 'object' 
          ? custo.categoria.nome 
          : 'Sem categoria';

        if (!totalPorCategoria[categoriaId]) {
          totalPorCategoria[categoriaId] = {
            id: categoriaId,
            nome: categoriaNome,
            total: 0
          };
        }

        totalPorCategoria[categoriaId].total += custo.valor || 0;

        // Total por status
        if (custo.status && totalPorStatus[custo.status] !== undefined) {
          totalPorStatus[custo.status] += custo.valor || 0;
        }

        // Total geral
        totalGeral += custo.valor || 0;
      });

      return {
        totalGeral,
        totalPorCategoria: Object.values(totalPorCategoria),
        totalPorStatus,
        count: response.count
      };
    } catch (err) {
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
