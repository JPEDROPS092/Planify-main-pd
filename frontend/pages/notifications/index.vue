<!-- filepath: pages/notifications/index.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: "auth",
});

import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { formatDistanceToNow } from "date-fns";
import { ptBR } from "date-fns/locale";

// 1. Importar funções e tipos corretos do Orval para notificações
import {
  useCommunicationsNotificacoesList,
  useCommunicationsNotificacoesMarcarComoLidaCreate,
  useCommunicationsNotificacoesMarcarTodasComoLidasCreate,
} from "@/api/comunicação/comunicação";
import type { PaginatedNotificacaoList, Notificacao } from "@/api/schemas";

const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 10; // Defina um tamanho de página para o cálculo

// 2. Usar o hook correto do Orval para buscar as notificações
const {
  data: paginatedNotifications,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedNotificacaoList>({
  queryKey: ["notifications", currentPage],
  queryFn: () =>
    useCommunicationsNotificacoesList({ page: currentPage.value }).then(
      (res) => res.data
    ),
  placeholderData: (previousData) => previousData,
});

// Calcula o total de páginas e extrai os resultados
const totalPages = computed(() => {
  if (!paginatedNotifications.value?.count) return 1;
  return Math.ceil(paginatedNotifications.value.count / pageSize);
});
const notifications = computed(
  () => paginatedNotifications.value?.results || []
);

// 3. Mutação para marcar uma notificação como lida
const markAsReadMutation = useCommunicationsNotificacoesMarcarComoLidaCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Notificação marcada como lida.",
      });
      queryClient.invalidateQueries({ queryKey: ["notifications"] });
      // Invalide também outras queries que dependem do status de leitura, se houver
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao marcar como lida.",
        variant: "destructive",
      });
    },
  },
});

// 4. Mutação para marcar TODAS as notificações como lidas
const markAllAsReadMutation =
  useCommunicationsNotificacoesMarcarTodasComoLidasCreate({
    mutation: {
      onSuccess: () => {
        toast({
          title: "Sucesso",
          description: "Todas as notificações foram marcadas como lidas.",
        });
        queryClient.invalidateQueries({ queryKey: ["notifications"] });
      },
      onError: (err: any) => {
        toast({
          title: "Erro",
          description:
            err.response?.data?.detail || "Falha ao marcar todas como lidas.",
          variant: "destructive",
        });
      },
    },
  });

const handleMarkAsRead = (notificationId: number) => {
  // A mutação gerada pelo Orval espera o corpo dentro de um objeto 'data'
  markAsReadMutation.mutate({ id: notificationId, data: {} as any });
};

const handleMarkAllAsRead = () => {
  // A mutação também espera um corpo, mesmo que não usemos
  markAllAsReadMutation.mutate({ data: {} as any });
};

// Funções de formatação e estilo
const timeAgo = (dateString: string) => {
  if (!dateString) return "";
  return formatDistanceToNow(new Date(dateString), {
    addSuffix: true,
    locale: ptBR,
  });
};

const getNotificationIcon = (type: Notificacao["tipo"]) => {
  const icons: Record<string, string> = {
    TAREFA: "lucide:file-plus-2",
    PROJETO: "lucide:folder-sync",
    COMENTARIO: "lucide:message-square-plus",
    RISCO: "lucide:shield-alert",
    DOCUMENTO: "lucide:file-text",
    EQUIPE: "lucide:users",
    CHAT: "lucide:messages-square",
    SISTEMA: "lucide:server-cog",
  };
  return icons[type] || "lucide:bell";
};

const getIconBgClass = (type: Notificacao["tipo"]) => {
  const classes: Record<string, string> = {
    TAREFA: "bg-blue-500",
    PROJETO: "bg-yellow-500",
    COMENTARIO: "bg-purple-500",
    RISCO: "bg-red-500",
    DOCUMENTO: "bg-indigo-500",
    EQUIPE: "bg-teal-500",
    CHAT: "bg-pink-500",
    SISTEMA: "bg-gray-500",
  };
  return classes[type] || "bg-gray-500";
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Notificações
      </h1>
      <div class="flex items-center space-x-4">
        <button
          @click="handleMarkAllAsRead"
          :disabled="
            !notifications.length ||
            notifications.every((n) => n.lida) ||
            markAllAsReadMutation.isPending.value
          "
          class="text-sm font-medium text-primary-600 hover:text-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Marcar todas como lidas
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !notifications.length" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
      <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
        Carregando notificações...
      </p>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md"
      role="alert"
    >
      <p class="font-bold">Ocorreu um erro ao carregar as notificações</p>
      <p>{{ (error as any).message }}</p>
      <button
        @click="refetch()"
        class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
      >
        Tentar Novamente
      </button>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="notifications.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:bell-off"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Caixa de entrada vazia
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Você está em dia com tudo!
      </p>
    </div>

    <!-- Notifications List -->
    <div
      v-else
      class="bg-white dark:bg-gray-800 shadow overflow-hidden rounded-lg"
    >
      <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
        <li
          v-for="notification in notifications"
          :key="notification.id"
          class="p-4 sm:p-5 transition-colors"
          :class="{
            'bg-primary-50 dark:bg-primary-900/20': !notification.lida,
            'hover:bg-gray-50 dark:hover:bg-gray-700/50': notification.lida,
          }"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-start flex-1">
              <div
                class="flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center"
                :class="getIconBgClass(notification.tipo)"
              >
                <Icon
                  :icon="getNotificationIcon(notification.tipo)"
                  class="h-5 w-5 text-white"
                />
              </div>
              <div class="ml-4 flex-1">
                <p class="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {{ notification.titulo }}
                </p>
                <p class="text-sm text-gray-600 dark:text-gray-300">
                  {{ notification.mensagem }}
                </p>
                <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                  {{ timeAgo(notification.criada_em) }}
                </p>
              </div>
            </div>
            <div class="ml-4 flex-shrink-0">
              <button
                v-if="!notification.lida"
                @click="handleMarkAsRead(notification.id)"
                :disabled="
                  markAsReadMutation.isPending.value &&
                  markAsReadMutation.variables.value?.id === notification.id
                "
                class="text-primary-600 hover:text-primary-500"
                title="Marcar como lida"
              >
                <Icon icon="lucide:check-circle" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav
        class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
        aria-label="Pagination"
      >
        <button
          @click="currentPage--"
          :disabled="!paginatedNotifications?.previous"
          class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
        <span
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-200"
        >
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button
          @click="currentPage++"
          :disabled="!paginatedNotifications?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>
  </div>
</template>
