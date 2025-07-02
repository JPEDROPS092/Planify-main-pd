<!-- filepath: pages/tasks/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { format } from "date-fns";

// 1. Importar funções e tipos do Orval
import { useTasksTarefasList, useTasksTarefasDestroy } from "@/api/tasks/tasks";
import type { TarefaList, PaginatedTarefaListList } from "@/api/schemas";

definePageMeta({
  middleware: "auth",
});

const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 10;

// 2. Query para buscar a lista de tarefas
const {
  data: paginatedTasks,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedTarefaListList>({
  queryKey: ["tasks", currentPage],
  queryFn: () =>
    useTasksTarefasList({ page: currentPage.value, page_size: pageSize }).then(
      (res) => res.data
    ),
});

const tasks = computed(() => paginatedTasks.value?.results || []);
const totalPages = computed(() =>
  paginatedTasks.value?.count
    ? Math.ceil(paginatedTasks.value.count / pageSize)
    : 1
);

// 3. Mutação para deletar uma tarefa
const deleteTaskMutation = useTasksTarefasDestroy({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Tarefa excluída com sucesso." });
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível excluir a tarefa.",
        variant: "destructive",
      });
    },
  },
});

// --- FUNÇÕES DE MANIPULAÇÃO ---
const handleCreateTask = () => {
  // TODO: Implementar modal de criação
  toast({
    title: "Em breve",
    description: "O modal para criar tarefas será implementado aqui.",
  });
};

const handleEditTask = (taskId: number) => {
  router.push(`/tasks/${taskId}`);
};

const handleDeleteTask = (taskId: number) => {
  if (window.confirm("Tem certeza que deseja excluir esta tarefa?")) {
    deleteTaskMutation.mutate({ id: taskId });
  }
};

// --- HELPERS DE FORMATAÇÃO ---
const formatDate = (dateString: string) =>
  dateString ? format(new Date(`${dateString}T12:00:00`), "dd/MM/yyyy") : "-";

const getStatusClass = (status?: TarefaList["status"]) =>
  ({
    A_FAZER:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
    EM_ANDAMENTO:
      "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
    FEITO:
      "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  })[status || ""] || "bg-gray-100 text-gray-800";

const getStatusLabel = (status?: TarefaList["status"]) =>
  ({
    A_FAZER: "A Fazer",
    EM_ANDAMENTO: "Em Andamento",
    FEITO: "Feito",
  })[status || ""] || "Desconhecido";

const getPriorityClass = (priority?: TarefaList["prioridade"]) =>
  ({
    ALTA: "text-red-600",
    MEDIA: "text-orange-500",
    BAIXA: "text-green-600",
  })[priority || ""] || "text-gray-500";

const getPriorityLabel = (priority?: TarefaList["prioridade"]) =>
  ({
    ALTA: "Alta",
    MEDIA: "Média",
    BAIXA: "Baixa",
  })[priority || ""] || "Não definida";
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Minhas Tarefas
      </h1>
      <button
        @click="handleCreateTask"
        class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
      >
        <Icon icon="lucide:plus" class="w-5 h-5" />
        Nova Tarefa
      </button>
    </div>

    <!-- Estados -->
    <div v-if="isLoading" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
    </div>
    <div v-else-if="error" class="text-center py-20">
      Erro ao carregar tarefas.
    </div>
    <div v-else-if="tasks.length === 0" class="text-center py-20">
      Nenhuma tarefa encontrada.
    </div>

    <!-- Lista de Tarefas -->
    <div v-else class="grid gap-4">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="border dark:border-gray-700 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow bg-white dark:bg-gray-800/50 cursor-pointer"
        @click="handleEditTask(task.id)"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3
                class="text-lg font-semibold text-gray-800 dark:text-gray-100"
              >
                {{ task.titulo }}
              </h3>
              <span
                :class="getStatusClass(task.status)"
                class="px-2 py-0.5 rounded-full text-xs font-medium"
                >{{ getStatusLabel(task.status) }}</span
              >
            </div>
            <div
              class="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-gray-500 dark:text-gray-400"
            >
              <div
                class="flex items-center gap-1.5"
                :title="`Projeto: ${task.projeto_nome}`"
              >
                <Icon icon="lucide:folder" class="w-4 h-4" />
                <span>{{ task.projeto_nome }}</span>
              </div>
              <div
                v-if="task.data_termino"
                class="flex items-center gap-1.5"
                title="Prazo"
              >
                <Icon icon="lucide:calendar" class="w-4 h-4" />
                <span>{{ formatDate(task.data_termino) }}</span>
              </div>
              <div class="flex items-center gap-1.5" title="Prioridade">
                <Icon
                  icon="lucide:flag"
                  class="w-4 h-4"
                  :class="getPriorityClass(task.prioridade)"
                />
                <span
                  class="font-medium"
                  :class="getPriorityClass(task.prioridade)"
                  >{{ getPriorityLabel(task.prioridade) }}</span
                >
              </div>
            </div>
          </div>
          <div class="flex gap-2 ml-4">
            <button
              @click.stop="handleDeleteTask(task.id)"
              class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-full transition-colors"
              title="Excluir tarefa"
            >
              <Icon icon="lucide:trash-2" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Paginação -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
        <button
          @click="currentPage--"
          :disabled="!paginatedTasks?.previous"
          class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
        <span
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-200"
          >Página {{ currentPage }} de {{ totalPages }}</span
        >
        <button
          @click="currentPage++"
          :disabled="!paginatedTasks?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>
  </div>
</template>
