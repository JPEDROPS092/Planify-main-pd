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
import ProjectCard from "@/components/ProjectCard.vue";
import ProjectModal from "@/components/ProjectModal.vue";

// 1. Importar funções do Orval
import {
  useProjectsProjectsList,
  useProjectsProjectsCreate,
  useProjectsProjectsUpdate,
  useProjectsProjectsArchiveCreate,
  useProjectsProjectsDestroy,
} from "~/api/projects/projects";

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
  refetch,
} = useQuery<PaginatedProjetoListList>({
  queryKey: ["projects", currentPage],
  queryFn: () =>
    useProjectsProjectsList({
      page: currentPage.value,
      page_size: pageSize,
    }).then((res) => res.data),
});

const projects = computed(() => paginatedProjects.value?.results || []);
const totalPages = computed(() =>
  paginatedProjects.value?.count
    ? Math.ceil(paginatedProjects.value.count / pageSize)
    : 1
);

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
      queryClient.invalidateQueries({
        queryKey: ["project", editingProject.value?.id],
      });
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
      <!-- ... (seu template da lista de projetos, que parece bom) ... -->
      <!-- O importante é que os botões chamem as funções corretas: -->
      <!-- openCreateModal, openEditModal, handleArchive, handleDelete -->
    </div>
  </div>
</template>
