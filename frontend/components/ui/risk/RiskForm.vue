<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Indicador de status do formulário -->
    <div v-if="formState.isDirty || formState.isSaving || formState.isSaved || formState.hasError"
         class="flex items-center justify-end text-sm mb-2"
         :class="{
           'text-yellow-600 dark:text-yellow-400': formState.isDirty && !formState.isSaving && !formState.isSaved && !formState.hasError,
           'text-blue-600 dark:text-blue-400': formState.isSaving,
           'text-green-600 dark:text-green-400': formState.isSaved && !formState.isDirty,
           'text-red-600 dark:text-red-400': formState.hasError
         }">
      <span v-if="formState.isSaving">Salvando...</span>
      <span v-else-if="formState.isSaved && !formState.isDirty">
        Salvo automaticamente {{ lastAutoSave ? new Date(lastAutoSave).toLocaleTimeString() : '' }}
      </span>
      <span v-else-if="formState.hasError">Erro ao salvar</span>
      <span v-else-if="formState.isDirty">Não salvo</span>
    </div>
    
    <div>
      <label
        for="risk-name"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Nome do Risco</label
      >
      <input
        type="text"
        id="risk-name"
        v-model="formState.formData.name"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        :class="{'border-red-500 dark:border-red-400': formState.errors.name}"
        aria-describedby="risk-name-error"
      />
      <p v-if="formState.errors.name" id="risk-name-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
        {{ formState.errors.name }}
      </p>
    </div>

    <div>
      <label
        for="risk-description"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Descrição</label
      >
      <textarea
        id="risk-description"
        v-model="formState.formData.description"
        rows="3"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        :class="{'border-red-500 dark:border-red-400': formState.errors.description}"
        aria-describedby="risk-description-error"
      ></textarea>
      <p v-if="formState.errors.description" id="risk-description-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
        {{ formState.errors.description }}
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label
          for="risk-impact"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Impacto</label
        >
        <select
          id="risk-impact"
          v-model="formState.formData.impact"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          :class="{'border-red-500 dark:border-red-400': formState.errors.impact}"
          aria-describedby="risk-impact-error"
        >
          <option value="BAIXO">Baixo</option>
          <option value="MEDIO">Médio</option>
          <option value="ALTO">Alto</option>
        </select>
        <p v-if="formState.errors.impact" id="risk-impact-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.impact }}
        </p>
      </div>
      <div>
        <label
          for="risk-probability"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Probabilidade</label
        >
        <select
          id="risk-probability"
          v-model="formState.formData.probability"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          :class="{'border-red-500 dark:border-red-400': formState.errors.probability}"
          aria-describedby="risk-probability-error"
        >
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
        </select>
        <p v-if="formState.errors.probability" id="risk-probability-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.probability }}
        </p>
      </div>
    </div>

    <div>
      <label
        for="risk-status"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Status</label
      >
      <select
        id="risk-status"
        v-model="formState.formData.status"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        :class="{'border-red-500 dark:border-red-400': formState.errors.status}"
        aria-describedby="risk-status-error"
      >
        <option value="IDENTIFICADO">Identificado</option>
        <option value="EM_ANDAMENTO">Em Andamento</option>
        <option value="MITIGADO">Mitigado</option>
        <option value="FECHADO">Fechado</option>
      </select>
      <p v-if="formState.errors.status" id="risk-status-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
        {{ formState.errors.status }}
      </p>
    </div>

    <div>
      <label
        for="risk-mitigation_plan"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Plano de Mitigação</label
      >
      <textarea
        id="risk-mitigation_plan"
        v-model="formState.formData.mitigation_plan"
        rows="3"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        :class="{'border-red-500 dark:border-red-400': formState.errors.mitigation_plan}"
        aria-describedby="risk-mitigation-plan-error"
      ></textarea>
      <p v-if="formState.errors.mitigation_plan" id="risk-mitigation-plan-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
        {{ formState.errors.mitigation_plan }}
      </p>
    </div>

    <div>
      <label
        for="risk-assignee"
        class="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Responsável (Opcional)</label
      >
      <select
        id="risk-assignee"
        v-model="formState.formData.assignee"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        :class="{'border-red-500 dark:border-red-400': formState.errors.assignee}"
        aria-describedby="risk-assignee-error"
      >
        <option :value="null">Ninguém atribuído</option>
        <option
          v-for="user in projectTeamMembers"
          :key="user.id"
          :value="user.id"
        >
          {{ user.name || user.username }}
        </option>
      </select>
      <p v-if="formState.errors.assignee" id="risk-assignee-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
        {{ formState.errors.assignee }}
      </p>
    </div>
    
    <!-- Upload de arquivos -->
    <div v-if="canUploadFiles">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Documentos do Risco</label>
      
      <!-- Arquivos existentes -->
      <div v-if="attachments.length > 0" class="mb-4">
        <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Arquivos anexados:</h4>
        <ul class="space-y-2">
          <li v-for="attachment in attachments" :key="attachment.id" class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
            <a :href="attachment.url" target="_blank" class="text-blue-600 dark:text-blue-400 hover:underline text-sm">
              {{ attachment.nome }}
            </a>
            <Button 
              variant="ghost" 
              size="sm" 
              @click="removeAttachment(attachment.id)"
              aria-label="Remover anexo"
            >
              <span class="sr-only">Remover</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </Button>
          </li>
        </ul>
      </div>
      
      <!-- Uploader de arquivos -->
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
        {{ props.risk && props.risk.id ? 'Salvar Alterações' : 'Registrar Risco' }}
      </LoadingButton>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue';
