<template>
  <div class="container mx-auto px-4 py-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <p class="mt-2 text-gray-600 dark:text-gray-300">
        Bem-vindo ao seu painel de controle do Planify
      </p>
    </div>

    <!-- Cards de resumo -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
      <MetricsCard
        v-for="(card, index) in summaryCards"
        :key="index"
        :title="card.title"
        :value="card.value"
        :description="card.description"
        :icon="card.icon"
        :icon-bg-color="card.bgColor"
        class="transition-all hover:shadow-lg"
      />
    </div>

    <!-- Projetos recentes -->
    <Card class="mb-8">
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle>Projetos Recentes</CardTitle>
          <NuxtLink
            to="/projetos"
            class="text-sm font-medium text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
          >
            Ver todos
          </NuxtLink>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="isLoading" class="py-4">
          <!-- Option 1: Simple spinner -->
          <div class="flex justify-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </div>
        <EmptyState
          v-else-if="recentProjects.length === 0"
          title="Nenhum projeto encontrado"
          message="Comece criando seu primeiro projeto para organizar suas tarefas."
          icon="FolderPlusIcon"
        >
          <template #actions>
            <RoleBasedContent :roles="['admin', 'manager']">
              <Button @click="isNewProjectModalOpen = true" variant="primary">
                Criar Projeto
              </Button>
            </RoleBasedContent>
          </template>
        </EmptyState>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Nome</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Progresso</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Data Limite</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="project in recentProjects" :key="project.id" class="hover:bg-gray-50 dark:hover:bg-gray-750">
                <td class="px-4 py-3 whitespace-nowrap">
                  <NuxtLink :to="`/projetos/${project.id}`" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
                    {{ project.nome }}
                  </NuxtLink>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <Badge :variant="getStatusVariant(project.status)">
                    {{ getStatusLabel(project.status) }}
                  </Badge>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <div class="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2.5">
                    <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${project.progresso || 0}%` }"></div>
                  </div>
                  <span class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ project.progresso || 0 }}%</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(project.data_termino) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>

    <!-- Tarefas pendentes -->
    <Card>
      <CardHeader>
        <div class="flex items-center justify-between">
          <CardTitle>Minhas Tarefas Pendentes</CardTitle>
          <NuxtLink
            to="/tarefas"
            class="text-sm font-medium text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
          >
            Ver todas
          </NuxtLink>
        </div>
      </CardHeader>
      <CardContent>
        <div v-if="isLoadingTasks" class="py-4">
          <div class="flex justify-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </div>
        <EmptyState
          v-else-if="pendingTasks.length === 0"
          title="Nenhuma tarefa pendente"
          message="Você está em dia! Crie novas tarefas para continuar produtivo."
          icon="CheckCircleIcon"
        >
          <template #actions>
            <Button @click="isNewTaskModalOpen = true" variant="primary">
              Criar Tarefa
            </Button>
          </template>
        </EmptyState>
        <div v-else>
          <ul class="divide-y divide-gray-200 dark:divide-gray-700">
            <li v-for="task in pendingTasks" :key="task.id" class="py-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <Badge :variant="getPriorityVariant(task.prioridade)" type="dot" class="mr-3" />
                  <NuxtLink :to="`/tarefas/${task.id}`" class="text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400">
                    {{ task.titulo }}
                  </NuxtLink>
                </div>
                <div class="flex items-center">
                  <span class="text-sm text-gray-500 dark:text-gray-400 mr-4">{{ formatDate(task.data_termino) }}</span>
                  <Badge :variant="getStatusVariant(task.status)">
                    {{ getStatusLabel(task.status) }}
                  </Badge>
                </div>
              </div>
              <p v-if="task.projeto" class="mt-1 text-sm text-gray-500 dark:text-gray-400 ml-5">
                Projeto:
                <NuxtLink :to="`/projetos/${task.projeto.id}`" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">
                  {{ task.projeto.nome }}
                </NuxtLink>
              </p>
            </li>
          </ul>
        </div>
      </CardContent>
    </Card>

    <!-- Modal para Novo Projeto -->
    <Modal :is-open="isNewProjectModalOpen" @close="isNewProjectModalOpen = false" title="Criar Novo Projeto">
      <ProjectForm @submit="handleProjectSubmit" :is-loading="isProjectFormLoading" @cancel="isNewProjectModalOpen = false"/>
    </Modal>

    <!-- Modal para Nova Tarefa -->
    <Modal :is-open="isNewTaskModalOpen" @close="isNewTaskModalOpen = false" title="Criar Nova Tarefa">
      <TaskForm @submit="handleTaskSubmit" :is-loading="isTaskFormLoading" @cancel="isNewTaskModalOpen = false" :projects="recentProjectsForTaskForm"/>
    </Modal>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useProjectService } from '~/services/api/services/projectService';
import { useTaskService } from '~/services/api/services/taskService';
import { useNotification } from '~/stores/composables/useNotification';
import { useAuth } from '~/stores/composables/useAuth';
import RoleBasedContent from '~/components/shared/RoleBasedContent.vue';

// Import your custom components
import Card from '~/components/ui/display/card/Card.vue';
import CardHeader from '~/components/ui/display/card/CardHeader.vue';
import CardTitle from '~/components/ui/display/card/CardTitle.vue';
import CardContent from '~/components/ui/display/card/CardContent.vue';
import MetricsCard from '~/components/ui/feedback/metrics-card/MetricsCard.vue';
import Button from '~/components/ui/input/button/Button.vue';
import Badge from '~/components/ui/feedback/badge/Badge.vue';
import EmptyState from '~/components/shared/data/empty-state/EmptyState.vue';
import Modal from '~/components/ui/display/Modal.vue';
import ProjectForm from '~/components/shared/forms/project/ProjectForm.vue';
import TaskForm from '~/components/business/project/tasks/TaskForm.vue';

// Serviços
const projectService = useProjectService();
const taskService = useTaskService();
const notification = useNotification();
const auth = useAuth();

// Estado
const isLoading = ref(false);
const isLoadingTasks = ref(false);
const recentProjects = ref([]);
const pendingTasks = ref([]);
const isNewProjectModalOpen = ref(false);
const isNewTaskModalOpen = ref(false);
const isProjectFormLoading = ref(false);
const isTaskFormLoading = ref(false);

// Permissões baseadas em papel
const userRole = computed(() => auth.user?.role || 'viewer');
const userCanCreate = computed(() => ['admin', 'manager'].includes(userRole.value));
const userCanEdit = computed(() => ['admin', 'manager', 'editor'].includes(userRole.value));
const userCanDelete = computed(() => ['admin', 'manager'].includes(userRole.value));

// Cards de resumo
const summaryCards = ref([
  {
    title: 'Total de Projetos',
    value: '0',
    description: 'Ativos',
    icon: 'FolderIcon',
    bgColor: 'bg-blue-500',
  },
  {
    title: 'Tarefas Pendentes',
    value: '0',
    description: 'Atribuídas a você',
    icon: 'ClipboardCheckIcon',
    bgColor: 'bg-amber-500',
  },
  {
    title: 'Projetos Concluídos',
    value: '0',
    description: 'Este mês',
    icon: 'CheckCircleIcon',
    bgColor: 'bg-green-500',
  },
  {
    title: 'Riscos Ativos',
    value: '0',
    description: 'Requerem atenção',
    icon: 'ExclamationTriangleIcon',
    bgColor: 'bg-red-500',
  },
]);

// Computed para projetos disponíveis no formulário de tarefas
const recentProjectsForTaskForm = computed(() => {
  return recentProjects.value.map(project => ({
    id: project.id,
    nome: project.nome
  }));
});

// Métodos
async function fetchRecentProjects() {
  isLoading.value = true;
  try {
    const response = await projectService.getProjects({
      limit: 5,
      sort: '-data_criacao'
    });
    
    recentProjects.value = response.results || [];
    
    // Atualiza o card de resumo
    summaryCards.value[0].value = response.count?.toString() || '0';
    
    // Busca projetos concluídos este mês para o card de resumo
    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    
    const completedResponse = await projectService.getProjects({
      status: 'CONCLUIDO',
      data_termino_after: firstDayOfMonth.toISOString().split('T')[0]
    });
    
    summaryCards.value[2].value = completedResponse.count?.toString() || '0';
  } catch (error) {
    console.error('Erro ao buscar projetos recentes:', error);
  } finally {
    isLoading.value = false;
  }
}

async function fetchDashboardTaskStats() {
  try {
    // Busca estatísticas de tarefas para o card de resumo
    const response = await taskService.getTaskStats();
    
    if (response) {
      // Atualiza o card de tarefas pendentes
      const pendingCount = response.pending_tasks_count || 0;
      summaryCards.value[1].value = pendingCount.toString();
      
      // Atualiza o card de riscos, se a API retornar essa informação
      if (response.active_risks_count !== undefined) {
        summaryCards.value[3].value = response.active_risks_count.toString();
      }
    }
  } catch (error) {
    console.error('Erro ao buscar estatísticas de tarefas:', error);
  }
}

async function fetchPendingTasksList() {
  isLoadingTasks.value = true;
  try {
    const response = await taskService.getTasks({
      status__in: 'PENDENTE,EM_ANDAMENTO',
      responsavel: auth.user?.id,
      limit: 5,
      sort: 'data_termino'
    });
    
    pendingTasks.value = response.results || [];
  } catch (error) {
    console.error('Erro ao buscar tarefas pendentes:', error);
  } finally {
    isLoadingTasks.value = false;
  }
}

function formatDate(dateString?: string): string {
  if (!dateString) return 'N/A';
  
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date);
}

// Updated to return variant names for <Badge>
function getStatusVariant(status: string): string {
  switch (status?.toUpperCase()) {
    case 'CONCLUIDO':
      return 'success';
    case 'EM_ANDAMENTO':
      return 'info';
    case 'PENDENTE':
      return 'warning';
    case 'CANCELADO':
      return 'danger';
    case 'BLOQUEADO':
      return 'danger';
    default:
      return 'secondary';
  }
}

function getStatusLabel(status: string): string {
  switch (status?.toUpperCase()) {
    case 'CONCLUIDO':
      return 'Concluído';
    case 'EM_ANDAMENTO':
      return 'Em Andamento';
    case 'PENDENTE':
      return 'Pendente';
    case 'CANCELADO':
      return 'Cancelado';
    case 'BLOQUEADO':
      return 'Bloqueado';
    default:
      return status || 'Desconhecido';
  }
}

// For the priority dot badge
function getPriorityVariant(priority: string): string {
  switch (priority?.toUpperCase()) {
    case 'ALTA':
      return 'danger';
    case 'MEDIA':
      return 'warning';
    case 'BAIXA':
      return 'success';
    default:
      return 'secondary';
  }
}

async function handleProjectSubmit(projectData: any) {
  if (!userCanCreate.value) {
    notification.error('Permissão negada', 'Você não tem permissão para criar projetos.');
    return;
  }

  isProjectFormLoading.value = true;
  try {
    await projectService.createProject(projectData);
    
    notification.success('Projeto criado', 'Projeto criado com sucesso!');
    isNewProjectModalOpen.value = false;
    
    // Recarrega os projetos para atualizar a lista
    await fetchRecentProjects();
  } catch (error) {
    console.error('Erro ao criar projeto:', error);
    notification.error(
      'Erro ao criar projeto', 
      error.response?.data?.detail || 'Ocorreu um erro ao criar o projeto. Tente novamente.'
    );
  } finally {
    isProjectFormLoading.value = false;
  }
}

async function handleTaskSubmit(taskData: any) {
  isTaskFormLoading.value = true;
  try {
    await taskService.createTask(taskData);
    
    notification.success('Tarefa criada', 'Tarefa criada com sucesso!');
    isNewTaskModalOpen.value = false;
    
    // Recarrega as tarefas para atualizar a lista
    await fetchPendingTasksList();
  } catch (error) {
    console.error('Erro ao criar tarefa:', error);
    notification.error(
      'Erro ao criar tarefa', 
      error.response?.data?.detail || 'Ocorreu um erro ao criar a tarefa. Tente novamente.'
    );
  } finally {
    isTaskFormLoading.value = false;
  }
}

// Lifecycle hooks
onMounted(async () => {
  if (auth.isAuthenticated) { // Ensure user is authenticated before fetching
    await Promise.all([
      fetchRecentProjects(),
      fetchDashboardTaskStats(),
      fetchPendingTasksList()
    ]);
  }
});
</script>
