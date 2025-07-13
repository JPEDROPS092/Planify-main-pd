<!-- components/project/KanbanBoard.vue -->
<template>
  <div
    class="flex-1 flex flex-col overflow-hidden bg-gray-100 dark:bg-gray-900"
  >
    <!-- Header com filtros -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-center">
        <h1 class="text-xl font-semibold text-gray-800 dark:text-gray-200">
          Quadro Kanban do Projeto
        </h1>
        <div class="flex items-center space-x-4">
          <!-- Filtros -->
          <div class="flex items-center space-x-2">
            <input
              v-model="searchFilter"
              type="text"
              placeholder="Buscar tarefas..."
              class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
            <select
              v-model="priorityFilter"
              class="px-3 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              <option value="">Todas as prioridades</option>
              <option value="BAIXA">Baixa</option>
              <option value="MEDIA">Média</option>
              <option value="ALTA">Alta</option>
            </select>
          </div>
          <button
            @click="refreshTasks"
            class="flex items-center space-x-1 px-3 py-1 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            <Icon icon="lucide:refresh-cw" class="w-4 h-4" />
            <span>Atualizar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Feedback de Carregamento e Erro -->
    <div v-if="isLoading" class="flex-1 flex items-center justify-center">
      <svg
        class="animate-spin h-8 w-8 text-blue-500"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      <span class="ml-3 text-gray-600 dark:text-gray-400"
        >Carregando tarefas...</span
      >
    </div>

    <div
      v-if="error"
      class="flex-1 flex items-center justify-center text-red-500 p-4"
    >
      <p>Ocorreu um erro ao carregar as tarefas: {{ error.message }}</p>
    </div>

    <!-- Board Kanban -->
    <div v-if="!isLoading && !error" class="flex-1 overflow-x-auto">
      <div class="inline-flex h-full space-x-4 p-4 min-w-full">
        <!-- Colunas do Kanban -->
        <div
          v-for="column in columns"
          :key="column.id"
          class="flex flex-col flex-shrink-0 w-80 bg-gray-200/50 dark:bg-gray-800/50 rounded-lg"
        >
          <!-- Header da Coluna -->
          <div
            class="p-3 border-b-2"
            :style="{ borderBottomColor: column.color }"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <h3 class="font-semibold text-gray-800 dark:text-gray-200">
                  {{ column.name }}
                </h3>
                <span
                  class="text-sm text-gray-500 bg-gray-300/50 dark:bg-gray-700/50 px-2 py-0.5 rounded-full font-mono"
                >
                  {{ tasksByColumn[column.id]?.length || 0 }}
                </span>
              </div>

              <button
                @click="openCreateTaskModal(column.id)"
                class="text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
                title="Adicionar nova tarefa"
              >
                <Icon icon="lucide:plus-circle" class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Cards das Tarefas -->
          <div class="p-2 space-y-3 h-full overflow-y-auto">
            <div
              v-for="task in tasksByColumn[column.id]"
              :key="task.id"
              @click="openEditTaskModal(task)"
              class="bg-white dark:bg-gray-900/80 p-3 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-lg hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-200"
            >
              <h4 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                {{ task.titulo }}
              </h4>

              <div
                class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400"
              >
                <span
                  class="px-2 py-1 rounded-full font-medium"
                  :class="getPriorityClasses(task.prioridade)"
                >
                  {{ getPriorityLabel(task.prioridade) }}
                </span>
                <div
                  v-if="task.data_termino"
                  class="flex items-center space-x-1"
                  :class="{ 'text-red-500': isOverdue(task.data_termino) }"
                >
                  <Icon icon="lucide:calendar" class="w-3.5 h-3.5" />
                  <span>{{ formatDate(task.data_termino) }}</span>
                </div>
              </div>
            </div>

            <div
              v-if="!tasksByColumn[column.id]?.length"
              class="text-center py-10 text-gray-500 dark:text-gray-400"
            >
              <Icon
                icon="lucide:inbox"
                class="w-10 h-10 mx-auto mb-2 opacity-50"
              />
              <p class="text-sm">Nenhuma tarefa</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Criar/Editar Tarefa -->
    <TaskModal
      v-if="isModalOpen"
      :task-data="selectedTask"
      :project-id="props.projectId"
      @close="closeModal"
      @task-saved="handleTaskSaved"
      @task-deleted="handleTaskDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { Icon } from "@iconify/vue";
import {
  useTasksTarefasList,
  useTasksTarefasUpdateStatusCreate,
} from "../../api/tasks/tasks";
import type {
  TarefaList,
  NovoStatusBbcEnum,
  PrioridadeEnum,
  TasksUpdateStatusRequest,
} from "../../api/schemas";
import { useToast } from "../../composables/useToast";
import TaskModal from "./TaskModal.vue";

// --- PROPS ---
const props = defineProps<{
  projectId: number;
  project?: any;
  isAdmin?: boolean;
}>();

// --- TOAST ---
const { toast } = useToast();

