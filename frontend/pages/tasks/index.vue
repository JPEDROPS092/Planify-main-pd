<!-- filepath: pages/tasks/index.vue -->
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useRouter } from "vue-router";
import { useToast } from "@/composables/useToast";
import { useApiErrorHandler } from "@/composables/useApiErrorHandler";
import { format, isAfter, isBefore, addDays } from "date-fns";
import { ptBR } from "date-fns/locale";

// API imports
import { useTasksTarefasList, useTasksTarefasDestroy } from "@/api/tasks/tasks";
import { useProjectsProjectsList } from "@/api/projetos/projetos";
import type {
  TarefaList,
  PaginatedTarefaListList,
  NovoStatusBbcEnum,
  PrioridadeEnum,
  ProjetoList,
} from "@/api/schemas";

// definePageMeta({
//   middleware: "auth",
// });

const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();
const { handleApiError } = useApiErrorHandler();

// State management
const currentPage = ref(1);
const searchQuery = ref("");
const selectedStatus = ref<NovoStatusBbcEnum | "ALL">("ALL");
const selectedPriority = ref<PrioridadeEnum | "ALL">("ALL");
const selectedProjeto = ref<number | "ALL">("ALL");
const sortBy = ref<"titulo" | "data_termino" | "prioridade" | "status">(
  "data_termino"
);
const sortOrder = ref<"asc" | "desc">("asc");
const viewMode = ref<"grid" | "list">("grid");
const showFilters = ref(false);

// Query for tasks list - only fetch tasks assigned to the authenticated user
const {
  data: tasksResponse,
  isLoading,
  error,
  refetch,
} = useTasksTarefasList(
  computed(() => ({
    page: currentPage.value,
    search: searchQuery.value || undefined,
    status: selectedStatus.value !== "ALL" ? selectedStatus.value : undefined,
    prioridade:
      selectedPriority.value !== "ALL" ? selectedPriority.value : undefined,
    minhas_tarefas: true, // Only show tasks assigned to the authenticated user
    projeto:
      selectedProjeto.value !== "ALL" ? selectedProjeto.value : undefined,
  }))
);

// Filtro de projeto
const {
  data: projectsResponse,
  isLoading: isLoadingProjects,
  error: errorProjects,
} = useProjectsProjectsList();
const projects = computed<ProjetoList[]>(
  () => projectsResponse.value?.data?.results || []
);

// Paginated tasks response
const paginatedTasks = computed(() => tasksResponse.value?.data);
const allTasks = computed(() => paginatedTasks.value?.results || []);

// Filtered and sorted tasks
const tasks = computed(() => {
  let filtered = [...allTasks.value];

  // Apply local search if needed
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter((task) =>
      task.titulo?.toLowerCase().includes(query)
    );
  }

  // Apply sorting
  filtered.sort((a, b) => {
    let aValue: any, bValue: any;

    switch (sortBy.value) {
      case "titulo":
        aValue = a.titulo?.toLowerCase() || "";
        bValue = b.titulo?.toLowerCase() || "";
        break;
      case "data_termino":
        aValue = a.data_termino ? new Date(a.data_termino) : new Date(0);
        bValue = b.data_termino ? new Date(b.data_termino) : new Date(0);
        break;
      case "prioridade":
        const priorityOrder = { ALTA: 3, MEDIA: 2, BAIXA: 1 };
        aValue = priorityOrder[a.prioridade as keyof typeof priorityOrder] || 0;
        bValue = priorityOrder[b.prioridade as keyof typeof priorityOrder] || 0;
        break;
      case "status":
        aValue = a.status || "";
        bValue = b.status || "";
        break;
      default:
        return 0;
    }

    if (aValue < bValue) return sortOrder.value === "asc" ? -1 : 1;
    if (aValue > bValue) return sortOrder.value === "asc" ? 1 : -1;
    return 0;
  });

  return filtered;
});

const totalPages = computed(() =>
  paginatedTasks.value?.count ? Math.ceil(paginatedTasks.value.count / 20) : 1
);

// Task statistics
const taskStats = computed(() => {
  const stats = {
    total: allTasks.value.length,
    todo: 0,
    inProgress: 0,
    done: 0,
    overdue: 0,
    highPriority: 0,
  };

  allTasks.value.forEach((task) => {
    switch (task.status) {
      case "A_FAZER":
        stats.todo++;
        break;
      case "EM_ANDAMENTO":
        stats.inProgress++;
        break;
      case "FEITO":
        stats.done++;
        break;
    }

    if (task.prioridade === "ALTA") stats.highPriority++;

    if (
      task.data_termino &&
      isAfter(new Date(), new Date(task.data_termino)) &&
      task.status !== "FEITO"
    ) {
      stats.overdue++;
    }
  });

  return stats;
});

