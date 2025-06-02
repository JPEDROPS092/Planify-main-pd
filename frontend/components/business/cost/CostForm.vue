<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Indicador de status do formulário -->
    <div v-if="formState.isDirty || formState.isSaving || formState.isSaved || formState.hasError"
         class="flex items-center justify-end text-sm mb-2"
         :class="{
           'text-yellow-500 dark:text-yellow-400': formState.isDirty && !formState.isSaving,
           'text-blue-500 dark:text-blue-400': formState.isSaving,
           'text-green-500 dark:text-green-400': formState.isSaved && !formState.isDirty,
           'text-red-500 dark:text-red-400': formState.hasError
         }">
      <span v-if="formState.isDirty && !formState.isSaving">
        <span class="mr-1">●</span> Não salvo
      </span>
      <span v-else-if="formState.isSaving">
        <span class="mr-1">●</span> Salvando...
      </span>
      <span v-else-if="formState.isSaved && !formState.isDirty">
        <span class="mr-1">●</span> Salvo
      </span>
      <span v-else-if="formState.hasError">
        <span class="mr-1">●</span> Erro ao salvar
      </span>
    </div>

    <div>
      <label
        for="cost-description"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Descrição do Custo</label
      >
      <input
        type="text"
        id="cost-description"
        v-model="formData.description"
        @input="updateField('description', $event.target.value)"
        required
        aria-describedby="cost-description-error"
        :aria-invalid="!!errors.description"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        :class="{ 'border-red-500': errors.description }"
      />
      <span 
        v-if="errors.description" 
        id="cost-description-error"
        class="text-xs text-red-500"
      >
        {{ errors.description }}
      </span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label
          for="cost-amount"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Valor (R$)</label
        >
        <input
          type="number"
          id="cost-amount"
          v-model.number="formData.amount"
          @input="updateField('amount', Number($event.target.value))"
          required
          step="0.01"
          min="0"
          aria-describedby="cost-amount-error"
          :aria-invalid="!!errors.amount"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          :class="{ 'border-red-500': errors.amount }"
        />
        <span 
          v-if="errors.amount" 
          id="cost-amount-error"
          class="text-xs text-red-500"
        >
          {{ errors.amount }}
        </span>
      </div>
      <div>
        <label
          for="cost-date"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Data do Custo</label
        >
        <input
          type="date"
          id="cost-date"
          v-model="formData.date"
          @input="updateField('date', $event.target.value)"
          required
          aria-describedby="cost-date-error"
          :aria-invalid="!!errors.date"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          :class="{ 'border-red-500': errors.date }"
        />
        <span 
          v-if="errors.date" 
          id="cost-date-error"
          class="text-xs text-red-500"
        >
          {{ errors.date }}
        </span>
      </div>
    </div>

    <div>
      <label
        for="cost-category"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Categoria</label
      >
      <select
        id="cost-category"
        v-model="formData.category"
        @change="updateField('category', $event.target.value)"
        required
        aria-describedby="cost-category-error"
        :aria-invalid="!!errors.category"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        :class="{ 'border-red-500': errors.category }"
      >
        <option value="" disabled>Selecione uma categoria</option>
        <option value="EQUIPAMENTOS">Equipamentos</option>
        <option value="RECURSOS_HUMANOS">Recursos Humanos</option>
        <option value="SOFTWARE">Software/Licenças</option>
        <option value="MARKETING">Marketing</option>
        <option value="VIAGENS">Viagens</option>
        <option value="TREINAMENTO">Treinamento</option>
        <option value="CONSULTORIA">Consultoria</option>
        <option value="INFRAESTRUTURA">Infraestrutura</option>
        <option value="OUTROS">Outros</option>
      </select>
      <span 
        v-if="errors.category" 
        id="cost-category-error"
        class="text-xs text-red-500"
      >
        {{ errors.category }}
      </span>
    </div>

    <!-- Seção de upload de arquivos -->
    <div v-if="canUploadFiles">
      <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        Comprovantes e Documentos
      </h3>
      
      <!-- Lista de anexos existentes -->
      <div v-if="attachments.length > 0" class="mb-4">
        <h4 class="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
          Anexos existentes:
        </h4>
        <ul class="space-y-2">
          <li 
            v-for="attachment in attachments" 
            :key="attachment.id"
            class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded-md"
          >
            <div class="flex items-center">
              <span class="text-sm">{{ attachment.nome }}</span>
            </div>
            <div class="flex space-x-2">
              <button
                type="button"
                @click="removeAttachment(attachment.id)"
                class="text-red-500 hover:text-red-700 text-sm"
                aria-label="Remover anexo"
              >
                Remover
              </button>
            </div>
          </li>
        </ul>
      </div>
      
      <!-- Contador de arquivos selecionados -->
      <div v-if="filesToUpload.length > 0" class="mb-2">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          {{ filesToUpload.length }} arquivo(s) selecionado(s) para upload
        </p>
      </div>
      
      <!-- Componente de upload -->
      <FileUploader
        accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt,.zip,.rar,.jpg,.jpeg,.png"
        :multiple="true"
        :max-size="10 * 1024 * 1024" <!-- 10MB -->
        :max-files="5"
        @files-selected="handleFilesSelected"
        class="border-dashed border-2 border-gray-300 dark:border-gray-600 rounded-lg p-4"
      />
    </div>

    <div class="flex justify-end space-x-3 pt-4">
      <Button type="button" variant="outline" @click="cancelForm"
        >Cancelar</Button
      >
      <LoadingButton
        type="submit"
        :loading="formState.isSaving || isSubmitting"
        :disabled="!formState.isValid || formState.isSaving || isSubmitting"
      >
        {{ props.cost && props.cost.id ? 'Salvar Alterações' : 'Registrar Custo' }}
      </LoadingButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue';
