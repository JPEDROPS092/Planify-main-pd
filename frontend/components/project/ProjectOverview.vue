<!-- filepath: components/project/ProjectOverview.vue -->
<script setup lang="ts">
import { computed } from "vue";
import { Icon } from "@iconify/vue";
import type { Projeto } from "@/api/schemas";

const props = defineProps<{
  projectId: number;
  project: Projeto;
}>();

const getStatusColor = (status: string) => {
  const colors = {
    PLANEJADO: "text-blue-500",
    EM_ANDAMENTO: "text-green-500",
    PAUSADO: "text-yellow-500",
    CONCLUIDO: "text-green-600",
    CANCELADO: "text-red-500",
  };
  return colors[status as keyof typeof colors] || "text-gray-500";
};

const getPriorityColor = (priority: string) => {
  const colors = {
    BAIXA: "text-gray-500",
    MEDIA: "text-yellow-500",
    ALTA: "text-orange-500",
    CRITICA: "text-red-500",
  };
  return colors[priority as keyof typeof colors] || "text-gray-500";
};

const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("pt-BR");
};

// Métricas do projeto (usando dados reais se existirem)
const projectMetrics = computed(() => {
  return {
    totalTasks: props.project.tasks_count ?? 0,
    completedTasks: props.project.tasks_completed ?? 0,
    inProgressTasks: props.project.tasks_in_progress ?? 0,
    overdueTasks: props.project.tasks_overdue ?? 0,
  };
});

const projectProgress = computed(() => {
  if (projectMetrics.value.totalTasks === 0) return 0;
  return Math.round(
    (projectMetrics.value.completedTasks / projectMetrics.value.totalTasks) * 100
  );
});
</script>

<template>
  <div class="space-y-6">
    <!-- Header com resumo das tarefas -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Total de Tarefas -->
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
    </div>

    <!-- Descrição -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
        Descrição
      </h3>
      <p class="text-gray-600 dark:text-gray-300 whitespace-pre-wrap">
        {{ project.descricao || "Nenhuma descrição disponível." }}
      </p>
    </div>

    <!-- Informações Gerais -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Status e Progresso -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
          Status e Progresso
        </h3>

        <div class="space-y-4">
          <!-- Status -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400">Status</span>
            <span :class="[getStatusColor(project.status), 'font-medium']">
              {{ project.status_display }}
            </span>
          </div>

          <!-- Prioridade -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400"
              >Prioridade</span
            >
            <span
              :class="[getPriorityColor(project.prioridade), 'font-medium']"
            >
              {{ project.prioridade_display }}
            </span>
          </div>
        </div>
      </div>

      <!-- Datas e Prazos -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
          Datas e Prazos
        </h3>

        <div class="space-y-4">
          <!-- Data de Início -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400"
              >Data de Início</span
            >
            <span class="font-medium text-gray-900 dark:text-gray-100">
              {{ formatDate(project.data_inicio) }}
            </span>
          </div>

          <!-- Data de Fim -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400"
              >Data de Fim</span
            >
            <span class="font-medium text-gray-900 dark:text-gray-100">
              {{ formatDate(project.data_fim) }}
            </span>
          </div>

          <!-- Dias Restantes -->
          <div class="flex items-center justify-between">
            <span class="text-sm text-gray-500 dark:text-gray-400"
              >Dias Restantes</span
            >
            <span
              :class="[
                project.atrasado
                  ? 'text-red-500'
                  : 'text-gray-900 dark:text-gray-100',
                'font-medium',
              ]"
            >
              {{ project.dias_restantes }} dias
              <span v-if="project.atrasado" class="text-xs ml-1"
                >(Atrasado)</span
              >
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
