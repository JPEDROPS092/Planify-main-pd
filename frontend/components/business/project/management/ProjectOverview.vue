<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">Visão Geral do Projeto</h3>
      <Button v-if="!loading && !error" @click="fetchProjectData" variant="outline" size="sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Atualizar
      </Button>
    </div>
    
    <div v-if="loading" class="space-y-4">
      <SkeletonLoader type="list-item-avatar" :count="3" />
    </div>
    <div v-else-if="error" class="text-center text-red-500 dark:text-red-400 py-6">
      <p>{{ error.message || 'Erro ao carregar dados do projeto.' }}</p>
      <Button variant="outline" size="sm" class="mt-2" @click="fetchProjectData">Tentar Novamente</Button>
    </div>
    <div v-else class="space-y-6">      
      <!-- Estatísticas do Projeto -->
      <ProjectStatistics :project-id="projectId" />
      
      <!-- Detalhes do Projeto -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Progresso do Projeto -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Progresso do Projeto</h4>
        <div class="flex items-center mb-4">
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 mr-2">
            <div class="bg-blue-600 h-4 rounded-full" :style="{ width: `${projectProgress}%` }"></div>
          </div>
          <span class="text-sm font-medium text-gray-700 dark:text-gray-300 min-w-[45px] text-right">{{ projectProgress }}%</span>
        </div>
        <div class="grid grid-cols-3 gap-2 text-center text-sm">
          <div>
            <div class="font-medium text-gray-700 dark:text-gray-300">{{ stats.pendingTasks }}</div>
            <div class="text-gray-500 dark:text-gray-400">A Fazer</div>
          </div>
          <div>
            <div class="font-medium text-gray-700 dark:text-gray-300">{{ stats.inProgressTasks }}</div>
            <div class="text-gray-500 dark:text-gray-400">Em Andamento</div>
          </div>
          <div>
            <div class="font-medium text-gray-700 dark:text-gray-300">{{ stats.completedTasks }}</div>
            <div class="text-gray-500 dark:text-gray-400">Concluídas</div>
          </div>
        </div>
      </div>
      
      <!-- Distribuição de Tarefas -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Distribuição de Tarefas</h4>
        <div class="h-48 flex items-center justify-center">
          <canvas ref="taskDistributionChart"></canvas>
        </div>
      </div>
      
      <!-- Próximos Prazos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Próximos Prazos</h4>
        <div v-if="upcomingDeadlines.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-4">
          <p>Nenhum prazo próximo encontrado.</p>
        </div>
        <ul v-else class="space-y-3">
          <li v-for="deadline in upcomingDeadlines" :key="deadline.id" class="flex items-start">
            <div :class="getDeadlineStatusClass(deadline.daysRemaining)" class="w-2 h-2 rounded-full mt-1.5 mr-2"></div>
            <div class="flex-1">
              <div class="flex justify-between">
                <span class="font-medium text-gray-700 dark:text-gray-300">{{ deadline.title }}</span>
                <span :class="getDeadlineTextClass(deadline.daysRemaining)" class="text-xs">
                  {{ formatDeadline(deadline.daysRemaining) }}
                </span>
              </div>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ deadline.date }}</p>
            </div>
          </li>
        </ul>
      </div>
      
      <!-- Membros Ativos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Membros Ativos</h4>
        <div v-if="activeMembers.length === 0" class="text-center text-gray-500 dark:text-gray-400 py-4">
          <p>Nenhum membro ativo encontrado.</p>
        </div>
        <ul v-else class="space-y-3">
          <li v-for="member in activeMembers" :key="member.id" class="flex items-center">
            <div class="w-8 h-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center text-gray-700 dark:text-gray-300 mr-3">
              {{ member.initials }}
            </div>
            <div class="flex-1">
              <div class="font-medium text-gray-700 dark:text-gray-300">{{ member.name }}</div>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ member.role }}</p>
            </div>
            <div class="text-sm text-gray-500 dark:text-gray-400">
              {{ member.taskCount }} tarefas
            </div>
          </li>
        </ul>
      </div>
      
      <!-- Resumo de Custos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 md:col-span-2">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Resumo de Custos</h4>
        <div v-if="!costSummary" class="text-center text-gray-500 dark:text-gray-400 py-4">
          <p>Nenhum dado de custo disponível.</p>
        </div>
        <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <div class="text-sm text-gray-500 dark:text-gray-400">Orçamento Total</div>
            <div class="font-medium text-gray-800 dark:text-gray-200 text-lg">{{ formatCurrency(costSummary.budget) }}</div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <div class="text-sm text-gray-500 dark:text-gray-400">Custos Atuais</div>
            <div class="font-medium text-gray-800 dark:text-gray-200 text-lg">{{ formatCurrency(costSummary.currentCosts) }}</div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <div class="text-sm text-gray-500 dark:text-gray-400">Restante</div>
            <div class="font-medium text-gray-800 dark:text-gray-200 text-lg">{{ formatCurrency(costSummary.remaining) }}</div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
            <div class="text-sm text-gray-500 dark:text-gray-400">Utilizado</div>
            <div class="font-medium text-gray-800 dark:text-gray-200 text-lg">{{ costSummary.percentUsed }}%</div>
          </div>
        </div>
      </div>
      
      <!-- Informações do Projeto -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
        <h4 class="font-medium text-gray-700 dark:text-gray-300 mb-3">Informações do Projeto</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-2">
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Status:</span>
              <span :class="getStatusClass(projectDetails.status)" class="ml-2 px-2 py-1 rounded-full text-xs">
                {{ getStatusText(projectDetails.status) }}
              </span>
            </div>
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Prioridade:</span>
              <span :class="getPriorityClass(projectDetails.prioridade)" class="ml-2 px-2 py-1 rounded-full text-xs">
                {{ getPriorityText(projectDetails.prioridade) }}
              </span>
            </div>
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Data de Início:</span>
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ formatDate(projectDetails.data_inicio) }}</span>
            </div>
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Data de Término (Previsão):</span>
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ formatDate(projectDetails.data_fim) }}</span>
            </div>
          </div>
          <div class="space-y-2">
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Gerente:</span>
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ projectDetails.gerente_nome || 'Não definido' }}</span>
            </div>
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Membros:</span>
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ activeMembers.length }}</span>
            </div>
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Total de Tarefas:</span>
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ stats.totalTasks }}</span>
            </div>
            <div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Dias Restantes:</span>
              <span class="ml-2 text-sm" :class="getDaysRemainingClass(projectDetails)">{{ getDaysRemaining(projectDetails) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, toRefs, computed, onUnmounted } from 'vue'
import { useProjectService } from '~/services/api/services/projectService'
import { useTaskService } from '~/services/api/services/taskService'
import { useTeamService } from '~/services/api/services/teamService'
import { useCostService } from '~/services/api/services/costService'
import { useNotification } from '~/composables/useNotification'
import ProjectStatistics from './ProjectStatistics.vue'
import Button from '~/components/ui/Button.vue'
import SkeletonLoader from '~/components/SkeletonLoader.vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

const { projectId } = toRefs(props)
const projectService = useProjectService()
const taskService = useTaskService()
const teamService = useTeamService()
const costService = useCostService()
const { showApiError } = useNotification()

// Estado
const loading = ref(false)
const error = ref<Error | null>(null)
const chartInstance = ref<any>(null)
const taskDistributionChart = ref<HTMLCanvasElement | null>(null)

// Dados do projeto
const projectDetails = ref<any>({})
const stats = ref({
  totalTasks: 0,
  pendingTasks: 0,
  inProgressTasks: 0,
  completedTasks: 0
})

const upcomingDeadlines = ref<any[]>([])
const activeMembers = ref<any[]>([])
const costSummary = ref<any>(null)

// Progresso calculado
const projectProgress = computed(() => {
  if (stats.value.totalTasks === 0) return 0
  return Math.round((stats.value.completedTasks / stats.value.totalTasks) * 100)
})

// Métodos
async function fetchProjectData() {
  loading.value = true
  error.value = null
  
  try {
    // Buscar detalhes do projeto
    const project = await projectService.retrieveProjeto(projectId.value)
    projectDetails.value = project
    
    // Buscar tarefas do projeto
    const tasksResponse = await taskService.listTarefas({ projeto: projectId.value })
    const tasks = tasksResponse.results || []
    
    // Calcular estatísticas de tarefas
    const taskStats = {
      totalTasks: tasks.length,
      pendingTasks: 0,
      inProgressTasks: 0,
      completedTasks: 0
    }
    
    tasks.forEach(task => {
      if (task.status === 'A_FAZER') taskStats.pendingTasks++
      else if (task.status === 'EM_ANDAMENTO') taskStats.inProgressTasks++
      else if (task.status === 'FEITO') taskStats.completedTasks++
    })
    
    stats.value = taskStats
    
    // Buscar prazos próximos (tarefas com data de vencimento próxima)
    const upcomingTasks = tasks
      .filter(task => task.data_vencimento && task.status !== 'FEITO')
      .map(task => {
        const dueDate = new Date(task.data_vencimento)
        const today = new Date()
        const daysRemaining = Math.ceil((dueDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
        
        return {
          id: task.id,
          title: task.titulo,
          date: task.data_vencimento,
          daysRemaining
        }
      })
      .sort((a, b) => a.daysRemaining - b.daysRemaining)
      .slice(0, 5) // Mostrar apenas os 5 prazos mais próximos
    
    upcomingDeadlines.value = upcomingTasks
    
    // Buscar membros ativos da equipe
    const membersResponse = await teamService.listMembros({ projeto: projectId.value })
    const members = membersResponse.results || []
    
    // Contar tarefas por membro
    const memberTaskCounts = {}
    tasks.forEach(task => {
      if (task.responsavel) {
        memberTaskCounts[task.responsavel] = (memberTaskCounts[task.responsavel] || 0) + 1
      }
    })
    
    // Formatar dados dos membros
    const formattedMembers = members.map(member => {
      const nameParts = (member.usuario_nome || '').split(' ')
      const initials = nameParts.length > 1 
        ? `${nameParts[0][0]}${nameParts[1][0]}` 
        : nameParts[0] ? nameParts[0][0] : '?'
      
      return {
        id: member.id,
        name: member.usuario_nome || 'Usuário',
        initials: initials.toUpperCase(),
        role: member.papel || 'Membro',
        taskCount: memberTaskCounts[member.usuario] || 0
      }
    })
    
    // Ordenar por número de tarefas (decrescente)
    activeMembers.value = formattedMembers.sort((a, b) => b.taskCount - a.taskCount)
    
    // Buscar resumo de custos
    const costsResponse = await costService.listCustos({ projeto: projectId.value })
    const costs = costsResponse.results || []
    
    // Calcular total gasto
    const totalSpent = costs.reduce((sum, cost) => sum + cost.valor, 0)
    
    // Agrupar por categoria
    const categories = {}
    costs.forEach(cost => {
      const category = cost.categoria || 'Outros'
      categories[category] = (categories[category] || 0) + cost.valor
    })
    
    // Formatar dados de categorias
    const formattedCategories = Object.entries(categories).map(([name, amount]) => ({ name, amount }))
    
    costSummary.value = {
      budget: project.orcamento || 0,
      spent: totalSpent,
      remaining: (project.orcamento || 0) - totalSpent,
      spentPercent: totalSpent > 0 ? Math.round((totalSpent / (project.orcamento || 0)) * 100) : 0,
      categories: formattedCategories
    }
    
    // Renderizar gráfico
    renderTaskDistributionChart()
  } catch (err: any) {
    error.value = err
    console.error('Erro ao buscar dados do projeto:', err)
    showApiError(err, 'Erro ao carregar visão geral do projeto')
  } finally {
    loading.value = false
  }
}

// ... restante do código
function processDeadlines(deadlines: any[]) {
  return deadlines.map(deadline => {
    const dueDate = new Date(deadline.due_date)
    const today = new Date()
    const diffTime = dueDate.getTime() - today.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    return {
      id: deadline.id,
      title: deadline.title,
      date: new Date(deadline.due_date).toLocaleDateString('pt-BR'),
      daysRemaining: diffDays
    }
  }).sort((a, b) => a.daysRemaining - b.daysRemaining).slice(0, 5)
}

function processMembers(members: any[]) {
  return members.map(member => {
    const names = `${member.first_name || ''} ${member.last_name || ''}`.trim() || member.username
    const initials = names.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
    
    return {
      id: member.id,
      name: names,
      initials,
      role: member.role || 'Membro',
      taskCount: member.task_count || 0
    }
  }).sort((a, b) => b.taskCount - a.taskCount).slice(0, 5)
}

function processCostSummary(summary: any) {
  if (!summary) return null
  
  const budget = summary.budget || 0
  const currentCosts = summary.current_costs || 0
  const remaining = budget - currentCosts
  const percentUsed = budget > 0 ? Math.round((currentCosts / budget) * 100) : 0
  
  return {
    budget,
    currentCosts,
    remaining,
    percentUsed
  }
}

function renderTaskDistributionChart() {
  if (!taskDistributionChart.value) return
  
  // Destruir gráfico existente se houver
  if (chart) {
    chart.destroy()
  }
  
  const ctx = taskDistributionChart.value.getContext('2d')
  if (!ctx) return
  
  const data = {
    labels: ['A Fazer', 'Em Andamento', 'Concluídas', 'Bloqueadas'],
    datasets: [{
      data: [
        stats.value.pendingTasks,
        stats.value.inProgressTasks,
        stats.value.completedTasks,
        stats.value.blockedTasks
      ],
      backgroundColor: [
        'rgba(156, 163, 175, 0.7)', // Cinza para A Fazer
        'rgba(59, 130, 246, 0.7)',  // Azul para Em Andamento
        'rgba(16, 185, 129, 0.7)',  // Verde para Concluídas
        'rgba(245, 158, 11, 0.7)'   // Amarelo para Bloqueadas
      ],
      borderColor: [
        'rgb(156, 163, 175)',
        'rgb(59, 130, 246)',
        'rgb(16, 185, 129)',
        'rgb(245, 158, 11)'
      ],
      borderWidth: 1
    }]
  }
  
  chart = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: {
              size: 12
            }
          }
        }
      }
    }
  })
}