import { z } from 'zod';
import { useCostService } from '~/services/api'; // Updated import from central API service
import { useDocumentService } from '~/services/api'; // Updated import from central API service
import { useNotification } from '~/stores/composables/useNotification';
import { useFormValidation } from '~/composables/useFormValidation';
import { useAuth } from '~/stores/composables/useAuth';
import type { Cost, CostResponse, Document } from '~/services/api/endpoints/costs'; // Updated types import
import type { DocumentResponse } from '~/services/api/endpoints/documents'; // Added document types
import Button from '../Button.vue';
import LoadingButton from '../LoadingButton.vue';
import FileUploader from '../file-uploader/FileUploader.vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
  cost: {
    type: Object as () => CostResponse | null,
    default: null,
  },
});

const emit = defineEmits(['submit', 'cancel']);

const { createCost, updateCost } = useCostService();
const documentService = useDocumentService();
const notify = useNotification();
const { user } = useAuth();

const isSubmitting = ref(false);
const canUploadFiles = ref(true);
const attachments = ref<DocumentResponse[]>([]);
const lastAutoSave = ref<number | null>(null);
const filesToUpload = ref<File[]>([]);

// Definir o schema de validação usando Zod
const costSchema = z.object({
  title: z.string().min(3, 'A descrição deve ter pelo menos 3 caracteres'),
  amount: z.number().positive('O valor deve ser positivo'),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida'),
  category: z.enum(['EQUIPAMENTOS', 'RECURSOS_HUMANOS', 'SOFTWARE', 'MARKETING', 'VIAGENS', 'TREINAMENTO', 'CONSULTORIA', 'INFRAESTRUTURA', 'OUTROS'], {
    errorMap: () => ({ message: 'Selecione uma categoria válida' })
  }),
  project_id: z.number(),
});

// Valores iniciais do formulário
const initialFormData = {
  title: '',
  amount: 0,
  date: new Date().toISOString().split('T')[0], // Data atual por padrão
  category: 'OUTROS',
  project_id: props.projectId,
};

// Usar o composable de validação de formulário
const { formData, errors, updateField, validateForm, resetForm, saveForm, formState } = useFormValidation({
  schema: costSchema,
  initialData: initialFormData,
  onSave: saveCost,
  autoSaveDebounce: 2000, // 2 segundos de debounce para auto-save
});

// Verificar permissões do usuário atual
async function checkPermissions() {
  if (!user.value) return;
  
  try {
    // Verificar se o usuário pode fazer upload de arquivos
    canUploadFiles.value = ['ADMIN', 'GERENTE', 'MEMBRO'].includes(user.value.role);
  } catch (error) {
    console.error('Erro ao verificar permissões:', error);
    canUploadFiles.value = false;
  }
}

// Carregar anexos do custo
async function loadAttachments() {
  if (!props.cost?.id) return;
  
  try {
    // Using the new document service structure
    const response = await documentService.fetchDocuments({ 
      related_to: 'cost',
      related_id: props.cost.id 
    });
    attachments.value = response.results || [];
  } catch (error) {
    console.error('Erro ao carregar anexos:', error);
    notify.error('Não foi possível carregar os anexos do custo');
  }
}

