<template>
  <div class="kanban-board">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Quadro Kanban
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
      v-else-if="!hasAnyTasks"
      class="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhuma tarefa encontrada para este projeto.</p>
      <p class="text-sm">Crie a primeira tarefa clicando em "Nova Tarefa".</p>
    </div>
    <div
      v-else
      class="kanban-container grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4"
    >
      <!-- Coluna "A Fazer" -->
      <div class="kanban-column bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
        <div
          class="column-header flex justify-between items-center mb-3 pb-2 border-b border-gray-200 dark:border-gray-700"
        >
          <h4 class="font-medium text-gray-700 dark:text-gray-300">A Fazer</h4>
          <span
            class="bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300 text-xs px-2 py-1 rounded-full"
          >
            {{ pendingTasks.length }}
          </span>
        </div>
        <draggable
          v-model="pendingTasks"
          group="tasks"
          item-key="id"
          class="min-h-[50px] space-y-2"
          @start="drag = true"
          @end="handleDragEnd"
          :animation="200"
          ghost-class="ghost-card"
        >
          <template #item="{ element }">
            <div
              class="task-card bg-white dark:bg-gray-700 p-3 rounded shadow-sm hover:shadow-md cursor-move"
            >
              <div class="task-header flex justify-between items-start">
                <h5 class="font-medium text-gray-800 dark:text-white text-sm">
                  {{ element.name }}
                </h5>
                <span class="text-xs text-gray-500 dark:text-gray-400">{{
                  formatDate(element.due_date)
                }}</span>
              </div>
              <p
                class="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2"
              >
                {{ element.description }}
              </p>
              <div
                class="task-footer flex justify-between items-center mt-2 pt-2 border-t border-gray-100 dark:border-gray-600"
              >
                <span
                  v-if="element.assignee_details"
                  class="text-xs text-gray-500 dark:text-gray-400"
                >
                  {{
                    element.assignee_details.first_name ||
                    element.assignee_details.username
                  }}
                </span>
                <span v-else class="text-xs text-gray-400 dark:text-gray-500"
                  >Não atribuído</span
                >
                <div class="task-actions flex space-x-1">
                  <Button
                    variant="ghost"
                    size="icon-xs"
                    @click="openEditTaskModal(element)"
                    title="Editar Tarefa"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3 w-3"
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
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>

      <!-- Coluna "Em Andamento" -->
      <div class="kanban-column bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
        <div
          class="column-header flex justify-between items-center mb-3 pb-2 border-b border-gray-200 dark:border-gray-700"
        >
          <h4 class="font-medium text-gray-700 dark:text-gray-300">
            Em Andamento
          </h4>
          <span
            class="bg-blue-200 text-blue-700 dark:bg-blue-900 dark:text-blue-300 text-xs px-2 py-1 rounded-full"
          >
            {{ inProgressTasks.length }}
          </span>
        </div>
        <draggable
          v-model="inProgressTasks"
          group="tasks"
          item-key="id"
          class="min-h-[50px] space-y-2"
          @start="drag = true"
          @end="handleDragEnd"
          :animation="200"
          ghost-class="ghost-card"
        >
          <template #item="{ element }">
            <div
              class="task-card bg-white dark:bg-gray-700 p-3 rounded shadow-sm hover:shadow-md cursor-move"
            >
              <div class="task-header flex justify-between items-start">
                <h5 class="font-medium text-gray-800 dark:text-white text-sm">
                  {{ element.name }}
                </h5>
                <span class="text-xs text-gray-500 dark:text-gray-400">{{
                  formatDate(element.due_date)
                }}</span>
              </div>
              <p
                class="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2"
              >
                {{ element.description }}
              </p>
              <div
                class="task-footer flex justify-between items-center mt-2 pt-2 border-t border-gray-100 dark:border-gray-600"
              >
                <span
                  v-if="element.assignee_details"
                  class="text-xs text-gray-500 dark:text-gray-400"
                >
                  {{
                    element.assignee_details.first_name ||
                    element.assignee_details.username
                  }}
                </span>
                <span v-else class="text-xs text-gray-400 dark:text-gray-500"
                  >Não atribuído</span
                >
                <div class="task-actions flex space-x-1">
                  <Button
                    variant="ghost"
                    size="icon-xs"
                    @click="openEditTaskModal(element)"
                    title="Editar Tarefa"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3 w-3"
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
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>

      <!-- Coluna "Concluído" -->
      <div class="kanban-column bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
        <div
          class="column-header flex justify-between items-center mb-3 pb-2 border-b border-gray-200 dark:border-gray-700"
        >
          <h4 class="font-medium text-gray-700 dark:text-gray-300">
            Concluído
          </h4>
          <span
            class="bg-green-200 text-green-700 dark:bg-green-900 dark:text-green-300 text-xs px-2 py-1 rounded-full"
          >
            {{ completedTasks.length }}
          </span>
        </div>
        <draggable
          v-model="completedTasks"
          group="tasks"
          item-key="id"
          class="min-h-[50px] space-y-2"
          @start="drag = true"
          @end="handleDragEnd"
          :animation="200"
          ghost-class="ghost-card"
        >
          <template #item="{ element }">
            <div
              class="task-card bg-white dark:bg-gray-700 p-3 rounded shadow-sm hover:shadow-md cursor-move"
            >
              <div class="task-header flex justify-between items-start">
                <h5 class="font-medium text-gray-800 dark:text-white text-sm">
                  {{ element.name }}
                </h5>
                <span class="text-xs text-gray-500 dark:text-gray-400">{{
                  formatDate(element.due_date)
                }}</span>
              </div>
              <p
                class="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2"
              >
                {{ element.description }}
              </p>
              <div
                class="task-footer flex justify-between items-center mt-2 pt-2 border-t border-gray-100 dark:border-gray-600"
              >
                <span
                  v-if="element.assignee_details"
                  class="text-xs text-gray-500 dark:text-gray-400"
                >
                  {{
                    element.assignee_details.first_name ||
                    element.assignee_details.username
                  }}
                </span>
                <span v-else class="text-xs text-gray-400 dark:text-gray-500"
                  >Não atribuído</span
                >
                <div class="task-actions flex space-x-1">
                  <Button
                    variant="ghost"
                    size="icon-xs"
                    @click="openEditTaskModal(element)"
                    title="Editar Tarefa"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3 w-3"
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
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>

      <!-- Coluna "Bloqueado" -->
      <div class="kanban-column bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
        <div
          class="column-header flex justify-between items-center mb-3 pb-2 border-b border-gray-200 dark:border-gray-700"
        >
          <h4 class="font-medium text-gray-700 dark:text-gray-300">
            Bloqueado
          </h4>
          <span
            class="bg-yellow-200 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300 text-xs px-2 py-1 rounded-full"
          >
            {{ blockedTasks.length }}
          </span>
        </div>
        <draggable
          v-model="blockedTasks"
          group="tasks"
          item-key="id"
          class="min-h-[50px] space-y-2"
          @start="drag = true"
          @end="handleDragEnd"
          :animation="200"
          ghost-class="ghost-card"
        >
          <template #item="{ element }">
            <div
              class="task-card bg-white dark:bg-gray-700 p-3 rounded shadow-sm hover:shadow-md cursor-move"
            >
              <div class="task-header flex justify-between items-start">
                <h5 class="font-medium text-gray-800 dark:text-white text-sm">
                  {{ element.name }}
                </h5>
                <span class="text-xs text-gray-500 dark:text-gray-400">{{
                  formatDate(element.due_date)
                }}</span>
              </div>
              <p
                class="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2"
              >
                {{ element.description }}
              </p>
              <div
                class="task-footer flex justify-between items-center mt-2 pt-2 border-t border-gray-100 dark:border-gray-600"
              >
                <span
                  v-if="element.assignee_details"
                  class="text-xs text-gray-500 dark:text-gray-400"
                >
                  {{
                    element.assignee_details.first_name ||
                    element.assignee_details.username
                  }}
                </span>
                <span v-else class="text-xs text-gray-400 dark:text-gray-500"
                  >Não atribuído</span
                >
                <div class="task-actions flex space-x-1">
                  <Button
                    variant="ghost"
                    size="icon-xs"
                    @click="openEditTaskModal(element)"
                    title="Editar Tarefa"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-3 w-3"
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
                </div>
              </div>
            </div>
          </template>
        </draggable>
      </div>
    </div>

    <!-- Modal para Criar/Editar Tarefa -->
    <Modal
      :is-open="!!editingTask"
      @close="closeTaskModal"
      title="Editar Tarefa"
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
import { ref, computed, watch, defineProps, defineEmits } from 'vue';
import { useTaskService } from '~/services/api/tasks';
import { useNotification } from '~/composables/useNotification';
import draggable from 'vuedraggable';
import type { Tarefa, TarefaUpdate } from '~/services/api/types';
import type { User } from '~/services/api/types';
import { useUserService } from '~/services/api/userService';

