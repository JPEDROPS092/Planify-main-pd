<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold tracking-tight">Tarefas</h1>
        <button @click="openNewTaskModal" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2">
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Nova Tarefa
        </button>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar tarefas..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute right-3 top-2.5 h-4 w-4 text-gray-400">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </svg>
        </div>
        <select
          v-model="statusFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todos os status</option>
          <option value="A_FAZER">A Fazer</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="FEITO">Feito</option>
        </select>
        <select
          v-model="priorityFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todas as prioridades</option>
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
        </select>
        <select
          v-model="projectFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todos os projetos</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.titulo }}
          </option>
        </select>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-8">
        <div class="h-8 w-8 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4 text-red-700">
        <p>{{ error }}</p>
        <button @click="fetchTasks" class="mt-2 text-sm font-medium underline">Tentar novamente</button>
      </div>

      <!-- Empty state -->
      <div v-else-if="filteredTasks.length === 0" class="flex flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 bg-gray-50 p-12 text-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-12 w-12 text-gray-400">
          <rect width="8" height="8" x="3" y="3" rx="2"></rect>
          <rect width="8" height="8" x="13" y="3" rx="2"></rect>
          <rect width="8" height="8" x="3" y="13" rx="2"></rect>
          <rect width="8" height="8" x="13" y="13" rx="2"></rect>
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">Nenhuma tarefa encontrada</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{ tasks && tasks.length === 0 ? 'Comece criando sua primeira tarefa.' : 'Nenhuma tarefa corresponde aos filtros aplicados.' }}
        </p>
        <button
          v-if="tasks && tasks.length === 0"
          @click="openNewTaskModal"
          class="mt-4 inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2">
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Criar Tarefa
        </button>
      </div>

      <!-- Task list -->
      <div v-else>
        <div class="overflow-hidden rounded-lg border bg-white shadow">
          <table class="w-full border-collapse text-left">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500">Título</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500">Projeto</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500">Status</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500">Prioridade</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500">Prazo</th>
                <th class="px-4 py-3.5 text-left text-sm font-semibold text-gray-900">Ações</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="task in filteredTasks" :key="task.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm">
                  <div class="font-medium text-gray-900">{{ task.titulo }}</div>
                  <div class="mt-1 line-clamp-1 text-xs text-gray-500">{{ task.descricao }}</div>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">
                  {{ getProjectName(task.projeto) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-yellow-100 text-yellow-800': task.status === 'A_FAZER',
                      'bg-blue-100 text-blue-800': task.status === 'EM_ANDAMENTO',
                      'bg-green-100 text-green-800': task.status === 'FEITO',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getStatusLabel(task.status) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-green-100 text-green-800': task.prioridade === 'BAIXA',
                      'bg-yellow-100 text-yellow-800': task.prioridade === 'MEDIA',
                      'bg-red-100 text-red-800': task.prioridade === 'ALTA',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getPriorityLabel(task.prioridade) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">
                  {{ formatDate(task.data_termino) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <div class="flex space-x-2">
                    <button
                      @click="viewTask(task.id)"
                      class="rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 hover:bg-blue-100"
                    >
                      Ver
                    </button>
                    <button
                      @click="editTask(task)"
                      class="rounded-md bg-amber-50 px-2 py-1 text-xs font-medium text-amber-700 hover:bg-amber-100"
                    >
                      Editar
                    </button>
                    <button
                      @click="confirmDeleteTask(task)"
                      class="rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 hover:bg-red-100"
                    >
                      Excluir
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex items-center justify-center space-x-2 pt-4">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="m15 18-6-6 6-6"></path>
          </svg>
        </button>
        <div v-for="page in paginationRange" :key="page" class="inline-flex h-9 w-9 items-center justify-center rounded-md text-sm font-medium"
          :class="page === currentPage ? 'bg-blue-600 text-white' : 'border border-gray-300 text-gray-700 hover:bg-gray-50'"
          @click="changePage(page)"
        >
          {{ page }}
        </div>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="m9 18 6-6-6-6"></path>
          </svg>
        </button>
      </div>

      <!-- Modal para nova tarefa -->
      <div v-if="showTaskModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium">{{ editingTask ? 'Editar Tarefa' : 'Nova Tarefa' }}</h3>
            <button @click="showTaskModal = false" class="rounded-full p-1 hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="saveTask" class="mt-4 space-y-4">
            <div>
              <label for="titulo" class="block text-sm font-medium text-gray-700">Título</label>
              <input
                id="titulo"
                v-model="taskForm.titulo"
                type="text"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label for="descricao" class="block text-sm font-medium text-gray-700">Descrição</label>
              <textarea
                id="descricao"
                v-model="taskForm.descricao"
                rows="3"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              ></textarea>
            </div>
            <div>
              <label for="projeto" class="block text-sm font-medium text-gray-700">Projeto</label>
              <select
                id="projeto"
                v-model="taskForm.projeto"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option v-for="project in projects" :key="project.id" :value="project.id">
                  {{ project.titulo }}
                </option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="data_inicio" class="block text-sm font-medium text-gray-700">Data de Início</label>
                <input
                  id="data_inicio"
                  v-model="taskForm.data_inicio"
                  type="date"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
              <div>
                <label for="data_termino" class="block text-sm font-medium text-gray-700">Data de Término</label>
                <input
                  id="data_termino"
                  v-model="taskForm.data_termino"
                  type="date"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
                <select
                  id="status"
                  v-model="taskForm.status"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="A_FAZER">A Fazer</option>
                  <option value="EM_ANDAMENTO">Em Andamento</option>
                  <option value="FEITO">Feito</option>
                </select>
              </div>
              <div>
                <label for="prioridade" class="block text-sm font-medium text-gray-700">Prioridade</label>
                <select
                  id="prioridade"
                  v-model="taskForm.prioridade"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="BAIXA">Baixa</option>
                  <option value="MEDIA">Média</option>
                  <option value="ALTA">Alta</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showTaskModal = false"
                class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70"
              >
                <span v-if="saving" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
                {{ saving ? 'Salvando...' : (editingTask ? 'Salvar' : 'Criar') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeMount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { listTarefas, createTarefa, retrieveTarefa, updateTarefa, destroyTarefa } from '~/services/api/tasks'
import { listProjetos } from '~/services/api/projects'
import { useAuth } from '~/services/api/auth'

definePageMeta({
  middleware: ['auth']
})

const router = useRouter()
const route = useRoute()
const { $api } = useNuxtApp()

// Estado
const tasks = ref([])
const projects = ref([])
const loading = ref(true)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')
const statusFilter = ref('')
const priorityFilter = ref('')
const projectFilter = ref('')
const showTaskModal = ref(false)
const saving = ref(false)
const editingTask = ref(null)

// Formulário de tarefa
const taskForm = ref({
  titulo: '',
  descricao: '',
  projeto: '',
  status: 'A_FAZER',
  prioridade: 'MEDIA',
  data_inicio: new Date().toISOString().split('T')[0],
  data_fim: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
})

// Filtrar tarefas
const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    const matchesSearch = searchQuery.value === '' || 
      task.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (task.descricao && task.descricao.toLowerCase().includes(searchQuery.value.toLowerCase()))
    
    const matchesStatus = statusFilter.value === '' || task.status === statusFilter.value
    const matchesPriority = priorityFilter.value === '' || task.prioridade === priorityFilter.value
    const matchesProject = projectFilter.value === '' || task.projeto === parseInt(projectFilter.value)
    
    return matchesSearch && matchesStatus && matchesPriority && matchesProject
  })
})

// Paginação
const paginationRange = computed(() => {
  const range = []
  const maxVisiblePages = 5
  
  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) {
      range.push(i)
    }
  } else {
    let start = Math.max(1, currentPage.value - Math.floor(maxVisiblePages / 2))
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1)
    
    if (end - start + 1 < maxVisiblePages) {
      start = Math.max(1, end - maxVisiblePages + 1)
    }
    
    for (let i = start; i <= end; i++) {
      range.push(i)
    }
  }
  
  return range
})

