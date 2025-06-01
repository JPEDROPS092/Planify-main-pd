<template>
  <div class="gantt-chart">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Gráfico de Gantt
      </h3>
      <div class="flex space-x-2">
        <Button
          @click="reloadTasks"
          size="sm"
          variant="outline"
          class="flex items-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          Atualizar
        </Button>
        <Button
          @click="zoomIn"
          size="sm"
          variant="outline"
          class="flex items-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"
            />
          </svg>
          Zoom +
        </Button>
        <Button
          @click="zoomOut"
          size="sm"
          variant="outline"
          class="flex items-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 mr-1"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7"
            />
          </svg>
          Zoom -
        </Button>
      </div>
    </div>

    <div v-if="loading" class="space-y-4">
      <SkeletonLoader type="list-item-avatar" :count="3" />
    </div>
    <div
      v-else-if="error"
      class="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ error.message || 'Erro ao carregar tarefas.' }}</p>
      <Button variant="outline" size="sm" class="mt-2" @click="reloadTasks"
        >Tentar Novamente</Button
      >
    </div>
    <div
      v-else-if="!tasks.length"
      class="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhuma tarefa encontrada para este projeto.</p>
      <p class="text-sm">Crie a primeira tarefa clicando em "Nova Tarefa".</p>
    </div>
    <div v-else class="gantt-container overflow-x-auto">
      <!-- Cabeçalho com datas -->
      <div
        class="gantt-header flex border-b border-gray-200 dark:border-gray-700 sticky top-0 bg-white dark:bg-gray-800 z-10"
      >
        <div
          class="gantt-header-task min-w-[200px] p-2 font-medium text-gray-700 dark:text-gray-300 border-r border-gray-200 dark:border-gray-700"
        >
          Tarefa
        </div>
        <div class="gantt-header-timeline flex-1 flex">
          <div
            v-for="(date, index) in dateRange"
            :key="index"
            class="gantt-header-day text-center p-2 text-xs font-medium text-gray-600 dark:text-gray-400 border-r border-gray-200 dark:border-gray-700"
            :style="{ width: `${dayWidth}px` }"
          >
            {{ formatDateHeader(date) }}
          </div>
        </div>
      </div>

      <!-- Linhas de tarefas -->
      <div class="gantt-body">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="gantt-row flex border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750"
        >
          <div
            class="gantt-row-task min-w-[200px] p-2 border-r border-gray-200 dark:border-gray-700 flex items-center"
          >
            <div class="w-full">
              <div
                class="font-medium text-sm text-gray-800 dark:text-gray-200 truncate"
              >
                {{ task.titulo }}
              </div>
              <div
                class="text-xs text-gray-500 dark:text-gray-400 flex items-center mt-1"
              >
                <span class="mr-2">{{ getStatusLabel(task.status) }}</span>
                <span
                  v-if="task.responsavel_nome"
                  class="text-xs text-gray-500 dark:text-gray-400"
                >
                  {{ task.responsavel_nome }}
                </span>
                <span v-else class="text-xs text-gray-400 dark:text-gray-500"
                  >Não atribuído</span
                >
              </div>
            </div>
          </div>
          <div
            class="gantt-row-timeline flex-1 relative"
            :style="{ height: '60px' }"
          >
            <!-- Barras de tarefas -->
            <div
              v-if="task.data_inicio && (task.data_fim || task.data_inicio)"
              class="gantt-bar absolute rounded-md cursor-pointer"
              :class="getTaskStatusClass(task.status)"
              :style="getTaskBarStyle(task)"
              @click="openEditTaskModal(task)"
            >
              <div
                class="gantt-bar-label px-2 text-xs font-medium whitespace-nowrap overflow-hidden text-ellipsis"
              >
                {{ task.titulo }}
              </div>
            </div>
            <!-- Grade de fundo -->
            <div class="gantt-grid flex absolute inset-0">
              <div
                v-for="(date, index) in dateRange"
                :key="index"
                class="gantt-grid-cell border-r border-gray-200 dark:border-gray-700"
                :style="{ width: `${dayWidth}px` }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Editar Tarefa -->
    <Modal
      :is-open="!!editingTask"
      @close="closeTaskModal"
      title="Editar Tarefa"
    >
      <TaskForm
        v-if="editingTask"
        :project-id="projectId"
        :task="editingTask"
        @submit="handleTaskFormSubmit"
        @cancel="closeTaskModal"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, defineProps, onMounted } from 'vue';
import { useTaskService } from '~/services/api/tasks';
import { useNotification } from '~/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import SkeletonLoader from '~/components/SkeletonLoader.vue';
import Modal from '~/components/ui/Modal.vue';
import TaskForm from '~/components/task/TaskForm.vue';
import type { Tarefa } from '~/services/api/types';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const taskService = useTaskService();
const {
  error: notifyError,
  success: notifySuccess,
  showApiError,
} = useNotification();

const tasks = ref<Tarefa[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);
const editingTask = ref<Tarefa | null>(null);
const dayWidth = ref(40); // Largura padrão de cada dia em pixels

// Função para buscar tarefas do projeto
async function fetchTasks() {
  loading.value = true;
  error.value = null;

  try {
    const response = await taskService.listTarefas({
      projeto: props.projectId,
      ordering: 'data_inicio',
    });

    // Filtra tarefas que têm data de início ou fim definidas
    tasks.value = response.results.filter(
      (task) => task.data_inicio || task.data_fim
    );
  } catch (err: any) {
    error.value = err;
    showApiError(err);
  } finally {
    loading.value = false;
  }
}

