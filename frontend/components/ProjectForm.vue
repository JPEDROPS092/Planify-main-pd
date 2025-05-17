<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
      <!-- Nome do Projeto -->
      <div class="col-span-2">
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome do Projeto</label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
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

      <!-- Data de Início -->
      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Início</label>
        <input
          id="start_date"
          v-model="form.start_date"
          type="date"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.start_date" class="mt-1 text-sm text-red-600">{{ errors.start_date }}</p>
      </div>

      <!-- Data de Término -->
      <div>
        <label for="end_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Data de Término</label>
        <input
          id="end_date"
          v-model="form.end_date"
          type="date"
          required
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.end_date" class="mt-1 text-sm text-red-600">{{ errors.end_date }}</p>
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
          <option value="PLANEJAMENTO">Planejamento</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="CONCLUIDO">Concluído</option>
          <option value="PAUSADO">Pausado</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
        <p v-if="errors.status" class="mt-1 text-sm text-red-600">{{ errors.status }}</p>
      </div>

      <!-- Orçamento -->
      <div>
        <label for="budget" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Orçamento (R$)</label>
        <input
          id="budget"
          v-model="form.budget"
          type="number"
          min="0"
          step="0.01"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading"
        />
        <p v-if="errors.budget" class="mt-1 text-sm text-red-600">{{ errors.budget }}</p>
      </div>

      <!-- Gerente do Projeto -->
      <div v-if="!isCreating">
        <label for="manager" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Gerente do Projeto</label>
        <select
          id="manager"
          v-model="form.manager"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
          :disabled="loading || !isManager"
        >
          <option v-for="user in users" :key="user.id" :value="user.id">{{ user.name }}</option>
        </select>
        <p v-if="errors.manager" class="mt-1 text-sm text-red-600">{{ errors.manager }}</p>
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
        {{ isCreating ? 'Criar Projeto' : 'Salvar Alterações' }}
      </LoadingButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProjectService } from '~/services/api/projects'
import type { Projeto } from '~/services/api/types'
import { useUserService } from '~/services/api/auth'
import type { User } from '~/services/api/types'
import { useNotification } from '~/composables/useNotification'
import LoadingButton from './LoadingButton.vue'

const props = defineProps({
  project: {
    type: Object as () => Projeto | null,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

    const projectService = useProjectService()
    const userService = useUserService()
    const notify = useNotification()
    
    const users = ref<any[]>([])
    const isManager = ref(true)
    const errors = ref<Record<string, string>>({})
    
    // Formulário
    const form = ref({
      name: '',
      description: '',
      start_date: new Date().toISOString().split('T')[0],
      end_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      status: 'PLANEJADO',
      prioridade: 'MEDIA',
      manager: undefined
    })
    
    // Verificar se estamos criando ou editando
    const isCreating = computed(() => !props.project?.id)
    
    // Validação do formulário
    const isFormValid = computed(() => {
      return (
        !!form.value.name &&
        !!form.value.description &&
        !!form.value.start_date &&
        !!form.value.end_date &&
        !!form.value.status &&
        new Date(form.value.start_date) <= new Date(form.value.end_date)
      )
    })
    
    // Carregar usuários para o select de gerente
    const loadUsers = async () => {
      try {
        const response = await userService.getAll()
        users.value = response
      } catch (error) {
        notify.showApiError(error)
      }
    }
    
    // Verificar permissões do usuário atual
    const checkPermissions = async () => {
      try {
        const currentUser = await userService.getCurrentUser()
        
        // Se estamos editando, verificar se o usuário é gerente do projeto
        if (!isCreating.value && props.project) {
          isManager.value = props.project.manager === currentUser.id || currentUser.is_staff
        }
      } catch (error) {
        console.error('Erro ao verificar permissões:', error)
      }
    }
    
    // Inicializar o formulário com os dados do projeto
    const initForm = () => {
      if (props.project) {
        form.value = { ...props.project }
        
        // Garantir que as datas estejam no formato correto
        if (form.value.start_date) {
          form.value.start_date = new Date(form.value.start_date).toISOString().split('T')[0]
        }
        
        if (form.value.end_date) {
          form.value.end_date = new Date(form.value.end_date).toISOString().split('T')[0]
        }
      }
    }
    
    // Validar o formulário
    const validateForm = () => {
      errors.value = {}
      
      if (!form.value.name) {
        errors.value.name = 'O nome do projeto é obrigatório'
      }
      
      if (!form.value.description) {
        errors.value.description = 'A descrição é obrigatória'
      }
      
      if (!form.value.start_date) {
        errors.value.start_date = 'A data de início é obrigatória'
      }
      
      if (!form.value.end_date) {
        errors.value.end_date = 'A data de término é obrigatória'
      }
      
      if (form.value.start_date && form.value.end_date) {
        const startDate = new Date(form.value.start_date)
        const endDate = new Date(form.value.end_date)
        
        if (startDate > endDate) {
          errors.value.end_date = 'A data de término deve ser posterior à data de início'
        }
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
    
    // Inicializar
    onMounted(() => {
      initForm()
      loadUsers()
      checkPermissions()
    })
</script>
