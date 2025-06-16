<template>
  <div class="project-costs-report-container">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Relatório de Custos</h1>
      <div class="flex space-x-2">
        <button 
          @click="exportPDF" 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Exportar PDF
        </button>
        <button 
          @click="printReport" 
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
          </svg>
          Imprimir
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- Total de Custos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Total de Custos</h2>
        <div v-if="loading" class="flex justify-center py-4">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else>
          <p class="text-3xl font-bold text-green-600">R$ {{ formatCurrency(totalCost) }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ costs.length }} itens de custo registrados
          </p>
        </div>
      </div>

      <!-- Orçamento Planejado -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Orçamento Planejado</h2>
        <div v-if="loading" class="flex justify-center py-4">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else>
          <p class="text-3xl font-bold text-blue-600">R$ {{ formatCurrency(plannedBudget) }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Definido no início do projeto
          </p>
        </div>
      </div>

      <!-- Variação Orçamentária -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Variação Orçamentária</h2>
        <div v-if="loading" class="flex justify-center py-4">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else>
          <p :class="[
            'text-3xl font-bold',
            budgetVariance > 0 ? 'text-red-600' : 'text-green-600'
          ]">
            {{ budgetVariance > 0 ? '+' : '' }}R$ {{ formatCurrency(budgetVariance) }}
          </p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            {{ budgetVariancePercentage }}% do orçamento planejado
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- Custos por Categoria -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">Custos por Categoria</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else class="h-64">
          <canvas ref="categoryChartRef"></canvas>
        </div>
      </div>

      <!-- Custos por Mês -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">Custos por Mês</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else class="h-64">
          <canvas ref="monthlyChartRef"></canvas>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold mb-4">Detalhamento de Custos</h2>
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <div v-else-if="costs.length === 0" class="text-center py-8 text-gray-500">
        Não há custos registrados para este projeto.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Descrição
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Categoria
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Data
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Valor (R$)
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="cost in sortedCosts" :key="cost.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ cost.descricao }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ getCategoryLabel(cost.categoria) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ formatDate(cost.data) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                {{ formatCurrency(cost.valor) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'bg-green-100 text-green-800': cost.status === 'PAGO',
                  'bg-yellow-100 text-yellow-800': cost.status === 'PENDENTE',
                  'bg-red-100 text-red-800': cost.status === 'ATRASADO'
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ getStatusLabel(cost.status) }}
                </span>
              </td>
            </tr>
          </tbody>
          <tfoot class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <td colspan="3" class="px-6 py-3 text-right text-sm font-medium text-gray-900 dark:text-white">
                Total:
              </td>
              <td class="px-6 py-3 text-sm font-bold text-gray-900 dark:text-white">
                R$ {{ formatCurrency(totalCost) }}
              </td>
              <td></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useCostService } from '@/composables/useCostService';
