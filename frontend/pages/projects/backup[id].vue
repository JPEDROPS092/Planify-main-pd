
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

const route = useRoute();
const router = useRouter();
const projectService = useProjectService();
const queryClient = useQueryClient();
const { toast } = useToast();

const projectId = computed(() => parseInt(route.params.id as string));
const activeTab = ref('overview');
const showEditModal = ref(false);

// Queries
const { data: project, isLoading: projectLoading, error: projectError } = useQuery({
  queryKey: ['project', projectId],
  queryFn: () => projectService.getProject(projectId.value),
  enabled: computed(() => !!projectId.value)
});

/*const { data: members, isLoading: membersLoading } = useQuery({
  queryKey: ['project-members', projectId],
  queryFn: () => projectService.getProjectMembers(projectId.value),
  enabled: computed(() => !!projectId.value && activeTab.value === 'members')
});*/

/*const { data: sprints, isLoading: sprintsLoading } = useQuery({
  queryKey: ['project-sprints', projectId],
  queryFn: () => projectService.getProjectSprints(projectId.value),
  enabled: computed(() => !!projectId.value && activeTab.value === 'sprints')
});*/

const { data: tasks, isLoading: tasksLoading } = useQuery({
  queryKey: ['project-tasks', projectId],
  queryFn: () => projectService.getProjectTasks(projectId.value),
  enabled: computed(() => !!projectId.value && activeTab.value === 'tasks')
});

const { data: kanban, isLoading: kanbanLoading } = useQuery({
  queryKey: ['project-kanban', projectId],
  queryFn: () => projectService.getProjectKanban(projectId.value),
  enabled: computed(() => !!projectId.value && activeTab.value === 'kanban')
});

/*const { data: gantt, isLoading: ganttLoading } = useQuery({
  queryKey: ['project-gantt', projectId],
  queryFn: () => projectService.getProjectGantt(projectId.value),
  enabled: computed(() => !!projectId.value && activeTab.value === 'gantt')
});*/

const { data: metrics, isLoading: metricsLoading } = useQuery({
  queryKey: ['project-metrics', projectId],
  queryFn: () => projectService.getProjectMetrics(projectId.value),
  enabled: computed(() => !!projectId.value && activeTab.value === 'metrics')
});

// Mutations
const updateProjectMutation = useMutation({
  mutationFn: (data: ProjetoRequest) => projectService.updateProject(projectId.value, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['project', projectId] });
    toast.success('Projeto atualizado com sucesso!');
    showEditModal.value = false;
  },
  onError: (error: any) => {
    console.error('Erro ao atualizar projeto:', error);
    toast.error('Erro ao atualizar projeto. Tente novamente.');
  }
});

const deleteProjectMutation = useMutation({
  mutationFn: () => projectService.deleteProject(projectId.value),
  onSuccess: () => {
    toast.success('Projeto excluído com sucesso!');
    router.push('/projects');
  },
  onError: (error: any) => {
    console.error('Erro ao excluir projeto:', error);
    toast.error('Erro ao excluir projeto. Tente novamente.');
  }
});

// Methods
const handleEdit = () => {
  showEditModal.value = true;
};

const handleDelete = () => {
  if (confirm('Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita.')) {
    deleteProjectMutation.mutate();
  }
};

const handleArchive = () => {
  if (!project.value) return;
  
  const data: ProjetoRequest = {
    titulo: project.value.titulo,
    descricao: project.value.descricao || '',
    data_inicio: project.value.data_inicio,
    data_fim: project.value.data_fim,
    status: project.value.status,
    prioridade: project.value.prioridade,
    arquivado: !project.value.arquivado
  };
  
  updateProjectMutation.mutate(data);
};

