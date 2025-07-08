<!-- filepath: pages/projects/index.vue -->
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import type { AxiosResponse } from "axios";
import { definePageMeta, useRouter } from "#imports";
import BlueButton from "@/components/ui/button/Button.vue";

import { useToast } from "@/composables/useToast";
import type {
  Projeto,
  ProjetoRequest,
  PaginatedProjetoListList,
  ProjectsProjectsListParams,
} from "@/api/schemas";
import ProjectCard from "@/components/project/ProjectCard.vue";
import ProjectModal from "@/components/project/ProjectModal.vue";
import ProjectFilters from "@/components/project/ProjectFilters.vue";
import LoadingSpinner from "@/components/ui/LoadingSpinner.vue";

import {
  projectsProjectsList,
  useProjectsProjectsCreate,
  useProjectsProjectsUpdate,
  useProjectsProjectsArchiveCreate,
  useProjectsProjectsDestroy,
} from "@/api/projetos/projetos";

definePageMeta({
  middleware: ["auth"],
});

const router = useRouter();
const { toast } = useToast();
const queryClient = useQueryClient();

const currentPage = ref(1);
const pageSize = 20;
const showModal = ref(false);
const editingProject = ref<Projeto | null>(null);
const viewMode = ref<"grid" | "list">("grid");

// Filtros
const filters = ref({
  search: "",
  status: "",
  prioridade: "",
  arquivado: "",
  atrasado: false,
  data_inicio_apos_after: "",
  data_inicio_antes_before: "",
  data_fim_apos_after: "",
  data_fim_antes_before: "",
  ordering: "",
});

// Query principal para listar projetos
const {
  data: paginatedProjectsResponse,
  isLoading,
  error,
  refetch,
} = useQuery({
  queryKey: ["projects", currentPage, filters],
  queryFn: () =>
    projectsProjectsList({
      pageSize,
      page: currentPage.value,
      ...filters.value,
    } as ProjectsProjectsListParams),
  enabled: true,
});

const projects = computed(
  () => paginatedProjectsResponse.value?.data.results || []
);

const pagination = computed(() => ({
  count: paginatedProjectsResponse.value?.data.count || 0,
  next: paginatedProjectsResponse.value?.data.next || null,
  previous: paginatedProjectsResponse.value?.data.previous || null,
}));

const totalPages = computed(() =>
  Math.ceil((pagination.value.count || 0) / pageSize)
);

// Estatísticas dos projetos
const projectStats = computed(() => {
  const total = projects.value.length;
  const ativos = projects.value.filter((p) => !p.arquivado).length;
  const concluidos = projects.value.filter(
    (p) => p.status === "CONCLUIDO"
  ).length;
  const atrasados = projects.value.filter((p) => {
    if (!p.data_fim) return false;
    const today = new Date();
    const endDate = new Date(p.data_fim);
    return endDate < today && p.status !== "CONCLUIDO";
  }).length;

  return { total, ativos, concluidos, atrasados };
});

// Mutations para operações CRUD
const createMutation = useProjectsProjectsCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Projeto criado com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      closeModal();
    },
    onError: (error) => {
      toast({
        title: "Erro!",
        description: "Não foi possível criar o projeto.",
        type: "error",
      });
    },
  },
});

const updateMutation = useProjectsProjectsUpdate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Projeto atualizado com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      closeModal();
    },
    onError: (error) => {
      toast({
        title: "Erro!",
        description: "Não foi possível atualizar o projeto.",
        type: "error",
      });
    },
  },
});

const archiveMutation = useProjectsProjectsArchiveCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Status do projeto alterado.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
    onError: (error) => {
      toast({
        title: "Erro!",
        description: "Não foi possível arquivar o projeto.",
        type: "error",
      });
    },
  },
});

const deleteMutation = useProjectsProjectsDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Projeto excluído.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
    onError: (error) => {
      toast({
        title: "Erro!",
        description: "Não foi possível excluir o projeto.",
        type: "error",
      });
    },
  },
});

// Handlers
const openCreateModal = () => {
  editingProject.value = null;
  showModal.value = true;
};