const props = defineProps({
  projectId: {
    type: [Number, String],
    required: true,
  },
});

const emit = defineEmits(['tasksUpdated']);

const taskService = useTaskService();
const userService = useUserService();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
  confirm,
} = useNotification();

// Estado
const allTasks = ref<Tarefa[]>([]);
const loading = ref(true);
const error = ref<Error | null>(null);
const drag = ref(false);
const editingTask = ref<Tarefa | null>(null);
const taskFormKey = ref(0);

// Tarefas agrupadas por status
const pendingTasks = computed(() => {
  return allTasks.value.filter(
    (task) =>
      task.status?.toLowerCase() === 'a fazer' ||
      task.status?.toLowerCase() === 'pendente'
  );
});

const inProgressTasks = computed(() => {
  return allTasks.value.filter(
    (task) => task.status?.toLowerCase() === 'em andamento'
  );
});

const completedTasks = computed(() => {
  return allTasks.value.filter(
    (task) =>
      task.status?.toLowerCase() === 'concluído' ||
      task.status?.toLowerCase() === 'feito'
  );
});

const blockedTasks = computed(() => {
  return allTasks.value.filter(
    (task) => task.status?.toLowerCase() === 'bloqueado'
  );
});

const hasAnyTasks = computed(() => allTasks.value.length > 0);

