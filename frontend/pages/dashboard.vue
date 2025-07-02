<!-- filepath: pages/dashboard.vue -->
<script setup lang="ts">
import { computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useAuthStore } from "@/stores/auth";
import { useAuth } from "@/composables/useAuth";

// 1. Importar os hooks e tipos REAIS do Orval
import { useProjectsProjectsList } from "@/api/projetos/projetos";
import { useTasksTarefasList } from "@/api/tasks/tasks";
import type {
  ProjetoList,
  TarefaList,
  PaginatedProjetoListList,
  PaginatedTarefaListList,
} from "@/api/schemas";

definePageMeta({
  middleware: "auth",
});

const { logout } = useAuth();
const authStore = useAuthStore();
const user = computed(() => authStore.user);

// --- BUSCA DE DADOS REAIS ---

// 2. Buscar projetos REAIS usando o hook do Orval
const { data: paginatedProjects, isLoading: projectsLoading } =
  useQuery<PaginatedProjetoListList>({
    queryKey: ["dashboard-projects"],
    // Busca os 4 projetos mais recentes para exibir
    queryFn: () =>
      useProjectsProjectsList({ page_size: 4, ordering: "-criado_em" }).then(
        (res) => res.data
      ),
  });

// 3. Buscar tarefas REAIS usando o hook do Orval
const { data: paginatedTasks, isLoading: tasksLoading } =
  useQuery<PaginatedTarefaListList>({
    queryKey: ["dashboard-tasks"],
    // Busca as 5 tarefas mais recentes atribuídas ao usuário
    queryFn: () =>
      useTasksTarefasList({
        page_size: 5,
        minhas_tarefas: true,
        ordering: "-id",
      }).then((res) => res.data),
  });

// --- DADOS COMPUTADOS ---

const projects = computed<ProjetoList[]>(
  () => paginatedProjects.value?.results || []
);
const tasks = computed<TarefaList[]>(() => paginatedTasks.value?.results || []);

// 4. Estatísticas calculadas a partir dos dados REAIS (pode ser melhorado com endpoints de métricas)
const projectStats = computed(() => {
  if (!paginatedProjects.value) return { active: 0, completed: 0, total: 0 };
  const total = paginatedProjects.value.count || 0;
  // Nota: Para ter contagens precisas de ativos/concluídos, o ideal seria ter um endpoint de métricas.
  // Isso é uma aproximação baseada nos dados carregados.
  const active = projects.value.filter(
    (p) => p.status === "EM_ANDAMENTO" || p.status === "PLANEJADO"
  ).length;
  const completed = projects.value.filter(
    (p) => p.status === "CONCLUIDO"
  ).length;
  return { active, completed, total };
});

const taskStats = computed(() => {
  if (!paginatedTasks.value) return { completed: 0, pending: 0, total: 0 };
  const total = paginatedTasks.value.count || 0;
  const completed = tasks.value.filter((t) => t.status === "FEITO").length;
  const pending = total - completed;
  return { completed, pending, total };
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
              </dl>
            </div>
          </div>
        </div>

        <!-- Tarefas Concluídas -->
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
                  Tarefas Concluídas
                </dt>
                <dd class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ taskStats.completed }}
                </dd>
              </dl>
            </div>
          </div>
        </div>

        <!-- Tarefas Pendentes -->
        <div
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-5"
        >
          <div class="flex items-center">
            <div
              class="flex-shrink-0 bg-yellow-100 dark:bg-yellow-900/50 rounded-md p-3"
            >
              <Icon
                icon="lucide:clock"
                class="h-6 w-6 text-yellow-600 dark:text-yellow-400"
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
              </dl>
            </div>
          </div>
        </div>

        <!-- Total de Projetos -->
        <div
          class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg p-5"
        >
          <div class="flex items-center">
            <div
              class="flex-shrink-0 bg-purple-100 dark:bg-purple-900/50 rounded-md p-3"
            >
              <Icon
                icon="lucide:folder-git-2"
                class="h-6 w-6 text-purple-600 dark:text-purple-400"
              />
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt
                  class="text-sm font-medium text-gray-500 dark:text-gray-400 truncate"
                >
                  Total de Projetos
                </dt>
                <dd class="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {{ projectStats.total }}
                </dd>
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
            Carregando...
          </div>
          <div
            v-else-if="projects.length === 0"
            class="p-6 text-center text-gray-500"
          >
            Nenhum projeto para mostrar.
          </div>
          <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <li
              v-for="project in projects"
              :key="project.id"
              class="px-6 py-4 flex items-center justify-between"
            >
              <p class="text-sm font-medium text-gray-900 dark:text-gray-200">
                {{ project.titulo }}
              </p>
              <span
                class="text-xs font-semibold px-2 py-1 rounded-full"
                :class="
                  project.status === 'CONCLUIDO'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-blue-100 text-blue-800'
                "
                >{{ project.status_display }}</span
              >
            </li>
          </ul>
        </div>

        <!-- Tarefas Recentes -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg">
          <div
            class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700"
          >
            <h3
              class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
            >
              Minhas Tarefas Recentes
            </h3>
          </div>
          <div v-if="tasksLoading" class="p-6 text-center">Carregando...</div>
          <div
            v-else-if="tasks.length === 0"
            class="p-6 text-center text-gray-500"
          >
            Você não tem tarefas atribuídas.
          </div>
          <ul v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <li
              v-for="task in tasks"
              :key="task.id"
              class="px-6 py-4 flex items-center justify-between"
            >
              <p class="text-sm font-medium text-gray-900 dark:text-gray-200">
                {{ task.titulo }}
              </p>
              <span
                class="text-xs font-semibold px-2 py-1 rounded-full"
                :class="
                  task.status === 'FEITO'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                "
                >{{ task.status_display }}</span
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
