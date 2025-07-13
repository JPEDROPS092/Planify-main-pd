<!-- filepath: pages/dashboard.vue -->
<script setup lang="ts">
import { computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useAuthStore } from "@/stores/auth";
import { useAuth } from "@/composables/useAuth";

// 1. Importar os hooks e tipos do Orval
import { useProjectsProjectsList } from "@/api/projetos/projetos";
import { useTasksTarefasList } from "@/api/tasks/tasks";
import { useCostsAlertasPendentesRetrieve } from "@/api/custo/custo";
import { useCommunicationsNotificacoesList } from "@/api/communications/communications";
import type {
  ProjetoList,
  TarefaList,
  PaginatedProjetoListList,
  PaginatedTarefaListList,
  Alerta,
  PaginatedNotificacaoList,
} from "@/api/schemas";

definePageMeta({
  middleware: "auth",
});

const { logout } = useAuth();
const authStore = useAuthStore();
const user = computed(() => authStore.user);

// --- BUSCA DE DADOS ---

// 2. Query para projetos recentes
const { data: projectsResponse, isLoading: projectsLoading } = useProjectsProjectsList(
  computed(() => ({
    pageSize: 4,
    ordering: "-criado_em",
    responsavel: user.value?.id,
  }))
);

// 3. Query para tarefas do usuário
const { data: tasksResponse, isLoading: tasksLoading } = useTasksTarefasList(
  computed(() => ({
    pageSize: 5,
    minhasTarefas: true,
    ordering: "-criado_em",
  }))
);

// 4. Query para alertas pendentes
const { data: alertsResponse, isLoading: alertsLoading } = useCostsAlertasPendentesRetrieve();

// 5. Query para notificações recentes
const { data: notificationsResponse, isLoading: notificationsLoading } = useCommunicationsNotificacoesList(
  computed(() => ({
    pageSize: 5,
    lida: false,
    ordering: "-criado_em",
  }))
);

// --- DADOS COMPUTADOS ---

// 4. Acesso correto aos dados da resposta
const projects = computed<ProjetoList[]>(
  () => projectsResponse.value?.data?.results || []
);

const tasks = computed<TarefaList[]>(
  () => tasksResponse.value?.data?.results || []
);

const notifications = computed(
  () => notificationsResponse.value?.data?.results || []
);

const pendingAlerts = computed(() => alertsResponse.value?.data || []);

// 5. Estatísticas calculadas
const projectStats = computed(() => {
  if (!projectsResponse.value?.data) return { active: 0, completed: 0, total: 0 };

  const total = projectsResponse.value.data.count || 0;
  const active = projects.value.filter(
    (p) =>
      !p.arquivado &&
      ["EM_ANDAMENTO", "PLANEJADO"].includes(p.status || "")
  ).length;
  const completed = projects.value.filter(
    (p) => !p.arquivado && p.status === "CONCLUIDO"
  ).length;

  return { active, completed, total };
});

const taskStats = computed(() => {
  if (!tasksResponse.value?.data) return { completed: 0, pending: 0, total: 0 };

  const total = tasksResponse.value.data.count || 0;
  const completed = tasks.value.filter((t) => t.status === "FEITO").length;
  const pending = tasks.value.filter((t) => t.status !== "FEITO").length;

  return { completed, pending, total };
});

const notificationStats = computed(() => {
  if (!notificationsResponse.value?.data) return { unread: 0, total: 0 };

  return {
    unread: notifications.value.filter((n) => !n.lida).length,
    total: notificationsResponse.value.data.count || 0,
  };
});

const alertStats = computed(() => {
  return {
    active: pendingAlerts.value.filter((a) => a.status === "ATIVO").length,
    total: pendingAlerts.value.length,
  };
});

const handleLogout = async () => {
  await logout();
};
</script>