import { useNotification } from '~/composables/useNotification';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'ProjectCostsReportPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { fetchCustos } = useCostService();
    const { showError } = useNotification();

    const loading = ref(true);
    const error = ref('');
    const costs = ref<any[]>([]);
    const project = ref<any>(null);

    const categoryChartRef = ref<HTMLCanvasElement | null>(null);
    const monthlyChartRef = ref<HTMLCanvasElement | null>(null);
    
    const categoryChart = ref<Chart | null>(null);
    const monthlyChart = ref<Chart | null>(null);

    // Valores calculados
    const totalCost = computed(() => {
      return costs.value.reduce((sum, cost) => sum + (parseFloat(cost.valor) || 0), 0);
    });

    const plannedBudget = computed(() => {
      return project.value?.orcamento || 0;
    });

    const budgetVariance = computed(() => {
      return totalCost.value - plannedBudget.value;
    });

    const budgetVariancePercentage = computed(() => {
      if (plannedBudget.value === 0) return 0;
      return Math.round((budgetVariance.value / plannedBudget.value) * 100);
    });

    const sortedCosts = computed(() => {
      return [...costs.value].sort((a, b) => {
        const dateA = new Date(a.data);
        const dateB = new Date(b.data);
        return dateB.getTime() - dateA.getTime(); // Ordenar do mais recente para o mais antigo
      });
    });

    const fetchData = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        // Carregar projeto e custos
        const projectData = await getProject(projectId);
        project.value = projectData;
        
        const costsData = await fetchCustos(projectId);
        costs.value = costsData;
        
        // Renderizar gráficos após carregar os dados
        renderCharts();
      } catch (err: any) {
        error.value = err.message || 'Erro ao carregar dados do relatório';
        showError('Erro ao carregar relatório', error.value);
      } finally {
        loading.value = false;
      }
    };

    const renderCharts = () => {
      renderCategoryChart();
      renderMonthlyChart();
    };

    const renderCategoryChart = () => {
      if (!categoryChartRef.value) return;
      
      // Agrupar custos por categoria
      const categoryCosts: Record<string, number> = {};
      
      costs.value.forEach(cost => {
        const category = cost.categoria || 'OUTROS';
        if (!categoryCosts[category]) {
          categoryCosts[category] = 0;
        }
        categoryCosts[category] += parseFloat(cost.valor) || 0;
      });
      
      const categoryLabels: Record<string, string> = {
        'PESSOAL': 'Pessoal',
        'MATERIAL': 'Material',
        'EQUIPAMENTO': 'Equipamento',
        'SERVICO': 'Serviço',
        'SOFTWARE': 'Software',
        'VIAGEM': 'Viagem',
        'OUTROS': 'Outros'
      };
      
      const categoryColors = [
        '#4F46E5', // Indigo
        '#10B981', // Emerald
        '#F59E0B', // Amber
        '#EF4444', // Red
        '#8B5CF6', // Violet
        '#EC4899', // Pink
        '#6B7280'  // Gray
      ];
      
      // Criar gráfico de categorias
      if (categoryChart.value) {
        categoryChart.value.destroy();
      }
      
      const categories = Object.keys(categoryCosts);
      
      categoryChart.value = new Chart(categoryChartRef.value, {
        type: 'pie',
        data: {
          labels: categories.map(cat => categoryLabels[cat] || cat),
          datasets: [{
            data: categories.map(cat => categoryCosts[cat]),
            backgroundColor: categoryColors.slice(0, categories.length),
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right'
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw as number;
                  const percentage = Math.round((value / totalCost.value) * 100);
                  return `${label}: R$ ${formatCurrency(value)} (${percentage}%)`;
                }
              }
            }
          }
        }
      });
    };

    const renderMonthlyChart = () => {
      if (!monthlyChartRef.value) return;
      
      // Agrupar custos por mês
      const monthlyCosts: Record<string, number> = {};
      
      costs.value.forEach(cost => {
        if (!cost.data) return;
        
        const date = new Date(cost.data);
        const monthYear = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        
        if (!monthlyCosts[monthYear]) {
          monthlyCosts[monthYear] = 0;
        }
        monthlyCosts[monthYear] += parseFloat(cost.valor) || 0;
      });
      
      // Ordenar meses cronologicamente
      const sortedMonths = Object.keys(monthlyCosts).sort();
      
      // Formatar labels dos meses
      const monthNames = [
        'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
      ];
      
      const formatMonthLabel = (monthYear: string) => {
        const [year, month] = monthYear.split('-');
        return `${monthNames[parseInt(month) - 1]}/${year.slice(2)}`;
      };
      
      // Criar gráfico mensal
      if (monthlyChart.value) {
        monthlyChart.value.destroy();
      }
      
      monthlyChart.value = new Chart(monthlyChartRef.value, {
        type: 'bar',
        data: {
          labels: sortedMonths.map(formatMonthLabel),
          datasets: [{
            label: 'Custos Mensais',
            data: sortedMonths.map(month => monthlyCosts[month]),
            backgroundColor: '#3B82F6',
            borderColor: '#2563EB',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return 'R$ ' + formatCurrency(value as number);
                }
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.dataset.label || '';
                  const value = context.raw as number;
                  return `${label}: R$ ${formatCurrency(value)}`;
                }
              }
            }
          }
        }
      });
    };

    const formatCurrency = (value: number) => {
      return value.toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    const formatDate = (dateString: string) => {
      if (!dateString) return 'N/A';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    };

    const getCategoryLabel = (category: string) => {
      const categoryLabels: Record<string, string> = {
        'PESSOAL': 'Pessoal',
        'MATERIAL': 'Material',
        'EQUIPAMENTO': 'Equipamento',
        'SERVICO': 'Serviço',
        'SOFTWARE': 'Software',
        'VIAGEM': 'Viagem',
        'OUTROS': 'Outros'
      };
      
      return categoryLabels[category] || category;
    };

    const getStatusLabel = (status: string) => {
      const statusLabels: Record<string, string> = {
        'PAGO': 'Pago',
        'PENDENTE': 'Pendente',
        'ATRASADO': 'Atrasado'
      };
      
      return statusLabels[status] || status;
    };

    const exportPDF = () => {
      showError('Funcionalidade em desenvolvimento', 'A exportação para PDF será implementada em breve.');
    };

    const printReport = () => {
      window.print();
    };

    onMounted(() => {
      fetchData();
    });

    return {
      projectId,
      loading,
      error,
      costs,
      project,
      categoryChartRef,
      monthlyChartRef,
      totalCost,
      plannedBudget,
      budgetVariance,
      budgetVariancePercentage,
      sortedCosts,
      formatCurrency,
      formatDate,
      getCategoryLabel,
      getStatusLabel,
      exportPDF,
      printReport
    };
  }
});
</script>

<style scoped>
.project-costs-report-container {
  padding: 1rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #09f;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media print {
  button {
    display: none;
  }
}
</style>
