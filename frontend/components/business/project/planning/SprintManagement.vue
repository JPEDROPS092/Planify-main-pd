<template>
  <div class="sprint-management space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Gerenciamento de Sprints
      </h3>
      <Button @click="showCreateSprintModal = true" size="sm">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 mr-1.5"
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
        Nova Sprint
      </Button>
    </div>

    <div v-if="loading" class="space-y-4">
      <SkeletonLoader type="list-item-avatar" :count="3" />
    </div>
    <div
      v-else-if="error"
      class="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ error.message || 'Erro ao carregar sprints.' }}</p>
      <Button variant="outline" size="sm" class="mt-2" @click="fetchSprints"
        >Tentar Novamente</Button
      >
    </div>
    <div
      v-else-if="sprints.length === 0"
      class="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhuma sprint encontrada para este projeto.</p>
      <p class="text-sm">Crie a primeira sprint clicando em "Nova Sprint".</p>
    </div>
    <div v-else class="sprint-list space-y-6">
      <div
        v-for="sprint in sprints"
        :key="sprint.id"
        class="sprint-container bg-gray-50 dark:bg-gray-800 rounded-lg p-4"
      >
        <div class="sprint-header flex justify-between items-start mb-4">
          <div>
            <h4 class="font-medium text-gray-800 dark:text-white">
              {{ sprint.name }}
            </h4>
            <div
              class="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400 mt-1"
            >
              <span
                >{{ formatDate(sprint.start_date) }} -
                {{ formatDate(sprint.end_date) }}</span
              >
              <span class="flex items-center">
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
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
                {{ getTasksInSprint(sprint.id).length }} tarefas
              </span>
            </div>
          </div>
          <div class="flex space-x-2">
            <Button
              variant="ghost"
              size="icon-sm"
              @click="editSprint(sprint)"
              title="Editar Sprint"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
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
              @click="confirmDeleteSprint(sprint.id)"
              title="Excluir Sprint"
              class="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
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

        <div class="sprint-content grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Tarefas na Sprint -->
          <div class="sprint-tasks bg-white dark:bg-gray-700 p-3 rounded-lg">
            <div
              class="flex justify-between items-center mb-3 pb-2 border-b border-gray-200 dark:border-gray-600"
            >
              <h5 class="text-sm font-medium text-gray-700 dark:text-gray-300">
                Tarefas na Sprint
              </h5>
              <span
                class="bg-blue-200 text-blue-700 dark:bg-blue-900 dark:text-blue-300 text-xs px-2 py-1 rounded-full"
              >
                {{ getTasksInSprint(sprint.id).length }}
              </span>
            </div>
            <draggable
              v-model="sprintTasksMap[sprint.id]"
              group="tasks"
              item-key="id"
              class="min-h-[100px] space-y-2"
              @start="drag = true"
              @end="handleDragEnd($event, sprint.id)"
              :animation="200"
              ghost-class="ghost-card"
            >
              <template #item="{ element }">
                <div
                  class="task-card bg-gray-50 dark:bg-gray-800 p-2 rounded shadow-sm hover:shadow-md cursor-move"
                >
                  <div class="task-header flex justify-between items-start">
                    <h6
                      class="font-medium text-gray-800 dark:text-white text-sm"
                    >
                      {{ element.name }}
                    </h6>
                    <span
                      :class="getStatusClass(element.status)"
                      class="text-xs px-1.5 py-0.5 rounded-full"
                    >
                      {{ element.status }}
                    </span>
                  </div>
                  <p
                    class="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-1"
                  >
                    {{ element.description }}
                  </p>
                </div>
              </template>
              <template #footer v-if="getTasksInSprint(sprint.id).length === 0">
                <div
                  class="text-center text-gray-500 dark:text-gray-400 py-4 text-xs"
                >
                  Arraste tarefas para esta sprint
                </div>
              </template>
            </draggable>
          </div>

          <!-- Tarefas disponíveis -->
          <div class="available-tasks bg-white dark:bg-gray-700 p-3 rounded-lg">
            <div
              class="flex justify-between items-center mb-3 pb-2 border-b border-gray-200 dark:border-gray-600"
            >
              <h5 class="text-sm font-medium text-gray-700 dark:text-gray-300">
                Tarefas Disponíveis
              </h5>
              <span
                class="bg-gray-200 text-gray-700 dark:bg-gray-800 dark:text-gray-300 text-xs px-2 py-1 rounded-full"
              >
                {{ getAvailableTasks().length }}
              </span>
            </div>
            <draggable
              v-model="availableTasks"
              group="tasks"
              item-key="id"
              class="min-h-[100px] space-y-2"
              @start="drag = true"
              @end="handleDragEnd($event, null)"
              :animation="200"
              ghost-class="ghost-card"
            >
              <template #item="{ element }">
                <div
                  class="task-card bg-gray-50 dark:bg-gray-800 p-2 rounded shadow-sm hover:shadow-md cursor-move"
                >
                  <div class="task-header flex justify-between items-start">
                    <h6
                      class="font-medium text-gray-800 dark:text-white text-sm"
                    >
                      {{ element.name }}
                    </h6>
                    <span
                      :class="getStatusClass(element.status)"
                      class="text-xs px-1.5 py-0.5 rounded-full"
                    >
                      {{ element.status }}
                    </span>
                  </div>
                  <p
                    class="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-1"
                  >
                    {{ element.description }}
                  </p>
                </div>
              </template>
              <template #footer v-if="getAvailableTasks().length === 0">
                <div
                  class="text-center text-gray-500 dark:text-gray-400 py-4 text-xs"
                >
                  Todas as tarefas já estão atribuídas a sprints
                </div>
              </template>
            </draggable>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Criar/Editar Sprint -->
    <Modal
      :is-open="showCreateSprintModal || !!editingSprint"
      @close="closeSprintModal"
      :title="editingSprint ? 'Editar Sprint' : 'Criar Nova Sprint'"
    >
      <div class="space-y-4 p-4">
        <div class="form-group">
          <label
            for="sprint-name"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >Nome da Sprint</label
          >
          <input
            id="sprint-name"
            v-model="sprintForm.name"
            type="text"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            placeholder="Ex: Sprint 1 - MVP"
          />
        </div>
        <div class="form-group grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label
              for="start-date"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >Data de Início</label
            >
            <input
              id="start-date"
              v-model="sprintForm.start_date"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            />
          </div>
          <div>
            <label
              for="end-date"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
              >Data de Término</label
            >
            <input
              id="end-date"
              v-model="sprintForm.end_date"
              type="date"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            />
          </div>
        </div>
        <div class="form-group">
          <label
            for="sprint-goal"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
            >Objetivo da Sprint</label
          >
          <textarea
            id="sprint-goal"
            v-model="sprintForm.goal"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
            placeholder="Descreva o objetivo principal desta sprint"
          ></textarea>
        </div>
        <div class="form-actions flex justify-end space-x-3 pt-4">
          <Button variant="outline" @click="closeSprintModal">Cancelar</Button>
          <Button @click="saveSprint" :disabled="!isSprintFormValid">
            {{ editingSprint ? 'Atualizar Sprint' : 'Criar Sprint' }}
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, defineProps, defineEmits } from 'vue';
import { useTaskService } from '~/services/api/services/taskService';
import { useProjectService } from '~/services/api/services/projectService';
import { useNotification } from '~/composables/useNotification';
import draggable from 'vuedraggable';
import type { Tarefa } from '~/services/api/types';