function getDeadlineStatusClass(daysRemaining: number) {
  if (daysRemaining < 0) return 'bg-red-500'
  if (daysRemaining <= 3) return 'bg-yellow-500'
  return 'bg-green-500'
}

function getDeadlineTextClass(daysRemaining: number) {
  if (daysRemaining < 0) return 'text-red-500'
  if (daysRemaining <= 3) return 'text-yellow-500'
  return 'text-green-500'
}

function formatDeadline(daysRemaining: number) {
  if (daysRemaining < 0) return `Atrasado por ${Math.abs(daysRemaining)} dias`
  if (daysRemaining === 0) return 'Hoje'
  if (daysRemaining === 1) return 'Amanhã'
  return `Em ${daysRemaining} dias`
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
}

function formatDate(dateString: string) {
  if (!dateString) return 'Não definida'
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR')
}

function getStatusClass(status: string) {
  switch (status) {
    case 'PLANEJADO': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
    case 'EM_ANDAMENTO': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
    case 'PAUSADO': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
    case 'CONCLUIDO': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
    case 'CANCELADO': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }
}

function getStatusText(status: string) {
  switch (status) {
    case 'PLANEJADO': return 'Planejado'
    case 'EM_ANDAMENTO': return 'Em Andamento'
    case 'PAUSADO': return 'Pausado'
    case 'CONCLUIDO': return 'Concluído'
    case 'CANCELADO': return 'Cancelado'
    default: return status
  }
}