// Reset page when filters change
watch([searchQuery, selectedStatus, selectedPriority, selectedProjeto], () => {
  currentPage.value = 1;
});

// Delete task mutation
const deleteTaskMutation = useTasksTarefasDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Tarefa excluída com sucesso!",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["tasks", "tarefas", "list"] });
    },
    onError: (err: any) => {
      console.error("Erro ao excluir tarefa:", err);
      toast({
        title: "Erro",
        description: "Erro ao excluir tarefa",
        type: "error",
      });
    },
  },
});

// --- ACTION HANDLERS ---
const handleCreateTask = () => {
  router.push("/tasks/create");
};

const handleEditTask = (taskId: number) => {
  router.push(`/tasks/${taskId}`);
};

const handleDeleteTask = (taskId: number) => {
  if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
    deleteTaskMutation.mutate({ id: taskId });
  }
};

const handleSort = (field: typeof sortBy.value) => {
  if (sortBy.value === field) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortBy.value = field;
    sortOrder.value = "asc";
  }
};

const clearFilters = () => {
  searchQuery.value = "";
  selectedStatus.value = "ALL";
  selectedPriority.value = "ALL";
  selectedProjeto.value = "ALL";
  sortBy.value = "data_termino";
  sortOrder.value = "asc";
};

const toggleViewMode = () => {
  viewMode.value = viewMode.value === "grid" ? "list" : "grid";
};

// --- FORMATTING HELPERS ---
const formatDate = (dateString: string) => {
  return format(new Date(dateString), "dd/MM/yyyy", { locale: ptBR });
};

const formatDateRelative = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffDays = Math.ceil(
    (date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
  );

  if (diffDays < 0) return `${Math.abs(diffDays)} dias atrás`;
  if (diffDays === 0) return "Hoje";
  if (diffDays === 1) return "Amanhã";
  return `Em ${diffDays} dias`;
};

const getStatusLabel = (status: NovoStatusBbcEnum | null | undefined) => {
  if (!status) return "";
  const labels = {
    A_FAZER: "A Fazer",
    EM_ANDAMENTO: "Em Andamento",
    FEITO: "Feito",
  };
  return labels[status] || status;
};

const getStatusIcon = (status: NovoStatusBbcEnum | null | undefined) => {
  if (!status) return "";
  const icons = {
    A_FAZER: "lucide:circle",
    EM_ANDAMENTO: "lucide:clock",
    FEITO: "lucide:check-circle",
  };
  return icons[status] || "lucide:circle";
};

const getStatusClass = (status: NovoStatusBbcEnum | null | undefined) => {
  if (!status) return "";
  const classes = {
    A_FAZER: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300",
    EM_ANDAMENTO:
      "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
    FEITO: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
  };
  return classes[status] || "bg-gray-100 text-gray-800";
};

const getPriorityClass = (priority: PrioridadeEnum | null | undefined) => {
  if (!priority) return "bg-gray-100 text-gray-800";
  const classes = {
    ALTA: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
    MEDIA:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
    BAIXA: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
  };
  return classes[priority] || "bg-gray-100 text-gray-800";
};

const getPriorityLabel = (priority: PrioridadeEnum | null | undefined) => {
  if (!priority) return "";
  const labels = {
    ALTA: "Alta",
    MEDIA: "Média",
    BAIXA: "Baixa",
  };
  return labels[priority] || priority;
};

const getPriorityIcon = (priority: PrioridadeEnum | null | undefined) => {
  if (!priority) return "lucide:minus";
  const icons = {
    ALTA: "lucide:arrow-up",
    MEDIA: "lucide:minus",
    BAIXA: "lucide:arrow-down",
  };
  return icons[priority] || "lucide:minus";
};

const isTaskOverdue = (task: TarefaList) => {
  if (!task.data_termino || task.status === "FEITO") return false;
  return isAfter(new Date(), new Date(task.data_termino));
};

