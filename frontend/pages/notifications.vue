<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Notificações</h1>
      <p class="mt-2 text-gray-600">
        Gerencie suas notificações e mantenha-se atualizado
      </p>
    </div>

    <!-- Filtros -->
    <div class="bg-white shadow rounded-lg p-6 mb-6">
      <div class="flex flex-wrap gap-4 items-center">
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">Filtrar por:</label>
          <select
            v-model="filters.tipo"
            class="rounded-md border-gray-300 text-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option value="">Todos os tipos</option>
            <option value="TAREFA">Tarefas</option>
            <option value="PROJETO">Projetos</option>
            <option value="COMENTARIO">Comentários</option>
            <option value="DOCUMENTO">Documentos</option>
            <option value="RISCO">Riscos</option>
            <option value="EQUIPE">Equipe</option>
            <option value="SISTEMA">Sistema</option>
          </select>
        </div>

        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">Status:</label>
          <select
            v-model="filters.lida"
            class="rounded-md border-gray-300 text-sm focus:border-primary-500 focus:ring-primary-500"
          >
            <option :value="null">Todas</option>
            <option :value="false">Não lidas</option>
            <option :value="true">Lidas</option>
          </select>
        </div>

        <button
          v-if="unreadCount > 0"
          @click="markAllAsRead"
          :disabled="markingAllAsRead"
          class="ml-auto inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          <Icon
            v-if="markingAllAsRead"
            icon="lucide:loader-2"
            class="animate-spin -ml-1 mr-2 h-4 w-4"
          />
          Marcar todas como lidas
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div
        class="animate-spin h-8 w-8 border-2 border-primary-600 border-t-transparent rounded-full"
      ></div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-50 border border-red-200 rounded-md p-4"
    >
      <div class="flex">
        <Icon icon="lucide:alert-circle" class="h-5 w-5 text-red-400" />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">
            Erro ao carregar notificações
          </h3>
          <p class="mt-1 text-sm text-red-700">
            Tente recarregar a página ou entre em contato com o suporte.
          </p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="notifications.length === 0" class="text-center py-12">
      <Icon icon="lucide:bell-off" class="mx-auto h-12 w-12 text-gray-400" />
      <h3 class="mt-2 text-sm font-medium text-gray-900">
        Nenhuma notificação
      </h3>
      <p class="mt-1 text-sm text-gray-500">
        Você não tem notificações
        {{ filters.lida === false ? "não lidas" : "" }}.
      </p>
    </div>

    <!-- Notifications List -->
    <div v-else class="bg-white shadow rounded-lg divide-y divide-gray-200">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        class="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
        :class="{ 'bg-blue-50': !notification.lida }"
        @click="handleNotificationClick(notification)"
      >
        <div class="flex items-start">
          <!-- Icon -->
          <div class="flex-shrink-0">
            <div
              class="h-10 w-10 rounded-full flex items-center justify-center"
              :class="notification.lida ? 'bg-gray-100' : 'bg-primary-100'"
            >
              <Icon
                :icon="getNotificationIcon(notification.tipo)"
                class="h-5 w-5"
                :class="
                  notification.lida ? 'text-gray-500' : 'text-primary-600'
                "
              />
            </div>
          </div>

          <!-- Content -->
          <div class="ml-4 flex-1">
            <div class="flex items-center justify-between">
              <h3
                class="text-sm font-medium"
                :class="notification.lida ? 'text-gray-700' : 'text-gray-900'"
              >
                {{ notification.titulo }}
              </h3>
              <div class="flex items-center space-x-2">
                <span class="text-xs text-gray-500">
                  {{ formatDate(notification.criada_em) }}
                </span>
                <div
                  v-if="!notification.lida"
                  class="h-2 w-2 rounded-full bg-primary-500"
                ></div>
              </div>
            </div>

            <p
              class="mt-1 text-sm"
              :class="notification.lida ? 'text-gray-500' : 'text-gray-700'"
            >
              {{ notification.mensagem }}
            </p>

            <!-- Type Badge -->
            <div class="mt-2">
              <span
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                :class="getTypeBadgeClass(notification.tipo)"
              >
                {{ getTypeLabel(notification.tipo) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div
      v-if="(data?.data?.count || 0) > pageSize"
      class="mt-6 flex justify-between items-center"
    >
      <div class="text-sm text-gray-700">
        Mostrando {{ (currentPage - 1) * pageSize + 1 }} até
        {{ Math.min(currentPage * pageSize, data?.data?.count || 0) }} de
        {{ data?.data?.count || 0 }} notificações
      </div>

      <div class="flex space-x-2">
        <button
          @click="previousPage"
          :disabled="currentPage === 1"
          class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Icon icon="lucide:chevron-left" class="h-4 w-4 mr-1" />
          Anterior
        </button>

        <button
          @click="nextPage"
          :disabled="currentPage * pageSize >= (data?.data?.count || 0)"
          class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Próxima
          <Icon icon="lucide:chevron-right" class="h-4 w-4 ml-1" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { Icon } from "@iconify/vue";
import { useNotifications } from "~/composables/useNotifications";
// Importações diretas para evitar problemas de path mapping
import {
  useCommunicationsNotificacoesList,
  useCommunicationsNotificacoesUpdate,
} from "@/api/comunicação/comunicação";

// Meta da página
definePageMeta({
  middleware: ["auth"],
  title: "Notificações",
});

// Composable de notificações para utilitários
const {
  getNotificationIcon,
  formatRelativeDate,
  getTypeBadgeClass,
  getTypeLabel,
} = useNotifications();

// Estado dos filtros
const filters = ref({
  tipo: "",
  lida: null as boolean | null,
});

// Paginação
const currentPage = ref(1);
const pageSize = 20;

// Estado de carregamento
const markingAllAsRead = ref(false);

// Query parameters como ref reativo
const queryParams = ref({
  page: currentPage.value,
  page_size: pageSize,
  ...(filters.value.tipo && { tipo: filters.value.tipo }),
  ...(filters.value.lida !== null && { lida: filters.value.lida }),
});

// Atualizar queryParams quando filtros ou página mudam
watch(
  [filters, currentPage],
  () => {
    queryParams.value = {
      page: currentPage.value,
      page_size: pageSize,
      ...(filters.value.tipo && { tipo: filters.value.tipo }),
      ...(filters.value.lida !== null && { lida: filters.value.lida }),
    };
  },
  { deep: true }
);

// Query para notificações (simplificado para evitar problemas de tipagem)
const { data, isLoading, error, refetch } = useCommunicationsNotificacoesList(
  undefined, // Usar parâmetros padrão por enquanto
  {
    query: {
      refetchOnWindowFocus: false,
      staleTime: 30000,
    },
  }
);

// Mutation para atualizar notificações
const updateMutation = useCommunicationsNotificacoesUpdate({
  mutation: {
    onSuccess: () => {
      refetch();
    },
    onError: (error: any) => {
      console.error("Erro ao atualizar notificação:", error);
    },
  },
});

// Dados computados
const notifications = computed(() => data.value?.data?.results || []);
const unreadCount = computed(
  () => notifications.value.filter((n: any) => !n.lida).length
);

// Função para marcar todas como lidas
const markAllAsRead = async () => {
  markingAllAsRead.value = true;
  try {
    const unreadNotifications = notifications.value.filter((n: any) => !n.lida);

    for (const notification of unreadNotifications) {
      updateMutation.mutate({
        id: notification.id,
        data: {
          ...notification,
          lida: true,
        },
      });
    }

    await refetch();
  } catch (error) {
    console.error("Erro ao marcar todas como lidas:", error);
  } finally {
    markingAllAsRead.value = false;
  }
};

// Função para lidar com clique na notificação
const handleNotificationClick = (notification: any) => {
  if (!notification.lida) {
    updateMutation.mutate({
      id: notification.id,
      data: {
        ...notification,
        lida: true,
      },
    });
  }

  // TODO: Navegação baseada no tipo
  // Implementar navegação específica baseada no tipo de notificação
};

// Paginação
const nextPage = () => {
  const totalCount = data.value?.data?.count || 0;
  if (currentPage.value * pageSize < totalCount) {
    currentPage.value++;
  }
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// Função para formatar data
const formatDate = formatRelativeDate;
</script>
