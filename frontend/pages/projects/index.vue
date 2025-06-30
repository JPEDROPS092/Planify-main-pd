<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { Projeto, ProjetoRequest } from '~/api-types';
import ProjectCard from '~/components/ProjectCard.vue';
import ProjectFilters from '~/components/ProjectFilters.vue';
import ProjectModal from '~/components/ProjectModal.vue';

const router = useRouter();
const projectService = useProjectService();
const queryClient = useQueryClient();
const { toast } = useToast();

// Estados
const currentPage = ref(1);
const showModal = ref(false);
const editingProject = ref<Projeto | undefined>();
const filters = ref({});
const viewMode = ref<'grid' | 'list'>('grid');

// Query para carregar projetos
const { data: projectsData, isLoading, error, refetch } = useQuery({
  queryKey: ['projects', currentPage, filters],
  queryFn: () => projectService.getProjects({
    page: currentPage.value,
    ...filters.value
  }),
  keepPreviousData: true
});

// Mutação para criar projeto
const createProjectMutation = useMutation({
  mutationFn: (project: ProjetoRequest) => projectService.createProject(project),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['projects'] });
    toast.success('Projeto criado com sucesso!');
    closeModal();
  },
  onError: (error: any) => {
    console.error('Erro ao criar projeto:', error);
    toast.error('Erro ao criar projeto. Tente novamente.');
  }
});

// Mutação para atualizar projeto
const updateProjectMutation = useMutation({
  mutationFn: ({ id, data }: { id: number; data: ProjetoRequest }) => 
    projectService.updateProject(id, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['projects'] });
    toast.success('Projeto atualizado com sucesso!');
    closeModal();
  },
  onError: (error: any) => {
    console.error('Erro ao atualizar projeto:', error);
    toast.error('Erro ao atualizar projeto. Tente novamente.');
  }
});

// Mutação para arquivar projeto
const archiveProjectMutation = useMutation({
  mutationFn: ({ id, data }: { id: number; data: ProjetoRequest }) => 
    projectService.archiveProject(id, data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['projects'] });
    toast.success('Status do projeto alterado com sucesso!');
  },
  onError: (error: any) => {
    console.error('Erro ao arquivar projeto:', error);
    toast.error('Erro ao alterar status do projeto.');
  }
});

// Mutação para excluir projeto
const deleteProjectMutation = useMutation({
  mutationFn: (id: number) => projectService.deleteProject(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['projects'] });
    toast.success('Projeto excluído com sucesso!');
  },
  onError: (error: any) => {
    console.error('Erro ao excluir projeto:', error);
    toast.error('Erro ao excluir projeto. Tente novamente.');
  }
});

// Computed
const projects = computed(() => projectsData.value?.results || []);
const totalPages = computed(() => {
  if (!projectsData.value?.count) return 1;
  return Math.ceil(projectsData.value.count / 20); // Assumindo 20 itens por página
});
const hasNextPage = computed(() => !!projectsData.value?.next);
const hasPrevPage = computed(() => !!projectsData.value?.previous);

// Métodos
const openCreateModal = () => {
  editingProject.value = undefined;
  showModal.value = true;
};

const openEditModal = (project: Projeto) => {
  editingProject.value = project;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingProject.value = undefined;
};

const handleSubmit = (data: ProjetoRequest) => {
  if (editingProject.value) {
    updateProjectMutation.mutate({ id: editingProject.value.id, data });
  } else {
    createProjectMutation.mutate(data);
  }
};

const handleArchive = (id: number) => {
  const project = projects.value.find(p => p.id === id);
  if (!project) return;
  
  const data: ProjetoRequest = {
    titulo: project.titulo,
    descricao: project.descricao || '',
    data_inicio: project.data_inicio,
    data_fim: project.data_fim,
    status: project.status,
    prioridade: project.prioridade,
    arquivado: !project.arquivado
  };
  
  archiveProjectMutation.mutate({ id, data });
};

const handleDelete = (id: number) => {
  if (confirm('Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita.')) {
    deleteProjectMutation.mutate(id);
  }
};