const getTaskUrgencyClass = (task: TarefaList) => {
  if (isTaskOverdue(task)) {
    return "border-l-4 border-l-red-500";
  }
  if (
    task.data_termino &&
    isBefore(new Date(task.data_termino), addDays(new Date(), 3))
  ) {
    return "border-l-4 border-l-amber-500";
  }
  return "";
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <div
          class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
        >
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              Gerenciamento de Tarefas
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mt-1">
              Organize e acompanhe suas tarefas de forma eficiente
            </p>
          </div>
          <button
            @click="handleCreateTask"
            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2 shadow-sm"
          >
            <Icon icon="lucide:plus" class="w-5 h-5" />
            Nova Tarefa
          </button>
        </div>
      </div>

      <!-- Filtro de Projeto -->
      <div class="mb-6 flex flex-col sm:flex-row gap-4 items-center">
        <label class="text-sm font-medium text-gray-700 dark:text-gray-300"
          >Projeto:</label
        >
        <select
          v-model="selectedProjeto"
          class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white min-w-[200px]"
        >
          <option value="ALL">Todos os Projetos</option>
          <option v-for="proj in projects" :key="proj.id" :value="proj.id">
            {{ proj.titulo }}
          </option>
        </select>
        <div
          v-if="isLoadingProjects"
          class="ml-2 text-gray-400 text-xs flex items-center gap-1"
        >
          <Icon
            icon="svg-spinners:180-ring-with-bg"
            class="w-4 h-4"
          />Carregando projetos...
        </div>
        <div v-if="errorProjects" class="ml-2 text-red-500 text-xs">
          Erro ao carregar projetos
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <div
          class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Total
              </p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ taskStats.total }}
              </p>
            </div>
            <div class="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <Icon
                icon="lucide:list-checks"
                class="w-6 h-6 text-blue-600 dark:text-blue-400"
              />
            </div>
          </div>
        </div>

        <div
          class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                A Fazer
              </p>
              <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">
                {{ taskStats.todo }}
              </p>
            </div>
            <div class="p-3 bg-amber-100 dark:bg-amber-900/30 rounded-lg">
              <Icon
                icon="lucide:circle"
                class="w-6 h-6 text-amber-600 dark:text-amber-400"
              />
            </div>
          </div>
        </div>

        <div
          class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Em Andamento
              </p>
              <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">
                {{ taskStats.inProgress }}
              </p>
            </div>
            <div class="p-3 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
              <Icon
                icon="lucide:clock"
                class="w-6 h-6 text-blue-600 dark:text-blue-400"
              />
            </div>
          </div>
        </div>

        <div
          class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Concluídas
              </p>
              <p
                class="text-2xl font-bold text-emerald-600 dark:text-emerald-400"
              >
                {{ taskStats.done }}
              </p>
            </div>
            <div class="p-3 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg">
              <Icon
                icon="lucide:check-circle"
                class="w-6 h-6 text-emerald-600 dark:text-emerald-400"
              />
            </div>
          </div>
        </div>

        <div
          class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">
                Atrasadas
              </p>
              <p class="text-2xl font-bold text-red-600 dark:text-red-400">
                {{ taskStats.overdue }}
              </p>
            </div>
            <div class="p-3 bg-red-100 dark:bg-red-900/30 rounded-lg">
              <Icon
                icon="lucide:alert-circle"
                class="w-6 h-6 text-red-600 dark:text-red-400"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Filters and Search -->
      <div
        class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 mb-8"
      >
        <div class="flex flex-col lg:flex-row gap-4">
          <!-- Search -->
          <div class="flex-1">
            <div class="relative">
              <Icon
                icon="lucide:search"
                class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5"
              />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar tarefas..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>
          </div>

          <!-- Status Filter -->
          <div class="min-w-[150px]">
            <select
              v-model="selectedStatus"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="ALL">Todos os Status</option>
              <option value="A_FAZER">A Fazer</option>
              <option value="EM_ANDAMENTO">Em Andamento</option>
              <option value="FEITO">Concluído</option>
            </select>
          </div>

          <!-- Priority Filter -->
          <div class="min-w-[150px]">
            <select
              v-model="selectedPriority"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="ALL">Todas as Prioridades</option>
              <option value="ALTA">Alta</option>
              <option value="MEDIA">Média</option>
              <option value="BAIXA">Baixa</option>
            </select>
          </div>

          <!-- Sort -->
          <div class="min-w-[150px]">
            <select
              v-model="sortBy"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            >
              <option value="data_termino">Ordenar por Prazo</option>
              <option value="titulo">Ordenar por Título</option>
              <option value="prioridade">Ordenar por Prioridade</option>
              <option value="status">Ordenar por Status</option>
            </select>
          </div>

          <!-- View Mode Toggle -->
          <div
            class="flex rounded-lg border border-gray-300 dark:border-gray-600 overflow-hidden"
          >
            <button
              @click="viewMode = 'grid'"
              :class="[
                'px-3 py-2 text-sm font-medium transition-colors',
                viewMode === 'grid'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600',
              ]"
            >
              <Icon icon="lucide:grid-3x3" class="w-4 h-4" />
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'px-3 py-2 text-sm font-medium transition-colors',
                viewMode === 'list'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600',
              ]"
            >
              <Icon icon="lucide:list" class="w-4 h-4" />
            </button>
          </div>

          <!-- Clear Filters -->
          <button
            @click="clearFilters"
            class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Limpar
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-20">
        <div class="text-center">
          <Icon
            icon="svg-spinners:180-ring-with-bg"
            class="w-12 h-12 mx-auto text-blue-600 mb-4"
          />
          <p class="text-gray-600 dark:text-gray-400">Carregando tarefas...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-20">
        <div
          class="bg-red-50 dark:bg-red-900/30 rounded-xl p-8 max-w-md mx-auto"
        >
          <Icon
            icon="lucide:alert-circle"
            class="w-12 h-12 mx-auto text-red-600 dark:text-red-400 mb-4"
          />
          <h3 class="text-lg font-semibold text-red-900 dark:text-red-100 mb-2">
            Erro ao carregar tarefas
          </h3>
          <p class="text-red-700 dark:text-red-300 mb-4">
            Não foi possível carregar as tarefas. Tente novamente.
          </p>
          <button
            @click="refetch"
            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-medium transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="tasks.length === 0" class="text-center py-20">
        <div
          class="bg-gray-50 dark:bg-gray-800 rounded-xl p-8 max-w-md mx-auto"
        >
          <Icon
            icon="lucide:clipboard-list"
            class="w-16 h-16 mx-auto text-gray-400 mb-4"
          />
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Nenhuma tarefa encontrada
          </h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            Comece criando sua primeira tarefa para organizar seu trabalho.
          </p>
          <button
            @click="handleCreateTask"
            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center gap-2 mx-auto"
          >
            <Icon icon="lucide:plus" class="w-5 h-5" />
            Criar Primeira Tarefa
          </button>
        </div>
      </div>

      <!-- Tasks Grid/List -->
      <div v-else>
        <div
          :class="[
            viewMode === 'grid'
              ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
              : 'space-y-4',
          ]"
        >
          <div
            v-for="task in tasks"
            :key="task.id"
            :class="[
              'bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-all duration-200 cursor-pointer group',
              getTaskUrgencyClass(task),
            ]"
            @click="handleEditTask(task.id)"
          >
            <div class="p-6">
              <!-- Task Header -->
              <div class="flex items-start justify-between mb-4">
                <div class="flex-1">
                  <h3
                    class="text-lg font-semibold text-gray-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors"
                  >
                    {{ task.titulo }}
                  </h3>
                  <div class="flex items-center gap-2 mb-3">
                    <span
                      :class="getStatusClass(task.status)"
                      class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border"
                    >
                      <Icon
                        :icon="getStatusIcon(task.status)"
                        class="w-3 h-3"
                      />
                      {{ getStatusLabel(task.status) }}
                    </span>
                    <span
                      :class="getPriorityClass(task.prioridade)"
                      class="inline-flex items-center gap-1 text-xs font-medium"
                    >
                      <Icon
                        :icon="getPriorityIcon(task.prioridade)"
                        class="w-3 h-3"
                      />
                      {{ getPriorityLabel(task.prioridade) }}
                    </span>
                  </div>
                </div>
                <div class="flex items-center gap-1 ml-4">
                  <button
                    @click.stop="handleDeleteTask(task.id)"
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                    title="Excluir tarefa"
                  >
                    <Icon icon="lucide:trash-2" class="w-4 h-4" />
                  </button>
                </div>
              </div>

              <!-- Task Details -->
              <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                <div class="flex items-center gap-2">
                  <Icon icon="lucide:folder" class="w-4 h-4" />
                  <span>Projeto {{ task.projeto }}</span>
                </div>

                <div v-if="task.data_termino" class="flex items-center gap-2">
                  <Icon
                    icon="lucide:calendar"
                    class="w-4 h-4"
                    :class="isTaskOverdue(task) ? 'text-red-500' : ''"
                  />
                  <span
                    :class="
                      isTaskOverdue(task)
                        ? 'text-red-600 dark:text-red-400 font-medium'
                        : ''
                    "
                  >
                    {{ formatDate(task.data_termino) }}
                    <span class="text-xs ml-1"
                      >({{ formatDateRelative(task.data_termino) }})</span
                    >
                  </span>
                </div>
              </div>

              <!-- Overdue Warning -->
              <div
                v-if="isTaskOverdue(task)"
                class="mt-3 p-2 bg-red-50 dark:bg-red-900/30 rounded-lg"
              >
                <div
                  class="flex items-center gap-2 text-red-700 dark:text-red-300 text-xs"
                >
                  <Icon icon="lucide:alert-triangle" class="w-4 h-4" />
                  <span class="font-medium">Tarefa em atraso</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div
          v-if="totalPages > 1"
          class="mt-8 flex items-center justify-center"
        >
          <nav class="flex items-center gap-2">
            <button
              @click="currentPage--"
              :disabled="!paginatedTasks?.previous"
              class="px-3 py-2 text-sm font-medium text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Icon icon="lucide:chevron-left" class="w-4 h-4" />
            </button>

            <span
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg"
            >
              Página {{ currentPage }} de {{ totalPages }}
            </span>

            <button
              @click="currentPage++"
              :disabled="!paginatedTasks?.next"
              class="px-3 py-2 text-sm font-medium text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Icon icon="lucide:chevron-right" class="w-4 h-4" />
            </button>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>
