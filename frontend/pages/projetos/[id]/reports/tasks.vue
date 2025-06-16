<template>
  <div class="project-tasks-report-container">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Relatório de Tarefas</h1>
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

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- Resumo de tarefas por status -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">Tarefas por Status</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else class="h-64">
          <canvas ref="statusChartRef"></canvas>
        </div>
      </div>

      <!-- Resumo de tarefas por prioridade -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold mb-4">Tarefas por Prioridade</h2>
        <div v-if="loading" class="flex justify-center py-8">
          <div class="spinner"></div>
        </div>
        <div v-else-if="error" class="text-red-500">
          {{ error }}
        </div>
        <div v-else class="h-64">
          <canvas ref="priorityChartRef"></canvas>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
      <h2 class="text-lg font-semibold mb-4">Progresso do Projeto</h2>
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <div v-else>
        <div class="flex items-center mb-2">
          <div class="w-full bg-gray-200 rounded-full h-4 mr-2">
            <div 
              class="bg-blue-600 h-4 rounded-full" 
              :style="`width: ${taskCompletionRate}%`"
            ></div>
          </div>
          <span class="text-sm font-medium">{{ taskCompletionRate }}%</span>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          {{ completedTasks }} de {{ totalTasks }} tarefas concluídas
        </p>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
      <h2 class="text-lg font-semibold mb-4">Distribuição de Tarefas por Membro</h2>
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <div v-else class="h-80">
        <canvas ref="memberChartRef"></canvas>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold mb-4">Tarefas Atrasadas</h2>
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      <div v-else-if="error" class="text-red-500">
        {{ error }}
      </div>
      <div v-else-if="overdueTasks.length === 0" class="text-center py-8 text-gray-500">
        Não há tarefas atrasadas no momento.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Tarefa
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Responsável
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Prazo
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Atraso (dias)
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="task in overdueTasks" :key="task.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ task.titulo }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ task.responsavel ? task.responsavel.nome : 'Não atribuído' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ formatDate(task.data_fim) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-red-500">
                {{ calculateDaysOverdue(task.data_fim) }}
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
import { useTaskService } from '@/composables/useTaskService';
import { useNotification } from '~/composables/useNotification';
import Chart from 'chart.js/auto';

