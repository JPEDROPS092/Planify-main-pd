<template>
  <div class="ml-3 relative">
    <div>
      <button
        @click="toggleDropdown"
        type="button"
        class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        <span class="sr-only">Ver notificações</span>
        <div class="relative">
          <Icon icon="lucide:bell" class="h-6 w-6" />
          <span
            v-if="unreadCount > 0"
            class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"
          ></span>
        </div>
      </button>
    </div>

    <div
      v-if="isOpen"
      @click.outside="isOpen = false"
      class="origin-top-right absolute right-0 mt-2 w-80 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
      role="menu"
      aria-orientation="vertical"
      tabindex="-1"
    >
      <div
        class="px-4 py-2 border-b border-gray-100 flex justify-between items-center"
      >
        <h3 class="text-sm font-medium text-gray-900">Notificações</h3>
        <button
          v-if="unreadCount > 0"
          @click="markAllAsRead"
          class="text-xs text-primary hover:text-primary-600"
        >
          Marcar todas como lidas
        </button>
      </div>

      <div v-if="isLoading" class="px-4 py-6 flex justify-center">
        <div
          class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"
        ></div>
      </div>

      <div v-else-if="error" class="px-4 py-3 text-sm text-red-500">
        Erro ao carregar notificações
      </div>

      <div
        v-else-if="notifications?.length === 0"
        class="px-4 py-6 text-center"
      >
        <Icon icon="lucide:bell-off" class="h-8 w-8 mx-auto text-gray-400" />
        <p class="mt-2 text-sm text-gray-500">Nenhuma notificação</p>
      </div>

      <div v-else class="max-h-96 overflow-y-auto">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="px-4 py-3 hover:bg-gray-50 cursor-pointer"
          :class="{ 'bg-blue-50': !notification.lida }"
          @click="handleNotificationClick(notification)"
        >
          <div class="flex">
            <div class="flex-shrink-0">
              <div
                class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center"
              >
                <Icon
                  :icon="getNotificationIcon(notification.tipo)"
                  class="h-4 w-4 text-primary-600"
                />
              </div>
            </div>
            <div class="ml-3 flex-1">
              <p
                class="text-sm font-medium text-gray-900"
                :class="{ 'font-semibold': !notification.lida }"
              >
                {{ notification.titulo }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {{ notification.mensagem }}
              </p>
              <p class="text-xs text-gray-400 mt-1">
                {{ formatDate(notification.criada_em) }}
              </p>
            </div>
            <div v-if="!notification.lida" class="flex-shrink-0 self-center">
              <div class="h-2 w-2 rounded-full bg-primary-500"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="px-4 py-2 border-t border-gray-100">
        <NuxtLink
          to="/notifications"
          class="text-xs text-primary hover:text-primary-600 block text-center"
        >
          Ver todas as notificações
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useNotifications } from "~/composables/useNotifications";
// Importações diretas para evitar problemas de path mapping
import {
  useCommunicationsNotificacoesList,
  useCommunicationsNotificacoesUpdate,
} from "@/api/comunicação/comunicação";

const isOpen = ref(false);
const queryClient = useQueryClient();

// Usar o composable de notificações para utilitários
const { getNotificationIcon, formatRelativeDate } = useNotifications();

// Consulta para buscar notificações não lidas
const { data, isLoading, error } = useCommunicationsNotificacoesList(
  { lida: false, page_size: 10 },
  {
    query: {
      refetchOnWindowFocus: false,
      staleTime: 30000,
    },
  }
);

// Computar notificações e contagem de não lidas
const notifications = computed(() => data.value?.data?.results || []);
const unreadCount = computed(
  () => notifications.value.filter((n) => !n.lida).length
);

// Mutação para atualizar notificações
const updateMutation = useCommunicationsNotificacoesUpdate({
  mutation: {
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["communications-notificacoes-list"],
      });
    },
    onError: (error) => {
      console.error("Erro ao marcar notificação como lida:", error);
    },
  },
});

// Função para alternar o dropdown
const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    queryClient.invalidateQueries({
      queryKey: ["communications-notificacoes-list"],
    });
  }
};

// Função para marcar todas como lidas
const markAllAsRead = async () => {
  try {
    const unreadNotifications = notifications.value.filter((n) => !n.lida);

    for (const notification of unreadNotifications) {
      updateMutation.mutate({
        id: notification.id,
        data: {
          ...notification,
          lida: true,
        },
      });
    }

    console.log("Todas as notificações foram marcadas como lidas");
  } catch (error) {
    console.error("Erro ao marcar todas as notificações como lidas:", error);
  }
};

// Função para lidar com clique na notificação
const handleNotificationClick = (notification) => {
  if (!notification.lida) {
    updateMutation.mutate({
      id: notification.id,
      data: {
        ...notification,
        lida: true,
      },
    });
  }

  // TODO: Implementar navegação baseada no tipo de notificação
  // Por exemplo:
  // if (notification.tipo === 'TAREFA' && notification.tarefa_id) {
  //   navigateTo(`/tasks/${notification.tarefa_id}`);
  // } else if (notification.tipo === 'PROJETO' && notification.projeto_id) {
  //   navigateTo(`/projects/${notification.projeto_id}`);
  // }

  isOpen.value = false;
};

// Função para formatar data (usar a do composable)
const formatDate = formatRelativeDate;

// Buscar notificações ao montar o componente
onMounted(() => {
  queryClient.prefetchQuery({
    queryKey: [
      "communications-notificacoes-list",
      { lida: false, page_size: 10 },
    ],
    queryFn: () => {
      // A query será executada automaticamente pelo hook useCommunicationsNotificacoesList
    },
  });
});
</script>
