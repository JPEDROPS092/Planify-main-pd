<template>
  <div class="project-statistics">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Estatística: Tarefas por Status -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
          Tarefas por Status
        </h3>
        <div class="h-48">
          <canvas ref="taskStatusChart"></canvas>
        </div>
        <div class="mt-2 grid grid-cols-3 gap-2 text-xs">
          <div class="flex items-center">
            <span class="w-3 h-3 rounded-full bg-blue-500 mr-1"></span>
            <span class="text-gray-600 dark:text-gray-400">A Fazer</span>
          </div>
          <div class="flex items-center">
            <span class="w-3 h-3 rounded-full bg-yellow-500 mr-1"></span>
            <span class="text-gray-600 dark:text-gray-400">Em Andamento</span>
          </div>
          <div class="flex items-center">
            <span class="w-3 h-3 rounded-full bg-green-500 mr-1"></span>
            <span class="text-gray-600 dark:text-gray-400">Concluído</span>
          </div>
        </div>
      </div>

      <!-- Estatística: Progresso do Projeto -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
          Progresso do Projeto
        </h3>
        <div class="flex justify-center items-center h-48">
          <div class="relative w-32 h-32">
            <canvas ref="progressChart"></canvas>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-2xl font-bold text-gray-800 dark:text-white"
                >{{ progressPercentage }}%</span
              >
            </div>
          </div>
        </div>
        <div class="mt-2 text-center text-xs text-gray-600 dark:text-gray-400">
          {{ completedTasks }} de {{ totalTasks }} tarefas concluídas
        </div>
      </div>

      <!-- Estatística: Riscos por Severidade -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
          Riscos por Severidade
        </h3>
        <div class="h-48">
          <canvas ref="riskSeverityChart"></canvas>
        </div>
        <div class="mt-2 grid grid-cols-3 gap-2 text-xs">
          <div class="flex items-center">
            <span class="w-3 h-3 rounded-full bg-green-500 mr-1"></span>
            <span class="text-gray-600 dark:text-gray-400">Baixo</span>
          </div>
          <div class="flex items-center">
            <span class="w-3 h-3 rounded-full bg-yellow-500 mr-1"></span>
            <span class="text-gray-600 dark:text-gray-400">Médio</span>
          </div>
          <div class="flex items-center">
            <span class="w-3 h-3 rounded-full bg-red-500 mr-1"></span>
            <span class="text-gray-600 dark:text-gray-400">Alto</span>
          </div>
        </div>
      </div>

      <!-- Estatística: Custos por Categoria -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
          Custos por Categoria
        </h3>
        <div class="h-48">
          <canvas ref="costCategoryChart"></canvas>
        </div>
        <div class="mt-2 text-center text-xs">
          <div class="flex justify-center space-x-4">
            <span class="text-gray-600 dark:text-gray-400"
              >Total: R$ {{ totalCost.toLocaleString('pt-BR') }}</span
            >
            <span :class="isOverBudget ? 'text-red-500' : 'text-green-500'">
              {{ isOverBudget ? 'Acima do orçamento' : 'Dentro do orçamento' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, defineProps } from 'vue';
import Chart from 'chart.js/auto';
import { useProjectService } from '~/services/api/services/projectService';
import { useTaskService } from '~/services/api/services/taskService';
import { useRiskService } from '~/services/api/services/riskService';
import { useCostService } from '~/services/api/services/costService';
import { useNotification } from '~/composables/useNotification';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

// Refs para os elementos canvas dos gráficos
const taskStatusChart = ref(null);
const progressChart = ref(null);
const riskSeverityChart = ref(null);
const costCategoryChart = ref(null);

// Instâncias dos gráficos
let taskStatusChartInstance = null;
let progressChartInstance = null;
let riskSeverityChartInstance = null;
let costCategoryChartInstance = null;

// Dados para os gráficos
const taskStatusData = ref({
  labels: ['A Fazer', 'Em Andamento', 'Concluído'],
  datasets: [
    {
      data: [0, 0, 0],
      backgroundColor: ['#3B82F6', '#F59E0B', '#10B981'],
      borderWidth: 0,
    },
  ],
});

const riskSeverityData = ref({
  labels: ['Baixo', 'Médio', 'Alto'],
  datasets: [
    {
      data: [0, 0, 0],
      backgroundColor: ['#10B981', '#F59E0B', '#EF4444'],
      borderWidth: 0,
    },
  ],
});

const costCategoryData = ref({
  labels: [],
  datasets: [
    {
      data: [],
      backgroundColor: [
        '#3B82F6',
        '#10B981',
        '#F59E0B',
        '#EF4444',
        '#8B5CF6',
        '#EC4899',
        '#6366F1',
        '#14B8A6',
      ],
      borderWidth: 0,
    },
  ],
});

// Dados computados
const totalTasks = ref(0);
const completedTasks = ref(0);
const progressPercentage = computed(() => {
  if (totalTasks.value === 0) return 0;
  return Math.round((completedTasks.value / totalTasks.value) * 100);
});

const totalCost = ref(0);
const budgetAmount = ref(0);
const isOverBudget = computed(() => totalCost.value > budgetAmount.value);

// Métodos para buscar dados
async function fetchData() {
  try {
    await Promise.all([
      fetchTaskStats(),
      fetchRiskStats(),
      fetchCostStats(),
      fetchProjectDetails(),
    ]);

    // Atualizar os gráficos com os novos dados
    updateCharts();
  } catch (err) {
    const { showApiError } = useNotification();
    showApiError(err, 'Erro ao carregar estatísticas do projeto');
  }
}

async function fetchTaskStats() {
  const taskService = useTaskService();

  try {
    const response = await taskService.listTarefas({
      projeto: props.projectId,
    });

    // Resetar contadores
    const statusCounts = {
      A_FAZER: 0,
      EM_ANDAMENTO: 0,
      FEITO: 0,
    };

    // Contar tarefas por status
    response.results.forEach((task) => {
      if (statusCounts[task.status] !== undefined) {
        statusCounts[task.status]++;
      }
    });

    // Atualizar dados para o gráfico
    taskStatusData.value.datasets[0].data = [
      statusCounts['A_FAZER'],
      statusCounts['EM_ANDAMENTO'],
      statusCounts['FEITO'],
    ];

    // Atualizar contadores de progresso
    totalTasks.value = response.results.length;
    completedTasks.value = statusCounts['FEITO'];
  } catch (err) {
    console.error('Erro ao buscar estatísticas de tarefas:', err);
    throw err;
  }
}

async function fetchRiskStats() {
  const riskService = useRiskService();

  try {
    const response = await riskService.listRiscos({
      projeto: props.projectId,
    });

    // Resetar contadores
    const severityCounts = {
      BAIXO: 0,
      MEDIO: 0,
      ALTO: 0,
    };

    // Contar riscos por severidade
    response.results.forEach((risk) => {
      if (severityCounts[risk.severidade] !== undefined) {
        severityCounts[risk.severidade]++;
      }
    });

    // Atualizar dados para o gráfico
    riskSeverityData.value.datasets[0].data = [
      severityCounts['BAIXO'],
      severityCounts['MEDIO'],
      severityCounts['ALTO'],
    ];
  } catch (err) {
    console.error('Erro ao buscar estatísticas de riscos:', err);
    throw err;
  }
}

async function fetchCostStats() {
  const costService = useCostService();

  try {
    const response = await costService.listCustos({
      projeto: props.projectId,
    });

    // Agrupar custos por categoria
    const categoryCosts = {};
    let total = 0;

    response.results.forEach((cost) => {
      const category = cost.categoria || 'Outros';

      if (!categoryCosts[category]) {
        categoryCosts[category] = 0;
      }

      categoryCosts[category] += cost.valor;
      total += cost.valor;
    });

    // Preparar dados para o gráfico
    const categories = Object.keys(categoryCosts);
    const values = categories.map((cat) => categoryCosts[cat]);

    costCategoryData.value.labels = categories;
    costCategoryData.value.datasets[0].data = values;

    // Atualizar total de custos
    totalCost.value = total;
  } catch (err) {
    console.error('Erro ao buscar estatísticas de custos:', err);
    throw err;
  }
}

async function fetchProjectDetails() {
  const projectService = useProjectService();

  try {
    const project = await projectService.retrieveProjeto(props.projectId);

    // Atualizar orçamento do projeto
    budgetAmount.value = project.orcamento || 0;
  } catch (err) {
    console.error('Erro ao buscar detalhes do projeto:', err);
    throw err;
  }
}

// Método para atualizar os gráficos
function updateCharts() {
  // Configurações comuns para os gráficos
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  // Atualizar ou criar gráfico de status de tarefas
  if (taskStatusChartInstance) {
    taskStatusChartInstance.data = taskStatusData.value;
    taskStatusChartInstance.update();
  } else if (taskStatusChart.value) {
    taskStatusChartInstance = new Chart(taskStatusChart.value, {
      type: 'doughnut',
      data: taskStatusData.value,
      options: commonOptions,
    });
  }

  // Atualizar ou criar gráfico de progresso
  if (progressChartInstance) {
    progressChartInstance.data.datasets[0].data = [
      progressPercentage.value,
      100 - progressPercentage.value,
    ];
    progressChartInstance.update();
  } else if (progressChart.value) {
    progressChartInstance = new Chart(progressChart.value, {
      type: 'doughnut',
      data: {
        labels: ['Concluído', 'Pendente'],
        datasets: [
          {
            data: [progressPercentage.value, 100 - progressPercentage.value],
            backgroundColor: ['#10B981', '#E5E7EB'],
            borderWidth: 0,
          },
        ],
      },
      options: {
        ...commonOptions,
        cutout: '80%',
      },
    });
  }

  // Atualizar ou criar gráfico de severidade de riscos
  if (riskSeverityChartInstance) {
    riskSeverityChartInstance.data = riskSeverityData.value;
    riskSeverityChartInstance.update();
  } else if (riskSeverityChart.value) {
    riskSeverityChartInstance = new Chart(riskSeverityChart.value, {
      type: 'doughnut',
      data: riskSeverityData.value,
      options: commonOptions,
    });
  }

  // Atualizar ou criar gráfico de custos por categoria
  if (costCategoryChartInstance) {
    costCategoryChartInstance.data = costCategoryData.value;
    costCategoryChartInstance.update();
  } else if (costCategoryChart.value) {
    costCategoryChartInstance = new Chart(costCategoryChart.value, {
      type: 'doughnut',
      data: costCategoryData.value,
      options: commonOptions,
    });
  }
}

// Limpar instâncias dos gráficos ao desmontar o componente
function destroyCharts() {
  if (taskStatusChartInstance) {
    taskStatusChartInstance.destroy();
    taskStatusChartInstance = null;
  }

  if (progressChartInstance) {
    progressChartInstance.destroy();
    progressChartInstance = null;
  }

  if (riskSeverityChartInstance) {
    riskSeverityChartInstance.destroy();
    riskSeverityChartInstance = null;
  }

  if (costCategoryChartInstance) {
    costCategoryChartInstance.destroy();
    costCategoryChartInstance = null;
  }
}

// Inicializar e limpar
onMounted(() => {
  fetchData();
});

watch(
  () => props.projectId,
  () => {
    destroyCharts();
    fetchData();
  }
);

// Limpar ao desmontar o componente
onUnmounted(() => {
  destroyCharts();
});
</script>
