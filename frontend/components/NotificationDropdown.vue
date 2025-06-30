<template>
  <div class="ml-3 relative">
    <div>
      <button @click="toggleDropdown" type="button" class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
        <span class="sr-only">Ver notificações</span>
        <div class="relative">
          <Icon icon="lucide:bell" class="h-6 w-6" />
          <span v-if="unreadCount > 0" class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
        </div>
      </button>
    </div>
    
    <div v-if="isOpen" @click.outside="isOpen = false" class="origin-top-right absolute right-0 mt-2 w-80 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10" role="menu" aria-orientation="vertical" tabindex="-1">
      <div class="px-4 py-2 border-b border-gray-100 flex justify-between items-center">
        <h3 class="text-sm font-medium text-gray-900">Notificações</h3>
        <button v-if="unreadCount > 0" @click="markAllAsRead" class="text-xs text-primary hover:text-primary-600">
          Marcar todas como lidas
        </button>
      </div>
      
      <div v-if="isLoading" class="px-4 py-6 flex justify-center">
        <div class="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
      </div>
      
      <div v-else-if="error" class="px-4 py-3 text-sm text-red-500">
        Erro ao carregar notificações
      </div>
      
      <div v-else-if="notifications?.length === 0" class="px-4 py-6 text-center">
        <Icon icon="lucide:bell-off" class="h-8 w-8 mx-auto text-gray-400" />
        <p class="mt-2 text-sm text-gray-500">Nenhuma notificação</p>
      </div>
      
      <div v-else class="max-h-96 overflow-y-auto">
        <div v-for="notification in notifications" :key="notification.id" class="px-4 py-3 hover:bg-gray-50 cursor-pointer" :class="{ 'bg-blue-50': !notification.lida }" @click="handleNotificationClick(notification)">
          <div class="flex">
            <div class="flex-shrink-0">
              <div class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                <Icon :icon="getNotificationIcon(notification.tipo)" class="h-4 w-4 text-primary-600" />
              </div>
            </div>
            <div class="ml-3 flex-1">
              <p class="text-sm font-medium text-gray-900" :class="{ 'font-semibold': !notification.lida }">
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
        <NuxtLink to="/notifications" class="text-xs text-primary hover:text-primary-600 block text-center">
          Ver todas as notificações
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { Icon } from '@iconify/vue';
import { useNotificationService } from '~/services/notificationService';
import { useToast } from '~/composables/useToast';

const isOpen = ref(false);
const notificationService = useNotificationService();
const queryClient = useQueryClient();
const { toast } = useToast();

// Consulta para buscar notificações
const { data, isLoading, error } = useQuery({
  queryKey: ['notifications'],
  queryFn: () => notificationService.getNotifications({ limit: 5, lida: false }),
  enabled: false
});

// Computar notificações e contagem de não lidas
const notifications = computed(() => data.value?.results || []);
const unreadCount = computed(() => notifications.value.filter(n => !n.lida).length);

// Mutação para marcar notificação como lida
const markAsReadMutation = useMutation({
  mutationFn: (id) => notificationService.markNotificationAsRead(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['notifications'] });
  }
});

// Mutação para marcar todas como lidas
const markAllAsReadMutation = useMutation({
  mutationFn: () => notificationService.markAllNotificationsAsRead(),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['notifications'] });
    toast({
      title: 'Notificações atualizadas',
      description: 'Todas as notificações foram marcadas como lidas'
    });
  },
  onError: (error) => {
    toast({
      title: 'Erro',
      description: 'Não foi possível marcar as notificações como lidas',
      variant: 'destructive'
    });
  }
});

// Função para alternar o dropdown
const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    queryClient.invalidateQueries({ queryKey: ['notifications'] });
  }
};

// Função para marcar todas como lidas
const markAllAsRead = () => {
  markAllAsReadMutation.mutate();
};

// Função para lidar com clique na notificação
const handleNotificationClick = (notification) => {
  if (!notification.lida) {
    markAsReadMutation.mutate(notification.id);
  }
  
  // Navegar para o recurso relacionado com base no tipo de notificação
  // Implementar lógica de navegação aqui
  
  isOpen.value = false;
};

// Função para obter ícone com base no tipo de notificação
const getNotificationIcon = (type) => {
  const icons = {
    'TAREFA': 'lucide:check-square',
    'COMENTARIO': 'lucide:message-square',
    'PROJETO': 'lucide:briefcase',
    'DOCUMENTO': 'lucide:file-text',
    'RISCO': 'lucide:alert-triangle',
    'EQUIPE': 'lucide:users',
    'SISTEMA': 'lucide:info'
  };
  
  return icons[type] || 'lucide:bell';
};

// Função para formatar data
const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.round(diffMs / 60000);
  const diffHours = Math.round(diffMs / 3600000);
  const diffDays = Math.round(diffMs / 86400000);
  
  if (diffMins < 60) {
    return `${diffMins} min atrás`;
  } else if (diffHours < 24) {
    return `${diffHours} h atrás`;
  } else if (diffDays < 7) {
    return `${diffDays} dias atrás`;
  } else {
    return date.toLocaleDateString();
  }
};

// Buscar notificações ao montar o componente
onMounted(() => {
  queryClient.prefetchQuery({
    queryKey: ['notifications'],
    queryFn: () => notificationService.getNotifications({ limit: 5, lida: false })
  });
});
</script>
