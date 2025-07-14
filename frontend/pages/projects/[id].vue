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
import ProjectModal from "@/components/project/ProjectModal.vue";

// Importar funções do Orval
import {
  useProjectsProjectsRetrieve,
  useProjectsProjectsUpdate,
  useProjectsProjectsDestroy,
} from "@/api/projetos/projetos";

const route = useRoute();
const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();

const projectId = computed(() => {
  if (typeof route.params.id === "string") {
    return parseInt(route.params.id, 10);
  }
  return 1; // fallback
});
const activeTab = ref("overview");
const showEditModal = ref(false);

// Query principal para buscar os dados do projeto.
// Esta query é a ÚNICA que carrega os dados do PROJETO.
const {
  data: projectResponse,
  isLoading: projectLoading,
  error: projectError,
} = useProjectsProjectsRetrieve(projectId, {
  query: {
    enabled: computed(() => !!projectId.value && !isNaN(projectId.value)),
  },
});

// Extrair o projeto da resposta
const project = computed(() => projectResponse.value?.data);

// Mutação para atualizar o projeto (usada pelo modal)
const updateMutation = useProjectsProjectsUpdate({
  mutation: {
    onSuccess: (updatedProject) => {
      toast({
        title: "Sucesso!",
        description: "Projeto atualizado.",
        type: "success",
      });
      // Invalida e refaz a query para obter os dados atualizados
      queryClient.invalidateQueries({
        queryKey: ["projects", "projects", "retrieve", projectId.value],
      });
      showEditModal.value = false;
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao atualizar o projeto.",
        type: "error",
      }),
  },
});

// Mutação para excluir o projeto
const deleteMutation = useProjectsProjectsDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso!",
        description: "Projeto excluído.",
        type: "success",
      });
      router.push("/projects");
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao excluir o projeto.",
        type: "error",
      }),
  },
});

const handleDelete = () => {
  if (
    confirm("Atenção! Excluir este projeto é irreversível. Deseja continuar?")
  ) {
    deleteMutation.mutate({ id: projectId.value });
  }
};

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
  // Adicione outras abas aqui conforme necessário
];

const currentTabComponent = computed(() => {
  return tabs.find((tab) => tab.id === activeTab.value)?.component;
});

const getStatusColor = (status: string | undefined) => {
  if (!status) return "text-gray-500";
  const colors = {
    PLANEJADO: "text-blue-500",
    EM_ANDAMENTO: "text-green-500",
    PAUSADO: "text-yellow-500",
    CONCLUIDO: "text-green-600",
    CANCELADO: "text-red-500",
  };
  return colors[status as keyof typeof colors] || "text-gray-500";
};

const formatDate = (date: string | undefined) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("pt-BR");
};
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <div v-if="projectLoading" class="text-center py-8">
        Carregando projeto...
      </div>
      <div v-else-if="projectError" class="text-center py-8 text-red-500">
        Erro ao carregar o projeto.
      </div>
      <div v-else-if="project">
        <!-- Header do Projeto -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg mb-6 p-6">
          <div class="flex justify-between items-start mb-4">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {{ project?.titulo || "Projeto" }}
              </h1>
              <div class="mt-1 flex items-center space-x-4">
                <span
                  :class="[
                    getStatusColor(project?.status),
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  ]"
                >
                  {{ project?.status_display || "N/A" }}
                </span>
                <span class="text-sm text-gray-500">
                  Criado por {{ project?.criador_username || "N/A" }}
                </span>
                <span class="text-sm text-gray-500">
                  {{ formatDate(project?.criado_em) }}
                </span>
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <button
                @click="showEditModal = true"
                class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                <Icon icon="lucide:edit" class="h-4 w-4 mr-2" />
                Editar
              </button>
              <button
                @click="handleDelete"
                class="inline-flex items-center px-3 py-2 border border-red-300 shadow-sm text-sm leading-4 font-medium rounded-md text-red-700 bg-white hover:bg-red-50"
              >
                <Icon icon="lucide:trash" class="h-4 w-4 mr-2" />
                Excluir
              </button>
            </div>
          </div>

          <!-- Progresso -->
          <div class="mt-4">
            <div
              class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-1"
            >
              <span>Progresso Geral</span>
              <span>{{ project?.progresso || 0 }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
              <div
                class="bg-primary-600 h-2.5 rounded-full transition-all duration-300"
                :style="{ width: `${project?.progresso || 0}%` }"
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
        <component
          :is="currentTabComponent"
          v-if="currentTabComponent && project"
          :project-id="projectId"
          :project="project"
        />

        <!-- Modal de Edição -->
        <ProjectModal
          v-if="project"
          :show="showEditModal"
          :project="project"
          :loading="updateMutation.isPending.value"
          @close="showEditModal = false"
          @submit="(data) => updateMutation.mutate({ id: projectId, data })"
        />
      </div>
    </div>
  </div>
</template>