// Verificar se há um parâmetro na URL para abrir o modal
onBeforeMount(() => {
  if (route.query.new === 'true') {
    showTaskModal.value = true
  }
})

// Escutar evento global para abrir o modal
onMounted(() => {
  window.addEventListener('open-new-task-modal', () => {
    showTaskModal.value = true
  })
  
  // Buscar dados iniciais
  fetchProjects()
  fetchTasks()
  
  return () => {
    window.removeEventListener('open-new-task-modal', () => {
      showTaskModal.value = true
    })
  }
})

// Buscar tarefas
const fetchTasks = async () => {
  loading.value = true
  error.value = null
  
  try {
    const params = {
      page: currentPage.value,
      ordering: '-data_criacao'
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    if (priorityFilter.value) {
      params.prioridade = priorityFilter.value
    }
    
    if (projectFilter.value) {
      params.projeto = projectFilter.value
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    // Usar o novo serviço de API para tarefas
    const response = await listTarefas(params)
    
    // Processar dados da resposta paginada
    tasks.value = response.results.map(task => ({
      id: task.id,
      titulo: task.titulo,
      descricao: task.descricao,
      projeto: task.projeto,
      projeto_nome: task.projeto_nome,
      responsavel: task.responsavel,
      responsavel_nome: task.responsavel_nome,
      prioridade: task.prioridade,
      prioridade_display: task.prioridade_display,
      status: task.status,
      status_display: task.status_display,
      data_inicio: task.data_inicio,
      data_fim: task.data_fim,
      progresso: task.progresso
    }))
    
    totalItems.value = response.count
    totalPages.value = Math.ceil(response.count / itemsPerPage.value)
  } catch (err) {
    console.error('Erro ao buscar tarefas:', err)
    error.value = 'Não foi possível carregar as tarefas. Por favor, tente novamente.'
  } finally {
    loading.value = false
  }
}

// Buscar projetos
const fetchProjects = async () => {
  try {
    // Usar o novo serviço de API para projetos
    const response = await listProjetos()
    projects.value = response.results.map(project => ({
      id: project.id,
      nome: project.nome
    }))
  } catch (err) {
    console.error('Erro ao buscar projetos:', err)
  }
}

// Mudar página
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR')
}

// Obter label do status
const getStatusLabel = (status) => {
  const statusMap = {
    'A_FAZER': 'A Fazer',
    'EM_ANDAMENTO': 'Em Andamento',
    'FEITO': 'Feito'
  }
  return statusMap[status] || status
}

// Obter label da prioridade
const getPriorityLabel = (priority) => {
  const priorityMap = {
    'BAIXA': 'Baixa',
    'MEDIA': 'Média',
    'ALTA': 'Alta'
  }
  return priorityMap[priority] || priority
}

// Obter nome do projeto
const getProjectName = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  return project ? project.titulo : 'Projeto não encontrado'
}

