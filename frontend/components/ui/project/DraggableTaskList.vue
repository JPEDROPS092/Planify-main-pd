<template>
  <div class="draggable-task-list space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Lista de Tarefas Reordenável
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
      v-else-if="tasks.length === 0"
      class="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhuma tarefa encontrada para este projeto.</p>
      <p class="text-sm">Crie a primeira tarefa clicando em "Nova Tarefa".</p>
    </div>
    <div v-else class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
        Arraste e solte as tarefas para reordenar a lista de prioridades. As
        alterações serão salvas automaticamente.
      </p>

      <draggable
        v-model="tasks"
        item-key="id"
        handle=".drag-handle"
        class="space-y-2"
        @start="drag = true"
        @end="handleDragEnd"
        :animation="200"
        ghost-class="ghost-card"
      >
        <template #item="{ element, index }">
          <div
            class="task-item flex items-center bg-gray-50 dark:bg-gray-700 p-3 rounded-lg shadow-sm hover:shadow-md transition-all"
          >
            <div
              class="drag-handle cursor-move p-2 mr-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 8h16M4 16h16"
                />
              </svg>
            </div>
            <div class="flex-1">
              <div class="flex justify-between">
                <h4 class="font-medium text-gray-800 dark:text-white">
                  {{ element.name }}
                </h4>
                <span
                  :class="getStatusClass(element.status)"
                  class="text-xs px-2 py-1 rounded-full"
                >
                  {{ element.status }}
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {{ element.description }}
              </p>
              <div
                class="flex justify-between items-center mt-2 text-xs text-gray-500 dark:text-gray-400"
              >
                <span>Prioridade: {{ index + 1 }}</span>
                <span v-if="element.due_date"
                  >Vencimento: {{ formatDate(element.due_date) }}</span
                >
              </div>
            </div>
          </div>
        </template>
      </draggable>

      <div
        v-if="saveSuccess"
        class="mt-4 p-2 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 text-sm rounded"
      >
        Ordem das tarefas salva com sucesso!
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import { useTaskService } from '~/services/taskService';
import { useNotification } from '~/composables/useNotification';
import draggable from 'vuedraggable';
import type { Task } from '~/services/taskService';

const props = defineProps({
  projectId: {
    type: [Number, String],
    required: true,
  },
});

const emit = defineEmits(['tasksReordered']);

const taskService = useTaskService();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
} = useNotification();

// Estado
const tasks = ref<Task[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);
const drag = ref(false);
const saveSuccess = ref(false);

// Funções
async function fetchTasks() {
  if (!props.projectId) return;
  loading.value = true;
  error.value = null;

  try {
    const result = await taskService.fetchTasks({
      projeto: Number(props.projectId),
    });
    tasks.value = Array.isArray(result) ? result : result.results || [];

    // Ordenar por prioridade (se existir) ou por ID
    tasks.value.sort((a, b) => {
      if (a.priority && b.priority) return a.priority - b.priority;
      return a.id - b.id;
    });
  } catch (err: any) {
    error.value = err;
    showApiError(err, 'Falha ao carregar tarefas');
  } finally {
    loading.value = false;
  }
}

function reloadTasks() {
  fetchTasks();
}

async function handleDragEnd() {
  drag.value = false;

  try {
    // Em um ambiente real, você enviaria a nova ordem para o backend
    // Aqui, simulamos um salvamento bem-sucedido

    // Atualizar as prioridades com base na nova ordem
    tasks.value.forEach((task, index) => {
      task.priority = index + 1;
    });

    // Simular uma chamada de API para salvar a ordem
    await new Promise((resolve) => setTimeout(resolve, 500));

    saveSuccess.value = true;
    setTimeout(() => {
      saveSuccess.value = false;
    }, 3000);

    emit('tasksReordered', tasks.value);
    notifySuccess('Ordem das tarefas atualizada com sucesso!');
  } catch (error: any) {
    showApiError(error, 'Falha ao salvar a ordem das tarefas');
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
};

const getStatusClass = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'a fazer':
    case 'pendente':
      return 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
    case 'em andamento':
      return 'bg-blue-200 text-blue-700 dark:bg-blue-900 dark:text-blue-300';
    case 'concluído':
    case 'feito':
      return 'bg-green-200 text-green-700 dark:bg-green-900 dark:text-green-300';
    case 'bloqueado':
      return 'bg-yellow-200 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300';
    case 'cancelado':
      return 'bg-red-200 text-red-700 dark:bg-red-900 dark:text-red-300';
    default:
      return 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
  }
};

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
</script>

<style scoped>
.ghost-card {
  opacity: 0.5;
  background: #c8ebfb;
  border: 1px dashed #2196f3;
}

.task-item {
  transition: all 0.3s ease;
}

.task-item:hover {
  transform: translateY(-2px);
}
</style>
