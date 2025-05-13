<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
      <!-- Título da Tarefa -->
      <div class="col-span-2">
        <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Título da Tarefa</label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
      </div>

      <!-- Descrição -->
      <div class="col-span-2">
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Descrição</label>
        <textarea
          id="description"
          v-model="form.description"
          rows="3"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        ></textarea>
        <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
      </div>

      <!-- Projeto -->
      <div>
        <label for="project" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Projeto</label>
        <select
          id="project"
          v-model="form.project"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading || projectFixed"
          @change="loadProjectMembers"
        >
          <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
        </select>
        <p v-if="errors.project" class="mt-1 text-sm text-red-600">{{ errors.project }}</p>
      </div>

      <!-- Responsável -->
      <div>
        <label for="assigned_to" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Responsável</label>
        <select
          id="assigned_to"
          v-model="form.assigned_to"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading || !projectMembers.length"
        >
          <option :value="null">Selecione um responsável</option>
          <option v-for="member in projectMembers" :key="member.id" :value="member.id">{{ member.name }}</option>
        </select>
        <p v-if="errors.assigned_to" class="mt-1 text-sm text-red-600">{{ errors.assigned_to }}</p>
      </div>

      <!-- Status -->
      <div>
        <label for="status" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
        <select
          id="status"
          v-model="form.status"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        >
          <option value="PENDENTE">Pendente</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="CONCLUIDA">Concluída</option>
          <option value="BLOQUEADA">Bloqueada</option>
          <option value="CANCELADA">Cancelada</option>
        </select>
        <p v-if="errors.status" class="mt-1 text-sm text-red-600">{{ errors.status }}</p>
      </div>

      <!-- Prioridade -->
      <div>
        <label for="priority" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Prioridade</label>
        <select
          id="priority"
          v-model="form.priority"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        >
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
          <option value="URGENTE">Urgente</option>
        </select>
        <p v-if="errors.priority" class="mt-1 text-sm text-red-600">{{ errors.priority }}</p>
      </div>

      <!-- Data de Vencimento -->
      <div>
        <label for="due_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Vencimento</label>
        <input
          id="due_date"
          v-model="form.due_date"
          type="date"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.due_date" class="mt-1 text-sm text-red-600">{{ errors.due_date }}</p>
      </div>

      <!-- Horas Estimadas -->
      <div>
        <label for="estimated_hours" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Horas Estimadas</label>
        <input
          id="estimated_hours"
          v-model="form.estimated_hours"
          type="number"
          min="0"
          step="0.5"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.estimated_hours" class="mt-1 text-sm text-red-600">{{ errors.estimated_hours }}</p>
      </div>
    </div>

    <!-- Botões -->
    <div class="flex justify-end space-x-3">
      <button
        type="button"
        class="inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
        @click="$emit('cancel')"
        :disabled="loading"
      >
        Cancelar
      </button>
      <LoadingButton
        type="submit"
        variant="primary"
        :loading="loading"
        :disabled="!isFormValid"
      >
        {{ isCreating ? 'Criar Tarefa' : 'Salvar Alterações' }}
      </LoadingButton>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue'
import { useTaskService } from '~/services/taskService'
import type { Task } from '~/services/taskService'
import { useProjectService } from '~/services/projectService'
import type { Project } from '~/services/projectService'
import { useUserService } from '~/services/userService'
import type { User } from '~/services/userService'
import { useNotification } from '~/composables/useNotification'
import LoadingButton from './LoadingButton.vue'

export default defineComponent({
  name: 'TaskForm',
  components: {
    LoadingButton
  },
  props: {
    task: {
      type: Object as () => Task | null,
      default: null
    },
    projectId: {
      type: Number,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit', 'cancel'],
  setup(props, { emit }) {
    const taskService = useTaskService()
    const projectService = useProjectService()
    const userService = useUserService()
    const notify = useNotification()
    
    const projects = ref<any[]>([])
    const projectMembers = ref<any[]>([])
    const errors = ref<Record<string, string>>({})
    
    // Verificar se o projeto está fixo (quando vem da prop projectId)
    const projectFixed = computed(() => !!props.projectId)
    
    // Formulário
    const form = ref<Task>({
      title: '',
      description: '',
      project: props.projectId || 0,
      status: 'PENDENTE',
      priority: 'MEDIA',
      due_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      estimated_hours: 0
    })
    
    // Verificar se estamos criando ou editando
    const isCreating = computed(() => !props.task?.id)
    
    // Validação do formulário
    const isFormValid = computed(() => {
      return (
        !!form.value.title &&
        !!form.value.description &&
        !!form.value.project &&
        !!form.value.status &&
        !!form.value.priority &&
        !!form.value.due_date
      )
    })
    
    // Carregar projetos
    const loadProjects = async () => {
      try {
        // Carregar apenas projetos do usuário atual
        const response = await projectService.getUserProjects()
        projects.value = response
        
        // Se não temos um projeto selecionado e temos projetos disponíveis, selecionar o primeiro
        if (!form.value.project && projects.value.length > 0) {
          form.value.project = projects.value[0].id
          await loadProjectMembers()
        }
      } catch (error) {
        notify.showApiError(error)
      }
    }
    
    // Carregar membros do projeto selecionado
    const loadProjectMembers = async () => {
      if (!form.value.project) return
      
      try {
        const projectDetails = await projectService.getById(form.value.project)
        
        if (projectDetails.team_members && projectDetails.team_members.length > 0) {
          // Carregar detalhes dos usuários
          const userPromises = projectDetails.team_members.map((userId: number) => userService.getById(userId))
          const users = await Promise.all(userPromises)
          projectMembers.value = users
          
          // Se não temos um responsável selecionado, definir o usuário atual como responsável
          if (!form.value.assigned_to) {
            const currentUser = await userService.getCurrentUser()
            if (projectDetails.team_members.includes(currentUser.id)) {
              form.value.assigned_to = currentUser.id
            }
          }
        } else {
          projectMembers.value = []
        }
      } catch (error) {
        notify.showApiError(error)
      }
    }
    
    // Inicializar o formulário com os dados da tarefa
    const initForm = () => {
      if (props.task) {
        form.value = { ...props.task }
        
        // Garantir que a data esteja no formato correto
        if (form.value.due_date) {
          form.value.due_date = new Date(form.value.due_date).toISOString().split('T')[0]
        }
      } else if (props.projectId) {
        form.value.project = props.projectId
      }
    }
    
    // Validar o formulário
    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.title) {
        errors.value.title = 'O título da tarefa é obrigatório'
      }
      
      if (!form.value.description) {
        errors.value.description = 'A descrição é obrigatória'
      }
      
      if (!form.value.project) {
        errors.value.project = 'O projeto é obrigatório'
      }
      
      if (!form.value.due_date) {
        errors.value.due_date = 'A data de vencimento é obrigatória'
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    // Enviar o formulário
    const handleSubmit = async () => {
      if (!validateForm()) return
      
      try {
        emit('submit', form.value)
      } catch (error) {
        notify.showApiError(error)
      }
    }
    
    // Observar mudanças no projeto selecionado
    watch(() => form.value.project, async () => {
      if (form.value.project) {
        await loadProjectMembers()
      }
    })
    
    // Inicializar
    onMounted(async () => {
      initForm()
      await loadProjects()
      
      if (form.value.project) {
        await loadProjectMembers()
      }
    })
    
    return {
      form,
      projects,
      projectMembers,
      projectFixed,
      errors,
      isCreating,
      isFormValid,
      loadProjectMembers,
      handleSubmit
    }
  }
})
</script>
