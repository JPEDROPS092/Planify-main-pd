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

import {
  useCommunicationsNotificacoesList,
  useCommunicationsNotificacoesMarcarComoLidaCreate,
  useCommunicationsNotificacoesMarcarTodasComoLidasCreate,
} from "@/api/comunicação/comunicação";
import type { PaginatedNotificacaoList, Notificacao } from "@/api/schemas";

const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 15;

const {
  data: paginatedNotifications,
  isLoading,
  error,
  refetch,
} = useCommunicationsNotificacoesList(
  computed(() => ({
    page: currentPage.value,
    page_size: pageSize,
  })),
  {
    query: {
      queryKey: ["notifications", currentPage],
      placeholderData: (previousData) => previousData,
      // Manter os dados enquanto busca novos para uma transição suave entre páginas
      keepPreviousData: true,
    },
  }
);

const totalPages = computed(() => {
  if (!paginatedNotifications.value?.data?.count) return 1;
  return Math.ceil(paginatedNotifications.value.data.count / pageSize);
});
const notifications = computed(
  () => paginatedNotifications.value?.data?.results || []
);
const unreadCount = computed(
  () => paginatedNotifications.value?.data?.unread_count || 0 // Supondo que a API possa fornecer isso
);

const markAsReadMutation = useCommunicationsNotificacoesMarcarComoLidaCreate({
  mutation: {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notifications"] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao marcar como lida.",
        type: "error",
      });
    },
  },
});

const markAllAsReadMutation =
  useCommunicationsNotificacoesMarcarTodasComoLidasCreate({
    mutation: {
      onSuccess: () => {
        toast({
          title: "Tudo em dia!",
          description: "Todas as notificações foram marcadas como lidas.",
          type: "success",
        });
        queryClient.invalidateQueries({ queryKey: ["notifications"] });
      },
      onError: (err: any) => {
        toast({
          title: "Erro",
          description:
            err.response?.data?.detail || "Falha ao marcar todas como lidas.",
          type: "error",
        });
      },
    },
  });

const handleMarkAsRead = (notificationId: number) => {
  if (markAsReadMutation.isPending.value) return;
  markAsReadMutation.mutate({ id: notificationId, data: {} as any });
};

const handleMarkAllAsRead = () => {
  if (markAllAsReadMutation.isPending.value) return;
  markAllAsReadMutation.mutate({ data: {} as any });
};

const timeAgo = (dateString: string) => {
  if (!dateString) return "";
  return formatDistanceToNow(new Date(dateString), {
    addSuffix: true,
    locale: ptBR,
  });
};

const getNotificationIcon = (type: Notificacao["tipo"]) => {
  const icons: Record<string, string> = {
    TAREFA: "lucide:check-circle-2",
    PROJETO: "lucide:folder-git-2",
    COMENTARIO: "lucide:message-square-plus",
    RISCO: "lucide:shield-alert",
    DOCUMENTO: "lucide:file-text",
    EQUIPE: "lucide:users-2",
    CHAT: "lucide:message-circle",
    SISTEMA: "lucide:server-cog",
  };
  return icons[type] || "lucide:bell";
};

const getIconAppearance = (type: Notificacao["tipo"]) => {
  const appearances: Record<string, string> = {
    TAREFA: "bg-blue-100 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400",
    PROJETO:
      "bg-amber-100 text-amber-600 dark:bg-amber-500/20 dark:text-amber-400",
    COMENTARIO:
      "bg-violet-100 text-violet-600 dark:bg-violet-500/20 dark:text-violet-400",
    RISCO: "bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400",
    DOCUMENTO:
      "bg-teal-100 text-teal-600 dark:bg-teal-500/20 dark:text-teal-400",
    EQUIPE:
      "bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400",
    CHAT: "bg-pink-100 text-pink-600 dark:bg-pink-500/20 dark:text-pink-400",
    SISTEMA:
      "bg-slate-200 text-slate-600 dark:bg-slate-600/30 dark:text-slate-300",
  };
  return (
    appearances[type] ||
    "bg-slate-200 text-slate-600 dark:bg-slate-600/30 dark:text-slate-300"
  );
};
</script>

