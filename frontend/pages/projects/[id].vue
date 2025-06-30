<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { Projeto, ProjetoRequest, Membro, Sprint, Tarefa } from '~/api-types';
import ProjectModal from '~/components/ProjectModal.vue';
import { useTaskService } from '../../services';
import draggable from "vuedraggable"

const columns = ["A_FAZER", "EM_ANDAMENTO", "FEITO"];

const route = useRoute();
const router = useRouter();
const projectService = useProjectService();
const taskService = useTaskService();

const projectId = computed(() => parseInt(route.params.id as string));

const selectedSprint = ref<number | null>(null);

const sprintTasks = ref<Tarefa[] | null>(null);
const sprintTasksLoading = ref(false);
const sprintTasksError = ref<string | null>(null);

// Queries
const { data: project, isLoading: projectLoading, error: projectError } = useQuery({
  queryKey: ['project', projectId],
  queryFn: () => projectService.getProject(projectId.   value),
  enabled: computed(() => !!projectId.value)
});

const { data: sprints, isLoading: sprintsLoading, error: sprintsError } = useQuery({
  queryKey: ['project-sprints', projectId],
  queryFn: () => projectService.getProjectSprints(projectId.   value),
  enabled: computed(() => !!projectId.value)
});

async function handleSprintSelect(sprintId: number) {
  selectedSprint.value = sprintId;
  sprintTasks.value = null;
  sprintTasksError.value = null;
  sprintTasksLoading.value = true;
  
  try {
    console.log('Buscando tarefas da sprint', sprintId);
    const result = await taskService.getTasksBySprint(sprintId);
    console.log('Resultado da API:', result);
    sprintTasks.value = result.results;
  } catch (e: any) {
    sprintTasksError.value = 'Erro ao carregar tarefas da sprint';
    console.error(e);
  } finally {
    sprintTasksLoading.value = false;
    console.log('Finalizou loading');
  }
}

async function onTaskDrop(event: any, newStatus: string) {
  // O item movido está em event.added.element
  const tarefa = event?.added?.element;
  if (tarefa && tarefa.status !== newStatus) {
    const oldStatus = tarefa.status;
    tarefa.status = newStatus;
    const statusUpdate: {} = { status: newStatus, comentario: "Movido pelo Kanban" };
    try {
      await taskService.updateTaskStatus(tarefa.id, statusUpdate);
    } catch (e) {
      tarefa.status = oldStatus;
    }
  }
}

</script>

<template>
  <div class="p-6">
    <div v-if="projectLoading" class="flex justify-center items-center py-12">
      <Icon icon="lucide:loader-2" class="h-8 w-8 animate-spin text-primary" />
    </div>
    <!-- Error -->
    <div v-else-if="projectError" class="bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <Icon icon="lucide:alert-circle" class="h-5 w-5 text-red-400" />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">
            Erro ao carregar projeto
          </h3>
          <div class="mt-2 text-sm text-red-700">
            <p>Projeto não encontrado ou você não tem permissão para visualizá-lo.</p>
          </div>
          <div class="mt-4">
            <button
              @click="router.push('/projects')"
              class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200"
            >
              Voltar aos Projetos
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Project Content -->
    <div v-else-if="project">
      <!-- Header -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <h1 class="text-xl">{{ project?.titulo }}</h1>
              <!-- Lista de Sprints -->
              <div class=""></div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex gap-8 h-auto">
        <!-- Sprint Sidebar -->
        <aside class="min-w-64 bg-white shadow rounded-lg p-4 h-fit">
          <h2 class="text-lg font-semibold mb-4">Sprints</h2>
          <ul>
            <li
              v-for="sprint in sprints"
              :key="sprint.id"
              class="mb-2"
            >
              <div
                class="p-2 rounded hover:bg-gray-100 cursor-pointer"
                :class="{ 'bg-primary text-white': selectedSprint === sprint.id }"
                @click="handleSprintSelect(sprint.id)"
              >
                {{ sprint.nome }}
              </div>
            </li>
            <li v-if="!sprints?.length" class="text-gray-400 text-sm">
              Nenhuma sprint cadastrada.
            </li>
          </ul>
        </aside>

        <!-- Quadro Kanban? -->
        <div v-if="selectedSprint" class="flex-1 bg-white shadow rounded-lg p-4">
          <h2 class="text-lg font-semibold mb-4">Tarefas da Sprint</h2>
          <div v-if="sprintTasksLoading" class="text-gray-500">Carregando tarefas...</div>
          <div v-else-if="sprintTasksError" class="text-red-500">{{ sprintTasksError }}</div>
          <div v-else class="flex">
            <div
              v-for="coluna in columns"
              :key="coluna"
              class="grow"
            >
              <p class="font-bold border-b">{{ coluna }}</p>
              <draggable
                :list="sprintTasks?.filter(t => t.status === coluna) || []"
                :group="'tasks'"
                tag="ul"
                :itemKey="'id'"
                @change="event => onTaskDrop(event, coluna)"
              >
                <template #item="{ element: tarefa }">
                  <li>
                    <p class="font-bold">{{ tarefa.titulo }}</p>
                    <p>{{ tarefa.descricao }}</p>
                    <ul>
                      <li v-for="atribuicao in tarefa.atribuicoes" :key="atribuicao.id">
                        <p class="text-sm">{{ atribuicao.usuario_nome }}</p>
                      </li>
                    </ul>
                  </li>
                </template>
              </draggable>
              <div v-if="sprintTasks && sprintTasks.filter(t => t.status === coluna).length === 0" class="text-gray-400 text-sm mt-2">
                Nenhuma tarefa nesta coluna.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>