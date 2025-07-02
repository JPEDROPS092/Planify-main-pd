<!-- filepath: components/project/ProjectTasks.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "~/composables/useToast";
import type {
  Projeto,
  TarefaList,
  PaginatedTarefaListList,
  TarefaRequest,
} from "~/api/schemas";
import {
  useTasksTarefasList,
  useTasksTarefasCreate,
  useTasksTarefasUpdate,
  useTasksTarefasDestroy,
} from "~/api/tasks/tasks";

const props = defineProps<{
  projectId: number;
  project: Projeto;
}>();

const queryClient = useQueryClient();
const { toast } = useToast();

const showTaskModal = ref(false);
const editingTask = ref<TarefaList | null>(null);
const taskForm = ref<Partial<TarefaRequest>>({
  titulo: "",
  descricao: "",
  status: "PENDENTE",
  prioridade: "MEDIA",
  data_inicio: "",
  data_fim: "",
  projeto: props.projectId,
});

// Query para buscar as tarefas DESTE projeto
const {
  data: paginatedTasks,
  isLoading,
  error,
} = useQuery<PaginatedTarefaListList>({
  queryKey: ["project-tasks", props.projectId],
  queryFn: () =>
    useTasksTarefasList({
      projeto: props.projectId,
      page_size: 100,
      ordering: "-criado_em",
    }).then((res) => res.data),
});

const tasks = computed(() => paginatedTasks.value?.results || []);

// Mutações
const createTaskMutation = useMutation({
  mutationFn: (data: TarefaRequest) =>
    useTasksTarefasCreate({ data }).then((res) => res.data),
  onSuccess: () => {
    toast({ title: "Sucesso!", description: "Tarefa criada com sucesso." });
    queryClient.invalidateQueries({
      queryKey: ["project-tasks", props.projectId],
    });
    closeTaskModal();
  },
  onError: () => {
    toast({
      title: "Erro",
      description: "Erro ao criar a tarefa.",
      variant: "destructive",
    });
  },
});

const updateTaskMutation = useMutation({
  mutationFn: (params: { id: number; data: TarefaRequest }) =>
    useTasksTarefasUpdate(params).then((res) => res.data),
  onSuccess: () => {
    toast({ title: "Sucesso!", description: "Tarefa atualizada com sucesso." });
    queryClient.invalidateQueries({
      queryKey: ["project-tasks", props.projectId],
    });
    closeTaskModal();
  },
  onError: () => {
    toast({
      title: "Erro",
      description: "Erro ao atualizar a tarefa.",
      variant: "destructive",
    });
  },
});

const deleteTaskMutation = useMutation({
  mutationFn: (id: number) => useTasksTarefasDestroy({ id }),
  onSuccess: () => {
    toast({ title: "Sucesso!", description: "Tarefa excluída com sucesso." });
    queryClient.invalidateQueries({
      queryKey: ["project-tasks", props.projectId],
    });
  },
  onError: () => {
    toast({
      title: "Erro",
      description: "Erro ao excluir a tarefa.",
      variant: "destructive",
    });
  },
});

const handleCreateTask = () => {
  editingTask.value = null;
  taskForm.value = {
    titulo: "",
    descricao: "",
    status: "PENDENTE",
    prioridade: "MEDIA",
    data_inicio: "",
    data_fim: "",
    projeto: props.projectId,
  };
  showTaskModal.value = true;
};

const handleEditTask = (task: TarefaList) => {
  editingTask.value = task;
  taskForm.value = { ...task };
  showTaskModal.value = true;
};

const handleDeleteTask = (task: TarefaList) => {
  if (confirm("Tem certeza que deseja excluir esta tarefa?")) {
    deleteTaskMutation.mutate(task.id);
  }
};

const closeTaskModal = () => {
  showTaskModal.value = false;
  editingTask.value = null;
};

const submitTask = () => {
  if (editingTask.value) {
    updateTaskMutation.mutate({
      id: editingTask.value.id,
      data: taskForm.value as TarefaRequest,
    });
  } else {
    createTaskMutation.mutate(taskForm.value as TarefaRequest);
  }
};

const getStatusColor = (status: string) => {
  const colors = {
    PENDENTE: "bg-yellow-100 text-yellow-800",
    EM_ANDAMENTO: "bg-blue-100 text-blue-800",
    CONCLUIDA: "bg-green-100 text-green-800",
    CANCELADA: "bg-red-100 text-red-800",
  };
  return colors[status as keyof typeof colors] || "bg-gray-100 text-gray-800";
};