// Abrir modal de nova tarefa
const openNewTaskModal = () => {
  editingTask.value = null
  taskForm.value = {
    titulo: '',
    descricao: '',
    projeto: projects.value.length > 0 ? projects.value[0].id : '',
    status: 'A_FAZER',
    prioridade: 'MEDIA',
    data_inicio: new Date().toISOString().split('T')[0],
    data_fim: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  }
  showTaskModal.value = true
}

// Editar tarefa
const editTask = async (task) => {
  try {
    // Buscar detalhes completos da tarefa usando o novo serviço de API
    const taskDetails = await retrieveTarefa(task.id)
    
    editingTask.value = taskDetails
    taskForm.value = {
      titulo: taskDetails.titulo,
      descricao: taskDetails.descricao || '',
      projeto: taskDetails.projeto,
      responsavel: taskDetails.responsavel || null,
      status: taskDetails.status,
      prioridade: taskDetails.prioridade,
      data_inicio: taskDetails.data_inicio || null,
      data_fim: taskDetails.data_fim || null,
      estimativa_horas: taskDetails.estimativa_horas || null
    }
    showTaskModal.value = true
  } catch (err) {
    console.error('Erro ao buscar detalhes da tarefa para edição:', err)
    error.value = 'Não foi possível carregar os detalhes da tarefa para edição.'
  }
}

// Salvar tarefa
const saveTask = async () => {
  if (!taskForm.titulo || !taskForm.projeto) {
    alert('Preencha os campos obrigatórios')
    return
  }
  
  saving.value = true
  
  try {
    // Preparar dados para o novo formato da API
    const taskData = {
      titulo: taskForm.titulo,
      descricao: taskForm.descricao || null,
      projeto: taskForm.projeto,
      responsavel: taskForm.responsavel || null,
      prioridade: taskForm.prioridade,
      status: taskForm.status,
      data_inicio: taskForm.data_inicio || null,
      data_fim: taskForm.data_fim || null,
      estimativa_horas: taskForm.estimativa_horas || null
    }
    
    if (editingTask.value) {
      // Atualizar tarefa existente usando o novo serviço de API
      await updateTarefa(editingTask.value.id, taskData)
    } else {
      // Criar nova tarefa usando o novo serviço de API
      await createTarefa(taskData)
    }
    
    showTaskModal.value = false
    fetchTasks()
  } catch (err) {
    console.error('Erro ao salvar tarefa:', err)
  } finally {
    saving.value = false
  }
}

// Ver detalhes da tarefa
const viewTask = async (id) => {
  try {
    // Buscar detalhes da tarefa usando o novo serviço de API antes de navegar
    await retrieveTarefa(id)
    router.push(`/tarefas/${id}`)
  } catch (err) {
    console.error('Erro ao buscar detalhes da tarefa:', err)
    error.value = 'Não foi possível carregar os detalhes da tarefa.'
  }
}

// Confirmar exclusão de tarefa
const confirmDeleteTask = (task) => {
  if (confirm(`Tem certeza que deseja excluir a tarefa "${task.titulo}"?`)) {
    deleteTask(task.id)
  }
}

// Excluir tarefa
const deleteTask = async (id) => {
  try {
    // Usar o novo serviço de API para excluir a tarefa
    await destroyTarefa(id)
    // Atualizar a lista após a exclusão
    fetchTasks()
  } catch (err) {
    console.error('Erro ao excluir tarefa:', err)
    error.value = 'Não foi possível excluir a tarefa. Por favor, tente novamente.'
  }
}

// Observar mudanças nos filtros e página
watch([currentPage, searchQuery, statusFilter, priorityFilter, projectFilter], () => {
  fetchTasks()
})
</script>
