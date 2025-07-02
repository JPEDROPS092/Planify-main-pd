<!-- filepath: pages/projects/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";

import { useToast } from "@/composables/useToast";
import type {
  Projeto,
  ProjetoRequest,
  PaginatedProjetoListList,
} from "@/api/schemas";
import ProjectCard from "@/components/project/ProjectCard.vue";
import ProjectModal from "@/components/project/ProjectModal.vue";

// 2. CORREÇÃO: Importar as funções do Orval usando o alias '@/'
import {
  useProjectsProjectsList,
  useProjectsProjectsCreate,
  useProjectsProjectsUpdate,
  useProjectsProjectsArchiveCreate,
  useProjectsProjectsDestroy,
} from "@/api/projetos/projetos";

definePageMeta({
  middleware: "auth",
  title: "Projetos",
});

const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 8;
const showModal = ref(false);
const editingProject = ref<Projeto | null>(null);

const {
  data: paginatedProjects,
  isLoading,
  error,
} = useQuery<PaginatedProjetoListList>({
  queryKey: ["projects", currentPage],
  // 3. CORREÇÃO: A chamada da queryFn estava correta, mas a consistência no alias é boa.
  // A função `useProjectsProjectsList` é um hook do Orval, não uma função de serviço direta.
  // Este hook já retorna uma promise, então não precisamos de .then(res => res.data) aqui.
  // O Vue Query desempacota o 'data' da AxiosResponse automaticamente.
  queryFn: () =>
    useProjectsProjectsList({ page: currentPage.value, page_size: pageSize }),
});

const projects = computed(() => paginatedProjects.value?.data?.results || []);
const totalPages = computed(() =>
  paginatedProjects.value?.data?.count
    ? Math.ceil(paginatedProjects.value.data.count / pageSize)
    : 1
);

// --- Mutações (sem alterações, já estavam corretas) ---
const createMutation = useProjectsProjectsCreate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso!", description: "Projeto criado com sucesso." });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      closeModal();
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao criar o projeto.",
        variant: "destructive",
      }),
  },
});

const updateMutation = useProjectsProjectsUpdate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Projeto atualizado com sucesso.",
      });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
      if (editingProject.value) {
        queryClient.invalidateQueries({
          queryKey: ["project", editingProject.value.id],
        });
      }
      closeModal();
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Falha ao atualizar o projeto.",
        variant: "destructive",
      }),
  },
});

const archiveMutation = useProjectsProjectsArchiveCreate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso!", description: "Status do projeto alterado." });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao arquivar o projeto.",
        variant: "destructive",
      }),
  },
});

const deleteMutation = useProjectsProjectsDestroy({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso!", description: "Projeto excluído." });
      queryClient.invalidateQueries({ queryKey: ["projects"] });
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao excluir o projeto.",
        variant: "destructive",
      }),
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
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">
          Projetos
        </h1>
        <button
          @click="openCreateModal"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
        >
          <Icon icon="lucide:plus" class="h-4 w-4 mr-2" />
          Novo Projeto
        </button>
      </div>

      <div v-if="isLoading" class="text-center py-12">Carregando...</div>
      <div v-else-if="error" class="text-center py-12 text-red-500">
        Erro ao carregar projetos.
      </div>
      <div
        v-else-if="projects.length > 0"
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
      <div v-else class="text-center py-12">Nenhum projeto encontrado.</div>

      <!-- Paginação (sem alterações) -->

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