function getPriorityClass(priority: string) {
  switch (priority) {
    case 'BAIXA': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
    case 'MEDIA': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
    case 'ALTA': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
    case 'CRITICA': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
  }
}

function getPriorityText(priority: string) {
  switch (priority) {
    case 'BAIXA': return 'Baixa'
    case 'MEDIA': return 'Média'
    case 'ALTA': return 'Alta'
    case 'CRITICA': return 'Crítica'
    default: return priority
  }
}

function getDaysRemaining(project: any) {
  if (!project.data_fim) return 'Sem data definida'
  
  const endDate = new Date(project.data_fim)
  const today = new Date()
  
  // Se a data de término já passou
  if (endDate < today) {
    const daysLate = Math.ceil((today.getTime() - endDate.getTime()) / (1000 * 60 * 60 * 24))
    return `${daysLate} dias atrasado`
  }
  
  // Se a data de término ainda não chegou
  const daysRemaining = Math.ceil((endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  return `${daysRemaining} dias restantes`
}

function getDaysRemainingClass(project: any) {
  if (!project.data_fim) return 'text-gray-700 dark:text-gray-300'
  
  const endDate = new Date(project.data_fim)
  const today = new Date()
  
  // Se a data de término já passou
  if (endDate < today) {
    return 'text-red-600 dark:text-red-400'
  }
  
  // Se faltam menos de 7 dias
  const daysRemaining = Math.ceil((endDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
  if (daysRemaining <= 7) {
    return 'text-yellow-600 dark:text-yellow-400'
  }
  
  return 'text-green-600 dark:text-green-400'
}

// Lifecycle
onMounted(() => {
  fetchProjectData()
})

onUnmounted(() => {
  if (chart) {
    chart.destroy()
  }
})

watch(projectId, () => {
  fetchProjectData()
})
</script>