const openEditModal = (project: Projeto) => {
  editingProject.value = project;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingProject.value = null;
};

const handleSubmit = (data: ProjetoRequest) => {
  if (editingProject.value) {
    updateMutation.mutate({ id: editingProject.value.id, data });
  } else {
    createMutation.mutate({ data });
  }
};

const handleArchive = (projectId: number) => {
  const project = projects.value.find((p) => p.id === projectId);
  if (!project) return;

  const willBeArchived = !project.arquivado;
  if (
    confirm(
      `Tem certeza que deseja ${willBeArchived ? "arquivar" : "desarquivar"} este projeto?`
    )
  ) {
    archiveMutation.mutate({
      id: projectId,
      data: { arquivado: willBeArchived } as any,
    });
  }
};

const handleDelete = (id: number) => {
  if (
    confirm(
      "Atenção! Excluir um projeto é uma ação irreversível. Deseja continuar?"
    )
  ) {
    deleteMutation.mutate({ id });
  }
};

const handleFiltersUpdate = (newFilters: any) => {
  filters.value = { ...newFilters };
  currentPage.value = 1; // Reset page when filters change
};

const isMutationLoading = computed(
  () => createMutation.isPending.value || updateMutation.isPending.value
);

// Reset page when filters change
watch(
  filters,
  () => {
    currentPage.value = 1;
  },
  { deep: true }
);

// Helper functions para UI
const getProjectIcon = (status: string) => {
  const icons = {
    PLANEJADO: "lucide:calendar",
    EM_ANDAMENTO: "lucide:play-circle",
    PAUSADO: "lucide:pause-circle",
    CONCLUIDO: "lucide:check-circle",
    CANCELADO: "lucide:x-circle",
  };
  return icons[status as keyof typeof icons] || "lucide:folder";
};

const getStatusIconBg = (status: string) => {
  const colors = {
    PLANEJADO: "bg-blue-500",
    EM_ANDAMENTO: "bg-green-500",
    PAUSADO: "bg-yellow-500",
    CONCLUIDO: "bg-emerald-500",
    CANCELADO: "bg-red-500",
  };
  return colors[status as keyof typeof colors] || "bg-gray-500";
};

const getStatusVariant = (status: string) => {
  const variants = {
    PLANEJADO: "status-planejado" as const,
    EM_ANDAMENTO: "status-andamento" as const,
    PAUSADO: "status-pausado" as const,
    CONCLUIDO: "status-concluido" as const,
    CANCELADO: "status-cancelado" as const,
  };
  return variants[status as keyof typeof variants] || ("default" as const);
};

const getStatusLabel = (status: string) => {
  const labels = {
    PLANEJADO: "Planejado",
    EM_ANDAMENTO: "Em Andamento",
    PAUSADO: "Pausado",
    CONCLUIDO: "Concluído",
    CANCELADO: "Cancelado",
  };
  return labels[status as keyof typeof labels] || status;
};

const getPriorityVariant = (priority: string) => {
  const variants = {
    BAIXA: "priority-baixa" as const,
    MEDIA: "priority-media" as const,
    ALTA: "priority-alta" as const,
    CRITICA: "priority-critica" as const,
  };
  return variants[priority as keyof typeof variants] || ("default" as const);
};

const getPriorityLabel = (priority: string) => {
  const labels = {
    BAIXA: "Baixa",
    MEDIA: "Média",
    ALTA: "Alta",
    CRITICA: "Crítica",
  };
  return labels[priority as keyof typeof labels] || priority;
};

const getProjectProgress = (project: any) => {
  const total = project.total_tarefas || 0;
  const completed = project.tarefas_concluidas || 0;
  return total > 0 ? Math.round((completed / total) * 100) : 0;
};

const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
  });
};