const props = defineProps({
  projectId: {
    type: [Number, String],
    required: true,
  },
});

const emit = defineEmits(['sprintsUpdated']);

const taskService = useTaskService();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
  confirm,
} = useNotification();

// Estado
const sprints = ref<any[]>([]);
const allTasks = ref<Tarefa[]>([]);
const availableTasks = ref<Tarefa[]>([]);
const sprintTasksMap = ref<Record<number, Tarefa[]>>({});
const loading = ref(true);
const error = ref<Error | null>(null);
const drag = ref(false);
const showCreateSprintModal = ref(false);
const editingSprint = ref<any | null>(null);
const sprintForm = ref({
  name: '',
  start_date: '',
  end_date: '',
  goal: '',
  project: null as number | null,
});

// Validação do formulário
const isSprintFormValid = computed(() => {
  return (
    sprintForm.value.name.trim() !== '' &&
    sprintForm.value.start_date !== '' &&
    sprintForm.value.end_date !== ''
  );
});

// Funções auxiliares
function getTasksInSprint(sprintId: number) {
  return sprintTasksMap.value[sprintId] || [];
}

function getAvailableTasks() {
  return availableTasks.value;
}

function getStatusClass(status?: string) {
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
}

// Funções de gerenciamento de sprints
async function fetchSprints() {
  loading.value = true;
  error.value = null;

  try {
    const response = await projectService.listSprints({
      projeto: props.projectId,
      ordering: 'start_date',
    });

    sprints.value = response.results;

    // Inicializar o mapa de tarefas por sprint
    response.results.forEach((sprint) => {
      if (!sprintTasksMap.value[sprint.id]) {
        sprintTasksMap.value[sprint.id] = [];
      }
    });
  } catch (err: any) {
    error.value = err;
    console.error('Erro ao buscar sprints:', err);
    showApiError(err);
  } finally {
    loading.value = false;
  }
}

