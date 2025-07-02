<!-- filepath: pages/projects/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import type { AxiosResponse } from "axios";
import { definePageMeta, useRouter } from "#imports";

import { useToast } from "@/composables/useToast";
import type {
  Projeto,
  ProjetoRequest,
  PaginatedProjetoListList,
  ProjectsProjectsListParams,
} from "@/api/schemas";
import ProjectCard from "@/components/project/ProjectCard.vue";
import ProjectModal from "@/components/project/ProjectModal.vue";

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
const pageSize = 10;
const showModal = ref(false);
const editingProject = ref<Projeto | null>(null);

// Query principal para listar projetos
const {
  data: paginatedProjectsResponse,
  isLoading,
  error,
} = useQuery({
  queryKey: ["projects", currentPage],
  queryFn: () =>
    projectsProjectsList({
      pageSize,
      page: currentPage.value,
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
      if (editingProject.value?.id) {
        queryClient.invalidateQueries({
          queryKey: ["projects", editingProject.value.id],
        });
      }
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

// --- Handlers (sem alterações, já estavam corretos) ---
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
};

const handleSubmit = (data: ProjetoRequest) => {
  if (editingProject.value) {
    updateMutation.mutate({ id: editingProject.value.id, data });
  } else {
    createMutation.mutate({ data });
  }
};

const handleArchive = (project: Projeto) => {
  const willBeArchived = !project.arquivado;
  if (
    confirm(
      `Tem certeza que deseja ${willBeArchived ? "arquivar" : "desarquivar"} este projeto?`
    )
  ) {
    // 4. CORREÇÃO: O endpoint 'archive' espera um corpo, mesmo que seja parcial.
    // Usar 'as any' é um hack rápido. O ideal seria ter um tipo PatchedProjetoRequest que permita 'arquivado'.
    archiveMutation.mutate({
      id: project.id,
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

const isMutationLoading = computed(
  () => createMutation.isPending.value || updateMutation.isPending.value
);
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">
          Projetos
        </h1>
        <button
          @click="openCreateModal"
          :disabled="isLoading"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
        >
          <Icon icon="lucide:plus" class="h-4 w-4 mr-2" />
          Novo Projeto
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex items-center justify-center py-12">
        <div class="flex items-center space-x-2">
          <Icon
            icon="lucide:loader"
            class="h-5 w-5 animate-spin text-primary-600"
          />
          <span class="text-gray-600">Carregando projetos...</span>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="flex flex-col items-center space-y-4">
          <Icon icon="lucide:alert-circle" class="h-12 w-12 text-red-500" />
          <p class="text-red-600 font-medium">Erro ao carregar projetos</p>
          <p class="text-gray-500 text-sm">Tente novamente mais tarde</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="projects.length === 0" class="text-center py-12">
        <div class="flex flex-col items-center space-y-4">
          <Icon icon="lucide:folder" class="h-12 w-12 text-gray-400" />
          <h3 class="text-gray-900 font-medium">Nenhum projeto encontrado</h3>
          <p class="text-gray-500">Clique em "Novo Projeto" para começar</p>
        </div>
      </div>

      <!-- Projects Grid -->
      <div
        v-else
        class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
      >
        <ProjectCard
          v-for="project in projects"
          :key="project.id"
          :project="project"
          @edit="openEditModal(project)"
          @archive="handleArchive(project)"
          @delete="handleDelete(project.id)"
        />
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="mt-6 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="p-2 rounded-md border border-gray-300 hover:bg-gray-50 disabled:opacity-50"
          >
            <Icon icon="lucide:chevron-left" class="h-5 w-5" />
          </button>
          <span class="px-4 py-2 text-sm text-gray-700">
            Página {{ currentPage }} de {{ totalPages }}
          </span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="p-2 rounded-md border border-gray-300 hover:bg-gray-50 disabled:opacity-50"
          >
            <Icon icon="lucide:chevron-right" class="h-5 w-5" />
          </button>
        </nav>
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