<template>
  <div class="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8">
    <div
      class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-8 gap-4"
    >
      <div>
        <h1 class="text-3xl font-bold text-slate-900 dark:text-slate-100">
          Notificações
        </h1>
        <p class="mt-1 text-slate-600 dark:text-slate-400">
          Mantenha-se atualizado com as últimas atividades.
        </p>
      </div>
      <button
        @click="handleMarkAllAsRead"
        :disabled="unreadCount === 0 || markAllAsReadMutation.isPending.value"
        class="inline-flex items-center justify-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:scale-105 active:scale-100"
      >
        <Icon
          v-if="markAllAsReadMutation.isPending.value"
          icon="svg-spinners:ring-resize"
          class="w-5 h-5"
        />
        <Icon v-else icon="lucide:check-check" class="w-5 h-5" />
        <span>Marcar todas como lidas</span>
      </button>
    </div>

    <!-- Skeleton Loading State -->
    <div v-if="isLoading">
      <div
        class="bg-white dark:bg-slate-800 shadow-md overflow-hidden rounded-xl"
      >
        <ul class="divide-y divide-slate-200 dark:divide-slate-700">
          <li v-for="i in 5" :key="i" class="p-4 sm:p-5 animate-pulse">
            <div class="flex items-center justify-between">
              <div class="flex items-start flex-1 gap-4">
                <div
                  class="flex-shrink-0 h-11 w-11 rounded-full bg-slate-200 dark:bg-slate-700"
                ></div>
                <div class="flex-1 min-w-0 space-y-2">
                  <div
                    class="h-4 w-3/4 rounded bg-slate-200 dark:bg-slate-700"
                  ></div>
                  <div
                    class="h-3 w-full rounded bg-slate-200 dark:bg-slate-700"
                  ></div>
                  <div
                    class="h-2 w-1/4 rounded bg-slate-200 dark:bg-slate-700"
                  ></div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="text-center py-24 bg-red-50 dark:bg-red-500/10 rounded-xl"
    >
      <Icon icon="lucide:wifi-off" class="w-16 h-16 mx-auto text-red-500" />
      <h3 class="mt-4 text-xl font-semibold text-red-800 dark:text-red-300">
        Falha na Conexão
      </h3>
      <p class="mt-1 text-red-600 dark:text-red-400">
        {{ (error as any).message }}
      </p>
      <button
        @click="refetch()"
        class="mt-6 inline-flex items-center gap-2 px-4 py-2 font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 transition"
      >
        <Icon icon="lucide:refresh-cw" class="w-4 h-4" /> Tentar Novamente
      </button>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="notifications.length === 0"
      class="text-center py-24 bg-slate-100/50 dark:bg-slate-800/20 rounded-xl"
    >
      <Icon
        icon="lucide:party-popper"
        class="w-16 h-16 mx-auto text-green-500"
      />
      <h3 class="mt-4 text-xl font-semibold text-slate-800 dark:text-slate-200">
        Caixa de entrada limpa!
      </h3>
      <p class="mt-1 text-slate-500 dark:text-slate-400">
        Você está em dia com tudo. Bom trabalho!
      </p>
    </div>

    <!-- Notifications List -->
    <div
      v-else
      class="bg-white dark:bg-slate-800 shadow-md overflow-hidden rounded-xl"
    >
      <transition-group
        name="list"
        tag="ul"
        class="divide-y divide-slate-200 dark:divide-slate-700"
      >
        <li
          v-for="notification in notifications"
          :key="notification.id"
          class="relative p-4 sm:p-5 group transition-all duration-300"
          :class="{
            'hover:bg-slate-50 dark:hover:bg-slate-700/50': notification.lida,
            'bg-blue-50/50 dark:bg-blue-500/10 hover:bg-blue-50 dark:hover:bg-blue-500/20 cursor-pointer':
              !notification.lida,
            'hover:shadow-md hover:-translate-y-0.5': true,
          }"
          @click="!notification.lida && handleMarkAsRead(notification.id)"
        >
          <div
            v-if="!notification.lida"
            class="absolute left-0 top-0 bottom-0 w-1 bg-blue-500 rounded-r-full transition-transform duration-300 transform group-hover:scale-y-110"
          ></div>
          <div class="flex items-center justify-between">
            <div class="flex items-start flex-1 gap-4">
              <div
                class="flex-shrink-0 h-11 w-11 rounded-full flex items-center justify-center"
                :class="getIconAppearance(notification.tipo)"
              >
                <Icon
                  :icon="getNotificationIcon(notification.tipo)"
                  class="h-6 w-6"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="text-md font-semibold text-slate-800 dark:text-slate-100 truncate"
                >
                  {{ notification.titulo }}
                </p>
                <p
                  class="text-sm text-slate-600 dark:text-slate-300 mt-0.5 line-clamp-2"
                >
                  {{ notification.mensagem }}
                </p>
                <p class="text-xs text-slate-400 dark:text-slate-500 mt-2">
                  {{ timeAgo(notification.criada_em) }}
                </p>
              </div>
            </div>
            <div class="ml-4 flex-shrink-0">
              <button
                v-if="!notification.lida"
                @click.stop="handleMarkAsRead(notification.id)"
                :disabled="
                  markAsReadMutation.isPending &&
                  markAsReadMutation.variables.value?.id === notification.id
                "
                class="opacity-0 group-hover:opacity-100 focus:opacity-100 p-2 rounded-full text-blue-500 hover:bg-blue-100 dark:hover:bg-blue-500/20 transition-all duration-200 disabled:opacity-50"
                title="Marcar como lida"
              >
                <Icon
                  v-if="
                    markAsReadMutation.isPending &&
                    markAsReadMutation.variables.value?.id === notification.id
                  "
                  icon="svg-spinners:8-dots-rotate"
                  class="h-5 w-5"
                />
                <Icon v-else icon="lucide:check" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </li>
      </transition-group>
    </div>

    <!-- Pagination -->
    <div
      v-if="totalPages > 1"
      class="mt-8 flex justify-center items-center gap-4"
    >
      <button
        @click="currentPage--"
        :disabled="!paginatedNotifications?.data?.previous"
        class="inline-flex items-center justify-center px-4 h-10 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-slate-800 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-white transition"
      >
        <Icon icon="lucide:arrow-left" class="w-4 h-4 mr-2" /> Anterior
      </button>
      <span class="text-sm text-slate-700 dark:text-slate-400">
        Página
        <span class="font-semibold text-slate-900 dark:text-white">{{
          currentPage
        }}</span>
        de
        <span class="font-semibold text-slate-900 dark:text-white">{{
          totalPages
        }}</span>
      </span>
      <button
        @click="currentPage++"
        :disabled="!paginatedNotifications?.data?.next"
        class="inline-flex items-center justify-center px-4 h-10 text-sm font-medium text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-100 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-slate-800 dark:border-slate-700 dark:text-slate-400 dark:hover:bg-slate-700 dark:hover:text-white transition"
      >
        Próximo <Icon icon="lucide:arrow-right" class="w-4 h-4 ml-2" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Garante que a classe line-clamp funcione. */
/* Em um projeto real, isso viria do plugin @tailwindcss/line-clamp */
.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}
</style>