<template>
  <div class="py-6">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
            Dashboard
          </h1>
          <p class="mt-1 text-gray-600 dark:text-gray-400">
            Bem-vindo de volta,
            {{ user?.full_name || user?.username || "Usuário" }}!
          </p>
        </div>
        <button
          @click="handleLogout"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
        >
          <Icon icon="lucide:log-out" class="mr-2 h-5 w-5" />
          Sair
        </button>
      </div>

      <!-- Cards de Resumo -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <!-- Projetos Ativos -->
        <div
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-5"
        >
          <div class="flex items-center">
            <div
              class="flex-shrink-0 bg-blue-100 dark:bg-blue-900/50 rounded-md p-3"
            >
              <Icon
                icon="lucide:briefcase"
                class="h-6 w-6 text-blue-600 dark:text-blue-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate"
                >
                  Projetos Ativos
                </dt>
                <dd class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ projectStats.active }}
                </dd>
                <dt class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Total: {{ projectStats.total }}
                </dt>
              </dl>
            </div>
          </div>
        </div>

        <!-- Tarefas -->
        <div
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-5"
        >
          <div class="flex items-center">
            <div
              class="flex-shrink-0 bg-green-100 dark:bg-green-900/50 rounded-md p-3"
            >
              <Icon
                icon="lucide:check-square"
                class="h-6 w-6 text-green-600 dark:text-green-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate"
                >
                  Tarefas Pendentes
                </dt>
                <dd class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ taskStats.pending }}
                </dd>
                <dt class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Concluídas: {{ taskStats.completed }}
                </dt>
              </dl>
            </div>
          </div>
        </div>

        <!-- Alertas -->
        <div
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-5"
        >
          <div class="flex items-center">
            <div
              class="flex-shrink-0 bg-yellow-100 dark:bg-yellow-900/50 rounded-md p-3"
            >
              <Icon
                icon="lucide:alert-triangle"
                class="h-6 w-6 text-yellow-600 dark:text-yellow-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate"
                >
                  Alertas Ativos
                </dt>
                <dd class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ alertStats.active }}
                </dd>
                <dt class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Total: {{ alertStats.total }}
                </dt>
              </dl>
            </div>
          </div>
        </div>

        <!-- Notificações -->
        <div
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-5"
        >
          <div class="flex items-center">
            <div
              class="flex-shrink-0 bg-purple-100 dark:bg-purple-900/50 rounded-md p-3"
            >
              <Icon
                icon="lucide:bell"
                class="h-6 w-6 text-purple-600 dark:text-purple-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate"
                >
                  Notificações Não Lidas
                </dt>
                <dd class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ notificationStats.unread }}
                </dd>
                <dt class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                  Total: {{ notificationStats.total }}
                </dt>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Seções de listas -->
      <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Projetos Recentes -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div
            class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700"
          >
            <h3
              class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
            >
              Projetos Recentes
            </h3>
          </div>
          <div v-if="projectsLoading" class="p-6 text-center">
            <Icon
              icon="svg-spinners:180-ring-with-bg"
              class="w-8 h-8 mx-auto text-primary-600"
            />
            <p class="mt-2">Carregando projetos...</p>
          </div>
          <div
            v-else-if="projects.length === 0"
            class="p-6 text-center text-gray-500"
          >
            <Icon
              icon="lucide:folder"
              class="w-12 h-12 mx-auto text-gray-400"
            />
            <p class="mt-2">Nenhum projeto para mostrar.</p>
          </div>
          <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <li
              v-for="project in projects"
              :key="project.id"
              class="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
            >
              <div class="flex items-center justify-between mb-1">
                <div class="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {{ project.titulo }}
                </div>
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full dark:bg-opacity-30 dark:text-opacity-90"
                  :class="{
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200':
                      project.status === 'CONCLUIDO',
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200':
                      project.status === 'EM_ANDAMENTO',
                    'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200':
                      project.status === 'PLANEJADO',
                    'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200':
                      project.status === 'CANCELADO'
                  }"
                >{{ project.status }}</span
                >
              </div>
              <div class="flex items-center text-xs text-gray-500 dark:text-gray-400 space-x-4">
                <span class="flex items-center">
                  <Icon icon="lucide:users" class="w-4 h-4 mr-1" />
                  {{ project.membros_count || 0 }} membros
                </span>
                <span class="flex items-center">
                  <Icon icon="lucide:check-square" class="w-4 h-4 mr-1" />
                  {{ project.tarefas_count || 0 }} tarefas
                </span>
              </div>
            </li>
          </ul>
        </div>

        <!-- Tarefas Pendentes -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div
            class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700"
          >
            <h3
              class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
            >
              Minhas Tarefas Pendentes
            </h3>
          </div>
          <div v-if="tasksLoading" class="p-6 text-center">
            <Icon
              icon="svg-spinners:180-ring-with-bg"
              class="w-8 h-8 mx-auto text-primary-600"
            />
            <p class="mt-2">Carregando tarefas...</p>
          </div>
          <div
            v-else-if="tasks.length === 0"
            class="p-6 text-center text-gray-500"
          >
            <Icon
              icon="lucide:check-circle"
              class="w-12 h-12 mx-auto text-gray-400"
            />
            <p class="mt-2">Nenhuma tarefa pendente.</p>
          </div>
          <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <li
              v-for="task in tasks"
              :key="task.id"
              class="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
            >
              <div class="flex items-center justify-between mb-1">
                <div class="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {{ task.titulo }}
                </div>
                <span
                  class="text-xs font-semibold px-2 py-1 rounded-full dark:bg-opacity-30 dark:text-opacity-90"
                  :class="{
                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200':
                      task.status === 'FEITO',
                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200':
                      task.status === 'EM_ANDAMENTO',
                    'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200':
                      task.status === 'A_FAZER'
                  }"
                >{{ task.status }}</span
                >
              </div>
              <div class="flex items-center text-xs text-gray-500 dark:text-gray-400 space-x-4">
                <span class="flex items-center">
                  <Icon icon="lucide:folder" class="w-4 h-4 mr-1" />
                  {{ task.projeto_titulo }}
                </span>
                <span v-if="task.prazo" class="flex items-center">
                  <Icon icon="lucide:calendar" class="w-4 h-4 mr-1" />
                  {{ new Date(task.prazo).toLocaleDateString() }}
                </span>
                <span v-if="task.prioridade" class="flex items-center">
                  <Icon icon="lucide:flag" class="w-4 h-4 mr-1" />
                  {{ task.prioridade }}
                </span>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Alertas e Notificações -->
      <div class="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Alertas Ativos -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div
            class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700"
          >
            <h3
              class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
            >
              Alertas Ativos
            </h3>
          </div>
          <div v-if="alertsLoading" class="p-6 text-center">
            <Icon
              icon="svg-spinners:180-ring-with-bg"
              class="w-8 h-8 mx-auto text-primary-600"
            />
            <p class="mt-2">Carregando alertas...</p>
          </div>
          <div
            v-else-if="pendingAlerts.length === 0"
            class="p-6 text-center text-gray-500"
          >
            <Icon
              icon="lucide:shield-check"
              class="w-12 h-12 mx-auto text-gray-400"
            />
            <p class="mt-2">Nenhum alerta ativo.</p>
          </div>
          <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <li
              v-for="alert in pendingAlerts"
              :key="alert.id"
              class="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
            >
              <div class="flex items-start">
                <Icon
                  icon="lucide:alert-triangle"
                  class="w-5 h-5 text-yellow-500 mt-0.5 mr-2 flex-shrink-0"
                />
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {{ alert.mensagem }}
                  </p>
                  <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                    {{ alert.tipo_display }}: {{ alert.projeto_nome }}
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- Notificações Não Lidas -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div
            class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700"
          >
            <h3
              class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
            >
              Notificações Recentes
            </h3>
          </div>
          <div v-if="notificationsLoading" class="p-6 text-center">
            <Icon
              icon="svg-spinners:180-ring-with-bg"
              class="w-8 h-8 mx-auto text-primary-600"
            />
            <p class="mt-2">Carregando notificações...</p>
          </div>
          <div
            v-else-if="notifications.length === 0"
            class="p-6 text-center text-gray-500"
          >
            <Icon
              icon="lucide:bell"
              class="w-12 h-12 mx-auto text-gray-400"
            />
            <p class="mt-2">Nenhuma notificação nova.</p>
          </div>
          <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <li
              v-for="notification in notifications"
              :key="notification.id"
              class="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
            >
              <div class="flex items-start">
                <Icon
                  :icon="notification.lida ? 'lucide:mail-open' : 'lucide:mail'"
                  class="w-5 h-5 text-primary-500 mt-0.5 mr-2 flex-shrink-0"
                />
                <div>
                  <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {{ notification.titulo }}
                  </p>
                  <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                    {{ new Date(notification.criado_em).toLocaleString() }}
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