// --- ESTADO REATIVO ---
const tasks = ref<TarefaList[]>([]);
const isLoading = ref(true);
const error = ref<Error | null>(null);

// --- FILTROS ---
const searchFilter = ref("");
const priorityFilter = ref("");

// --- MODAL ---
const isModalOpen = ref(false);
const selectedTask = ref<TarefaList | null>(null);

// --- COLUNAS DO KANBAN ---
const columns = ref([
  { id: "A_FAZER", name: "A Fazer", color: "#6B7280" },
  { id: "EM_ANDAMENTO", name: "Em Andamento", color: "#3B82F6" },
  { id: "FEITO", name: "Feito", color: "#10B981" },
]);

// --- API QUERIES ---
const {
  data: tasksData,
  isLoading: tasksLoading,
  error: tasksError,
  refetch: refetchTasks,
} = useTasksTarefasList(
  computed(() => ({ projeto: props.projectId })),
  {
    query: {
      enabled: computed(() => !!props.projectId),
    },
  }
);

// --- API MUTATIONS ---
const updateStatusMutation = useTasksTarefasUpdateStatusCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Status atualizado",
        description: "O status da tarefa foi atualizado com sucesso.",
        type: "success",
      });
      refetchTasks();
    },
    onError: (error) => {
      toast({
        title: "Erro ao atualizar status",
        description: "Não foi possível atualizar o status da tarefa.",
        type: "error",
      });
    },
  },
});

// --- WATCHERS ---
watch(
  [tasksData, tasksLoading, tasksError],
  ([data, loading, err]) => {
    isLoading.value = loading;
    error.value = err;

    if (data?.data?.results) {
      tasks.value = data.data.results;
    }
  },
  { immediate: true }
);

// --- PROPRIEDADES COMPUTADAS ---
const filteredTasks = computed(() => {
  return tasks.value.filter((task: TarefaList) => {
    const matchesSearch =
      !searchFilter.value ||
      task.titulo.toLowerCase().includes(searchFilter.value.toLowerCase());

    const matchesPriority =
      !priorityFilter.value || task.prioridade === priorityFilter.value;

    return matchesSearch && matchesPriority;
  });
});

const tasksByColumn = computed(() => {
  const groupedTasks: Record<string, TarefaList[]> = {
    A_FAZER: [],
    EM_ANDAMENTO: [],
    FEITO: [],
  };
  filteredTasks.value.forEach((task: TarefaList) => {
    if (task.status && groupedTasks[task.status]) {
      groupedTasks[task.status].push(task);
    }
  });
  return groupedTasks;
});

// --- MÉTODOS ---
const refreshTasks = async () => {
  try {
    await refetchTasks();
    toast({
      title: "Tarefas atualizadas",
      description: "As tarefas foram recarregadas com sucesso.",
      type: "success",
    });
  } catch (e) {
    toast({
      title: "Erro ao atualizar",
      description: "Não foi possível recarregar as tarefas.",
      type: "error",
    });
  }
};

// --- Gerenciamento do Modal ---
const openEditTaskModal = (task: any) => {
  selectedTask.value = task;
  isModalOpen.value = true;
};

const openCreateTaskModal = (columnStatus: string) => {
  selectedTask.value = {
    status: columnStatus as NovoStatusBbcEnum,
    projeto: props.projectId,
    titulo: "",
    data_termino: "",
    id: 0,
    atribuicoes: [],
  };
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedTask.value = null;
};

const handleTaskSaved = async (savedTask: any) => {
  // Refresh tasks to get updated data from server
  await refetchTasks();
  toast({
    title: "Operação concluída",
    description: "A lista de tarefas foi atualizada.",
    type: "success",
  });
  closeModal();
};

const handleTaskDeleted = async (taskId: number) => {
  // Refresh tasks to get updated data from server
  await refetchTasks();
  toast({
    title: "Tarefa removida",
    description: "A tarefa foi removida da lista.",
    type: "success",
  });
  closeModal();
};

// --- Funções Utilitárias de UI ---
const getPriorityClasses = (priority: string | undefined) => {
  const classes: Record<string, string> = {
    BAIXA: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-200",
    MEDIA:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-700/50 dark:text-yellow-200",
    ALTA: "bg-red-100 text-red-800 dark:bg-red-700/50 dark:text-red-200",
  };
  return priority ? classes[priority] || classes.BAIXA : classes.BAIXA;
};

const getPriorityLabel = (priority: string | undefined) => {
  const labels: Record<string, string> = {
    BAIXA: "Baixa",
    MEDIA: "Média",
    ALTA: "Alta",
  };
  return priority ? labels[priority] || "N/A" : "N/A";
};

const formatDate = (dateString: string) => {
  if (!dateString) return "";
  return new Date(dateString).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "short",
  });
};

const isOverdue = (dateString: string) => {
  if (!dateString) return false;
  return new Date(dateString) < new Date();
};

// --- CICLO DE VIDA ---
onMounted(() => {
  // Tasks will be automatically loaded via the API query
});
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
