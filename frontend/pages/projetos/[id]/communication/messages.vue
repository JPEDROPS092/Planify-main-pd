<template>
  <div class="project-messages-container">
    <h1 class="text-2xl font-bold mb-4">Mensagens do Projeto</h1>
    
    <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Histórico de Comunicações</h2>
        <div class="flex space-x-2">
          <select 
            v-model="filters.tipo" 
            class="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white text-sm"
          >
            <option value="">Todos os tipos</option>
            <option value="informacao">Informação</option>
            <option value="alerta">Alerta</option>
            <option value="urgente">Urgente</option>
          </select>
          
          <button 
            @click="loadCommunications" 
            class="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm"
          >
            Filtrar
          </button>
        </div>
      </div>
      
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      
      <div v-else-if="communications.length === 0" class="text-center py-8 text-gray-500">
        Nenhuma comunicação encontrada
      </div>
      
      <div v-else class="space-y-4">
        <div 
          v-for="(communication, index) in communications" 
          :key="index" 
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 transition-all hover:shadow-md"
          :class="{
            'border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-900/20': communication.tipo === 'informacao',
            'border-yellow-200 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-900/20': communication.tipo === 'alerta',
            'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20': communication.tipo === 'urgente'
          }"
        >
          <div class="flex justify-between items-start">
            <div class="flex items-center">
              <div 
                class="w-2 h-2 rounded-full mr-2"
                :class="{
                  'bg-blue-500': communication.tipo === 'informacao',
                  'bg-yellow-500': communication.tipo === 'alerta',
                  'bg-red-500': communication.tipo === 'urgente'
                }"
              ></div>
              <h3 class="font-medium">{{ communication.titulo }}</h3>
            </div>
            <span class="text-xs text-gray-500">{{ formatDate(communication.data_criacao) }}</span>
          </div>
          
          <p class="text-sm text-gray-600 dark:text-gray-300 mt-2">{{ communication.mensagem }}</p>
          
          <div class="flex items-center justify-between mt-3">
            <span class="text-xs text-gray-500">Por: {{ communication.criado_por_nome }}</span>
            <span 
              class="text-xs px-2 py-1 rounded-full"
              :class="{
                'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200': communication.tipo === 'informacao',
                'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-200': communication.tipo === 'alerta',
                'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200': communication.tipo === 'urgente'
              }"
            >
              {{ getTipoLabel(communication.tipo) }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- Paginação -->
      <div v-if="communications.length > 0" class="flex justify-between items-center mt-6">
        <div class="text-sm text-gray-500">
          Mostrando {{ pagination.page * pagination.limit - pagination.limit + 1 }} a 
          {{ Math.min(pagination.page * pagination.limit, pagination.total) }} de 
          {{ pagination.total }} comunicações
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
import { useCommunicationService } from '@/composables/useCommunicationService';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

interface Communication {
  id?: string;
  titulo: string;
  mensagem: string;
  tipo: string;
  projeto_id: string;
  criado_por?: string;
  criado_por_nome?: string;
  data_criacao?: string;
}

interface Pagination {
  page: number;
  limit: number;
  total: number;
}

export default defineComponent({
  name: 'ProjectMessagesPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { getCommunications } = useCommunicationService();
    const { showError } = useNotification();
    
    const communications = ref<Communication[]>([]);
    const loading = ref(true);
    
    const filters = ref({
      tipo: ''
    });
    
    const pagination = ref<Pagination>({
      page: 1,
      limit: 10,
      total: 0
    });

    // Validar que o projeto existe
    getProject(projectId).catch(error => {
      showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
    });

    const loadCommunications = async () => {
      loading.value = true;
      try {
        const params = {
          projeto_id: projectId,
          page: pagination.value.page,
          limit: pagination.value.limit,
          ...filters.value.tipo ? { tipo: filters.value.tipo } : {}
        };
        
        const response = await getCommunications(params);
        communications.value = response.data || [];
        pagination.value.total = response.total || 0;
      } catch (error: any) {
        showError('Erro ao carregar comunicações', error.message || 'Não foi possível carregar as comunicações');
      } finally {
        loading.value = false;
      }
    };

    // Carregar comunicações iniciais
    onMounted(() => {
      loadCommunications();
    });

    const formatDate = (dateString?: string) => {
      if (!dateString) return '';
      return format(new Date(dateString), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", { locale: ptBR });
    };

    const getTipoLabel = (tipo: string) => {
      switch (tipo) {
        case 'informacao': return 'Informação';
        case 'alerta': return 'Alerta';
        case 'urgente': return 'Urgente';
        default: return tipo;
      }
    };

    const prevPage = () => {
      if (pagination.value.page > 1) {
        pagination.value.page--;
        loadCommunications();
      }
    };

    const nextPage = () => {
      if (pagination.value.page < Math.ceil(pagination.value.total / pagination.value.limit)) {
        pagination.value.page++;
        loadCommunications();
      }
    };

    return {
      projectId,
      communications,
      loading,
      filters,
      pagination,
      formatDate,
      getTipoLabel,
      loadCommunications,
      prevPage,
      nextPage
    };
  }
});
</script>

<style scoped>
.project-messages-container {
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
