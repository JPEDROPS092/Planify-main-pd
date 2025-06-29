<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Notificações</h1>
      <div class="flex items-center space-x-4">
        <button @click="markAllAsReadMutation.mutate()" :disabled="!notifications || notifications.results.every(n => n.lida)" class="text-sm text-primary hover:text-primary-700 disabled:opacity-50 disabled:cursor-not-allowed">
          Marcar todas como lidas
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-10">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="mt-2 text-gray-600">Carregando notificações...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 text-center">
      <Icon icon="lucide:alert-triangle" class="w-10 h-10 mx-auto text-red-500" />
      <p class="mt-2 font-semibold text-red-700">Erro ao carregar notificações</p>
      <p class="text-sm text-red-600">{{ error.message }}</p>
      <button @click="refetch()" class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700">Tentar Novamente</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!notifications || notifications.results.length === 0" class="text-center py-10 border-2 border-dashed rounded-lg">
      <Icon icon="lucide:bell-off" class="w-16 h-16 mx-auto text-gray-400" />
      <h3 class="mt-2 text-xl font-medium text-gray-800">Nenhuma notificação</h3>
      <p class="mt-1 text-gray-500">Você está em dia!</p>
    </div>

    <!-- Notifications List -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul role="list" class="divide-y divide-gray-200">
        <li v-for="notification in notifications.results" :key="notification.id" class="p-4 sm:p-6 hover:bg-gray-50" :class="{ 'bg-primary-50': !notification.lida }">
          <div class="flex items-start justify-between">
            <div class="flex items-start">
               <div class="flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center" :class="getIconBgClass(notification.tipo)">
                <Icon :icon="getNotificationIcon(notification.tipo)" class="h-6 w-6 text-white" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-900">{{ notification.titulo }}</p>
                <p class="text-sm text-gray-600">{{ notification.mensagem }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ timeAgo(notification.criado_em) }}</p>
              </div>
            </div>
            <div class="ml-2 flex-shrink-0 flex items-center space-x-2">
              <button v-if="!notification.lida" @click="markAsReadMutation.mutate(notification.id)" class="text-primary hover:text-primary-700" title="Marcar como lida">
                <Icon icon="lucide:check-circle" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Pagination -->
    <div v-if="notifications && notifications.total_pages > 1" class="mt-6 flex justify-center">
       <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
        <button @click="currentPage--" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Anterior
        </button>
        <span class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
          Página {{ currentPage }} de {{ notifications.total_pages }}
        </span>
        <button @click="currentPage++" :disabled="currentPage === notifications.total_pages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Próximo
        </button>
      </nav>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { ref } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useNotificationService } from '~/services/notificationService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { PaginatedNotificacaoList } from '~/api-types';
import { formatDistanceToNow } from 'date-fns';
import { ptBR } from 'date-fns/locale';

const queryClient = useQueryClient();
const notificationService = useNotificationService();
const { toast } = useToast();

const currentPage = ref(1);

// Fetch notifications
const { data: notifications, isLoading, error, refetch } = useQuery<PaginatedNotificacaoList>({
  queryKey: ['notifications', currentPage],
  queryFn: () => notificationService.getNotifications({ page: currentPage.value }),
});

// Mark as read mutation
const markAsReadMutation = useMutation({
  mutationFn: (id: number) => notificationService.markAsRead(id),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Notificação marcada como lida.' });
    queryClient.invalidateQueries({ queryKey: ['notifications'] });
    queryClient.invalidateQueries({ queryKey: ['user-profile'] }); // To update unread count in sidebar
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: 'Falha ao marcar como lida.', variant: 'destructive' });
  },
});

// Mark all as read mutation
const markAllAsReadMutation = useMutation({
  mutationFn: () => notificationService.markAllAsRead(),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Todas as notificações foram marcadas como lidas.' });
    queryClient.invalidateQueries({ queryKey: ['notifications'] });
    queryClient.invalidateQueries({ queryKey: ['user-profile'] }); // To update unread count in sidebar
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: 'Falha ao marcar todas como lidas.', variant: 'destructive' });
  },
});

const timeAgo = (dateString: string) => {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true, locale: ptBR });
};

const getNotificationIcon = (type: string) => {
  const icons: Record<string, string> = {
    NOVA_TAREFA: 'lucide:file-plus-2',
    TAREFA_CONCLUIDA: 'lucide:check-circle-2',
    COMENTARIO_ADICIONADO: 'lucide:message-square-plus',
    PROJETO_ATUALIZADO: 'lucide:folder-sync',
    ALERTA_RISCO: 'lucide:shield-alert',
  };
  return icons[type] || 'lucide:bell';
};

const getIconBgClass = (type: string) => {
  const classes: Record<string, string> = {
    NOVA_TAREFA: 'bg-blue-500',
    TAREFA_CONCLUIDA: 'bg-green-500',
    COMENTARIO_ADICIONADO: 'bg-purple-500',
    PROJETO_ATUALIZADO: 'bg-yellow-500',
    ALERTA_RISCO: 'bg-red-500',
  };
  return classes[type] || 'bg-gray-500';
}

</script>
