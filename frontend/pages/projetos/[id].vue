<template>
  <div class="container mx-auto p-4 md:p-6">
    <div v-if="loadingProject" class="flex justify-center items-center h-64">
      <SkeletonLoader type="article" :count="3" />
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
    <div v-else-if="project" class="space-y-8">
      <!-- Cabeçalho do Projeto com Ações Rápidas -->
      <header class="pb-6 border-b border-gray-200 dark:border-gray-700">
        <div
          class="flex flex-col md:flex-row justify-between items-start md:items-center"
        >
          <div>
            <h1
              class="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white mb-2"
            >
              {{ project.nome }}
            </h1>
            <p class="text-gray-600 dark:text-gray-400 text-lg">
              {{ project.descricao }}
            </p>
          </div>
          <div class="mt-4 md:mt-0 flex flex-wrap space-x-2">
            <Button variant="outline" @click="navigateToEditProject">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 mr-2"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z"
                />
                <path
                  fill-rule="evenodd"
                  d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"
                  clip-rule="evenodd"
                />
              </svg>
              Editar
            </Button>
            <Button variant="primary">
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
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              Exportar
            </Button>
          </div>
        </div>
      </header>

      <!-- Dashboard do Projeto -->
      <ProjectDashboard :project-id="projectId" />
    </div>
    <div v-else class="text-center text-gray-500 dark:text-gray-400 py-10">
      <p>Nenhum projeto encontrado com este ID.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProjectService } from '~/services/api/services/projectService';
import { useNotification } from '~/composables/useNotification';
import { useAuth } from '~/composables/useAuth';
import type { Projeto } from '~/services/api/types';
import Button from '~/components/ui/Button.vue';
import SkeletonLoader from '~/components/SkeletonLoader.vue';
import ProjectDashboard from '~/components/project/ProjectDashboard.vue';

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'], // Adicionando middleware de autenticação
});

const route = useRoute();
const router = useRouter();
const projectService = useProjectService();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
} = useNotification();

const { isAuthenticated } = useAuth();
const projectId = computed(() => Number(route.params.id));
const project = ref<Projeto | null>(null);
const loadingProject = ref(true);
const projectError = ref<Error | null>(null);

async function fetchProjectDetails() {
  if (!projectId.value) return;

  loadingProject.value = true;
  projectError.value = null;

  try {
    // Verificar autenticação antes de carregar
    if (!isAuthenticated.value) {
      return router.push('/login');
    }

    project.value = await projectService.retrieveProjeto(
      Number(projectId.value)
    );
  } catch (err: any) {
    projectError.value = err;
    console.error('Erro ao buscar detalhes do projeto:', err);
    showApiError(err, 'Erro ao carregar detalhes do projeto');
  } finally {
    loadingProject.value = false;
  }
}

function navigateToEditProject() {
  router.push(`/projetos/editar/${projectId.value}`);
}

function navigateToKanbanView() {
  router.push(`/projetos/${projectId.value}/kanban`);
}

function navigateToGanttView() {
  router.push(`/projetos/${projectId.value}/gantt`);
}

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};

const formatCurrency = (value?: number) => {
  if (value === undefined || value === null) return 'N/A';
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

function getStatusClass(status: string) {
  switch (status) {
    case 'PLANEJADO':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    case 'EM_ANDAMENTO':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    case 'PAUSADO':
      return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
    case 'CONCLUIDO':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    case 'CANCELADO':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
  }
}

function getStatusText(status: string) {
  switch (status) {
    case 'PLANEJADO':
      return 'Planejado';
    case 'EM_ANDAMENTO':
      return 'Em Andamento';
    case 'PAUSADO':
      return 'Pausado';
    case 'CONCLUIDO':
      return 'Concluído';
    case 'CANCELADO':
      return 'Cancelado';
    default:
      return status;
  }
}

function getPriorityClass(priority: string) {
  switch (priority) {
    case 'BAIXA':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    case 'MEDIA':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    case 'ALTA':
      return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300';
    case 'CRITICA':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300';
  }
}

function getPriorityText(priority: string) {
  switch (priority) {
    case 'BAIXA':
      return 'Baixa';
    case 'MEDIA':
      return 'Média';
    case 'ALTA':
      return 'Alta';
    case 'CRITICA':
      return 'Crítica';
    default:
      return priority;
  }
}

onMounted(() => {
  fetchProjectDetails();
});

// Recarregar dados se o ID do projeto na rota mudar
watch(projectId, (newId, oldId) => {
  if (newId !== oldId && newId) {
    fetchProjectDetails();
  }
});
</script>

<style scoped>
/* Estilos adicionais podem ser adicionados aqui, se necessário */
</style>
