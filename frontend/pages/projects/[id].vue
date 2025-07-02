<!-- filepath: pages/projects/[id].vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import type { Projeto, ProjetoRequest } from "@/api/schemas";

// Importar os componentes de cada aba
import ProjectOverview from "@/components/project/ProjectOverview.vue";
import ProjectTasks from "@/components/project/ProjectTasks.vue";
// Importe outros componentes de abas aqui quando criá-los
// import ProjectKanban from '@/components/project/ProjectKanban.vue';

// 1. Importar funções do Orval
import {
  useProjectsProjectsRetrieve,
  useProjectsProjectsUpdate,
  useProjectsProjectsArchiveCreate,
  useProjectsProjectsDestroy,
} from "@/api/projects/projects";

definePageMeta({
  middleware: "auth",
});

const route = useRoute();
const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();

const projectId = computed(() => parseInt(route.params.id as string, 10));
const activeTab = ref("overview");
const showEditModal = ref(false);

// 2. Query principal para buscar os dados do projeto.
// Esta query é a ÚNICA que carrega os dados do PROJETO.
const {
  data: project,
  isLoading: projectLoading,
  error: projectError,
} = useQuery<Projeto>({
  queryKey: ["project", projectId],
  queryFn: () =>
    useProjectsProjectsRetrieve(projectId.value).then((res) => res.data),
  enabled: computed(() => !!projectId.value && !isNaN(projectId.value)),
});

// Mutação para atualizar o projeto (usada pelo modal)
const updateMutation = useProjectsProjectsUpdate({
  mutation: {
    onSuccess: (updatedProject) => {
      toast({ title: "Sucesso!", description: "Projeto atualizado." });
      // Atualiza o cache da query com os novos dados para evitar um refetch
      queryClient.setQueryData(
        ["project", projectId.value],
        updatedProject.data
      );
      showEditModal.value = false;
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao atualizar o projeto.",
        variant: "destructive",
      }),
  },
});

// ... (outras mutações como delete, archive podem ser colocadas aqui também) ...

const tabs = [
  {
    id: "overview",
    name: "Visão Geral",
    icon: "lucide:layout-dashboard",
    component: ProjectOverview,
  },
  {
    id: "tasks",
    name: "Tarefas",
    icon: "lucide:check-square",
    component: ProjectTasks,
  },
  // Adicione outras abas aqui
];

const currentTabComponent = computed(() => {
  return tabs.find((tab) => tab.id === activeTab.value)?.component;
});

const progressPercentage = computed(() => project.value?.progresso || 0);
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Loading/Error/Content para o PROJETO PRINCIPAL -->
      <div v-if="projectLoading">Carregando Projeto...</div>
      <div v-else-if="projectError">Erro ao carregar o projeto.</div>
      <div v-else-if="project">
        <!-- Seu Header do Projeto aqui (o que já tinha) -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg mb-6 p-6">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
            {{ project.titulo }}
          </h1>
          <!-- ... outros detalhes do cabeçalho ... -->
          <div class="mt-4">
            <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div
                class="bg-primary-600 h-2.5 rounded-full"
                :style="{ width: `${progressPercentage}%` }"
              ></div>
            </div>
          </div>
        </div>

        <!-- Abas de Navegação -->
        <div class="border-b border-gray-200 dark:border-gray-700 mb-6">
          <nav class="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2',
              ]"
            >
              <Icon :icon="tab.icon" class="h-5 w-5" />
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <!-- Conteúdo da Aba Ativa -->
        <div>
          <keep-alive>
            <component
              :is="currentTabComponent"
              v-if="currentTabComponent"
              :project-id="projectId"
              :project="project"
            />
          </keep-alive>
        </div>
      </div>
    </div>
  </div>
</template>