const nextPage = () => {
  if (hasNextPage.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (hasPrevPage.value) {
    currentPage.value--;
  }
};

const updateFilters = (newFilters: any) => {
  filters.value = newFilters;
  currentPage.value = 1; // Reset para primeira página
};

const isMutationLoading = computed(() => 
  createProjectMutation.isLoading.value || 
  updateProjectMutation.isLoading.value
);
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-2xl font-semibold text-gray-900">Projetos</h1>
          <p class="mt-1 text-sm text-gray-600">
            Gerencie todos os seus projetos
          </p>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Toggle de visualização -->
          <div class="flex items-center bg-gray-100 rounded-lg p-1">
            <button
              @click="viewMode = 'grid'"
              :class="[
                'p-2 rounded-md transition-colors',
                viewMode === 'grid' 
                  ? 'bg-white text-primary shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              <Icon icon="lucide:grid-3x3" class="h-4 w-4" />
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'p-2 rounded-md transition-colors',
                viewMode === 'list' 
                  ? 'bg-white text-primary shadow-sm' 
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              <Icon icon="lucide:list" class="h-4 w-4" />
            </button>
          </div>

          <!-- Botão novo projeto -->
          <button 
            @click="openCreateModal"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <Icon icon="lucide:plus" class="h-4 w-4 mr-2" />
            Novo Projeto
          </button>
        </div>
      </div>

      <!-- Filtros -->
      <ProjectFilters 
        :filters="filters" 
        @update:filters="updateFilters"
      />

      <!-- Loading -->
      <div v-if="isLoading && !projects.length" class="flex justify-center items-center py-12">
        <Icon icon="lucide:loader-2" class="h-8 w-8 animate-spin text-primary" />
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <Icon icon="lucide:alert-circle" class="h-5 w-5 text-red-400" />
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              Erro ao carregar projetos
            </h3>
            <div class="mt-2 text-sm text-red-700">
              <p>Ocorreu um erro ao carregar os projetos. Tente novamente.</p>
            </div>
            <div class="mt-4">
              <button
                @click="refetch()"
                class="bg-red-100 px-3 py-2 rounded-md text-sm font-medium text-red-800 hover:bg-red-200"
              >
                Tentar novamente
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de projetos -->
      <div v-else-if="projects.length > 0">
        <!-- Grid view -->
        <div 
          v-if="viewMode === 'grid'"
          class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
        >
          <ProjectCard
            v-for="project in projects"
            :key="project.id"
            :project="project"
            @edit="openEditModal"
            @archive="handleArchive"
            @delete="handleDelete"
          />
        </div>

        <!-- List view -->
        <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
          <ul class="divide-y divide-gray-200">
            <li v-for="project in projects" :key="project.id">
              <div class="px-4 py-4 flex items-center justify-between hover:bg-gray-50">
                <div class="flex items-center space-x-4">
                  <div class="flex-shrink-0">
                    <Icon 
                      icon="lucide:folder" 
                      class="h-8 w-8 text-gray-400"
                    />
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 truncate">
                      {{ project.titulo }}
                    </p>
                    <p class="text-sm text-gray-500 truncate">
                      {{ project.descricao || 'Sem descrição' }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span 
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    {{ project.status_display }}
                  </span>
                  <button
                    @click="router.push(`/projects/${project.id}`)"
                    class="text-primary hover:text-primary-700"
                  >
                    <Icon icon="lucide:arrow-right" class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- Paginação -->
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-6">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="prevPage"
              :disabled="!hasPrevPage"
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Anterior
            </button>
            <button
              @click="nextPage"
              :disabled="!hasNextPage"
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Próximo
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Mostrando página <span class="font-medium">{{ currentPage }}</span> de <span class="font-medium">{{ totalPages }}</span>
                <span v-if="projectsData?.count"> - Total: {{ projectsData.count }} projetos</span>
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button
                  @click="prevPage"
                  :disabled="!hasPrevPage"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon icon="lucide:chevron-left" class="h-5 w-5" />
                </button>
                <span class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                  {{ currentPage }}
                </span>
                <button
                  @click="nextPage"
                  :disabled="!hasNextPage"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Icon icon="lucide:chevron-right" class="h-5 w-5" />
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado vazio -->
      <div v-else class="text-center py-12">
        <Icon icon="lucide:folder" class="mx-auto h-12 w-12 text-gray-400" />
        <h3 class="mt-2 text-sm font-medium text-gray-900">Nenhum projeto encontrado</h3>
        <p class="mt-1 text-sm text-gray-500">Comece criando um novo projeto.</p>
        <div class="mt-6">
          <button
            @click="openCreateModal"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <Icon icon="lucide:plus" class="h-4 w-4 mr-2" />
            Novo Projeto
          </button>
        </div>
      </div>

      <!-- Modal -->
      <ProjectModal
        :show="showModal"
        :project="editingProject"
        :loading="isMutationLoading"
        @close="closeModal"
        @submit="handleSubmit"
      />
    </div>
  </div>
</template>
