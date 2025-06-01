/**
 * Cálculos relacionados a custos
 * Fornece funções para análise financeira e orçamentária
 */
import { Cost } from '../../api/endpoints/costs';

/**
 * Calcula o custo total de uma lista de custos
 * @param costs Lista de custos
 * @returns Valor total dos custos
 */
export const calculateTotalCost = (costs: Cost[]): number => {
  return costs.reduce((total, cost) => total + (cost.valor || 0), 0);
};

/**
 * Calcula o custo total por categoria
 * @param costs Lista de custos
 * @returns Objeto com totais por categoria
 */
export const calculateCostByCategory = (costs: Cost[]): Record<string, number> => {
  const costByCategory: Record<string, number> = {};
  
  costs.forEach(cost => {
    const category = cost.categoria || 'Sem categoria';
    costByCategory[category] = (costByCategory[category] || 0) + (cost.valor || 0);
  });
  
  return costByCategory;
};

/**
 * Calcula a variação entre o custo planejado e o real
 * @param plannedCost Custo planejado
 * @param actualCost Custo real
 * @returns Objeto com valor e percentual de variação
 */
export const calculateCostVariance = (plannedCost: number, actualCost: number): { value: number; percentage: number } => {
  const variance = actualCost - plannedCost;
  const percentage = plannedCost !== 0 ? (variance / plannedCost) * 100 : 0;
  
  return {
    value: variance,
    percentage
  };
};

/**
 * Calcula o valor agregado (Earned Value)
 * @param plannedCost Custo planejado
 * @param percentComplete Percentual de conclusão (0-100)
 * @returns Valor agregado
 */
export const calculateEarnedValue = (plannedCost: number, percentComplete: number): number => {
  return plannedCost * (percentComplete / 100);
};

/**
 * Calcula indicadores de desempenho de custo
 * @param plannedValue Valor planejado (PV)
 * @param earnedValue Valor agregado (EV)
 * @param actualCost Custo real (AC)
 * @returns Objeto com indicadores CPI e SPI
 */
export const calculatePerformanceIndices = (
  plannedValue: number,
  earnedValue: number,
  actualCost: number
): { cpi: number; spi: number } => {
  // Cost Performance Index (CPI) = EV / AC
  const cpi = actualCost !== 0 ? earnedValue / actualCost : 0;
  
  // Schedule Performance Index (SPI) = EV / PV
  const spi = plannedValue !== 0 ? earnedValue / plannedValue : 0;
  
  return { cpi, spi };
};

/**
 * Calcula a estimativa de custo ao término (EAC)
 * @param actualCost Custo real até o momento
 * @param cpi Índice de desempenho de custo
 * @param remainingWork Trabalho restante (em percentual, 0-100)
 * @param budget Orçamento total
 * @returns Estimativa de custo ao término
 */
export const calculateEstimateAtCompletion = (
  actualCost: number,
  cpi: number,
  remainingWork: number,
  budget: number
): number => {
  if (cpi === 0) return budget;
  
  const remainingBudget = budget * (remainingWork / 100);
  return actualCost + (remainingBudget / cpi);
};

/**
 * Formata um valor monetário para exibição
 * @param value Valor a ser formatado
 * @param currency Moeda (padrão: BRL)
 * @returns String formatada
 */
export const formatCurrency = (value: number, currency: string = 'BRL'): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency
  }).format(value);
};