// Funções
async function fetchTasks() {
  if (!props.projectId) return;

  loading.value = true;
  error.value = null;

  try {
    const { showApiError } = useNotification();

    // Buscar tarefas do projeto
    const response = await taskService.listTarefas({
      projeto: Number(props.projectId),
      ordering: 'prioridade',
    });

    // Mapear tarefas para o formato esperado pelo componente
    const formattedTasks = response.results.map((task) => ({
      id: task.id,
      name: task.titulo,
      description: task.descricao,
      status: task.status,
      due_date: task.data_vencimento,
      assignee: task.responsavel,
      assignee_details: task.responsavel_nome
        ? {
            first_name: task.responsavel_nome.split(' ')[0],
            username: task.responsavel_nome,
          }
        : null,
      priority: task.prioridade,
      sprint: task.sprint,
    }));

    // Distribuir tarefas entre as colunas
    allTasks.value = formattedTasks;

    // Atualizar as colunas
    pendingTasks.value = formattedTasks.filter(
      (task) => task.status === 'A_FAZER'
    );
    inProgressTasks.value = formattedTasks.filter(
      (task) => task.status === 'EM_ANDAMENTO'
    );
    completedTasks.value = formattedTasks.filter(
      (task) => task.status === 'FEITO'
    );
    blockedTasks.value = formattedTasks.filter(
      (task) => task.status === 'BLOQUEADO'
    );

    emit('tasks-updated', formattedTasks);
  } catch (err: any) {
    error.value = err;
    console.error('Erro ao buscar tarefas:', err);
    showApiError(err, 'Erro ao carregar tarefas');
  } finally {
    loading.value = false;
  }
}

function reloadTasks() {
  fetchTasks();
}

function openEditTaskModal(task: Tarefa) {
  editingTask.value = { ...task }; // Cria uma cópia para edição
  taskFormKey.value++; // Muda a key para resetar o estado do TaskForm
}

function closeTaskModal() {
  editingTask.value = null;
  taskFormKey.value++; // Reseta o formulário ao fechar
}

async function handleTaskFormSubmit(formData: TarefaUpdate) {
  try {
    if (editingTask.value && editingTask.value.id) {
      await taskService.updateTask(editingTask.value.id, formData);
      notifySuccess('Tarefa atualizada com sucesso!');
      await fetchTasks(); // Recarrega a lista de tarefas
      closeTaskModal();
    }
  } catch (error: any) {
    showApiError(error, 'Falha ao atualizar tarefa');
  }
}

async function handleDragEnd(evt: any) {
  drag.value = false;

  if (evt.from !== evt.to) {
    const task = evt.item.__draggable_context.element;
    const newStatus = getNewStatus(evt.to);

    if (newStatus) {
      try {
        const taskService = useTaskService();
        const { success: notifySuccess, showApiError } = useNotification();

        // Atualizar o status da tarefa localmente
        const oldStatus = task.status;
        task.status = newStatus;

        // Atualizar no backend
        await taskService.partialUpdateTarefa(task.id, {
          status: newStatus,
        });

        notifySuccess(`Tarefa movida para ${getStatusText(newStatus)}`);

        // Emitir evento
        emit('tasks-updated', [
          ...pendingTasks.value,
          ...inProgressTasks.value,
          ...completedTasks.value,
          ...blockedTasks.value,
        ]);
      } catch (err: any) {
        console.error('Erro ao atualizar status da tarefa:', err);
        const { showApiError } = useNotification();
        showApiError(err, 'Erro ao mover tarefa');

        // Reverter a mudança em caso de erro
        await fetchTasks();
      }
    }
  }

  function getNewStatus(container: any) {
    const containerId = container.id || '';

    if (containerId.includes('pending')) return 'A_FAZER';
    if (containerId.includes('progress')) return 'EM_ANDAMENTO';
    if (containerId.includes('completed')) return 'FEITO';
    if (containerId.includes('blocked')) return 'BLOQUEADO';

    return null;
  }

  function getStatusText(status: string) {
    switch (status) {
      case 'A_FAZER':
        return 'A Fazer';
      case 'EM_ANDAMENTO':
        return 'Em Andamento';
      case 'FEITO':
        return 'Concluído';
      case 'BLOQUEADO':
        return 'Bloqueado';
      default:
        return status;
    }
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
.kanban-container {
  overflow-x: auto;
}

.kanban-column {
  min-width: 250px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.ghost-card {
  opacity: 0.5;
  background: #c8ebfb;
  border: 1px dashed #2196f3;
}

.task-card {
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-2px);
}

/* Estilo para limitar o texto em 2 linhas */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