export default defineComponent({
  name: 'ProjectTasksReportPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { getTasks } = useTaskService();
    const { showError } = useNotification();

    const loading = ref(true);
    const error = ref('');
    const tasks = ref<any[]>([]);
    const project = ref<any>(null);

    const statusChartRef = ref<HTMLCanvasElement | null>(null);
    const priorityChartRef = ref<HTMLCanvasElement | null>(null);
    const memberChartRef = ref<HTMLCanvasElement | null>(null);
    
    const statusChart = ref<Chart | null>(null);
    const priorityChart = ref<Chart | null>(null);
    const memberChart = ref<Chart | null>(null);

    const totalTasks = computed(() => tasks.value.length);
    const completedTasks = computed(() => tasks.value.filter(task => task.status === 'CONCLUIDA').length);
    const taskCompletionRate = computed(() => {
      if (totalTasks.value === 0) return 0;
      return Math.round((completedTasks.value / totalTasks.value) * 100);
    });

    const overdueTasks = computed(() => {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      return tasks.value
        .filter(task => {
          if (!task.data_fim || task.status === 'CONCLUIDA') return false;
          const deadline = new Date(task.data_fim);
          deadline.setHours(0, 0, 0, 0);
          return deadline < today;
        })
        .sort((a, b) => {
          const dateA = new Date(a.data_fim);
          const dateB = new Date(b.data_fim);
          return dateA.getTime() - dateB.getTime();
        });
    });

    const fetchData = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        // Carregar projeto e tarefas
        const projectData = await getProject(projectId);
        project.value = projectData;
        
        const tasksData = await getTasks(projectId);
        tasks.value = tasksData;
        
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
      renderStatusChart();
      renderPriorityChart();
      renderMemberChart();
    };

    const renderStatusChart = () => {
      if (!statusChartRef.value) return;
      
      // Contar tarefas por status
      const statusCounts: Record<string, number> = {
        'PENDENTE': 0,
        'EM_ANDAMENTO': 0,
        'CONCLUIDA': 0,
        'CANCELADA': 0,
        'BLOQUEADA': 0
      };
      
      tasks.value.forEach(task => {
        if (statusCounts[task.status] !== undefined) {
          statusCounts[task.status]++;
        }
      });
      
      const statusLabels: Record<string, string> = {
        'PENDENTE': 'Pendente',
        'EM_ANDAMENTO': 'Em Andamento',
        'CONCLUIDA': 'Concluída',
        'CANCELADA': 'Cancelada',
        'BLOQUEADA': 'Bloqueada'
      };
      
      const statusColors = {
        'PENDENTE': '#FCD34D',
        'EM_ANDAMENTO': '#60A5FA',
        'CONCLUIDA': '#34D399',
        'CANCELADA': '#F87171',
        'BLOQUEADA': '#9CA3AF'
      };
      
      // Criar gráfico de status
      if (statusChart.value) {
        statusChart.value.destroy();
      }
      
      statusChart.value = new Chart(statusChartRef.value, {
        type: 'doughnut',
        data: {
          labels: Object.keys(statusCounts).map(key => statusLabels[key]),
          datasets: [{
            data: Object.values(statusCounts),
            backgroundColor: Object.keys(statusCounts).map(key => statusColors[key as keyof typeof statusColors]),
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

    const renderPriorityChart = () => {
      if (!priorityChartRef.value) return;
      
      // Contar tarefas por prioridade
      const priorityCounts: Record<string, number> = {
        'BAIXA': 0,
        'MEDIA': 0,
        'ALTA': 0,
        'URGENTE': 0
      };
      
      tasks.value.forEach(task => {
        if (priorityCounts[task.prioridade] !== undefined) {
          priorityCounts[task.prioridade]++;
        }
      });
      
      const priorityLabels: Record<string, string> = {
        'BAIXA': 'Baixa',
        'MEDIA': 'Média',
        'ALTA': 'Alta',
        'URGENTE': 'Urgente'
      };
      
      const priorityColors = {
        'BAIXA': '#34D399',
        'MEDIA': '#FCD34D',
        'ALTA': '#F97316',
        'URGENTE': '#EF4444'
      };
      
      // Criar gráfico de prioridade
      if (priorityChart.value) {
        priorityChart.value.destroy();
      }
      
      priorityChart.value = new Chart(priorityChartRef.value, {
        type: 'pie',
        data: {
          labels: Object.keys(priorityCounts).map(key => priorityLabels[key]),
          datasets: [{
            data: Object.values(priorityCounts),
            backgroundColor: Object.keys(priorityCounts).map(key => priorityColors[key as keyof typeof priorityColors]),
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

    const renderMemberChart = () => {
      if (!memberChartRef.value) return;
      
      // Agrupar tarefas por membro
      const memberTasksMap = new Map<string, { name: string, count: number }>();
      
      tasks.value.forEach(task => {
        if (task.responsavel) {
          const memberId = task.responsavel.id;
          const memberName = task.responsavel.nome;
          
          if (memberTasksMap.has(memberId)) {
            const member = memberTasksMap.get(memberId);
            if (member) {
              member.count++;
            }
          } else {
            memberTasksMap.set(memberId, { name: memberName, count: 1 });
          }
        }
      });
      
      const memberNames = Array.from(memberTasksMap.values()).map(member => member.name);
      const memberCounts = Array.from(memberTasksMap.values()).map(member => member.count);
      
      // Criar gráfico de membros
      if (memberChart.value) {
        memberChart.value.destroy();
      }
      
      memberChart.value = new Chart(memberChartRef.value, {
        type: 'bar',
        data: {
          labels: memberNames,
          datasets: [{
            label: 'Número de Tarefas',
            data: memberCounts,
            backgroundColor: '#60A5FA',
            borderColor: '#3B82F6',
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

    const formatDate = (dateString: string) => {
      if (!dateString) return 'N/A';
      
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    };

    const calculateDaysOverdue = (dateString: string) => {
      if (!dateString) return 'N/A';
      
      const deadline = new Date(dateString);
      deadline.setHours(0, 0, 0, 0);
      
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const diffTime = today.getTime() - deadline.getTime();
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      return diffDays;
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
      tasks,
      project,
      statusChartRef,
      priorityChartRef,
      memberChartRef,
      totalTasks,
      completedTasks,
      taskCompletionRate,
      overdueTasks,
      formatDate,
      calculateDaysOverdue,
      exportPDF,
      printReport
    };
  }
});
</script>

<style scoped>
.project-tasks-report-container {
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