const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("pt-BR");
};
</script>

<template>
  <div>
    <!-- Header com botão de adicionar -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-gray-100">
        Tarefas do Projeto
      </h2>
      <button
        @click="handleCreateTask"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
      >
        <Icon icon="lucide:plus" class="h-4 w-4 mr-2" />
        Nova Tarefa
      </button>
    </div>

    <!-- Lista de Tarefas -->
    <div v-if="isLoading" class="text-center py-8">Carregando tarefas...</div>
    <div v-else-if="error" class="text-center py-8 text-red-500">
      Erro ao carregar tarefas.
    </div>
    <div v-else-if="tasks.length === 0" class="text-center py-8 text-gray-500">
      Nenhuma tarefa encontrada para este projeto.
    </div>
    <div v-else class="space-y-3">
      <div
        v-for="task in tasks"
        :key="task.id"
        class="p-4 bg-white dark:bg-gray-800 shadow rounded-lg hover:shadow-md transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
              {{ task.titulo }}
            </h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {{ task.descricao }}
            </p>

            <div class="mt-2 flex flex-wrap gap-2">
              <!-- Status -->
              <span
                :class="[
                  getStatusColor(task.status),
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                ]"
              >
                {{ task.status_display }}
              </span>

              <!-- Datas -->
              <span class="inline-flex items-center text-xs text-gray-500">
                <Icon icon="lucide:calendar" class="h-3 w-3 mr-1" />
                {{ formatDate(task.data_inicio) }} -
                {{ formatDate(task.data_fim) }}
              </span>

              <!-- Responsável -->
              <span
                v-if="task.responsavel"
                class="inline-flex items-center text-xs text-gray-500"
              >
                <Icon icon="lucide:user" class="h-3 w-3 mr-1" />
                {{ task.responsavel }}
              </span>
            </div>
          </div>

          <!-- Ações -->
          <div class="flex items-center space-x-2 ml-4">
            <button
              @click="handleEditTask(task)"
              class="p-2 text-gray-400 hover:text-primary-600 rounded-full"
            >
              <Icon icon="lucide:edit" class="h-4 w-4" />
            </button>
            <button
              @click="handleDeleteTask(task)"
              class="p-2 text-gray-400 hover:text-red-600 rounded-full"
            >
              <Icon icon="lucide:trash-2" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Tarefa -->
    <Modal
      v-if="showTaskModal"
      :title="editingTask ? 'Editar Tarefa' : 'Nova Tarefa'"
      @close="closeTaskModal"
    >
      <form @submit.prevent="submitTask" class="space-y-4">
        <div>
          <label for="titulo" class="block text-sm font-medium text-gray-700">
            Título
          </label>
          <input
            id="titulo"
            v-model="taskForm.titulo"
            type="text"
            required
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          />
        </div>

        <div>
          <label
            for="descricao"
            class="block text-sm font-medium text-gray-700"
          >
            Descrição
          </label>
          <textarea
            id="descricao"
            v-model="taskForm.descricao"
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          ></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label for="status" class="block text-sm font-medium text-gray-700">
              Status
            </label>
            <select
              id="status"
              v-model="taskForm.status"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            >
              <option value="PENDENTE">Pendente</option>
              <option value="EM_ANDAMENTO">Em Andamento</option>
              <option value="CONCLUIDA">Concluída</option>
              <option value="CANCELADA">Cancelada</option>
            </select>
          </div>

          <div>
            <label
              for="prioridade"
              class="block text-sm font-medium text-gray-700"
            >
              Prioridade
            </label>
            <select
              id="prioridade"
              v-model="taskForm.prioridade"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            >
              <option value="BAIXA">Baixa</option>
              <option value="MEDIA">Média</option>
              <option value="ALTA">Alta</option>
              <option value="CRITICA">Crítica</option>
            </select>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label
              for="data_inicio"
              class="block text-sm font-medium text-gray-700"
            >
              Data de Início
            </label>
            <input
              id="data_inicio"
              v-model="taskForm.data_inicio"
              type="date"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            />
          </div>

          <div>
            <label
              for="data_fim"
              class="block text-sm font-medium text-gray-700"
            >
              Data de Fim
            </label>
            <input
              id="data_fim"
              v-model="taskForm.data_fim"
              type="date"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            />
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="closeTaskModal"
            class="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            :disabled="
              createTaskMutation.isPending || updateTaskMutation.isPending
            "
          >
            {{ editingTask ? "Atualizar" : "Criar" }}
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>
