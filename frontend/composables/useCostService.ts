/**
 * Composable para gerenciamento de custos
 * Encapsula as funções do serviço de custos
 */
import { ref } from 'vue';
import { useState } from '#imports';
import { useAuth } from '~/services/api/auth';
import {
  listCustos,
  createCusto,
  retrieveCusto,
  updateCusto,
  partialUpdateCusto,
  destroyCusto,
  listCategorias,
  createCategoria,
  retrieveCategoria,
  updateCategoria,
  partialUpdateCategoria,
  destroyCategoria,
  listAlertas,
  createAlerta,
  retrieveAlerta,
  updateAlerta,
  partialUpdateAlerta,
  destroyAlerta,
  listOrcamentosProjeto,
  createOrcamentoProjeto,
  retrieveOrcamentoProjeto,
  updateOrcamentoProjeto,
  partialUpdateOrcamentoProjeto,
  destroyOrcamentoProjeto,
  retrieveProjetosSemOrcamento,
} from '~/services/api/costService';

export const useCostService = () => {
  const { user } = useAuth();
  
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
  const fetchCustos = async (params = {}) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await listCustos(params);
      return response;
    } catch (err) {
      error.value = err.message || 'Erro ao buscar custos';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Obtém detalhes de um custo pelo ID
   * @param id ID do custo
   * @returns Detalhes do custo
   */
  const getCusto = async (id) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const custo = await retrieveCusto(id);
      return custo;
    } catch (err) {
      error.value = err.message || `Erro ao buscar custo #${id}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Cria um novo custo
   * @param custoData Dados do custo
   * @returns Custo criado
   */
  const createCustoWrapper = async (custoData) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      // Associar o usuário logado como criador se não for especificado
      if (!custoData.criado_por && user.value) {
        custoData.criado_por = user.value.id;
      }
      
      const newCusto = await createCusto(custoData);
      return newCusto;
    } catch (err) {
      error.value = err.message || 'Erro ao criar custo';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Atualiza um custo existente
   * @param id ID do custo
   * @param custoData Dados do custo
   * @returns Custo atualizado
   */
  const updateCustoWrapper = async (id, custoData) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const updatedCusto = await updateCusto(id, custoData);
      return updatedCusto;
    } catch (err) {
      error.value = err.message || `Erro ao atualizar custo #${id}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Atualiza parcialmente um custo
   * @param id ID do custo
   * @param custoData Dados parciais do custo
   * @returns Custo atualizado
   */
  const partialUpdateCustoWrapper = async (id, custoData) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const updatedCusto = await partialUpdateCusto(id, custoData);
      return updatedCusto;
    } catch (err) {
      error.value = err.message || `Erro ao atualizar custo #${id}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Exclui um custo
   * @param id ID do custo
   * @returns true se excluído com sucesso
   */
  const deleteCusto = async (id) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      await destroyCusto(id);
      return true;
    } catch (err) {
      error.value = err.message || `Erro ao excluir custo #${id}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Busca categorias de custos
   * @param params Parâmetros de filtro e paginação
   * @returns Lista paginada de categorias
   */
  const fetchCategorias = async (params = {}) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await listCategorias(params);
      categories.value = response.results || [];
      return response;
    } catch (err) {
      error.value = err.message || 'Erro ao buscar categorias';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Obtém um resumo dos custos por categoria, status, etc.
   * @param projectId ID opcional do projeto para filtrar
   * @returns Resumo dos custos
   */
  const getResumoCustos = async (projectId = null) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      // Buscar custos com filtros apropriados
      const params = projectId ? { projeto: projectId } : {};
      const response = await listCustos(params);
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
      error.value = err.message || 'Erro ao obter resumo de custos';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    costs,
    categories,
    alerts,
    budgets,
    isLoading,
    error,
    fetchCustos,
    getCusto,
    createCusto: createCustoWrapper,
    updateCusto: updateCustoWrapper,
    partialUpdateCusto: partialUpdateCustoWrapper,
    deleteCusto,
    fetchCategorias,
    getResumoCustos,
  };
};
