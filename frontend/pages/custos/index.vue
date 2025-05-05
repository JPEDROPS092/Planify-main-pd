<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Custos</h1>
        <button @click="openNewCostModal" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2">
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Novo Custo
        </button>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar custos..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
          />
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute right-3 top-2.5 h-4 w-4 text-gray-400 dark:text-gray-500">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path>
            <path d="M12 18V6"></path>
          </svg>
        </div>
        <select
          v-model="categoryFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todas as categorias</option>
          <option value="PESSOAL">Pessoal</option>
          <option value="MATERIAL">Material</option>
          <option value="EQUIPAMENTO">Equipamento</option>
          <option value="SERVICO">Serviço</option>
          <option value="LICENCA">Licença</option>
          <option value="OUTRO">Outro</option>
        </select>
        <select
          v-model="statusFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os status</option>
          <option value="PREVISTO">Previsto</option>
          <option value="APROVADO">Aprovado</option>
          <option value="PAGO">Pago</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
        <select
          v-model="projectFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os projetos</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.titulo }}
          </option>
        </select>
      </div>

      <!-- Loading e estados vazios -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-12">
        <div class="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
        <p class="mt-4 text-sm text-gray-500 dark:text-gray-400">Carregando custos...</p>
      </div>

      <EmptyState 
        v-else-if="filteredCosts.length === 0" 
        title="Nenhum custo encontrado" 
        description="Não encontramos nenhum custo com os filtros atuais. Tente ajustar os filtros ou registre um novo custo."
        icon="dollar-sign"
      >
        <template #action>
          <button 
            @click="openNewCostModal" 
            class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2">
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Registrar novo custo
          </button>
        </template>
      </EmptyState>

      <!-- Costs table -->
      <div v-else>
        <div class="overflow-hidden rounded-lg border bg-white shadow dark:border-gray-700 dark:bg-gray-800">
          <table class="w-full border-collapse text-left">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Descrição</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Categoria</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Projeto</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Valor</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Status</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Data</th>
                <th scope="col" class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400">Ações</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="cost in filteredCosts" :key="cost.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-4 py-3 text-sm">
                  <div class="font-medium text-gray-900 dark:text-white">{{ cost.descricao }}</div>
                  <div v-if="cost.observacoes" class="mt-1 line-clamp-1 text-xs text-gray-500 dark:text-gray-400">{{ cost.observacoes }}</div>
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300': cost.categoria === 'PESSOAL',
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': cost.categoria === 'MATERIAL',
                      'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300': cost.categoria === 'EQUIPAMENTO',
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300': cost.categoria === 'SERVICO',
                      'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300': cost.categoria === 'LICENCA',
                      'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300': cost.categoria === 'OUTRO',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getCategoryLabel(cost.categoria) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                  {{ getProjectName(cost.projeto) }}
                </td>
                <td class="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">
                  {{ formatCurrency(cost.valor) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300': cost.status === 'PREVISTO',
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300': cost.status === 'APROVADO',
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': cost.status === 'PAGO',
                      'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300': cost.status === 'CANCELADO',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getStatusLabel(cost.status) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(cost.data) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <div class="flex items-center space-x-2">
                    <button
                      @click="editCost(cost)"
                      class="rounded-md p-1 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                      title="Editar"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                        <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path>
                      </svg>
                    </button>
                    <button
                      @click="viewCost(cost.id)"
                      class="rounded-md p-1 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900"
                      title="Ver detalhes"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
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
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50 dark:border-gray-700 dark:text-gray-400"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="m15 18-6-6 6-6"></path>
          </svg>
        </button>
        <div v-for="page in paginationRange" :key="page" class="inline-flex h-9 w-9 items-center justify-center rounded-md text-sm font-medium"
          :class="page === currentPage ? 'bg-blue-600 text-white dark:bg-blue-700 dark:text-white' : 'border border-gray-300 text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700'"
          @click="changePage(page)"
        >
          {{ page }}
        </div>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50 dark:border-gray-700 dark:text-gray-400"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="m9 18 6-6-6-6"></path>
          </svg>
        </button>
      </div>

      <!-- Modal para novo/editar custo -->
      <div v-if="showCostModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium">{{ editingCost ? 'Editar Custo' : 'Novo Custo' }}</h3>
            <button @click="showCostModal = false" class="rounded-full p-1 hover:bg-gray-100 dark:hover:bg-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="saveCost" class="mt-4 space-y-4">
            <div>
              <label for="descricao" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Descrição</label>
              <input
                id="descricao"
                v-model="costForm.descricao"
                type="text"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label for="projeto" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Projeto</label>
              <select
                id="projeto"
                v-model="costForm.projeto"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option v-for="project in projects" :key="project.id" :value="project.id">
                  {{ project.titulo }}
                </option>
              </select>
            </div>
            <div>
              <label for="categoria" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Categoria</label>
              <select
                id="categoria"
                v-model="costForm.categoria"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option value="PESSOAL">Pessoal</option>
                <option value="MATERIAL">Material</option>
                <option value="EQUIPAMENTO">Equipamento</option>
                <option value="SERVICO">Serviço</option>
                <option value="LICENCA">Licença</option>
                <option value="OUTRO">Outro</option>
              </select>
            </div>
            <div>
              <label for="valor" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Valor (R$)</label>
              <input
                id="valor"
                v-model="costForm.valor"
                type="number"
                step="0.01"
                min="0"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label for="data" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Data</label>
              <input
                id="data"
                v-model="costForm.data"
                type="date"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label for="status" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Status</label>
              <select
                id="status"
                v-model="costForm.status"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option value="PREVISTO">Previsto</option>
                <option value="APROVADO">Aprovado</option>
                <option value="PAGO">Pago</option>
                <option value="CANCELADO">Cancelado</option>
              </select>
            </div>
            <div>
              <label for="observacoes" class="block text-sm font-medium text-gray-700 dark:text-gray-400">Observações</label>
              <textarea
                id="observacoes"
                v-model="costForm.observacoes"
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              ></textarea>
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showCostModal = false"
                class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-700"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70 dark:bg-blue-700 dark:hover:bg-blue-600"
              >
                <span v-if="saving" class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
                {{ saving ? 'Salvando...' : (editingCost ? 'Salvar' : 'Criar') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import EmptyState from '~/components/EmptyState.vue'

definePageMeta({
  middleware: ['auth']
})

const router = useRouter()
const { $api } = useNuxtApp()

// Estado
const costs = ref([])
const projects = ref([])
const loading = ref(true)
const error = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const searchQuery = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')
const projectFilter = ref('')
const showCostModal = ref(false)
const saving = ref(false)
const editingCost = ref(null)

// Formulário de custo
const costForm = ref({
  descricao: '',
  projeto: '',
  categoria: 'OUTRO',
  valor: '',
  data: new Date().toISOString().split('T')[0],
  status: 'PREVISTO',
  observacoes: ''
})

// Filtrar custos
const filteredCosts = computed(() => {
  return costs.value.filter(cost => {
    const matchesSearch = searchQuery.value === '' || 
      cost.descricao.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (cost.observacoes && cost.observacoes.toLowerCase().includes(searchQuery.value.toLowerCase()))
    
    const matchesCategory = categoryFilter.value === '' || cost.categoria === categoryFilter.value
    const matchesStatus = statusFilter.value === '' || cost.status === statusFilter.value
    const matchesProject = projectFilter.value === '' || cost.projeto === parseInt(projectFilter.value)
    
    return matchesSearch && matchesCategory && matchesStatus && matchesProject
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

// Buscar custos
const fetchCosts = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await $api.get('/api/costs/', {
      params: {
        page: currentPage.value
      }
    })
    
    costs.value = response.data.results || response.data
    
    // Configurar paginação se disponível
    if (response.data.count !== undefined) {
      const count = response.data.count
      const pageSize = 10 // Ajuste conforme a API
      totalPages.value = Math.ceil(count / pageSize)
    }
  } catch (err) {
    console.error('Erro ao buscar custos:', err)
    error.value = 'Não foi possível carregar os custos. Por favor, tente novamente.'
  } finally {
    loading.value = false
  }
}

// Buscar projetos
const fetchProjects = async () => {
  try {
    const response = await $api.get('/api/projects/')
    projects.value = response.data.results || response.data
    
    if (projects.value.length > 0) {
      costForm.value.projeto = projects.value[0].id
    }
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

// Formatar moeda
const formatCurrency = (value) => {
  if (value === undefined || value === null) return 'R$ 0,00'
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
}

// Obter label da categoria
const getCategoryLabel = (category) => {
  const categoryMap = {
    'PESSOAL': 'Pessoal',
    'MATERIAL': 'Material',
    'EQUIPAMENTO': 'Equipamento',
    'SERVICO': 'Serviço',
    'LICENCA': 'Licença',
    'OUTRO': 'Outro'
  }
  return categoryMap[category] || category
}

// Obter label do status
const getStatusLabel = (status) => {
  const statusMap = {
    'PREVISTO': 'Previsto',
    'APROVADO': 'Aprovado',
    'PAGO': 'Pago',
    'CANCELADO': 'Cancelado'
  }
  return statusMap[status] || status
}

// Obter nome do projeto
const getProjectName = (projectId) => {
  const project = projects.value.find(p => p.id === projectId)
  return project ? project.titulo : 'Projeto não encontrado'
}

// Abrir modal de novo custo
const openNewCostModal = () => {
  editingCost.value = null
  costForm.value = {
    descricao: '',
    projeto: projects.value.length > 0 ? projects.value[0].id : '',
    categoria: 'OUTRO',
    valor: '',
    data: new Date().toISOString().split('T')[0],
    status: 'PREVISTO',
    observacoes: ''
  }
  showCostModal.value = true
}

// Editar custo
const editCost = (cost) => {
  editingCost.value = cost
  costForm.value = {
    descricao: cost.descricao,
    projeto: cost.projeto,
    categoria: cost.categoria,
    valor: cost.valor,
    data: cost.data,
    status: cost.status,
    observacoes: cost.observacoes || ''
  }
  showCostModal.value = true
}

// Salvar custo
const saveCost = async () => {
  saving.value = true
  
  try {
    if (editingCost.value) {
      await $api.put(`/api/costs/${editingCost.value.id}/`, costForm.value)
    } else {
      await $api.post('/api/costs/', costForm.value)
    }
    
    showCostModal.value = false
    await fetchCosts()
  } catch (err) {
    console.error('Erro ao salvar custo:', err)
    alert('Não foi possível salvar o custo. Por favor, tente novamente.')
  } finally {
    saving.value = false
  }
}

// Ver detalhes do custo
const viewCost = (id) => {
  router.push(`/custos/${id}`)
}

// Observar mudanças nos filtros e página
watch([currentPage, searchQuery, categoryFilter, statusFilter, projectFilter], () => {
  if (searchQuery.value === '' && categoryFilter.value === '' && statusFilter.value === '' && projectFilter.value === '') {
    fetchCosts()
  }
})

// Carregar dados ao montar o componente
onMounted(async () => {
  await fetchProjects()
  await fetchCosts()
})
</script>
