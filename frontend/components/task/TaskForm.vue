<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div>
      <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Título</label>
      <input
        id="title"
        v-model="form.title"
        type="text"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
        :class="{ 'border-red-500': errors.title }"
        placeholder="Título da tarefa"
        required
      />
      <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
    </div>
    
    <div>
      <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Descrição</label>
      <textarea
        id="description"
        v-model="form.description"
        rows="3"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
        :class="{ 'border-red-500': errors.description }"
        placeholder="Descrição da tarefa"
      ></textarea>
      <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Início</label>
        <input
          id="start_date"
          v-model="form.start_date"
          type="date"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          :class="{ 'border-red-500': errors.start_date }"
          required
        />
        <p v-if="errors.start_date" class="mt-1 text-sm text-red-600">{{ errors.start_date }}</p>
      </div>
      
      <div>
        <label for="due_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Término</label>
        <input
          id="due_date"
          v-model="form.due_date"
          type="date"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          :class="{ 'border-red-500': errors.due_date }"
          required
        />
        <p v-if="errors.due_date" class="mt-1 text-sm text-red-600">{{ errors.due_date }}</p>
      </div>
    </div>
    
    <div>
      <label for="status" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
      <select
        id="status"
        v-model="form.status"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
        :class="{ 'border-red-500': errors.status }"
        required
      >
        <option value="todo">A Fazer</option>
        <option value="in_progress">Em Progresso</option>
        <option value="review">Em Revisão</option>
        <option value="done">Concluída</option>
      </select>
      <p v-if="errors.status" class="mt-1 text-sm text-red-600">{{ errors.status }}</p>
    </div>
    
    <div>
      <label for="priority" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Prioridade</label>
      <select
        id="priority"
        v-model="form.priority"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
        :class="{ 'border-red-500': errors.priority }"
        required
      >
        <option value="low">Baixa</option>
        <option value="medium">Média</option>
        <option value="high">Alta</option>
        <option value="critical">Crítica</option>
      </select>
      <p v-if="errors.priority" class="mt-1 text-sm text-red-600">{{ errors.priority }}</p>
    </div>
    
    <div>
      <label for="assigned_to" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Responsável</label>
      <select
        id="assigned_to"
        v-model="form.assigned_to"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
        :class="{ 'border-red-500': errors.assigned_to }"
      >
        <option value="">Selecione um responsável</option>
        <option v-for="member in projectMembers" :key="member.id" :value="member.id">
          {{ member.name || member.username }}
        </option>
      </select>
      <p v-if="errors.assigned_to" class="mt-1 text-sm text-red-600">{{ errors.assigned_to }}</p>
    </div>
    
    <div class="flex justify-end space-x-3 pt-4">
      <button
        type="button"
        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600"
        @click="$emit('cancel')"
      >
        Cancelar
      </button>
      <button
        type="submit"
        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:bg-primary-700 dark:hover:bg-primary-600"
        :disabled="isLoading"
      >
        <span v-if="isLoading" class="flex items-center">
          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Salvando...
        </span>
        <span v-else>{{ task ? 'Atualizar' : 'Criar' }} Tarefa</span>
      </button>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed, watch } from 'vue'
import { useTaskService } from '~/services/taskService'
import { useUserService } from '~/services/userService'
import { useNotification } from '~/composables/useNotification'
import { useAuth } from '~/composables/useAuth'

export default defineComponent({
  name: 'TaskForm',
  
  props: {
    task: {
      type: Object,
      default: null
    },
    projectId: {
      type: [Number, String],
      required: true
    }
  },
  
  emits: ['created', 'updated', 'cancel'],
  
  setup(props, { emit }) {
    const taskService = useTaskService()
    const userService = useUserService()
    const notification = useNotification()
    const { user } = useAuth()
    
    const isLoading = ref(false)
    const projectMembers = ref([])
    const errors = ref({})
    
    // Formulário
    const form = ref({
      title: '',
      description: '',
      start_date: new Date().toISOString().split('T')[0],
      due_date: '',
      status: 'todo',
      priority: 'medium',
      assigned_to: '',
      project: props.projectId
    })
    
    // Carregar membros do projeto
    const loadProjectMembers = async () => {
      try {
        const members = await userService.fetchUsers()
        projectMembers.value = members
      } catch (error) {
        notification.error('Erro ao carregar membros do projeto')
        console.error('Erro ao carregar membros:', error)
      }
    }
    
    // Preencher o formulário se estiver editando uma tarefa existente
    const populateForm = () => {
      if (props.task) {
        form.value = {
          title: props.task.title || '',
          description: props.task.description || '',
          start_date: props.task.start_date ? new Date(props.task.start_date).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
          due_date: props.task.due_date ? new Date(props.task.due_date).toISOString().split('T')[0] : '',
          status: props.task.status || 'todo',
          priority: props.task.priority || 'medium',
          assigned_to: props.task.assigned_to?.id || '',
          project: props.projectId
        }
      }
    }
    
    // Validar o formulário
    const validateForm = () => {
      const newErrors = {}
      
      if (!form.value.title.trim()) {
        newErrors.title = 'O título é obrigatório'
      }
      
      if (!form.value.start_date) {
        newErrors.start_date = 'A data de início é obrigatória'
      }
      
      if (!form.value.due_date) {
        newErrors.due_date = 'A data de término é obrigatória'
      } else if (new Date(form.value.due_date) < new Date(form.value.start_date)) {
        newErrors.due_date = 'A data de término deve ser posterior à data de início'
      }
      
      errors.value = newErrors
      return Object.keys(newErrors).length === 0
    }
    
    // Enviar o formulário
    const handleSubmit = async () => {
      if (!validateForm()) return
      
      isLoading.value = true
      
      try {
        const taskData = {
          ...form.value,
          project: props.projectId
        }
        
        let result
        
        if (props.task) {
          // Atualizar tarefa existente
          result = await taskService.updateTask(props.task.id, taskData)
          notification.success('Tarefa atualizada com sucesso')
          emit('updated', result)
        } else {
          // Criar nova tarefa
          result = await taskService.createTask(taskData)
          notification.success('Tarefa criada com sucesso')
          emit('created', result)
        }
        
        // Limpar formulário após criação
        if (!props.task) {
          form.value = {
            title: '',
            description: '',
            start_date: new Date().toISOString().split('T')[0],
            due_date: '',
            status: 'todo',
            priority: 'medium',
            assigned_to: '',
            project: props.projectId
          }
        }
      } catch (error) {
        notification.error('Erro ao salvar tarefa')
        console.error('Erro ao salvar tarefa:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    // Carregar dados iniciais
    onMounted(() => {
      loadProjectMembers()
      populateForm()
    })
    
    // Atualizar formulário quando a tarefa mudar
    watch(() => props.task, () => {
      populateForm()
    })
    
    return {
      form,
      errors,
      isLoading,
      projectMembers,
      handleSubmit
    }
  }
})
</script>