// Função para recarregar tarefas
function reloadTasks() {
  fetchTasks();
}

// Funções para zoom
function zoomIn() {
  dayWidth.value = Math.min(dayWidth.value + 10, 100);
}

function zoomOut() {
  dayWidth.value = Math.max(dayWidth.value - 10, 20);
}

// Função para abrir modal de edição de tarefa
function openEditTaskModal(task: Tarefa) {
  editingTask.value = task;
}

// Função para fechar modal de edição de tarefa
function closeTaskModal() {
  editingTask.value = null;
}

// Função para lidar com o envio do formulário de tarefa
async function handleTaskFormSubmit(formData: any) {
  try {
    if (editingTask.value) {
      await taskService.updateTarefa(editingTask.value.id, formData);
      notifySuccess('Tarefa atualizada com sucesso!');
      fetchTasks();
      closeTaskModal();
    }
  } catch (err: any) {
    showApiError(err);
  }
}

// Função para formatar data no cabeçalho
function formatDateHeader(date: Date) {
  return date.toLocaleDateString('pt-BR', { day: 'numeric', month: 'short' });
}

// Função para obter o rótulo do status
function getStatusLabel(status: string) {
  const statusMap: Record<string, string> = {
    PENDENTE: 'A Fazer',
    EM_ANDAMENTO: 'Em Andamento',
    CONCLUIDO: 'Concluído',
    BLOQUEADO: 'Bloqueado',
    CANCELADO: 'Cancelado',
  };
  return statusMap[status] || status;
}

// Função para obter a classe CSS com base no status da tarefa
function getTaskStatusClass(status: string) {
  switch (status) {
    case 'PENDENTE':
      return 'bg-gray-200 dark:bg-gray-700 border border-gray-300 dark:border-gray-600';
    case 'EM_ANDAMENTO':
      return 'bg-blue-100 dark:bg-blue-900 border border-blue-300 dark:border-blue-800';
    case 'CONCLUIDO':
      return 'bg-green-100 dark:bg-green-900 border border-green-300 dark:border-green-800';
    case 'BLOQUEADO':
      return 'bg-yellow-100 dark:bg-yellow-900 border border-yellow-300 dark:border-yellow-800';
    case 'CANCELADO':
      return 'bg-red-100 dark:bg-red-900 border border-red-300 dark:border-red-800';
    default:
      return 'bg-gray-200 dark:bg-gray-700 border border-gray-300 dark:border-gray-600';
  }
}

// Função para calcular o estilo da barra de tarefa
function getTaskBarStyle(task: Tarefa) {
  if (!task.data_inicio) return {};

  const start = new Date(task.data_inicio);
  const end = task.data_fim
    ? new Date(task.data_fim)
    : new Date(task.data_inicio);

  // Adiciona um dia ao final para tarefas de um dia
  if (task.data_inicio === task.data_fim) {
    end.setDate(end.getDate() + 1);
  }

  const startPosition = getPositionForDate(start);
  const width = getPositionForDate(end) - startPosition;

  return {
    left: `${startPosition}px`,
    width: `${Math.max(width, dayWidth.value)}px`,
    height: '30px',
    top: '15px',
  };
}

// Função para obter a posição em pixels para uma data
function getPositionForDate(date: Date) {
  const startDate = dateRange.value[0];
  const diffDays = Math.floor(
    (date.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)
  );
  return diffDays * dayWidth.value;
}

// Calcula o intervalo de datas para o gráfico
const dateRange = computed(() => {
  if (!tasks.value.length) {
    // Intervalo padrão de 30 dias a partir de hoje
    const today = new Date();
    const dates = [];
    for (let i = 0; i < 30; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date);
    }
    return dates;
  }

  // Encontra a data mais antiga e mais recente
  let minDate: Date | null = null;
  let maxDate: Date | null = null;

  tasks.value.forEach((task) => {
    if (task.data_inicio) {
      const startDate = new Date(task.data_inicio);
      if (!minDate || startDate < minDate) {
        minDate = startDate;
      }
    }

    if (task.data_fim) {
      const endDate = new Date(task.data_fim);
      if (!maxDate || endDate > maxDate) {
        maxDate = endDate;
      }
    }
  });

  // Adiciona margem de 5 dias antes e depois
  if (minDate) {
    minDate.setDate(minDate.getDate() - 5);
  } else {
    minDate = new Date();
  }

  if (maxDate) {
    maxDate.setDate(maxDate.getDate() + 5);
  } else {
    maxDate = new Date();
    maxDate.setDate(minDate.getDate() + 30);
  }

  // Gera array de datas
  const dates = [];
  const currentDate = new Date(minDate);

  while (currentDate <= maxDate) {
    dates.push(new Date(currentDate));
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return dates;
});

// Carregar tarefas quando o componente for montado ou o projectId mudar
watch(
  () => props.projectId,
  (newProjectId) => {
    if (newProjectId) {
      fetchTasks();
    }
  },
  { immediate: true }
);

onMounted(() => {
  fetchTasks();
});
</script>

<style scoped>
.gantt-container {
  max-width: 100%;
  overflow-x: auto;
}

.gantt-bar {
  z-index: 1;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.gantt-bar:hover {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}
</style>
