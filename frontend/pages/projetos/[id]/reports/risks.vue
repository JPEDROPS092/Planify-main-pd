<template>
  <div class="project-risks-report-container">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Relatório de Riscos</h1>
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
      <!-- Total de Riscos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Total de Riscos</h2>
        <div v-if="loading" class="flex justify-center py-4">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else>
          <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ risks.length }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Riscos identificados
          </p>
        </div>
      </div>

      <!-- Riscos Ativos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Riscos Ativos</h2>
        <div v-if="loading" class="flex justify-center py-4">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else>
          <p class="text-3xl font-bold text-yellow-600">{{ activeRisksCount }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Necessitam monitoramento
          </p>
        </div>
      </div>

      <!-- Riscos Críticos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-2">Riscos Críticos</h2>
        <div v-if="loading" class="flex justify-center py-4">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else>
          <p class="text-3xl font-bold text-red-600">{{ criticalRisksCount }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
            Impacto alto e probabilidade alta
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- Riscos por Categoria -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">Riscos por Categoria</h2>
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

      <!-- Riscos por Impacto -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">Riscos por Impacto</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else class="h-64">
          <canvas ref="impactChartRef"></canvas>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
      <h2 class="text-lg font-semibold mb-4">Matriz de Riscos</h2>
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <div v-else class="h-80">
        <canvas ref="riskMatrixRef"></canvas>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold mb-4">Detalhamento de Riscos</h2>
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <div v-else-if="risks.length === 0" class="text-center py-8 text-gray-500">
        Não há riscos registrados para este projeto.
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
                Probabilidade
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Impacto
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Status
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Estratégia
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="risk in sortedRisks" :key="risk.id" :class="{'bg-red-50 dark:bg-red-900/20': isCriticalRisk(risk)}">
              <td class="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white">
                {{ risk.descricao }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ getCategoryLabel(risk.categoria) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'bg-green-100 text-green-800': risk.probabilidade === 'BAIXA',
                  'bg-yellow-100 text-yellow-800': risk.probabilidade === 'MEDIA',
                  'bg-red-100 text-red-800': risk.probabilidade === 'ALTA'
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ getProbabilityLabel(risk.probabilidade) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'bg-green-100 text-green-800': risk.impacto === 'BAIXO',
                  'bg-yellow-100 text-yellow-800': risk.impacto === 'MEDIO',
                  'bg-red-100 text-red-800': risk.impacto === 'ALTO'
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ getImpactLabel(risk.impacto) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'bg-green-100 text-green-800': risk.status === 'MITIGADO',
                  'bg-yellow-100 text-yellow-800': risk.status === 'ATIVO',
                  'bg-red-100 text-red-800': risk.status === 'OCORRIDO',
                  'bg-gray-100 text-gray-800': risk.status === 'FECHADO'
                }" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                  {{ getStatusLabel(risk.status) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ getStrategyLabel(risk.estrategia) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useRiskService } from '@/composables/useRiskService';
import { useNotification } from '~/composables/useNotification';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'ProjectRisksReportPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { getRisks } = useRiskService();
    const { showError } = useNotification();

    const loading = ref(true);
    const error = ref('');
    const risks = ref<any[]>([]);
    const project = ref<any>(null);

    const categoryChartRef = ref<HTMLCanvasElement | null>(null);
    const impactChartRef = ref<HTMLCanvasElement | null>(null);
    const riskMatrixRef = ref<HTMLCanvasElement | null>(null);
    
    const categoryChart = ref<Chart | null>(null);
    const impactChart = ref<Chart | null>(null);
    const riskMatrix = ref<Chart | null>(null);

    // Valores calculados
    const activeRisksCount = computed(() => {
      return risks.value.filter(risk => risk.status === 'ATIVO').length;
    });

    const criticalRisksCount = computed(() => {
      return risks.value.filter(risk => 
        risk.impacto === 'ALTO' && risk.probabilidade === 'ALTA' && risk.status === 'ATIVO'
      ).length;
    });

    const sortedRisks = computed(() => {
      return [...risks.value].sort((a, b) => {
        // Ordenar por criticidade (impacto * probabilidade)
        const impactValueA = getImpactValue(a.impacto);
        const impactValueB = getImpactValue(b.impacto);
        const probValueA = getProbabilityValue(a.probabilidade);
        const probValueB = getProbabilityValue(b.probabilidade);
        
        const criticalityA = impactValueA * probValueA;
        const criticalityB = impactValueB * probValueB;
        
        return criticalityB - criticalityA; // Do mais crítico para o menos crítico
      });
    });

    const isCriticalRisk = (risk: any) => {
      return risk.impacto === 'ALTO' && risk.probabilidade === 'ALTA' && risk.status === 'ATIVO';
    };

    const getImpactValue = (impact: string) => {
      switch (impact) {
        case 'ALTO': return 3;
        case 'MEDIO': return 2;
        case 'BAIXO': return 1;
        default: return 0;
      }
    };

    const getProbabilityValue = (probability: string) => {
      switch (probability) {
        case 'ALTA': return 3;
        case 'MEDIA': return 2;
        case 'BAIXA': return 1;
        default: return 0;
      }
    };

    const fetchData = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        // Carregar projeto e riscos
        const projectData = await getProject(projectId);
        project.value = projectData;
        
        const risksData = await getRisks(projectId);
        risks.value = risksData;
        
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
      renderImpactChart();
      renderRiskMatrix();
    };

    const renderCategoryChart = () => {
      if (!categoryChartRef.value) return;
      
      // Agrupar riscos por categoria
      const categoryCounts: Record<string, number> = {};
      
      risks.value.forEach(risk => {
        const category = risk.categoria || 'OUTROS';
        if (!categoryCounts[category]) {
          categoryCounts[category] = 0;
        }
        categoryCounts[category]++;
      });
      
      const categoryLabels: Record<string, string> = {
        'TECNICO': 'Técnico',
        'GERENCIAL': 'Gerencial',
        'COMERCIAL': 'Comercial',
        'EXTERNO': 'Externo',
        'ORGANIZACIONAL': 'Organizacional',
        'OUTROS': 'Outros'
      };
      
      const categoryColors = [
        '#4F46E5', // Indigo
        '#10B981', // Emerald
        '#F59E0B', // Amber
        '#EF4444', // Red
        '#8B5CF6', // Violet
        '#6B7280'  // Gray
      ];
      
      // Criar gráfico de categorias
      if (categoryChart.value) {
        categoryChart.value.destroy();
      }
      
      const categories = Object.keys(categoryCounts);
      
      categoryChart.value = new Chart(categoryChartRef.value, {
        type: 'doughnut',
        data: {
          labels: categories.map(cat => categoryLabels[cat] || cat),
          datasets: [{
            data: categories.map(cat => categoryCounts[cat]),
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
            }
          }
        }
      });
    };

    const renderImpactChart = () => {
      if (!impactChartRef.value) return;
      
      // Contar riscos por impacto
      const impactCounts: Record<string, number> = {
        'BAIXO': 0,
        'MEDIO': 0,
        'ALTO': 0
      };
      
      risks.value.forEach(risk => {
        if (impactCounts[risk.impacto] !== undefined) {
          impactCounts[risk.impacto]++;
        }
      });
      
      const impactLabels: Record<string, string> = {
        'BAIXO': 'Baixo',
        'MEDIO': 'Médio',
        'ALTO': 'Alto'
      };
      
      const impactColors = {
        'BAIXO': '#34D399', // Verde
        'MEDIO': '#FBBF24', // Amarelo
        'ALTO': '#EF4444'   // Vermelho
      };
      
      // Criar gráfico de impacto
      if (impactChart.value) {
        impactChart.value.destroy();
      }
      
      impactChart.value = new Chart(impactChartRef.value, {
        type: 'bar',
        data: {
          labels: Object.keys(impactCounts).map(key => impactLabels[key]),
          datasets: [{
            label: 'Número de Riscos',
            data: Object.values(impactCounts),
            backgroundColor: Object.keys(impactCounts).map(key => impactColors[key as keyof typeof impactColors]),
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
                precision: 0
              }
            }
          }
        }
      });
    };

    const renderRiskMatrix = () => {
      if (!riskMatrixRef.value) return;
      
      // Preparar dados para matriz de riscos
      const matrixData: any[] = [];
      
      // Mapear cada risco para um ponto na matriz
      risks.value.forEach(risk => {
        if (risk.status === 'ATIVO' || risk.status === 'OCORRIDO') {
          const x = getProbabilityValue(risk.probabilidade);
          const y = getImpactValue(risk.impacto);
          
          // Adicionar um ponto para cada risco
          matrixData.push({
            x,
            y,
            r: 10, // Tamanho do ponto
            risk // Referência ao risco para o tooltip
          });
        }
      });
      
      // Criar gráfico de matriz de riscos
      if (riskMatrix.value) {
        riskMatrix.value.destroy();
      }
      
      riskMatrix.value = new Chart(riskMatrixRef.value, {
        type: 'bubble',
        data: {
          datasets: [{
            label: 'Riscos',
            data: matrixData,
            backgroundColor: (context) => {
              const risk = context.raw as any;
              if (!risk) return '#6B7280';
              
              // Cor baseada na criticidade
              const criticality = risk.x * risk.y;
              if (criticality >= 6) return 'rgba(239, 68, 68, 0.7)'; // Vermelho (Alto)
              if (criticality >= 3) return 'rgba(251, 191, 36, 0.7)'; // Amarelo (Médio)
              return 'rgba(52, 211, 153, 0.7)'; // Verde (Baixo)
            },
            borderColor: (context) => {
              const risk = context.raw as any;
              if (!risk) return '#4B5563';
              
              // Cor baseada na criticidade
              const criticality = risk.x * risk.y;
              if (criticality >= 6) return '#DC2626'; // Vermelho (Alto)
              if (criticality >= 3) return '#F59E0B'; // Amarelo (Médio)
              return '#10B981'; // Verde (Baixo)
            },
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              min: 0.5,
              max: 3.5,
              title: {
                display: true,
                text: 'Probabilidade'
              },
              ticks: {
                callback: function(value) {
                  switch (value) {
                    case 1: return 'Baixa';
                    case 2: return 'Média';
                    case 3: return 'Alta';
                    default: return '';
                  }
                }
              }
            },
            y: {
              min: 0.5,
              max: 3.5,
              title: {
                display: true,
                text: 'Impacto'
              },
              ticks: {
                callback: function(value) {
                  switch (value) {
                    case 1: return 'Baixo';
                    case 2: return 'Médio';
                    case 3: return 'Alto';
                    default: return '';
                  }
                }
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(context) {
                  const point = context.raw as any;
                  if (!point || !point.risk) return '';
                  
                  const risk = point.risk;
                  return [
                    `Descrição: ${risk.descricao}`,
                    `Categoria: ${getCategoryLabel(risk.categoria)}`,
                    `Probabilidade: ${getProbabilityLabel(risk.probabilidade)}`,
                    `Impacto: ${getImpactLabel(risk.impacto)}`,
                    `Status: ${getStatusLabel(risk.status)}`
                  ];
                }
              }
            }
          }
        }
      });
    };

    const getCategoryLabel = (category: string) => {
      const categoryLabels: Record<string, string> = {
        'TECNICO': 'Técnico',
        'GERENCIAL': 'Gerencial',
        'COMERCIAL': 'Comercial',
        'EXTERNO': 'Externo',
        'ORGANIZACIONAL': 'Organizacional',
        'OUTROS': 'Outros'
      };
      
      return categoryLabels[category] || category;
    };

    const getProbabilityLabel = (probability: string) => {
      const probabilityLabels: Record<string, string> = {
        'BAIXA': 'Baixa',
        'MEDIA': 'Média',
        'ALTA': 'Alta'
      };
      
      return probabilityLabels[probability] || probability;
    };

    const getImpactLabel = (impact: string) => {
      const impactLabels: Record<string, string> = {
        'BAIXO': 'Baixo',
        'MEDIO': 'Médio',
        'ALTO': 'Alto'
      };
      
      return impactLabels[impact] || impact;
    };

    const getStatusLabel = (status: string) => {
      const statusLabels: Record<string, string> = {
        'ATIVO': 'Ativo',
        'MITIGADO': 'Mitigado',
        'OCORRIDO': 'Ocorrido',
        'FECHADO': 'Fechado'
      };
      
      return statusLabels[status] || status;
    };

    const getStrategyLabel = (strategy: string) => {
      const strategyLabels: Record<string, string> = {
        'ACEITAR': 'Aceitar',
        'MITIGAR': 'Mitigar',
        'TRANSFERIR': 'Transferir',
        'EVITAR': 'Evitar'
      };
      
      return strategyLabels[strategy] || strategy;
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
      risks,
      project,
      categoryChartRef,
      impactChartRef,
      riskMatrixRef,
      activeRisksCount,
      criticalRisksCount,
      sortedRisks,
      isCriticalRisk,
      getCategoryLabel,
      getProbabilityLabel,
      getImpactLabel,
      getStatusLabel,
      getStrategyLabel,
      exportPDF,
      printReport
    };
  }
});
</script>

<style scoped>
.project-risks-report-container {
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