// Computed para paginação visível
const visiblePages = computed(() => {
  const delta = 2;
  const range = [];
  const rangeWithDots = [];

  for (
    let i = Math.max(2, currentPage.value - delta);
    i <= Math.min(totalPages.value - 1, currentPage.value + delta);
    i++
  ) {
    range.push(i);
  }

  if (currentPage.value - delta > 2) {
    rangeWithDots.push(1, "...");
  } else {
    rangeWithDots.push(1);
  }

  rangeWithDots.push(...range);

  if (currentPage.value + delta < totalPages.value - 1) {
    rangeWithDots.push("...", totalPages.value);
  } else if (totalPages.value > 1) {
    rangeWithDots.push(totalPages.value);
  }

  return rangeWithDots;
});
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header Principal -->
      <div
        class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6"
      >
        <div
          class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
        >
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Projetos</h1>
            <p class="text-gray-600 mt-1">
              Gerencie todos os seus projetos em um só lugar
            </p>
          </div>

          <div class="flex items-center gap-3">
            <!-- Toggle de visualização -->
            <div class="flex items-center bg-gray-100 rounded-lg p-1">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'px-3 py-2 rounded-md text-sm font-medium transition-colors',
                  viewMode === 'grid'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900',
                ]"
              >
                <Icon icon="lucide:grid-3x3" class="h-4 w-4" />
              </button>
              <button
                @click="viewMode = 'list'"
                :class="[
                  'px-3 py-2 rounded-md text-sm font-medium transition-colors',
                  viewMode === 'list'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900',
                ]"
              >
                <Icon icon="lucide:list" class="h-4 w-4" />
              </button>
            </div>

            <!-- Botão Novo Projeto -->
            <BlueButton
              icon="lucide:plus"
              label="Novo Projeto"
              :onClick="openCreateModal"
              :disabled="isLoading"
            />
          </div>
        </div>

        <!-- Estatísticas -->
        <div
          class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-gray-200"
        >
          <div class="text-center">
            <div class="text-2xl font-bold text-gray-900">
              {{ projectStats.total }}
            </div>
            <div class="text-sm text-gray-500">Total</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">
              {{ projectStats.ativos }}
            </div>
            <div class="text-sm text-gray-500">Ativos</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">
              {{ projectStats.concluidos }}
            </div>
            <div class="text-sm text-gray-500">Concluídos</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-red-600">
              {{ projectStats.atrasados }}
            </div>
            <div class="text-sm text-gray-500">Atrasados</div>
          </div>
        </div>
      </div>

      <!-- Filtros -->
      <ProjectFilters
        :filters="filters"
        @update:filters="handleFiltersUpdate"
      />

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-16">
        <LoadingSpinner size="lg" text="Carregando projetos..." />
      </div>

      <!-- Error State -->
      <div
        v-else-if="error"
        class="bg-white rounded-lg shadow-sm border border-red-200 p-8 text-center"
      >
        <div class="flex flex-col items-center space-y-4">
          <div
            class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center"
          >
            <Icon icon="lucide:alert-circle" class="h-8 w-8 text-red-500" />
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Erro ao carregar projetos
            </h3>
            <p class="text-gray-500 mb-4">
              Ocorreu um erro ao tentar carregar a lista de projetos.
            </p>
            <button
              @click="refetch()"
              class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Icon icon="lucide:refresh-cw" class="h-4 w-4 mr-2" />
              Tentar Novamente
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="projects.length === 0"
        class="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center"
      >
        <div class="flex flex-col items-center space-y-4">
          <div
            class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center"
          >
            <Icon icon="lucide:folder" class="h-8 w-8 text-gray-400" />
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Nenhum projeto encontrado
            </h3>
            <p class="text-gray-500 mb-6">
              {{
                Object.values(filters).some((f) => f)
                  ? "Nenhum projeto corresponde aos filtros selecionados."
                  : "Você ainda não criou nenhum projeto."
              }}
            </p>
            <BlueButton
              icon="lucide:plus"
              label="Criar Primeiro Projeto"
              :onClick="openCreateModal"
            />
          </div>
        </div>
      </div>

      <!-- Projects Grid/List -->
      <div v-else>
        <!-- Grid View -->
        <div
          v-if="viewMode === 'grid'"
          class="grid grid-cols-1 gap-8 lg:grid-cols-2"
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

        <!-- List View -->
        <div
          v-else
          class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
        >
          <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
            <div
              class="grid grid-cols-12 gap-4 text-sm font-medium text-gray-500"
            >
              <div class="col-span-4">Projeto</div>
              <div class="col-span-2">Status</div>
              <div class="col-span-2">Prioridade</div>
              <div class="col-span-2">Progresso</div>
              <div class="col-span-1">Prazo</div>
              <div class="col-span-1">Ações</div>
            </div>
          </div>
          <div class="divide-y divide-gray-200">
            <div
              v-for="project in projects"
              :key="project.id"
              class="px-6 py-4 hover:bg-gray-50 transition-colors"
            >
              <div class="grid grid-cols-12 gap-4 items-center">
                <!-- Projeto -->
                <div class="col-span-4">
                  <div class="flex items-center gap-3">
                    <div
                      :class="[
                        'w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0',
                        getStatusIconBg(project.status),
                      ]"
                    >
                      <Icon
                        :icon="getProjectIcon(project.status)"
                        class="h-4 w-4 text-white"
                      />
                    </div>
                    <div class="min-w-0">
                      <h3 class="font-medium text-gray-900 truncate">
                        {{ project.titulo }}
                      </h3>
                      <p class="text-sm text-gray-500 truncate">
                        {{ project.descricao || "Sem descrição" }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Status -->
                <div class="col-span-2">
                  <Badge :variant="getStatusVariant(project.status)" size="sm">
                    {{ getStatusLabel(project.status) }}
                  </Badge>
                </div>

                <!-- Prioridade -->
                <div class="col-span-2">
                  <Badge
                    :variant="getPriorityVariant(project.prioridade)"
                    size="sm"
                  >
                    {{ getPriorityLabel(project.prioridade) }}
                  </Badge>
                </div>

                <!-- Progresso -->
                <div class="col-span-2">
                  <div class="flex items-center gap-2">
                    <Progress
                      :value="getProjectProgress(project)"
                      size="sm"
                      class="flex-1"
                    />
                    <span class="text-sm text-gray-500 font-medium">
                      {{ getProjectProgress(project) }}%
                    </span>
                  </div>
                </div>

                <!-- Prazo -->
                <div class="col-span-1 text-sm text-gray-500">
                  {{ formatDate(project.data_fim) }}
                </div>

                <!-- Ações -->
                <div class="col-span-1">
                  <Dropdown>
                    <template #trigger>
                      <button
                        class="p-1 text-gray-400 hover:text-gray-600 rounded transition-colors"
                      >
                        <Icon icon="lucide:more-horizontal" class="h-4 w-4" />
                      </button>
                    </template>

                    <DropdownItem
                      icon="lucide:eye"
                      label="Ver"
                      @click="() => router.push(`/projects/${project.id}`)"
                    />
                    <DropdownItem
                      icon="lucide:edit"
                      label="Editar"
                      @click="() => openEditModal(project)"
                    />
                    <DropdownItem
                      :icon="
                        project.arquivado
                          ? 'lucide:archive-restore'
                          : 'lucide:archive'
                      "
                      :label="project.arquivado ? 'Desarquivar' : 'Arquivar'"
                      @click="() => handleArchive(project.id)"
                    />
                    <DropdownItem
                      icon="lucide:trash-2"
                      label="Excluir"
                      danger
                      @click="() => handleDelete(project.id)"
                      divider
                    />
                  </Dropdown>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-8 flex justify-center">
          <nav class="flex items-center space-x-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="p-3 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Icon icon="lucide:chevron-left" class="h-4 w-4" />
            </button>

            <div class="flex items-center space-x-1">
              <template v-for="page in visiblePages" :key="page">
                <button
                  v-if="page !== '...'"
                  @click="currentPage = page"
                  :class="[
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    currentPage === page
                      ? 'bg-primary-600 text-white'
                      : 'text-gray-700 hover:bg-gray-100',
                  ]"
                >
                  {{ page }}
                </button>
                <span v-else class="px-2 py-2 text-gray-500">...</span>
              </template>
            </div>

            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="p-3 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Icon icon="lucide:chevron-right" class="h-4 w-4" />
            </button>
          </nav>
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
