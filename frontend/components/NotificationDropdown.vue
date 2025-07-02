<!-- components/NotificationDropdown.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { useNotifications } from "@/composables/useNotifications";

// Import Orval functions and types
import {
  useCommunicationsNotificacoesList,
  useCommunicationsNotificacoesMarcarComoLidaCreate,
  useCommunicationsNotificacoesMarcarTodasComoLidasCreate,
} from "@/api/comunicação/comunicação";
import type { Notificacao } from "@/api/schemas";

const isOpen = ref(false);
const queryClient = useQueryClient();
const { toast } = useToast();
const { getNotificationIcon, formatRelativeDate } = useNotifications();

// Use the Orval hook directly with options
const { data: notificationsResponse, isLoading } =
  useCommunicationsNotificacoesList(
    { lida: false, page_size: 10 },
    {
      query: {
        enabled: isOpen,
        refetchOnWindowFocus: true,
      },
    }
  );

// Computed properties to access the data
const notifications = computed<Notificacao[]>(
  () => notificationsResponse.value?.data.results || []
);
const unreadCount = computed(
  () => notificationsResponse.value?.data.count || 0
);

// Mark as read mutation
const markAsReadMutation = useCommunicationsNotificacoesMarcarComoLidaCreate({
  mutation: {
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["communications-notificacoes-list"],
      });
    },
    onError: (err: any) =>
      toast({
        title: "Erro",
        description: "Falha ao marcar como lida.",
        variant: "destructive",
      }),
  },
});

// Mark all as read mutation
const markAllAsReadMutation =
  useCommunicationsNotificacoesMarcarTodasComoLidasCreate({
    mutation: {
      onSuccess: () => {
        toast({
          title: "Sucesso",
          description: "Todas as notificações foram marcadas como lidas.",
        });
        queryClient.invalidateQueries({
          queryKey: ["communications-notificacoes-list"],
        });
      },
      onError: (err: any) =>
        toast({
          title: "Erro",
          description: "Falha ao marcar todas como lidas.",
          variant: "destructive",
        }),
    },
  });

// Handlers
const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const markAllAsRead = () => {
  markAllAsReadMutation.mutate({ data: {} });
};

const handleNotificationClick = (notification: Notificacao) => {
  // Marca como lida se ainda não estiver
  if (!notification.lida) {
    markAsReadMutation.mutate({ id: notification.id, data: {} });
  }

  // Navega para a URL da notificação, se existir
  if (notification.url) {
    navigateTo(notification.url);
  }

  isOpen.value = false; // Fecha o dropdown após o clique
};
</script>

<template>
  <div class="ml-3 relative">
    <div>
      <button
        @click="toggleDropdown"
        type="button"
        class="relative bg-white dark:bg-gray-800 p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        <span class="sr-only">Ver notificações</span>
        <Icon icon="lucide:bell" class="h-6 w-6" />
        <span
          v-if="unreadCount > 0"
          class="absolute -top-1 -right-1 block h-3 w-3 rounded-full bg-red-500 ring-2 ring-white dark:ring-gray-800"
        ></span>
      </button>
    </div>

    <div
      v-if="isOpen"
      v-on-click-outside="() => (isOpen = false)"
      class="origin-top-right absolute right-0 mt-2 w-80 md:w-96 rounded-md shadow-lg py-1 bg-white dark:bg-gray-800 ring-1 ring-black ring-opacity-5 focus:outline-none z-20"
    >
      <div
        class="px-4 py-2 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center"
      >
        <h3 class="text-sm font-medium text-gray-900 dark:text-gray-200">
          Notificações
        </h3>
        <button
          v-if="unreadCount > 0"
          @click="markAllAsRead"
          :disabled="markAllAsReadMutation.isPending.value"
          class="text-xs text-primary-600 hover:underline disabled:opacity-50"
        >
          Marcar todas como lidas
        </button>
      </div>

      <div v-if="isLoading" class="p-10 flex justify-center">
        <Icon
          icon="svg-spinners:ring-resize"
          class="h-6 w-6 text-primary-500"
        />
      </div>
      <div v-else-if="error" class="p-4 text-sm text-red-600">
        Erro ao carregar.
      </div>
      <div v-else-if="notifications.length === 0" class="p-6 text-center">
        <Icon
          icon="lucide:party-popper"
          class="h-10 w-10 mx-auto text-gray-400"
        />
        <p class="mt-2 text-sm text-gray-500">Tudo em dia!</p>
      </div>

      <div v-else class="max-h-96 overflow-y-auto">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="p-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer"
          @click="handleNotificationClick(notification)"
        >
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <div
                class="h-8 w-8 rounded-full flex items-center justify-center"
                :class="
                  notification.lida
                    ? 'bg-gray-200 dark:bg-gray-700'
                    : 'bg-primary-100 dark:bg-primary-900/40'
                "
              >
                <Icon
                  :icon="getNotificationIcon(notification.tipo)"
                  class="h-4 w-4"
                  :class="
                    notification.lida ? 'text-gray-500' : 'text-primary-600'
                  "
                />
              </div>
            </div>
            <div class="ml-3 flex-1">
              <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                {{ notification.titulo }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                {{ formatDate(notification.criada_em) }}
              </p>
            </div>
            <div
              v-if="!notification.lida"
              class="flex-shrink-0 self-center ml-2"
            >
              <div class="h-2.5 w-2.5 rounded-full bg-primary-500"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="px-4 py-2 border-t border-gray-100 dark:border-gray-700">
        <NuxtLink
          to="/notifications"
          @click="isOpen = false"
          class="text-xs font-medium text-primary-600 hover:underline block text-center"
        >
          Ver todas as notificações
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
