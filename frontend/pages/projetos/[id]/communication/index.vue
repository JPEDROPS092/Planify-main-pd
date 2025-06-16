<template>
  <div class="project-communication-container">
    <h1 class="text-2xl font-bold mb-4">Comunicações do Projeto</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">Mensagens Recentes</h2>
        <div v-if="loading" class="flex justify-center">
          <div class="spinner"></div>
        </div>
        <div v-else-if="communications.length === 0" class="text-center py-4 text-gray-500">
          Nenhuma comunicação encontrada
        </div>
        <div v-else class="space-y-4">
          <div v-for="(communication, index) in communications" :key="index" class="border-b border-gray-200 dark:border-gray-700 pb-3 last:border-0">
            <div class="flex justify-between items-start">
              <h3 class="font-medium">{{ communication.titulo }}</h3>
              <span class="text-xs text-gray-500">{{ formatDate(communication.data_criacao) }}</span>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">{{ communication.mensagem }}</p>
            <div class="flex items-center mt-2">
              <span class="text-xs text-gray-500">Por: {{ communication.criado_por_nome }}</span>
            </div>
          </div>
        </div>
        <div class="mt-4">
          <button @click="navigateToMessages" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
            Ver todas as mensagens →
          </button>
        </div>
      </div>
      
      <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold mb-4">Nova Comunicação</h2>
        <form @submit.prevent="sendCommunication">
          <div class="mb-4">
            <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Título</label>
            <input 
              id="title" 
              v-model="newCommunication.titulo" 
              type="text" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            />
          </div>
          
          <div class="mb-4">
            <label for="message" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Mensagem</label>
            <textarea 
              id="message" 
              v-model="newCommunication.mensagem" 
              rows="4" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            ></textarea>
          </div>
          
          <div class="mb-4">
            <label for="type" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tipo</label>
            <select 
              id="type" 
              v-model="newCommunication.tipo" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              required
            >
              <option value="informacao">Informação</option>
              <option value="alerta">Alerta</option>
              <option value="urgente">Urgente</option>
            </select>
          </div>
          
          <button 
            type="submit" 
            class="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="sending"
          >
            <span v-if="sending">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Enviando...
            </span>
            <span v-else>Enviar Comunicação</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
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

export default defineComponent({
  name: 'ProjectCommunicationPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { getCommunications, createCommunication } = useCommunicationService();
    const { showSuccess, showError } = useNotification();
    
    const communications = ref<Communication[]>([]);
    const loading = ref(true);
    const sending = ref(false);
    
    const newCommunication = ref<Communication>({
      titulo: '',
      mensagem: '',
      tipo: 'informacao',
      projeto_id: projectId
    });

    // Validar que o projeto existe
    getProject(projectId).catch(error => {
      showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
    });

    // Carregar comunicações
    onMounted(async () => {
      try {
        const response = await getCommunications({ projeto_id: projectId, limit: 5 });
        communications.value = response.data || [];
      } catch (error: any) {
        showError('Erro ao carregar comunicações', error.message || 'Não foi possível carregar as comunicações');
      } finally {
        loading.value = false;
      }
    });

    const formatDate = (dateString?: string) => {
      if (!dateString) return '';
      return format(new Date(dateString), "dd 'de' MMMM 'de' yyyy 'às' HH:mm", { locale: ptBR });
    };

    const sendCommunication = async () => {
      sending.value = true;
      try {
        await createCommunication(newCommunication.value);
        showSuccess('Sucesso', 'Comunicação enviada com sucesso');
        
        // Limpar formulário
        newCommunication.value = {
          titulo: '',
          mensagem: '',
          tipo: 'informacao',
          projeto_id: projectId
        };
        
        // Recarregar comunicações
        const response = await getCommunications({ projeto_id: projectId, limit: 5 });
        communications.value = response.data || [];
      } catch (error: any) {
        showError('Erro ao enviar comunicação', error.message || 'Não foi possível enviar a comunicação');
      } finally {
        sending.value = false;
      }
    };

    const navigateToMessages = () => {
      router.push(`/projetos/${projectId}/communication/messages`);
    };

    return {
      projectId,
      communications,
      loading,
      sending,
      newCommunication,
      formatDate,
      sendCommunication,
      navigateToMessages
    };
  }
});
</script>

<style scoped>
.project-communication-container {
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
