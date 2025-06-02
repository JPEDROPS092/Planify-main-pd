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
    
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
      <!-- Nome do Projeto -->
      <div class="col-span-2">
        <label
          for="name"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Nome do Projeto</label
        >
        <input
          id="name"
          v-model="formState.formData.name"
          type="text"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.name}"
          :disabled="loading"
          aria-describedby="name-error"
        />
        <p v-if="formState.errors.name" id="name-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.name }}
        </p>
      </div>

      <!-- Descrição -->
      <div class="col-span-2">
        <label
          for="description"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Descrição</label
        >
        <textarea
          id="description"
          v-model="formState.formData.description"
          rows="3"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.description}"
          :disabled="loading"
          aria-describedby="description-error"
        ></textarea>
        <p v-if="formState.errors.description" id="description-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.description }}
        </p>
      </div>

      <!-- Data de Início -->
      <div>
        <label
          for="start_date"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Data de Início</label
        >
        <input
          id="start_date"
          v-model="formState.formData.start_date"
          type="date"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.start_date}"
          :disabled="loading"
          aria-describedby="start-date-error"
        />
        <p v-if="formState.errors.start_date" id="start-date-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.start_date }}
        </p>
      </div>

      <!-- Data de Término -->
      <div>
        <label
          for="end_date"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Data de Término</label
        >
        <input
          id="end_date"
          v-model="formState.formData.end_date"
          type="date"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.end_date}"
          :disabled="loading"
          aria-describedby="end-date-error"
        />
        <p v-if="formState.errors.end_date" id="end-date-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.end_date }}
        </p>
      </div>

      <!-- Status -->
      <div>
        <label
          for="status"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Status</label
        >
        <select
          id="status"
          v-model="formState.formData.status"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.status}"
          :disabled="loading"
          aria-describedby="status-error"
        >
          <option value="PLANEJAMENTO">Planejamento</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="CONCLUIDO">Concluído</option>
          <option value="PAUSADO">Pausado</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
        <p v-if="formState.errors.status" id="status-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.status }}
        </p>
      </div>

      <!-- Orçamento -->
      <div>
        <label
          for="budget"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Orçamento (R$)</label
        >
        <input
          id="budget"
          v-model="formState.formData.budget"
          type="number"
          min="0"
          step="0.01"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.budget}"
          :disabled="loading"
          aria-describedby="budget-error"
        />
        <p v-if="formState.errors.budget" id="budget-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.budget }}
        </p>
      </div>

      <!-- Gerente do Projeto -->
      <div v-if="!isCreating">
        <label
          for="manager"
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Gerente do Projeto</label
        >
        <select
          id="manager"
          v-model="formState.formData.manager"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :class="{'border-red-500 dark:border-red-400': formState.errors.manager}"
          :disabled="loading || !isManager"
          aria-describedby="manager-error"
        >
          <option :value="null">Selecione um gerente</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name }}
          </option>
        </select>
        <p v-if="formState.errors.manager" id="manager-error" class="mt-1 text-sm text-red-600 dark:text-red-400">
          {{ formState.errors.manager }}
        </p>
        <p v-if="!isManager" class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Você não tem permissão para alterar o gerente do projeto
        </p>
      </div>
    </div>

    <!-- Upload de arquivos -->
    <div v-if="canUploadFiles">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Documentos do Projeto</label>
      
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
      ></FileUploader>
    </div>

    <!-- Botões -->
    <div class="flex justify-end space-x-3">
      <Button
        type="button"
        variant="outline"
        @click="$emit('cancel')"
        :disabled="loading"
      >
        Cancelar
      </Button>
      <LoadingButton
        type="submit"
        :loading="loading || formState.isSaving"
        :disabled="!formState.isValid || loading || formState.isSaving"
      >
        {{ isCreating ? 'Criar Projeto' : 'Salvar Alterações' }}
      </LoadingButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { z } from 'zod';
