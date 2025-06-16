<template>
  <div class="project-notifications-container">
    <h1 class="text-2xl font-bold mb-4">Notificações do Projeto</h1>
    
    <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Todas as Notificações</h2>
        <div class="flex space-x-2">
          <button 
            @click="markAllAsRead" 
            class="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm"
            :disabled="loading || notifications.filter(n => !n.lida).length === 0"
          >
            Marcar todas como lidas
          </button>
        </div>
      </div>
      
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="notifications.length === 0" class="text-center py-8 text-gray-500">
        Nenhuma notificação encontrada
      </div>
      
      <div v-else class="space-y-3">
        <div 
          v-for="(notification, index) in notifications" 
          :key="index" 
          class="border-l-4 rounded-lg p-4 transition-all hover:shadow-md flex items-start"
          :class="{
            'border-blue-500 bg-blue-50 dark:bg-blue-900/20': notification.tipo === 'informacao',
            'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20': notification.tipo === 'alerta',
            'border-red-500 bg-red-50 dark:bg-red-900/20': notification.tipo === 'urgente',
            'opacity-60': notification.lida
          }"
          @click="markAsRead(notification)"
        >
          <div class="flex-1">
            <div class="flex justify-between items-start">
              <h3 class="font-medium">{{ notification.titulo }}</h3>
              <span class="text-xs text-gray-500">{{ formatDate(notification.data_criacao) }}</span>
            </div>
            
            <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">{{ notification.mensagem }}</p>
            
            <div class="flex items-center justify-between mt-2">
              <span class="text-xs text-gray-500">{{ notification.origem }}</span>
              <div class="flex items-center">
                <span 
                  v-if="!notification.lida" 
                  class="inline-block w-2 h-2 bg-blue-500 rounded-full mr-2"
                ></span>
                <span class="text-xs">{{ notification.lida ? 'Lida' : 'Não lida' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Paginação -->
      <div v-if="notifications.length > 0" class="flex justify-between items-center mt-6">
        <div class="text-sm text-gray-500">
          Mostrando {{ pagination.page * pagination.limit - pagination.limit + 1 }} a 
          {{ Math.min(pagination.page * pagination.limit, pagination.total) }} de 
          {{ pagination.total }} notificações
        </div>
        
        <div class="flex space-x-2">
          <button 
            @click="prevPage" 
            :disabled="pagination.page <= 1" 
            class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Anterior
          </button>
          
          <button 
            @click="nextPage" 
            :disabled="pagination.page >= Math.ceil(pagination.total / pagination.limit)" 
            class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Próxima
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface Notification {
  id: string;
  titulo: string;
  mensagem: string;
  tipo: string;
  origem: string;
  lida: boolean;
  data_criacao: string;
  projeto_id: string;
  usuario_id: string;
}

interface Pagination {
  page: number;
  limit: number;
  total: number;
}

export default defineComponent({
  name: 'ProjectNotificationsPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { showSuccess, showError } = useNotification();
    
    const notifications = ref<Notification[]>([]);
    const loading = ref(true);
    
    const pagination = ref<Pagination>({
      page: 1,
      limit: 10,
      total: 0
    });

    // Validar que o projeto existe
    getProject(projectId).catch(error => {
      showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
    });

    // Simulação de serviço de notificações - em um projeto real, isso seria substituído pelo serviço real
    const loadNotifications = async () => {
      loading.value = true;
      try {
        // Simulação de chamada de API
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Dados de exemplo - em um projeto real, isso viria da API
        const mockNotifications = [
          {
            id: '1',
            titulo: 'Nova tarefa atribuída',
            mensagem: 'Você foi designado para a tarefa "Implementar autenticação"',
            tipo: 'informacao',
            origem: 'Sistema de Tarefas',
            lida: false,
            data_criacao: new Date(Date.now() - 3600000).toISOString(),
            projeto_id: projectId,
            usuario_id: '1'
          },
          {
            id: '2',
            titulo: 'Prazo se aproximando',
            mensagem: 'A tarefa "Desenvolver frontend" vence em 2 dias',
            tipo: 'alerta',
            origem: 'Sistema de Prazos',
            lida: true,
            data_criacao: new Date(Date.now() - 86400000).toISOString(),
            projeto_id: projectId,
            usuario_id: '1'
          },
          {
            id: '3',
            titulo: 'Risco identificado',
            mensagem: 'Um novo risco foi identificado: "Atraso na entrega de dependências"',
            tipo: 'urgente',
            origem: 'Sistema de Riscos',
            lida: false,
            data_criacao: new Date(Date.now() - 172800000).toISOString(),
            projeto_id: projectId,
            usuario_id: '1'
          }
        ];
        
        notifications.value = mockNotifications;
        pagination.value.total = mockNotifications.length;
      } catch (error: any) {
        showError('Erro ao carregar notificações', error.message || 'Não foi possível carregar as notificações');
      } finally {
        loading.value = false;
      }
    };

    // Carregar notificações iniciais
    onMounted(() => {
      loadNotifications();
    });

    const formatDate = (dateString: string) => {
      return format(new Date(dateString), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", { locale: ptBR });
    };

    const markAsRead = (notification: Notification) => {
      if (notification.lida) return;
      
      // Em um projeto real, isso seria uma chamada de API
      notification.lida = true;
      showSuccess('Notificação marcada como lida', '');
    };

    const markAllAsRead = () => {
      // Em um projeto real, isso seria uma chamada de API
      notifications.value.forEach(notification => {
        notification.lida = true;
      });
      showSuccess('Todas as notificações marcadas como lidas', '');
    };

    const prevPage = () => {
      if (pagination.value.page > 1) {
        pagination.value.page--;
        loadNotifications();
      }
    };

    const nextPage = () => {
      if (pagination.value.page < Math.ceil(pagination.value.total / pagination.value.limit)) {
        pagination.value.page++;
        loadNotifications();
      }
    };

    return {
      projectId,
      notifications,
      loading,
      pagination,
      formatDate,
      markAsRead,
      markAllAsRead,
      prevPage,
      nextPage
    };
  }
});
</script>

<style scoped>
.project-notifications-container {
  padding: 1rem;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #09f;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