// Lidar com arquivos selecionados para upload
function handleFilesSelected(files: File[]) {
  filesToUpload.value = [...filesToUpload.value, ...files];
}

// Remover um anexo existente
async function removeAttachment(attachmentId: number) {
  try {
    await documentService.deleteDocument(attachmentId);
    attachments.value = attachments.value.filter(a => a.id !== attachmentId);
    notify.success('Anexo removido com sucesso');
  } catch (error) {
    console.error('Erro ao remover anexo:', error);
    notify.error('Não foi possível remover o anexo');
  }
}

// Função para fazer upload de arquivos
async function uploadCostFiles(costId: number) {
  if (filesToUpload.value.length === 0) return;
  
  const uploadPromises = filesToUpload.value.map(file => {
    return documentService.createDocument({
      title: file.name,
      description: `Anexo para custo #${costId}`,
      project_id: props.projectId,
      file: file,
      document_type: 'COST_ATTACHMENT',
      related_entity: 'cost',
      related_id: costId
    });
  });
  
  try {
    await Promise.all(uploadPromises);
    notify.success(`${filesToUpload.value.length} arquivo(s) anexado(s) com sucesso`);
    filesToUpload.value = [];
    
    // Recarregar a lista de anexos
    if (costId) {
      // Using the new document service structure
      const response = await documentService.fetchDocuments({
        related_to: 'cost',
        related_id: costId
      });
      attachments.value = response.results || [];
    }
  } catch (error) {
    console.error('Erro ao fazer upload de arquivos:', error);
    notify.error('Ocorreu um erro ao anexar um ou mais arquivos');
  }
}

// Salvar o custo (chamado pelo composable useFormValidation)
async function saveCost(data: any) {
  try {
    let costId = props.cost?.id;
    let result;
    
    // Preparar os dados do custo conforme a nova estrutura da API
    const costData: Cost = {
      title: data.title,
      description: data.description || '',
      amount: data.amount,
      date: data.date,
      category: data.category,
      project_id: data.project_id,
    };
    
    if (costId) {
      // Atualizar custo existente usando o novo serviço
      result = await updateCost(costId, costData);
      notify.success('Custo atualizado com sucesso');
    } else {
      // Criar novo custo usando o novo serviço
      result = await createCost(costData);
      costId = result.id;
      notify.success('Custo registrado com sucesso');
    }
    
    // Fazer upload de arquivos se houver
    if (costId && filesToUpload.value.length > 0) {
      await uploadCostFiles(costId);
    }
    
    return result;
  } catch (error) {
    console.error('Erro ao salvar custo:', error);
    notify.error('Ocorreu um erro ao salvar o custo');
    throw error;
  }
}

// Enviar o formulário manualmente
async function submitForm() {
  isSubmitting.value = true;
  try {
    const result = await saveForm();
    if (result) {
      emit('submit', result);
    }
  } catch (error) {
    console.error('Erro ao submeter formulário:', error);
  } finally {
    isSubmitting.value = false;
  }
}

// Cancelar o formulário
function cancelForm() {
  emit('cancel');
}

// Inicializar o formulário com os dados do custo
function initForm() {
  if (!props.cost) return;
  
  // Preencher o formulário com os dados do custo de acordo com a nova estrutura
  resetForm({
    title: props.cost.title || '',
    description: props.cost.description || '',
    amount: props.cost.amount || 0,
    date: props.cost.date || new Date().toISOString().split('T')[0],
    category: props.cost.category || 'OUTROS',
    project_id: props.cost.project_id || props.projectId,
  });
  
  // Carregar anexos
  loadAttachments();
  
  // Verificar permissões
  checkPermissions();
  
  // Limpar arquivos para upload
  filesToUpload.value = [];
}

// Observar mudanças no custo para atualizar o formulário
watch(() => props.cost, () => {
  if (props.cost) {
    initForm();
  } else {
    // Se não houver custo, inicializar com valores padrão
    resetForm({
      ...initialFormData,
      project_id: props.projectId,
    });
    
    // Limpar anexos e arquivos para upload
    attachments.value = [];
    filesToUpload.value = [];
    
    // Verificar permissões
    checkPermissions();
  }
}, { immediate: true });

// Observar mudanças no projectId para atualizar o formulário
watch(() => props.projectId, (newProjectId) => {
  updateField('project_id', newProjectId);
});

onMounted(() => {
  checkPermissions();
  initForm();
});
</script>
