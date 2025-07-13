<!-- filepath: components/project/ProjectTasks.vue -->
<template>
  <div class="h-full">
    <!-- Header com informações do projeto -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Resumo de Tarefas -->
        <div class="bg-blue-50 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-blue-600">Total de Tarefas</p>
              <p class="text-2xl font-bold text-blue-900">
                {{ projectMetrics.totalTasks }}
              </p>
            </div>
            <Icon icon="lucide:list-checks" class="h-8 w-8 text-blue-500" />
          </div>
        </div>

        <div class="bg-green-50 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-green-600">Concluídas</p>
              <p class="text-2xl font-bold text-green-900">
                {{ projectMetrics.completedTasks }}
              </p>
            </div>
            <Icon icon="lucide:check-circle" class="h-8 w-8 text-green-500" />
          </div>
        </div>

        <div class="bg-yellow-50 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-yellow-600">Em Progresso</p>
              <p class="text-2xl font-bold text-yellow-900">
                {{ projectMetrics.inProgressTasks }}
              </p>
            </div>
            <Icon icon="lucide:clock" class="h-8 w-8 text-yellow-500" />
          </div>
        </div>

        <div class="bg-red-50 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-red-600">Atrasadas</p>
              <p class="text-2xl font-bold text-red-900">
                {{ projectMetrics.overdueTasks }}
              </p>
            </div>
            <Icon icon="lucide:alert-triangle" class="h-8 w-8 text-red-500" />
          </div>
        </div>
      </div>

      <!-- Progresso geral -->
      <div class="mt-6">
        <div class="flex justify-between items-center mb-2">
          <h4 class="text-sm font-medium text-gray-900">
            Progresso Geral do Projeto
          </h4>
          <span class="text-sm text-gray-500">{{ projectProgress }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-3">
          <div
            class="bg-blue-600 h-3 rounded-full transition-all duration-500"
            :style="{ width: `${projectProgress}%` }"
          ></div>
        </div>
      </div>

      <!-- Informações adicionais do projeto -->
      <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div class="flex items-center space-x-2">
          <Icon icon="lucide:users" class="h-4 w-4 text-gray-500" />
          <span class="text-gray-700"
            >{{ project?.equipe?.length || 0 }} membros na equipe</span
          >
        </div>
        <div class="flex items-center space-x-2">
          <Icon icon="lucide:calendar" class="h-4 w-4 text-gray-500" />
          <span class="text-gray-700">
            Prazo: {{ formatDate(project?.data_fim) }}
          </span>
        </div>
        <div class="flex items-center space-x-2">
          <Icon icon="lucide:target" class="h-4 w-4 text-gray-500" />
          <span class="text-gray-700">{{ project?.status_display }}</span>
        </div>
      </div>
    </div>

    <!-- Kanban Board -->
    <div
      class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
    >
      <KanbanBoard
        :project-id="projectId"
        :project="project"
        :is-admin="isProjectAdmin"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { Icon } from "@iconify/vue";
import KanbanBoard from "./KanbanBoard.vue";

const props = defineProps<{
  projectId: number;
  project: any;
}>();

// Verificar se o usuário é admin do projeto
const isProjectAdmin = computed(() => {
  // Aqui você implementaria a lógica para verificar se o usuário é admin
  // Por enquanto, vou usar um valor mock baseado no criador do projeto
  const currentUserId = 1; // Mock - substituir pela lógica real de usuário logado
  return (
    props.project?.criador === currentUserId ||
    props.project?.gerente === currentUserId
  );
});

// Métricas do projeto (mock - seriam carregadas via API)
const projectMetrics = computed(() => {
  // Aqui você carregaria as métricas reais via API
  return {
    totalTasks: 12,
    completedTasks: 5,
    inProgressTasks: 4,
    overdueTasks: 2,
  };
});

// Progresso geral do projeto
const projectProgress = computed(() => {
  if (projectMetrics.value.totalTasks === 0) return 0;
  return Math.round(
    (projectMetrics.value.completedTasks / projectMetrics.value.totalTasks) *
      100
  );
});

// Função para formatar data
const formatDate = (dateString: string) => {
  if (!dateString) return "Não definido";
  return new Date(dateString).toLocaleDateString("pt-BR");
};
</script>
