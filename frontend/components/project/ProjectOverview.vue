<!-- filepath: components/project/ProjectOverview.vue -->
<script setup lang="ts">
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
</script>

<template>
  <div class="space-y-6">
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

          <!-- Progresso -->
          <div>
            <div
              class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-1"
            >
              <span>Progresso</span>
              <span>{{ project.progresso }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${project.progresso}%` }"
              ></div>
            </div>
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

    <!-- Estatísticas -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-4">
        Estatísticas
      </h3>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
        <!-- Total de Tarefas -->
        <div class="text-center">
          <div class="text-2xl font-bold text-primary-600">
            {{ project.tasks_count }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Tarefas</div>
        </div>

        <!-- Membros -->
        <div class="text-center">
          <div class="text-2xl font-bold text-primary-600">
            {{ project.membros_count }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Membros</div>
        </div>

        <!-- Tarefas Concluídas -->
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600">
            {{ project.tasks_completed || 0 }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Concluídas</div>
        </div>

        <!-- Tarefas Pendentes -->
        <div class="text-center">
          <div class="text-2xl font-bold text-yellow-600">
            {{ project.tasks_pending || 0 }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Pendentes</div>
        </div>
      </div>
    </div>
  </div>
</template>