import { z } from 'zod';
import { useRiskService } from '~/services/api/riskService';
import { useDocumentService } from '~/services/api/documentService';
import { useTeamService } from '~/services/api/teamService';
import { useUserService } from '~/services/api/userService';
import { useNotification } from '~/composables/useNotification';
import { useFormValidation } from '~/composables/useFormValidation';
import { useAuth } from '~/composables/useAuth';
import type { Risco, Documento, User } from '~/services/api/types';
import Button from '../Button.vue';
import LoadingButton from '../LoadingButton.vue';
import FileUploader from '../file-uploader/FileUploader.vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
  risk: {
    type: Object as () => Risco | null,
    default: null,
  },
});

const emit = defineEmits(['submit', 'cancel']);

const riskService = useRiskService();
const userService = useUserService();
const teamService = useTeamService();
const documentService = useDocumentService();
const notify = useNotification();
const { user } = useAuth();

const projectTeamMembers = ref<User[]>([]);
const isSubmitting = ref(false);
const canUploadFiles = ref(true);
const attachments = ref<Documento[]>([]);
const lastAutoSave = ref<number | null>(null);
const filesToUpload = ref<File[]>([]);

// Não precisamos mais deste computed, pois usamos formState.isValid do composable

// Definir o schema de validação usando Zod
const riskSchema = z.object({
  name: z.string().min(3, 'O nome do risco deve ter pelo menos 3 caracteres'),
  description: z.string().min(10, 'A descrição deve ter pelo menos 10 caracteres'),
  impact: z.enum(['BAIXO', 'MEDIO', 'ALTO'], {
    errorMap: () => ({ message: 'Selecione um nível de impacto válido' })
  }),
  probability: z.enum(['BAIXA', 'MEDIA', 'ALTA'], {
    errorMap: () => ({ message: 'Selecione uma probabilidade válida' })
  }),
  status: z.enum(['IDENTIFICADO', 'EM_ANDAMENTO', 'MITIGADO', 'FECHADO'], {
    errorMap: () => ({ message: 'Selecione um status válido' })
  }),
  mitigation_plan: z.string().optional(),
  assignee: z.number().nullable(),
  project: z.number(),
});

// Valores iniciais do formulário
const initialFormData = {
  name: '',
  description: '',
  impact: 'MEDIO',
  probability: 'MEDIA',
  status: 'IDENTIFICADO',
  mitigation_plan: '',
  assignee: null,
  project: props.projectId,
};

// Usar o composable de validação de formulário
const { formState, updateField, validateForm, resetForm, saveForm } = useFormValidation({
  schema: riskSchema,
  initialData: initialFormData,
  onSave: saveRisk,
  autoSaveDebounce: 2000, // 2 segundos de debounce para auto-save
});

// Buscar membros da equipe do projeto
async function fetchProjectTeam() {
  try {
    const response = await teamService.getProjectTeamMembers(props.projectId);
    projectTeamMembers.value = response.data || [];
  } catch (error) {
    console.error('Erro ao buscar membros da equipe:', error);
    notify.error('Não foi possível carregar os membros da equipe');
  }
}

