<template>
  <div class="project-settings-container">
    <h1 class="text-2xl font-bold mb-4">Configurações do Projeto</h1>
    
    <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div v-if="loading" class="flex justify-center py-8">
        <div class="spinner"></div>
      </div>
      
      <div v-else>
        <form @submit.prevent="saveSettings">
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Informações Básicas</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="form-group">
                <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Nome do Projeto</label>
                <input 
                  id="name" 
                  v-model="project.nome" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="code" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Código do Projeto</label>
                <input 
                  id="code" 
                  v-model="project.codigo" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Data de Início</label>
                <input 
                  id="start_date" 
                  v-model="project.data_inicio" 
                  type="date" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="end_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Data de Término</label>
                <input 
                  id="end_date" 
                  v-model="project.data_fim" 
                  type="date" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  required
                />
              </div>
            </div>
            
            <div class="form-group mt-4">
              <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Descrição</label>
              <textarea 
                id="description" 
                v-model="project.descricao" 
                rows="4" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
              ></textarea>
            </div>
          </div>
          
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Configurações de Notificações</h2>
            
            <div class="space-y-3">
              <div class="flex items-center">
                <input 
                  id="notify_task_assignment" 
                  v-model="settings.notifications.task_assignment" 
                  type="checkbox" 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="notify_task_assignment" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  Notificar quando uma tarefa for atribuída
                </label>
              </div>
              
              <div class="flex items-center">
                <input 
                  id="notify_task_deadline" 
                  v-model="settings.notifications.task_deadline" 
                  type="checkbox" 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="notify_task_deadline" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  Notificar quando o prazo de uma tarefa estiver próximo
                </label>
              </div>
              
              <div class="flex items-center">
                <input 
                  id="notify_risk_creation" 
                  v-model="settings.notifications.risk_creation" 
                  type="checkbox" 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="notify_risk_creation" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  Notificar quando um novo risco for identificado
                </label>
              </div>
              
              <div class="flex items-center">
                <input 
                  id="notify_document_upload" 
                  v-model="settings.notifications.document_upload" 
                  type="checkbox" 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="notify_document_upload" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  Notificar quando um novo documento for enviado
                </label>
              </div>
            </div>
          </div>
          
          <div class="mb-6">
            <h2 class="text-xl font-semibold mb-4">Configurações de Privacidade</h2>
            
            <div class="space-y-3">
              <div class="flex items-center">
                <input 
                  id="privacy_public" 
                  v-model="settings.privacy.is_public" 
                  type="checkbox" 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="privacy_public" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  Projeto público (visível para todos os usuários da plataforma)
                </label>
              </div>
              
              <div class="flex items-center">
                <input 
                  id="privacy_require_approval" 
                  v-model="settings.privacy.require_approval" 
                  type="checkbox" 
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="privacy_require_approval" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                  Requer aprovação para novos membros
                </label>
              </div>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button 
              type="button" 
              @click="resetForm" 
              class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Cancelar
            </button>
            
            <button 
              type="submit" 
              class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              :disabled="saving"
            >
              <span v-if="saving">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Salvando...
              </span>
              <span v-else>Salvar Configurações</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '@/stores/composables/useNotification';

interface ProjectSettings {
  notifications: {
    task_assignment: boolean;
    task_deadline: boolean;
    risk_creation: boolean;
    document_upload: boolean;
  };
  privacy: {
    is_public: boolean;
    require_approval: boolean;
  };
}

export default defineComponent({
  name: 'ProjectSettingsPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const projectId = String(route.params.id);
    const { getProject, updateProject } = useProjectService();
    const { showSuccess, showError } = useNotification();
    
    const project = ref<any>({
      nome: '',
      codigo: '',
      descricao: '',
      data_inicio: '',
      data_fim: ''
    });
    
    const settings = ref<ProjectSettings>({
      notifications: {
        task_assignment: true,
        task_deadline: true,
        risk_creation: true,
        document_upload: false
      },
      privacy: {
        is_public: false,
        require_approval: true
      }
    });
    
    const loading = ref(true);
    const saving = ref(false);
    
    const originalProject = ref<any>(null);
    const originalSettings = ref<ProjectSettings | null>(null);

    // Carregar dados do projeto
    onMounted(async () => {
      try {
        const response = await getProject(projectId);
        project.value = response;
        
        // Formatar datas para o formato de input date
        if (project.value.data_inicio) {
          project.value.data_inicio = formatDateForInput(project.value.data_inicio);
        }
        if (project.value.data_fim) {
          project.value.data_fim = formatDateForInput(project.value.data_fim);
        }
        
        // Em um projeto real, aqui carregaríamos as configurações do projeto da API
        // Por enquanto, usamos valores padrão
        
        // Guardar cópias para reset
        originalProject.value = { ...project.value };
        originalSettings.value = JSON.parse(JSON.stringify(settings.value));
      } catch (error: any) {
        showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
      } finally {
        loading.value = false;
      }
    });

    const formatDateForInput = (dateString: string) => {
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    };

    const resetForm = () => {
      if (originalProject.value) {
        project.value = { ...originalProject.value };
      }
      
      if (originalSettings.value) {
        settings.value = JSON.parse(JSON.stringify(originalSettings.value));
      }
    };

    const saveSettings = async () => {
      saving.value = true;
      try {
        // Atualizar informações básicas do projeto
        await updateProject(projectId, project.value);
        
        // Em um projeto real, aqui salvaríamos as configurações do projeto na API
        
        showSuccess('Sucesso', 'Configurações do projeto atualizadas com sucesso');
        
        // Atualizar cópias originais
        originalProject.value = { ...project.value };
        originalSettings.value = JSON.parse(JSON.stringify(settings.value));
      } catch (error: any) {
        showError('Erro ao salvar configurações', error.message || 'Não foi possível salvar as configurações do projeto');
      } finally {
        saving.value = false;
      }
    };

    return {
      projectId,
      project,
      settings,
      loading,
      saving,
      resetForm,
      saveSettings
    };
  }
});
</script>

<style scoped>
.project-settings-container {
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
