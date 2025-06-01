<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Tarefas do Projeto
      </h3>
      <Button @click="showCreateTaskModal = true" size="sm">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class_name="h-4 w-4 mr-1.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 4v16m8-8H4"
          />
        </svg>
        Nova Tarefa
      </Button>
    </div>

    <div v-if="loadingTasks" class_name="space-y-4">
      <SkeletonLoader type="list-item-avatar" :count="3" />
    </div>
    <div
      v-else-if="tasksError"
      class_name="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ tasksError.message || 'Erro ao carregar tarefas.' }}</p>
      <Button variant="outline" size="sm" class_name="mt-2" @click="fetchTasks"
        >Tentar Novamente</Button
      >
    </div>
    <div
      v-else-if="tasks.length === 0"
      class_name="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhuma tarefa encontrada para este projeto.</p>
      <p class_name="text-sm">
        Crie a primeira tarefa clicando em "Nova Tarefa".
      </p>
    </div>
    <div v-else class_name="space-y-4">
      <!-- Aqui podemos implementar diferentes visualizações: Lista, Board (Kanban) -->
      <!-- Por agora, uma lista simples -->
      <div
        v-for="task in tasks"
        :key="task.id"
        class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div class_name="flex justify-between items-start">
          <div>
            <h4 class_name="text-lg font-medium text-gray-800 dark:text-white">
              {{ task.name }}
            </h4>
            <p class_name="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{ task.description }}
            </p>
            <div
              class_name="mt-2 flex items-center space-x-3 text-xs text-gray-500 dark:text-gray-400"
            >
              <span
                >Status:
                <span
                  :class_name="getStatusClass(task.status)"
                  class_name="font-semibold py-0.5 px-1.5 rounded-full"
                  >{{ task.status }}</span
                ></span
              >
              <span v-if="task.due_date"
                >Vencimento: {{ formatDate(task.due_date) }}</span
              >
              <span v-if="task.assignee_details"
                >Responsável:
                {{
                  task.assignee_details.first_name ||
                  task.assignee_details.username
                }}</span
              >
            </div>
          </div>
          <div class_name="flex space-x-1">
            <Button
              variant="ghost"
              size="icon-sm"
              @click="openEditTaskModal(task)"
              title="Editar Tarefa"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class_name="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </Button>
            <Button
              variant="ghost"
              size="icon-sm"
              @click="confirmDeleteTask(task.id)"
              title="Excluir Tarefa"
              class_name="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class_name="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Criar/Editar Tarefa -->
    <Modal
      :is-open="showCreateTaskModal || !!editingTask"
      @close="closeTaskModal"
      :title="editingTask ? 'Editar Tarefa' : 'Criar Nova Tarefa'"
    >
      <TaskForm
        :project-id="projectId"
        :task="editingTask"
        @submit="handleTaskFormSubmit"
        @cancel="closeTaskModal"
        :key="taskFormKey"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, toRefs } from 'vue';
import { useTaskService } from '~/services/taskService';
import type { Task, TaskCreate, TaskUpdate } from '~/services/taskService';
import { useUserService } from '~/services/userService'; // Para detalhes do responsável
import type { User } from '~/services/userService';
import { useNotification } from '~/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import Modal from '~/components/Modal.vue';
import TaskForm from '~/components/TaskForm.vue';
import SkeletonLoader from '~/components/SkeletonLoader.vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const { projectId } = toRefs(props);
const taskService = useTaskService();
const userService = useUserService();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
  confirm,
} = useNotification();

const tasks = ref<Task[]>([]);
const loadingTasks = ref(true);
const tasksError = ref<Error | null>(null);
const showCreateTaskModal = ref(false);
const editingTask = ref<Task | null>(null);
const taskFormKey = ref(0); // Para forçar o re-render do formulário

async function fetchTasks() {
  if (!projectId.value) return;
  loadingTasks.value = true;
  tasksError.value = null;
  try {
    const result = await taskService.getByProject(projectId.value);
    // O backend pode retornar um objeto com 'results' ou diretamente um array
    const taskList = Array.isArray(result) ? result : result.results || [];

    // Buscar detalhes do responsável para cada tarefa
    tasks.value = await Promise.all(
      taskList.map(async (task: any) => {
        let assigneeDetails: User | null = null;
        if (task.assignee) {
          try {
            assigneeDetails = await userService.getUserById(task.assignee);
          } catch (e) {
            console.warn(
              `Falha ao buscar detalhes do usuário ${task.assignee}`,
              e
            );
          }
        }
        return { ...task, assignee_details: assigneeDetails };
      })
    );
  } catch (error: any) {
    tasksError.value = error;
    showApiError(error, 'Falha ao carregar tarefas');
  } finally {
    loadingTasks.value = false;
  }
}

function openEditTaskModal(task: Task) {
  editingTask.value = { ...task }; // Cria uma cópia para edição
  taskFormKey.value++; // Muda a key para resetar o estado do TaskForm
  showCreateTaskModal.value = false; // Garante que o modal de criação não interfira
}

function closeTaskModal() {
  showCreateTaskModal.value = false;
  editingTask.value = null;
  taskFormKey.value++; // Reseta o formulário ao fechar
}

async function handleTaskFormSubmit(formData: TaskCreate | TaskUpdate) {
  try {
    if (editingTask.value && editingTask.value.id) {
      await taskService.update(editingTask.value.id, formData as TaskUpdate);
      notifySuccess('Tarefa atualizada com sucesso!');
    } else {
      await taskService.create(formData as TaskCreate);
      notifySuccess('Tarefa criada com sucesso!');
    }
    await fetchTasks(); // Recarrega a lista de tarefas
    closeTaskModal();
  } catch (error: any) {
    showApiError(
      error,
      editingTask.value ? 'Falha ao atualizar tarefa' : 'Falha ao criar tarefa'
    );
  }
}

async function confirmDeleteTask(taskId?: number) {
  if (!taskId) return;
  const confirmed = await confirm(
    'Excluir Tarefa',
    'Tem certeza que deseja excluir esta tarefa? Esta ação não pode ser desfeita.',
    {
      confirmButtonText: 'Excluir',
      cancelButtonText: 'Cancelar',
      type: 'danger',
    }
  );
  if (confirmed) {
    try {
      await taskService.remove(taskId);
      notifySuccess('Tarefa excluída com sucesso!');
      await fetchTasks();
    } catch (error: any) {
      showApiError(error, 'Falha ao excluir tarefa');
    }
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
};

const getStatusClass = (status?: string) => {
  // Lógica similar à da página de detalhes do projeto, ajuste conforme necessário
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

watch(
  projectId,
  (newProjectId) => {
    if (newProjectId) {
      fetchTasks();
    }
  },
  { immediate: true }
);
</script>

<style scoped>
/* Estilos específicos para este componente */
</style>