// Carregar anexos do risco
async function loadAttachments() {
  if (!props.risk?.id) return;
  
  try {
    const response = await documentService.getDocumentosByRisco(props.risk.id);
    attachments.value = response.data;
  } catch (error) {
    console.error('Erro ao carregar anexos:', error);
    notify.error('Não foi possível carregar os anexos do risco');
  }
}

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

// Lidar com arquivos selecionados para upload
function handleFilesSelected(files: File[]) {
  filesToUpload.value = [...filesToUpload.value, ...files];
}

// Remover um anexo existente
async function removeAttachment(attachmentId: number) {
  try {
    await documentService.deleteDocumento(attachmentId);
    attachments.value = attachments.value.filter(a => a.id !== attachmentId);
    notify.success('Anexo removido com sucesso');
  } catch (error) {
    console.error('Erro ao remover anexo:', error);
    notify.error('Não foi possível remover o anexo');
  }
}

// Função para fazer upload de arquivos
async function uploadRiskFiles(riskId: number) {
  if (filesToUpload.value.length === 0) return;
  
  const uploadPromises = filesToUpload.value.map(file => {
    const formData = new FormData();
    formData.append('arquivo', file);
    formData.append('nome', file.name);
    formData.append('tipo', file.type);
    formData.append('risco', riskId.toString());
    
    return documentService.createDocumento(formData);
  });
  
  try {
    await Promise.all(uploadPromises);
    notify.success(`${filesToUpload.value.length} arquivo(s) anexado(s) com sucesso`);
    filesToUpload.value = [];
    
    // Recarregar a lista de anexos
    if (riskId) {
      const response = await documentService.getDocumentosByRisco(riskId);
      attachments.value = response.data;
    }
  } catch (error) {
    console.error('Erro ao fazer upload de arquivos:', error);
    notify.error('Ocorreu um erro ao anexar um ou mais arquivos');
  }
}

// Salvar o risco (chamado pelo composable useFormValidation)
async function saveRisk(formData: any) {
  try {
    let riskId = props.risk?.id;
    let response;
    
    // Mapear os dados do formulário para o formato esperado pela API
    const riskData = {
      nome: formData.name,
      descricao: formData.description,
      impacto: formData.impact,
      probabilidade: formData.probability,
      status: formData.status,
      plano_mitigacao: formData.mitigation_plan,
      responsavel: formData.assignee,
      projeto: formData.project,
    };
    
    if (!props.risk) {
      // Criar novo risco
      response = await riskService.createRisco(riskData);
      riskId = response.data.id;
      notify.success('Risco criado com sucesso!');
    } else {
      // Atualizar risco existente
      response = await riskService.updateRisco(props.risk.id, riskData);
      riskId = props.risk.id;
      notify.success('Risco atualizado com sucesso!');
    }
    
    // Upload de arquivos se houver
    if (riskId && filesToUpload.value.length > 0) {
      await uploadRiskFiles(riskId);
    }
    
    lastAutoSave.value = Date.now();
    return response.data;
  } catch (error) {
    console.error('Erro ao salvar risco:', error);
    notify.error('Ocorreu um erro ao salvar o risco');
    throw error;
  }
}

// Enviar o formulário manualmente
async function submitForm() {
  try {
    isSubmitting.value = true;
    const isValid = await validateForm();
    if (!isValid) return;
    
    const savedData = await saveForm();
    emit('submit', savedData);
  } catch (error) {
    console.error('Erro ao enviar formulário:', error);
    notify.error('Ocorreu um erro ao enviar o formulário');
  } finally {
    isSubmitting.value = false;
  }
}

// Cancelar o formulário
function cancelForm() {
  emit('cancel');
}

// Inicializar o formulário com os dados do risco
function initForm() {
  if (props.risk) {
    resetForm({
      name: props.risk.nome || '',
      description: props.risk.descricao || '',
      impact: props.risk.impacto || 'MEDIO',
      probability: props.risk.probabilidade || 'MEDIA',
      status: props.risk.status || 'IDENTIFICADO',
      mitigation_plan: props.risk.plano_mitigacao || '',
      assignee: props.risk.responsavel?.id || null,
      project: props.projectId,
    });
  }
}

// Observar mudanças no risco para atualizar o formulário
watch(() => props.risk, () => {
  if (props.risk) {
    initForm();
    loadAttachments();
  }
}, { immediate: true });

// Inicializar
onMounted(() => {
  fetchProjectTeam();
  checkPermissions();
  if (props.risk) {
    loadAttachments();
  }
});
</script>