async function saveSprint() {
  savingForm.value = true;

  try {
    const { success: notifySuccess, showApiError } = useNotification();

    if (editingSprint.value) {
      // Atualizar sprint existente
      const updatedSprint = await projectService.updateSprint(
        editingSprint.value.id,
        {
          nome: sprintForm.value.name,
          descricao: sprintForm.value.goal,
          data_inicio: sprintForm.value.start_date,
          data_fim: sprintForm.value.end_date,
          projeto: props.projectId,
        }
      );

      // Atualizar localmente
      const sprintIndex = sprints.value.findIndex(
        (s) => s.id === editingSprint.value?.id
      );
      if (sprintIndex !== -1) {
        sprints.value[sprintIndex] = {
          ...updatedSprint,
          name: updatedSprint.nome,
          start_date: updatedSprint.data_inicio,
          end_date: updatedSprint.data_fim,
        };
      }

      notifySuccess('Sprint atualizada com sucesso!');
      emit('sprint-updated', updatedSprint);
    } else {
      // Criar nova sprint
      const newSprint = await projectService.createSprint({
        nome: sprintForm.value.name,
        descricao: sprintForm.value.goal,
        data_inicio: sprintForm.value.start_date,
        data_fim: sprintForm.value.end_date,
        projeto: props.projectId,
      });

      // Adicionar localmente
      sprints.value.push({
        ...newSprint,
        id: newSprint.id,
        name: newSprint.nome,
        start_date: newSprint.data_inicio,
        end_date: newSprint.data_fim,
        project: newSprint.projeto,
      });

      sprintTasksMap.value[newSprint.id] = [];
      notifySuccess('Sprint criada com sucesso!');
      emit('sprint-created', newSprint);
    }

    closeSprintModal();
  } catch (err: any) {
    showApiError(err, 'Erro ao salvar sprint');
    console.error('Erro ao salvar sprint:', err);
  } finally {
    savingForm.value = false;
  }
}

async function confirmDeleteSprint(sprintId: number) {
  const {
    confirm: confirmDialog,
    success: notifySuccess,
    showApiError,
  } = useNotification();

  // Confirmar exclusão
  const isConfirmed = await confirmDialog(
    'Excluir Sprint',
    'Tem certeza que deseja excluir esta sprint? Esta ação não pode ser desfeita e todas as tarefas associadas serão desvinculadas.',
    'Excluir',
    'Cancelar'
  );

  if (isConfirmed) {
    deletingSprint.value = sprintId;

    try {
      await projectService.destroySprint(sprintId);

      // Remover localmente
      sprints.value = sprints.value.filter((sprint) => sprint.id !== sprintId);

      // Limpar tarefas associadas
      if (sprintTasksMap.value[sprintId]) {
        // Mover tarefas de volta para disponíveis
        const tasksToMove = [...sprintTasksMap.value[sprintId]];
        availableTasks.value = [...availableTasks.value, ...tasksToMove];

        // Remover do mapa
        delete sprintTasksMap.value[sprintId];
      }

      notifySuccess('Sprint excluída com sucesso!');
      emit('sprint-deleted', sprintId);
    } catch (err: any) {
      showApiError(err, 'Erro ao excluir sprint');
      console.error('Erro ao excluir sprint:', err);
    } finally {
      deletingSprint.value = null;
    }
  }
}

async function handleDragEnd(evt: any, sprintId: number | null) {
  drag.value = false;

  // Se a tarefa foi movida entre listas diferentes
  if (evt.from !== evt.to) {
    updateAvailableTasks();

    // Em um ambiente real, você atualizaria a associação da tarefa com a sprint no backend
    // Exemplo:
    // const task = evt.item.__draggable_context.element
    // if (sprintId) {
    //   await taskService.associateWithSprint(task.id, sprintId)
    // } else {
    //   await taskService.removeFromSprint(task.id)
    // }

    notifySuccess('Tarefa movida com sucesso!');
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

// Carregar sprints quando o componente for montado ou o projectId mudar
watch(
  () => props.projectId,
  (newProjectId) => {
    if (newProjectId) {
      fetchSprints();
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

.task-card {
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-2px);
}

/* Estilo para limitar o texto em 1 linha */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
