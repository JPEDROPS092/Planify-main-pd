<!--
  TaskForm.vue
  
  Formulário de tarefas com validação em tempo real, auto-save com debounce,
  upload de arquivos e campos dinâmicos baseados em permissões.
  
  Props:
  - task: Tarefa existente para edição
  - projectId: ID do projeto associado
  - loading: Estado de carregamento
  
  Eventos:
  - submit: Emitido quando o formulário é enviado
  - cancel: Emitido quando o formulário é cancelado
-->

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { z } from 'zod'
import { useFormValidation } from '~/stores/composables/useFormValidation'
import { useAuth } from '~/stores/composables/useAuth'
import { useApiService } from '~/stores/composables/useApiService'
import { useTaskService } from '~/services/api/services/taskService'
import { useTeamService } from '~/services/api/services/teamService'
import { useDocumentService } from '~/services/api/services/documentService'
import Button from '~/components/ui/input/button/Button.vue'
import LoadingButton from '~/components/shared/feedback/loading'
import FileUploader from '~/components/ui/input/file-uploader/FileUploader.vue'
import { useNotification } from '~/stores/composables/useNotification'
import type { Tarefa, User } from '@/services/utils/types'

const props = defineProps({
  task: {
    type: Object as () => Tarefa | null,
    default: null
  },
  projectId: {
    type: Number,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

// Composables
const { user, hasPermission } = useAuth()
const apiService = useApiService()
const notification = useNotification()

// Estados
const teamMembers = ref<Usuario[]>([])
const isLoadingMembers = ref(false)
const selectedFiles = ref<File[]>([])
const attachments = ref<{id: number, nome: string, url: string}[]>([])
const autoSaveEnabled = ref(true)
const lastAutoSave = ref<Date | null>(null)

// Permissões
const canAssignTasks = computed(() => hasPermission('tarefas.pode_atribuir'))
const canSetPriority = computed(() => hasPermission('tarefas.pode_definir_prioridade'))
const canUploadFiles = computed(() => hasPermission('documentos.pode_adicionar'))

// Esquema de validação
const taskSchema = z.object({
  titulo: z.string().min(3, 'O título deve ter pelo menos 3 caracteres'),
  descricao: z.string().min(10, 'A descrição deve ter pelo menos 10 caracteres'),
  data_inicio: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida'),
  data_fim: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida')
    .refine(data => !form.formData.value.data_inicio || data >= form.formData.value.data_inicio, {
      message: 'A data de término deve ser posterior à data de início',
    }),
  status: z.enum(['PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA', 'ATRASADA']),
  prioridade: z.enum(['BAIXA', 'MEDIA', 'ALTA', 'CRITICA']),
  responsavel: z.number().nullable(),
  projeto: z.number(),
})

// Estado inicial do formulário
const initialData = {
  titulo: '',
  descricao: '',
  data_inicio: new Date().toISOString().split('T')[0],
  data_fim: '',
  status: 'PENDENTE',
  prioridade: 'MEDIA',
  responsavel: null,
  projeto: props.projectId,
}

// Configuração do formulário com validação e auto-save
const form = useFormValidation({
  initialData,
  schema: taskSchema,
  onSave: autoSaveTask,
  autoSave: autoSaveEnabled,
  debounceValidation: 300,
  debounceSave: 2000
})

// Carregar membros do projeto
async function loadProjectMembers() {
  if (!props.projectId) return
  
  isLoadingMembers.value = true
  try {
    const response = await apiService.get(`/api/projetos/${props.projectId}/membros/`)
    teamMembers.value = response.data
  } catch (error) {
    console.error('Erro ao carregar membros do projeto:', error)
  } finally {
    isLoadingMembers.value = false
  }
}

// Carregar anexos existentes
async function loadAttachments() {
  if (!props.task?.id) return
  
  try {
    const response = await apiService.get(`/api/tarefas/${props.task.id}/documentos/`)
    attachments.value = response.data
  } catch (error) {
    console.error('Erro ao carregar anexos:', error)
  }
}

// Auto-save da tarefa
async function autoSaveTask(data: typeof initialData) {
  if (!props.task?.id) return
  
  try {
    await apiService.patch(`/api/tarefas/${props.task.id}/`, data)
    lastAutoSave.value = new Date()
  } catch (error) {
    console.error('Erro ao auto-salvar tarefa:', error)
    throw error
  }
}

// Enviar formulário
async function submitForm() {
  if (!form.validateForm()) return
  
  // Desativar auto-save durante o envio manual
  autoSaveEnabled.value = false
  
  try {
    // Preparar dados para envio
    const formData = { ...form.formData.value }
    
    // Enviar formulário
    emit('submit', { formData, files: selectedFiles.value })
    
    // Resetar arquivos selecionados após envio
    selectedFiles.value = []
  } catch (error) {
    console.error('Erro ao enviar formulário:', error)
    notification.error('Erro ao salvar tarefa')
  } finally {
    // Reativar auto-save
    autoSaveEnabled.value = true
  }
}

// Cancelar formulário
function cancelForm() {
  emit('cancel')
}

// Manipular arquivos selecionados
function handleFilesSelected(files: File[]) {
  selectedFiles.value = files
}

// Remover anexo existente
async function removeAttachment(attachmentId: number) {
  try {
    await apiService.delete(`/api/documentos/${attachmentId}/`)
    attachments.value = attachments.value.filter(a => a.id !== attachmentId)
    notification.success('Anexo removido com sucesso')
  } catch (error) {
    console.error('Erro ao remover anexo:', error)
    notification.error('Erro ao remover anexo')
  }
}

// Observar mudanças na prop task
watch(() => props.task, (newTask) => {
  if (newTask) {
    // Preencher formulário com dados da tarefa
    form.formData.value = {
      titulo: newTask.titulo || '',
      descricao: newTask.descricao || '',
      data_inicio: newTask.data_inicio || new Date().toISOString().split('T')[0],
      data_fim: newTask.data_fim || '',
      status: newTask.status || 'PENDENTE',
      prioridade: newTask.prioridade || 'MEDIA',
      responsavel: newTask.responsavel?.id || null,
      projeto: newTask.projeto?.id || props.projectId,
    }
    
    // Carregar anexos se a tarefa existir
    loadAttachments()
  } else {
    // Resetar formulário
    form.resetForm()
    form.formData.value.projeto = props.projectId
    attachments.value = []
  }
}, { immediate: true, deep: true })

// Inicialização
onMounted(() => {
  loadProjectMembers()
})
</script>

<template>
  <form @submit.prevent="submitForm" class="space-y-6">
    <!-- Indicador de status do formulário -->
    <div v-if="form.isDirty || form.isSaving || form.isSaved || form.hasError"
         class="flex items-center justify-end text-sm mb-2"
         :class="{
           'text-yellow-600 dark:text-yellow-400': form.isDirty && !form.isSaving && !form.isSaved && !form.hasError,
           'text-blue-600 dark:text-blue-400': form.isSaving,
           'text-green-600 dark:text-green-400': form.isSaved && !form.isDirty,
           'text-red-600 dark:text-red-400': form.hasError
         }">
      <span v-if="form.isSaving">Salvando...</span>
      <span v-else-if="form.isSaved && !form.isDirty">
        Salvo automaticamente {{ lastAutoSave ? new Date(lastAutoSave).toLocaleTimeString() : '' }}
      </span>
      <span v-else-if="form.hasError">Erro ao salvar</span>
      <span v-else-if="form.isDirty">Não salvo</span>
    </div>
    
    <!-- Título da tarefa -->
    <div>
      <label for="task-title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Título da Tarefa</label>
      <input 
        type="text" 
        id="task-title" 
        v-model="form.formData.titulo" 
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        :class="{'border-red-500 dark:border-red-400': form.errors.titulo}"
        aria-describedby="title-error"
      />
      <p v-if="form.errors.titulo" id="title-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.titulo }}</p>
    </div>
    
    <!-- Descrição da tarefa -->
    <div>
      <label for="task-description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Descrição</label>
      <textarea 
        id="task-description" 
        v-model="form.formData.descricao" 
        rows="4"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        :class="{'border-red-500 dark:border-red-400': form.errors.descricao}"
        aria-describedby="description-error"
      ></textarea>
      <p v-if="form.errors.descricao" id="description-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.descricao }}</p>
    </div>
    
    <!-- Datas de início e fim -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="task-start-date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Início</label>
        <input 
          type="date" 
          id="task-start-date" 
          v-model="form.formData.data_inicio"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          :class="{'border-red-500 dark:border-red-400': form.errors.data_inicio}"
          aria-describedby="start-date-error"
        />
        <p v-if="form.errors.data_inicio" id="start-date-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.data_inicio }}</p>
      </div>
      
      <div>
        <label for="task-end-date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Término</label>
        <input 
          type="date" 
          id="task-end-date" 
          v-model="form.formData.data_fim"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          :class="{'border-red-500 dark:border-red-400': form.errors.data_fim}"
          aria-describedby="end-date-error"
        />
        <p v-if="form.errors.data_fim" id="end-date-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.data_fim }}</p>
      </div>
    </div>
    
    <!-- Status e Prioridade -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label for="task-status" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
        <select 
          id="task-status" 
          v-model="form.formData.status"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          :class="{'border-red-500 dark:border-red-400': form.errors.status}"
          aria-describedby="status-error"
        >
          <option value="PENDENTE">Pendente</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="CONCLUIDA">Concluída</option>
          <option value="ATRASADA">Atrasada</option>
        </select>
        <p v-if="form.errors.status" id="status-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.status }}</p>
      </div>
      
      <div>
        <label for="task-priority" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Prioridade</label>
        <select 
          id="task-priority" 
          v-model="form.formData.prioridade"
          :disabled="!canSetPriority"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
          :class="{
            'border-red-500 dark:border-red-400': form.errors.prioridade,
            'opacity-60 cursor-not-allowed': !canSetPriority
          }"
          aria-describedby="priority-error"
        >
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
          <option value="CRITICA">Crítica</option>
        </select>
        <p v-if="form.errors.prioridade" id="priority-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.prioridade }}</p>
        <p v-if="!canSetPriority" class="mt-1 text-xs text-gray-500 dark:text-gray-400">Você não tem permissão para definir a prioridade</p>
      </div>
    </div>
    
    <!-- Responsável -->
    <div>
      <label for="task-assignee" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Responsável</label>
      <select 
        id="task-assignee" 
        v-model="form.formData.responsavel"
        :disabled="!canAssignTasks || isLoadingMembers"
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        :class="{
          'border-red-500 dark:border-red-400': form.errors.responsavel,
          'opacity-60 cursor-not-allowed': !canAssignTasks || isLoadingMembers
        }"
        aria-describedby="assignee-error"
      >
        <option :value="null">Sem responsável</option>
        <option v-for="member in teamMembers" :key="member.id" :value="member.id">
          {{ member.nome }} ({{ member.email }})
        </option>
      </select>
      <p v-if="form.errors.responsavel" id="assignee-error" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ form.errors.responsavel }}</p>
      <p v-if="isLoadingMembers" class="mt-1 text-xs text-gray-500 dark:text-gray-400">Carregando membros da equipe...</p>
      <p v-else-if="!canAssignTasks" class="mt-1 text-xs text-gray-500 dark:text-gray-400">Você não tem permissão para atribuir tarefas</p>
    </div>
    
    <!-- Upload de arquivos -->
    <div v-if="canUploadFiles">
      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Anexos</label>
      
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
        :max-size="10 * 1024 * 1024" 
        :max-files="5"
        @files-selected="handleFilesSelected"
        class="border-dashed border-2 border-gray-300 dark:border-gray-600 rounded-lg p-4"
      ></FileUploader>
    </div>
    
    <!-- Botões de ação -->
    <div class="flex justify-end space-x-3 pt-4">
      <Button type="button" variant="outline" @click="cancelForm">Cancelar</Button>
      <LoadingButton 
        type="submit" 
        :loading="props.loading || form.isSaving" 
        :disabled="!form.isValid || props.loading || form.isSaving"
      >
        {{ props.task && props.task.id ? 'Salvar Alterações' : 'Criar Tarefa' }}
      </LoadingButton>
    </div>
  </form>
</template>