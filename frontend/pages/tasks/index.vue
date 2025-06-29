<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Minhas Tarefas</h1>
      <button
        @click="handleCreateTask"
        class="bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors"
      >
        <Icon name="lucide:plus" class="w-4 h-4 inline mr-2" />
        Nova Tarefa
      </button>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="text-center py-8">
      <Icon name="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="text-gray-600 mt-2">Carregando tarefas...</p>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="text-center py-8">
      <Icon name="lucide:alert-circle" class="w-12 h-12 mx-auto text-red-500" />
      <p class="text-red-600 mt-2">Erro ao carregar tarefas</p>
      <button
        @click="() => refetch()"
        class="mt-3 text-primary hover:text-primary-600 font-medium"
      >
        Tentar novamente
      </button>
    </div>
    
    <!-- Empty state -->
    <div v-else-if="!tasks?.length" class="text-center py-8">
      <Icon name="lucide:clipboard-list" class="w-12 h-12 mx-auto text-gray-400" />
      <p class="text-gray-600 mt-2">Nenhuma tarefa encontrada</p>
      <button
        @click="handleCreateTask"
        class="mt-3 text-primary hover:text-primary-600 font-medium"
      >
        Criar sua primeira tarefa
      </button>
    </div>
    
    <!-- Task list -->
    <div v-else class="grid gap-4">
      <div 
        v-for="task in tasks" 
        :key="task.id" 
        class="border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow bg-white"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <h3 class="text-xl font-semibold text-gray-800">{{ task.titulo }}</h3>
              <span 
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  getStatusClass(task.status)
                ]"
              >
                {{ getStatusLabel(task.status) }}
              </span>
            </div>
            
            <p v-if="task.descricao" class="text-gray-600 mb-3">{{ task.descricao }}</p>
            
            <div class="flex flex-wrap gap-4 text-sm text-gray-500">
              <div v-if="task.projeto" class="flex items-center gap-1">
                <Icon name="lucide:folder" class="w-4 h-4" />
                <span>{{ task.projeto.nome }}</span>
              </div>
              
              <div v-if="task.dataVencimento" class="flex items-center gap-1">
                <Icon name="lucide:calendar" class="w-4 h-4" />
                <span>{{ formatDate(task.dataVencimento) }}</span>
              </div>
              
              <div v-if="task.atribuido" class="flex items-center gap-1">
                <Icon name="lucide:user" class="w-4 h-4" />
                <span>{{ task.atribuido.nome }}</span>
              </div>
              
              <div class="flex items-center gap-1">
                <Icon name="lucide:flag" class="w-4 h-4" />
                <span 
                  :class="getPriorityClass(task.prioridade)"
                  class="font-medium"
                >
                  {{ getPriorityLabel(task.prioridade) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="flex gap-2 ml-4">
            <button
              @click="() => handleEditTask(task)"
              class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
              title="Editar tarefa"
            >
              <Icon name="lucide:edit" class="w-4 h-4" />
            </button>
            <button
              @click="() => handleDeleteTask(task.id)"
              class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="Excluir tarefa"
            >
              <Icon name="lucide:trash-2" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useQuery } from '@tanstack/vue-query'
import { TaskService, type Task } from '~/services/taskService'
import { useToastHelpers } from '~/composables/useToast'

// Meta do layout
definePageMeta({
  layout: 'default'
})

const { success, error: showError } = useToastHelpers()

// Query para buscar tarefas
const {
  data: tasks,
  isLoading,
  error,
  refetch
} = useQuery({
  queryKey: ['tasks'],
  queryFn: TaskService.getAllTasks,
  staleTime: 5 * 60 * 1000, // 5 minutos
})

// Formatação de data
function formatDate(dateString: string): string {
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })
  } catch {
    return dateString
  }
}

// Status helpers
function getStatusClass(status: Task['status']): string {
  switch (status) {
    case 'concluida':
      return 'bg-green-100 text-green-800'
    case 'em_andamento':
      return 'bg-blue-100 text-blue-800'
    case 'pendente':
      return 'bg-yellow-100 text-yellow-800'
    case 'cancelada':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

function getStatusLabel(status: Task['status']): string {
  switch (status) {
    case 'concluida':
      return 'Concluída'
    case 'em_andamento':
      return 'Em Andamento'
    case 'pendente':
      return 'Pendente'
    case 'cancelada':
      return 'Cancelada'
    default:
      return status
  }
}

// Priority helpers
function getPriorityClass(priority: Task['prioridade']): string {
  switch (priority) {
    case 'critica':
      return 'text-red-600'
    case 'alta':
      return 'text-orange-600'
    case 'media':
      return 'text-yellow-600'
    case 'baixa':
      return 'text-green-600'
    default:
      return 'text-gray-600'
  }
}

function getPriorityLabel(priority: Task['prioridade']): string {
  switch (priority) {
    case 'critica':
      return 'Crítica'
    case 'alta':
      return 'Alta'
    case 'media':
      return 'Média'
    case 'baixa':
      return 'Baixa'
    default:
      return priority
  }
}

// Handlers para ações
function handleCreateTask() {
  // TODO: Implementar modal de criação de tarefa
  success('Funcionalidade em desenvolvimento', 'Modal de criação será implementado em breve')
}

function handleEditTask(task: Task) {
  // TODO: Implementar modal de edição de tarefa
  success('Funcionalidade em desenvolvimento', `Edição da tarefa "${task.titulo}" será implementada em breve`)
}

async function handleDeleteTask(taskId: string) {
  if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return
  
  try {
    await TaskService.deleteTask(taskId)
    success('Tarefa excluída', 'A tarefa foi excluída com sucesso')
    refetch()
  } catch (err) {
    showError('Erro ao excluir', 'Não foi possível excluir a tarefa')
  }
}
</script>
