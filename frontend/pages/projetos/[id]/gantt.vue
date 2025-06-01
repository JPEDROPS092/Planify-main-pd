<template>
  <div class="container mx-auto p-4 md:p-6">
    <div v-if="loadingProject" class="flex justify-center items-center h-64">
      <SkeletonLoader type="article" :count="1" />
    </div>
    <div
      v-else-if="projectError"
      class="text-center text-red-500 dark:text-red-400 py-10"
    >
      <h2 class="text-2xl font-semibold mb-2">Erro ao Carregar Projeto</h2>
      <p>
        {{
          projectError.message ||
          'Não foi possível carregar os detalhes do projeto.'
        }}
      </p>
      <Button class="mt-4" @click="fetchProjectDetails"
        >Tentar Novamente</Button
      >
    </div>
    <div v-else-if="project" class="space-y-6">
      <!-- Cabeçalho do Projeto -->
      <header class="pb-4 border-b border-gray-200 dark:border-gray-700">
        <div
          class="flex flex-col md:flex-row justify-between items-start md:items-center"
        >
          <div>
            <div class="flex items-center mb-2">
              <Button
                variant="ghost"
                size="sm"
                @click="navigateToProject"
                class="mr-2"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                    clip-rule="evenodd"
                  />
                </svg>
              </Button>
              <h1
                class="text-2xl md:text-3xl font-bold text-gray-800 dark:text-white"
              >
                {{ project.name }}
              </h1>
            </div>
            <p class="text-gray-600 dark:text-gray-400">
              Gráfico Gantt - Visualização de Cronograma
            </p>
          </div>
          <div class="mt-4 md:mt-0 flex space-x-2">
            <Button variant="outline" @click="navigateToKanbanView">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 mr-2"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="9" y1="21" x2="9" y2="9"></line>
              </svg>
              Quadro Kanban
            </Button>
          </div>
        </div>
      </header>

      <!-- Visualização Gantt -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 md:p-6">
        <GanttChart :project-id="projectId" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProjectService } from '~/services/api/projects';
import { useNotification } from '~/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import SkeletonLoader from '~/components/SkeletonLoader.vue';
import GanttChart from '~/components/project/GanttChart.vue';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'], // Adicionando middleware de autenticação
});

const route = useRoute();
const router = useRouter();
const projectService = useProjectService();
const { showApiError } = useNotification();

const projectId = computed(() => Number(route.params.id));
const project = ref<any>(null);
const loadingProject = ref(true);
const projectError = ref<Error | null>(null);

async function fetchProjectDetails() {
  if (!projectId.value) {
    projectError.value = new Error('ID do projeto inválido.');
    loadingProject.value = false;
    return;
  }

  loadingProject.value = true;
  projectError.value = null;
  try {
    const fetchedProject = await projectService.retrieveProjeto(
      projectId.value
    );
    project.value = fetchedProject;
  } catch (error: any) {
    projectError.value = error;
    showApiError(error);
    project.value = null;
  } finally {
    loadingProject.value = false;
  }
}

function navigateToProject() {
  router.push(`/projetos/${projectId.value}`);
}

function navigateToKanbanView() {
  router.push(`/projetos/${projectId.value}/kanban`);
}

onMounted(() => {
  fetchProjectDetails();
});
</script>