const exportProject = async (format: 'pdf' | 'excel') => {
  try {
    const blob = await projectService.exportProject(projectId.value, format);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `projeto-${project.value?.titulo}-${format}.${format === 'pdf' ? 'pdf' : 'xlsx'}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
    toast.success(`Projeto exportado em ${format.toUpperCase()} com sucesso!`);
  } catch (error) {
    console.error('Erro ao exportar projeto:', error);
    toast.error('Erro ao exportar projeto. Tente novamente.');
  }
};

// Computed
const statusColor = computed(() => {
  if (!project.value) return 'gray';
  switch (project.value.status) {
    case 'CONCLUIDO': return 'green';
    case 'EM_ANDAMENTO': return 'blue';
    case 'PAUSADO': return 'yellow';
    case 'CANCELADO': return 'red';
    default: return 'gray';
  }
});

const priorityColor = computed(() => {
  if (!project.value) return 'gray';
  switch (project.value.prioridade) {
    case 'CRITICA': return 'red';
    case 'ALTA': return 'orange';
    case 'MEDIA': return 'yellow';
    case 'BAIXA': return 'green';
    default: return 'gray';
  }
});

const progressPercentage = computed(() => {
  if (!tasks.value?.results) return 0;
  const totalTasks = tasks.value.results.length;
  if (totalTasks === 0) return 0;
  const completedTasks = tasks.value.results.filter(task => task.status === 'CONCLUIDA').length;
  return Math.round((completedTasks / totalTasks) * 100);
});

const tabs = [
  { id: 'overview', name: 'Visão Geral', icon: 'lucide:layout-dashboard' },
  { id: 'members', name: 'Membros', icon: 'lucide:users' },
  { id: 'sprints', name: 'Sprints', icon: 'lucide:zap' },
  { id: 'tasks', name: 'Tarefas', icon: 'lucide:check-square' },
  { id: 'kanban', name: 'Kanban', icon: 'lucide:layout-kanban' },
  { id: 'gantt', name: 'Gantt', icon: 'lucide:gantt-chart' },
  { id: 'metrics', name: 'Métricas', icon: 'lucide:bar-chart-3' }
];
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Loading -->
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
                <button
                  @click="router.push('/projects')"
                  class="text-gray-400 hover:text-gray-600"
                >
                  <Icon icon="lucide:arrow-left" class="h-5 w-5" />
                </button>
                <div>
                  <h1 class="text-2xl font-bold text-gray-900">{{ project.titulo }}</h1>
                  <p class="text-sm text-gray-500 mt-1">{{ project.descricao || 'Sem descrição' }}</p>
                </div>
              </div>
              
              <div class="flex items-center space-x-2">
                <!-- Status Badge -->
                <span 
                  :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${statusColor}-100 text-${statusColor}-800`"
                >
                  {{ project.status_display }}
                </span>
                
                <!-- Priority Badge -->
                <span 
                  :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${priorityColor}-100 text-${priorityColor}-800`"
                >
                  {{ project.prioridade_display }}
                </span>
                
                <!-- Actions -->
                <div class="flex items-center space-x-1">
                  <button
                    @click="handleEdit"
                    class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100"
                    title="Editar projeto"
                  >
                    <Icon icon="lucide:edit" class="h-4 w-4" />
                  </button>
                  
                  <button
                    @click="handleArchive"
                    class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100"
                    :title="project.arquivado ? 'Desarquivar projeto' : 'Arquivar projeto'"
                  >
                    <Icon :icon="project.arquivado ? 'lucide:archive-restore' : 'lucide:archive'" class="h-4 w-4" />
                  </button>
                  
                  <!-- Export Dropdown -->
                  <div class="relative group">
                    <button class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100">
                      <Icon icon="lucide:download" class="h-4 w-4" />
                    </button>
                    <div class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
                      <div class="py-1">
                        <button
                          @click="exportProject('pdf')"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          <Icon icon="lucide:file-text" class="h-4 w-4 inline mr-2" />
                          Exportar PDF
                        </button>
                        <button
                          @click="exportProject('excel')"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                          <Icon icon="lucide:file-spreadsheet" class="h-4 w-4 inline mr-2" />
                          Exportar Excel
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <button
                    @click="handleDelete"
                    class="p-2 text-red-400 hover:text-red-600 rounded-md hover:bg-red-50"
                    title="Excluir projeto"
                  >
                    <Icon icon="lucide:trash-2" class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Project Info -->
            <div class="mt-4 grid grid-cols-1 sm:grid-cols-4 gap-4">
              <div class="flex items-center text-sm text-gray-500">
                <Icon icon="lucide:calendar" class="h-4 w-4 mr-2" />
                <span>Início: {{ new Date(project.data_inicio).toLocaleDateString('pt-BR') }}</span>
              </div>
              <div class="flex items-center text-sm text-gray-500">
                <Icon icon="lucide:flag" class="h-4 w-4 mr-2" />
                <span>Fim: {{ new Date(project.data_fim).toLocaleDateString('pt-BR') }}</span>
              </div>
              <div class="flex items-center text-sm text-gray-500">
                <Icon icon="lucide:clock" class="h-4 w-4 mr-2" />
                <span>Criado: {{ new Date(project.data_criacao).toLocaleDateString('pt-BR') }}</span>
              </div>
              <div class="flex items-center text-sm text-gray-500">
                <Icon icon="lucide:trending-up" class="h-4 w-4 mr-2" />
                <span>Progresso: {{ progressPercentage }}%</span>
              </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="mt-4">
              <div class="flex items-center justify-between text-sm text-gray-600 mb-1">
                <span>Progresso do Projeto</span>
                <span>{{ progressPercentage }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-primary h-2 rounded-full transition-all duration-300"
                  :style="`width: ${progressPercentage}%`"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="bg-white shadow rounded-lg">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8 px-6" aria-label="Tabs">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2',
                  activeTab === tab.id
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                <Icon :icon="tab.icon" class="h-4 w-4" />
                <span>{{ tab.name }}</span>
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="p-6">
            <!-- Overview Tab -->
            <div v-if="activeTab === 'overview'" class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Stats Cards -->
                <div class="bg-blue-50 rounded-lg p-4">
                  <div class="flex items-center">
                    <Icon icon="lucide:check-square" class="h-8 w-8 text-blue-600" />
                    <div class="ml-3">
                      <p class="text-sm font-medium text-blue-600">Tarefas</p>
                      <p class="text-2xl font-bold text-blue-900">{{ tasks?.count || 0 }}</p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-green-50 rounded-lg p-4">
                  <div class="flex items-center">
                    <Icon icon="lucide:users" class="h-8 w-8 text-green-600" />
                    <div class="ml-3">
                      <p class="text-sm font-medium text-green-600">Membros</p>
                      <p class="text-2xl font-bold text-green-900">{{ project?.membros.count || 0 }}</p>
                    </div>
                  </div>
                </div>
                <!--
                <div class="bg-purple-50 rounded-lg p-4">
                  <div class="flex items-center">
                    <Icon icon="lucide:zap" class="h-8 w-8 text-purple-600" />
                    <div class="ml-3">
                      <p class="text-sm font-medium text-purple-600">Sprints</p>
                      <p class="text-2xl font-bold text-purple-900">{{ sprints?.count || 0 }}</p>
                    </div>
                  </div>
                </div>
                -->
              </div>
              
              <!-- Recent Activity -->
              <div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">Atividade Recente</h3>
                <div class="bg-gray-50 rounded-lg p-4">
                  <p class="text-gray-500 text-center">Nenhuma atividade recente</p>
                </div>
              </div>
            </div>

            <!-- Members Tab -->
            <div v-else-if="activeTab === 'members'">
              <div v-if="membersLoading" class="flex justify-center py-8">
                <Icon icon="lucide:loader-2" class="h-6 w-6 animate-spin text-primary" />
              </div>
              <div v-else-if="members?.results?.length">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div
                    v-for="member in members.results"
                    :key="member.id"
                    class="bg-gray-50 rounded-lg p-4 flex items-center space-x-3"
                  >
                    <div class="flex-shrink-0">
                      <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                        <span class="text-white font-medium">
                          {{ member.usuario?.first_name?.charAt(0) || 'U' }}
                        </span>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900">
                        {{ member.usuario?.first_name }} {{ member.usuario?.last_name }}
                      </p>
                      <p class="text-sm text-gray-500">{{ member.funcao }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8">
                <Icon icon="lucide:users" class="mx-auto h-12 w-12 text-gray-400" />
                <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhum membro</h3>
                <p class="mt-1 text-sm text-gray-500">Este projeto ainda não possui membros.</p>
              </div>
            </div>

            <!-- Tasks Tab -->
            <div v-else-if="activeTab === 'tasks'">
              <div v-if="tasksLoading" class="flex justify-center py-8">
                <Icon icon="lucide:loader-2" class="h-6 w-6 animate-spin text-primary" />
              </div>
              <div v-else-if="tasks?.results?.length">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div
                    v-for="task in tasks.results"
                    :key="task.id"
                    class="bg-gray-50 rounded-lg p-4 flex items-center space-x-3"
                  >
                    <div class="flex-shrink-0">
                      <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                        <span class="text-white font-medium">
                          {{ task.titulo.charAt(0) || 'T' }}
                        </span>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900">
                        {{ task.titulo }}
                      </p>
                      <p class="text-sm text-gray-500">{{ task.descricao }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8">
                <Icon icon="lucide:check-square" class="mx-auto h-12 w-12 text-gray-400" />
                <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhuma tarefa</h3>
                <p class="mt-1 text-sm text-gray-500">Este projeto ainda não possui tarefas.</p>
              </div>
            </div>

            <!-- Sprints Tab -->
            <div v-else-if="activeTab === 'sprints'">
              <div v-if="sprintsLoading" class="flex justify-center py-8">
                <Icon icon="lucide:loader-2" class="h-6 w-6 animate-spin text-primary" />
              </div>
              <div v-else-if="sprints?.results?.length">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div
                    v-for="sprint in sprints.results"
                    :key="sprint.id"
                    class="bg-gray-50 rounded-lg p-4 flex items-center space-x-3"
                  >
                    <div class="flex-shrink-0">
                      <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                        <span class="text-white font-medium">
                          {{ sprint.nome.charAt(0) || 'S' }}
                        </span>
                      </div>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900">
                        {{ sprint.nome }}
                      </p>
                      <p class="text-sm text-gray-500">{{ sprint.descricao }}</p>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8">
                <Icon icon="lucide:zap" class="mx-auto h-12 w-12 text-gray-400" />
                <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhuma sprint</h3>
                <p class="mt-1 text-sm text-gray-500">Este projeto ainda não possui sprints.</p>
              </div>
            </div>

            <!-- Kanban Tab -->
            <div v-else-if="activeTab === 'kanban'">
              <div v-if="kanbanLoading" class="flex justify-center py-8">
                <Icon icon="lucide:loader-2" class="h-6 w-6 animate-spin text-primary" />
              </div>
              <div v-else>
                <!-- Kanban Board -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">To-Do</h3>
                    <div class="space-y-4">
                      <div
                        v-for="task in kanban.toDo"
                        :key="task.id"
                        class="bg-white rounded-lg p-4 flex items-center space-x-3"
                      >
                        <div class="flex-shrink-0">
                          <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                            <span class="text-white font-medium">
                              {{ task.titulo.charAt(0) || 'T' }}
                            </span>
                          </div>
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900">
                            {{ task.titulo }}
                          </p>
                          <p class="text-sm text-gray-500">{{ task.descricao }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">In Progress</h3>
                    <div class="space-y-4">
                      <div
                        v-for="task in kanban.inProgress"
                        :key="task.id"
                        class="bg-white rounded-lg p-4 flex items-center space-x-3"
                      >
                        <div class="flex-shrink-0">
                          <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                            <span class="text-white font-medium">
                              {{ task.titulo.charAt(0) || 'T' }}
                            </span>
                          </div>
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900">
                            {{ task.titulo }}
                          </p>
                          <p class="text-sm text-gray-500">{{ task.descricao }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="text-lg font-medium text-gray-900 mb-4">Done</h3>
                    <div class="space-y-4">
                      <div
                        v-for="task in kanban.done"
                        :key="task.id"
                        class="bg-white rounded-lg p-4 flex items-center space-x-3"
                      >
                        <div class="flex-shrink-0">
                          <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                            <span class="text-white font-medium">
                              {{ task.titulo.charAt(0) || 'T' }}
                            </span>
                          </div>
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900">
                            {{ task.titulo }}
                          </p>
                          <p class="text-sm text-gray-500">{{ task.descricao }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Gantt Tab -->
            <div v-else-if="activeTab === 'gantt'">
              <div v-if="ganttLoading" class="flex justify-center py-8">
                <Icon icon="lucide:loader-2" class="h-6 w-6 animate-spin text-primary" />
              </div>
              <div v-else>
                <!-- Gantt Chart -->
                <div class="bg-gray-50 rounded-lg p-4">
                  <h3 class="text-lg font-medium text-gray-900 mb-4">Gantt Chart</h3>
                  <div class="space-y-4">
                    <div
                      v-for="task in gantt"
                      :key="task.id"
                      class="bg-white rounded-lg p-4 flex items-center space-x-3"
                    >
                      <div class="flex-shrink-0">
                        <div class="h-10 w-10 bg-primary rounded-full flex items-center justify-center">
                          <span class="text-white font-medium">
                            {{ task.titulo.charAt(0) || 'T' }}
                          </span>
                        </div>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900">
                          {{ task.titulo }}
                        </p>
                        <p class="text-sm text-gray-500">{{ task.descricao }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Metrics Tab -->
            <div v-else-if="activeTab === 'metrics'">
              <div v-if="metricsLoading" class="flex justify-center py-8">
                <Icon icon="lucide:loader-2" class="h-6 w-6 animate-spin text-primary" />
              </div>
              <div v-else>
                <!-- Metrics Cards -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div class="bg-blue-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <Icon icon="lucide:check-square" class="h-8 w-8 text-blue-600" />
                      <div class="ml-3">
                        <p class="text-sm font-medium text-blue-600">Tarefas</p>
                        <p class="text-2xl font-bold text-blue-900">{{ metrics.tarefas }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="bg-green-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <Icon icon="lucide:users" class="h-8 w-8 text-green-600" />
                      <div class="ml-3">
                        <p class="text-sm font-medium text-green-600">Membros</p>
                        <p class="text-2xl font-bold text-green-900">{{ metrics.membros }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="bg-purple-50 rounded-lg p-4">
                    <div class="flex items-center">
                      <Icon icon="lucide:zap" class="h-8 w-8 text-purple-600" />
                      <div class="ml-3">
                        <p class="text-sm font-medium text-purple-600">Sprints</p>
                        <p class="text-2xl font-bold text-purple-900">{{ metrics.sprints }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Other tabs content would go here -->
            <div v-else class="text-center py-8">
              <Icon icon="lucide:construction" class="mx-auto h-12 w-12 text-gray-400" />
              <h3 class="mt-2 text-sm font-medium text-gray-900">Em desenvolvimento</h3>
              <p class="mt-1 text-sm text-gray-500">Esta seção está sendo desenvolvida.</p>
            </div>
          </div>
        </div>

        <!-- Edit Modal -->
        <ProjectModal
          :show="showEditModal"
          :project="project"
          :loading="updateProjectMutation.isLoading.value"
          @close="showEditModal = false"
          @submit="updateProjectMutation.mutate"
        />
      </div>
    </div>
  </div>
</template>