import { useProjectService } from '~/services/api/services/projectService';
import { useDocumentService } from '~/services/api/services/documentService';
import type { Projeto, Documento } from '~/services/utils/types.ts';
import { useUserService } from '~/services/api/services/userService';
import type { User } from '~/services/utils/types.ts';
import { useNotification } from '~/stores/composables/useNotification';
import { useFormValidation } from '~/stores/composables/useFormValidation';
import { useAuth } from '~/stores/composables/useAuth';
import LoadingButton from '~/components/shared/feedback/loading'
import Button from '~/components/ui/input';
import FileUploader from '~/components/ui/input/file-uploader/FileUploader.vue'
const props = defineProps({
  project: {
    type: Object as () => Projeto | null,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['submit', 'cancel']);

const projectService = useProjectService();
const userService = useUserService();
const documentService = useDocumentService();
const notify = useNotification();
const { user } = useAuth();

const users = ref<User[]>([]);
const isManager = ref(true);
const canUploadFiles = ref(true);
const attachments = ref<Documento[]>([]);
const lastAutoSave = ref<number | null>(null);
const filesToUpload = ref<File[]>([]);
const errors = ref<Record<string, string>>({});

// Formulário
// Definir o schema de validação usando Zod
const projectSchema = z.object({
  name: z.string().min(3, 'O nome do projeto deve ter pelo menos 3 caracteres'),
  description: z.string().min(10, 'A descrição deve ter pelo menos 10 caracteres'),
  start_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida'),
  end_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida')
    .refine(data => !formState.formData.start_date || data >= formState.formData.start_date, {
      message: 'A data de término deve ser posterior à data de início',
    }),
  status: z.enum(['PLANEJAMENTO', 'EM_ANDAMENTO', 'CONCLUIDO', 'PAUSADO', 'CANCELADO']),
  budget: z.coerce.number().min(0, 'O orçamento não pode ser negativo'),
  manager: z.number().nullable(),
});

// Valores iniciais do formulário
const initialFormData = {
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'PLANEJAMENTO',
  budget: 0,
  manager: null,
};

// Usar o composable de validação de formulário
const { formState, updateField, validateForm, resetForm, saveForm } = useFormValidation({
  schema: projectSchema,
  initialData: initialFormData,
  onSave: saveProject,
  autoSaveDebounce: 2000, // 2 segundos de debounce para auto-save
});

const isCreating = computed(() => !props.project);

// Carregar usuários para o select de gerente
async function loadUsers() {
  try {
    const response = await userService.getUsers();
    users.value = response.data;
  } catch (error) {
    console.error('Erro ao carregar usuários:', error);
    notify.error('Não foi possível carregar a lista de usuários');
  }
}

// Carregar anexos do projeto
async function loadAttachments() {
  if (!props.project?.id) return;
  
  try {
    const response = await documentService.getDocumentosByProjeto(props.project.id);
    attachments.value = response.data;
  } catch (error) {
    console.error('Erro ao carregar anexos:', error);
    notify.error('Não foi possível carregar os anexos do projeto');
  }
}

// Verificar permissões do usuário atual
async function checkPermissions() {
  if (!user.value) return;
  
  try {
    // Verificar se o usuário é gerente ou admin
    isManager.value = ['ADMIN', 'GERENTE'].includes(user.value.role);
    
    // Verificar se o usuário pode fazer upload de arquivos
    canUploadFiles.value = ['ADMIN', 'GERENTE', 'MEMBRO'].includes(user.value.role);
  } catch (error) {
    console.error('Erro ao verificar permissões:', error);
    isManager.value = false;
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

// Inicializar o formulário com os dados do projeto
function initForm() {
  if (props.project) {
    resetForm({
      name: props.project.nome || '',
      description: props.project.descricao || '',
      start_date: props.project.data_inicio || '',
      end_date: props.project.data_fim || '',
      status: props.project.status || 'PLANEJAMENTO',
      budget: props.project.orcamento || 0,
      manager: props.project.gerente?.id || null,
    });
  }
}

// Função para fazer upload de arquivos
async function uploadProjectFiles(projectId: number) {
  if (filesToUpload.value.length === 0) return;
  
  const uploadPromises = filesToUpload.value.map(file => {
    const formData = new FormData();
    formData.append('arquivo', file);
    formData.append('nome', file.name);
    formData.append('tipo', file.type);
    formData.append('projeto', projectId.toString());
    
    return documentService.createDocumento(formData);
  });
  
  try {
    await Promise.all(uploadPromises);
    notify.success(`${filesToUpload.value.length} arquivo(s) anexado(s) com sucesso`);
    filesToUpload.value = [];
    
    // Recarregar a lista de anexos
    if (projectId) {
      const response = await documentService.getDocumentosByProjeto(projectId);
      attachments.value = response.data;
    }
  } catch (error) {
    console.error('Erro ao fazer upload de arquivos:', error);
    notify.error('Ocorreu um erro ao anexar um ou mais arquivos');
  }
};

// Salvar o projeto (chamado pelo composable useFormValidation)
async function saveProject(formData: any) {
  try {
    let projectId = props.project?.id;
    let response;
    
    // Mapear os dados do formulário para o formato esperado pela API
    const projectData = {
      nome: formData.name,
      descricao: formData.description,
      data_inicio: formData.start_date,
      data_fim: formData.end_date,
      status: formData.status,
      orcamento: formData.budget,
      gerente: formData.manager,
    };
    
    if (isCreating.value) {
      // Criar novo projeto
      response = await projectService.createProjeto(projectData);
      projectId = response.data.id;
      notify.success('Projeto criado com sucesso!');
    } else {
      // Atualizar projeto existente
      response = await projectService.updateProjeto(props.project!.id, projectData);
      projectId = props.project!.id;
      notify.success('Projeto atualizado com sucesso!');
    }
    
    // Upload de arquivos se houver
    if (projectId && filesToUpload.value.length > 0) {
      await uploadProjectFiles(projectId);
    }
    
    lastAutoSave.value = Date.now();
    return response.data;
  } catch (error) {
    console.error('Erro ao salvar projeto:', error);
    notify.error('Ocorreu um erro ao salvar o projeto');
    throw error;
  }
}

// Enviar o formulário manualmente
async function submitForm() {
  try {
    const isValid = await validateForm();
    if (!isValid) return;
    
    const savedData = await saveForm();
    emit('submit', savedData);
  } catch (error) {
    console.error('Erro ao enviar formulário:', error);
  }
}

// Observar mudanças no projeto para atualizar o formulário
watch(() => props.project, () => {
  if (props.project) {
    initForm();
    loadAttachments();
  }
}, { immediate: true });

// Inicializar
onMounted(() => {
  loadUsers();
  checkPermissions();
  if (props.project) {
    loadAttachments();
  }
});
</script>
