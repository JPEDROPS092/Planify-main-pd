<template>
  <div class="project-dashboard">
    <!-- Painel superior com informações gerais do projeto -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <!-- Resumo do Projeto -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-4">Resumo do Projeto</h3>
        <div class="space-y-3">
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Nome:</span>
            <p class="font-medium text-gray-800 dark:text-gray-200">{{ project?.nome }}</p>
          </div>
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Status:</span>
            <span class="ml-2 px-2 py-1 text-xs font-medium rounded-full" :class="getStatusClass(project?.status)">
              {{ getStatusText(project?.status) }}
            </span>
          </div>
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Gerente:</span>
            <p class="font-medium text-gray-800 dark:text-gray-200">{{ project?.gerente_nome }}</p>
          </div>
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Progresso Geral:</span>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mt-1">
              <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${project?.progresso || 0}%` }"></div>
            </div>
            <p class="text-right text-xs text-gray-500 dark:text-gray-400 mt-1">{{ project?.progresso || 0 }}%</p>
          </div>
        </div>
      </div>
      
      <!-- Datas e Prazos -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-4">Datas e Prazos</h3>
        <div class="space-y-3">
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Data de Início:</span>
            <p class="font-medium text-gray-800 dark:text-gray-200">{{ formatDate(project?.data_inicio) }}</p>
          </div>
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Data de Término:</span>
            <p class="font-medium text-gray-800 dark:text-gray-200">{{ formatDate(project?.data_fim) }}</p>
          </div>
          <div>
            <span class="text-sm text-gray-500 dark:text-gray-400">Duração:</span>
            <p class="font-medium text-gray-800 dark:text-gray-200">{{ calculateDuration(project?.data_inicio, project?.data_fim) }}</p>
          </div>
          <div v-if="project?.data_fim">
            <span class="text-sm text-gray-500 dark:text-gray-400">Dias Restantes:</span>
            <p class="font-medium" :class="getRemainingDaysClass(project?.data_fim)">
              {{ calculateRemainingDays(project?.data_fim) }}
            </p>
          </div>
        </div>
      </div>
      
      <!-- Estatísticas Rápidas -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-4">Estatísticas</h3>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400">Tarefas</p>
            <p class="text-2xl font-bold text-gray-800 dark:text-gray-200">{{ taskStats.total }}</p>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400">Concluídas</p>
            <p class="text-2xl font-bold text-green-600 dark:text-green-400">{{ taskStats.completed }}</p>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400">Membros</p>
            <p class="text-2xl font-bold text-gray-800 dark:text-gray-200">{{ teamStats.members }}</p>
          </div>
          <div class="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400">Riscos Ativos</p>
            <p class="text-2xl font-bold text-yellow-600 dark:text-yellow-400">{{ riskStats.active }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Tabs para navegar entre diferentes visualizações -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm mb-6">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="flex -mb-px">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-4 px-6 text-sm font-medium border-b-2 focus:outline-none',
              activeTab === tab.id 
                ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-300' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:border-gray-500'
            ]"
          >
            <div class="flex items-center">
              <span v-html="tab.icon"></span>
              <span class="ml-2">{{ tab.name }}</span>
            </div>
          </button>
        </nav>
      </div>
    </div>
    
    <!-- Conteúdo das Tabs -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
      <div v-if="activeTab === 'overview'">
        <ProjectOverview :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'kanban'">
        <KanbanBoard :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'gantt'">
        <GanttChart :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'tasks'">
        <ProjectTasks :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'team'">
        <ProjectTeam :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'risks'">
        <ProjectRisks :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'costs'">
        <ProjectCosts :project-id="projectId" />
      </div>
      <div v-if="activeTab === 'documents'">
        <ProjectDocuments :project-id="projectId" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useProjectService } from '~/services/api/projects'
import { useTaskService } from '~/services/api/tasks'
import { useTeamService } from '~/services/api/teams'
import { useRiskService } from '~/services/api/risks'
import ProjectOverview from '~/components/project/ProjectOverview.vue'
import ProjectTasks from '~/components/project/ProjectTasks.vue'
import ProjectTeam from '~/components/project/ProjectTeam.vue'
import ProjectRisks from '~/components/project/ProjectRisks.vue'
import ProjectCosts from '~/components/project/ProjectCosts.vue'
import ProjectDocuments from '~/components/project/ProjectDocuments.vue'
import KanbanBoard from '~/components/project/KanbanBoard.vue'
import GanttChart from '~/components/project/GanttChart.vue'
import type { Projeto } from '~/services/api/types'

const props = defineProps<{
  projectId: number
}>()

const projectService = useProjectService()
const taskService = useTaskService()
const teamService = useTeamService()
const riskService = useRiskService()

// Estado do componente
const project = ref<Projeto | null>(null)
const loading = ref(true)
const error = ref<Error | null>(null)
const activeTab = ref('overview')

// Estatísticas
const taskStats = ref({
  total: 0,
  completed: 0,
  inProgress: 0,
  pending: 0,
  blocked: 0
})

const teamStats = ref({
  members: 0,
  teams: 0
})

const riskStats = ref({
  total: 0,
  active: 0,
  mitigated: 0
})

// Tabs disponíveis
const tabs = ref([
  { 
    id: 'overview', 
    name: 'Visão Geral',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>'
  },
  { 
    id: 'kanban', 
    name: 'Quadro Kanban',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" /></svg>'
  },
  { 
    id: 'gantt', 
    name: 'Gráfico Gantt',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>'
  },
  { 
    id: 'tasks', 
    name: 'Tarefas',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>'
  },
  { 
    id: 'team', 
    name: 'Equipe',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>'
  },
  { 
    id: 'risks', 
    name: 'Riscos',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>'
  },
  { 
    id: 'costs', 
    name: 'Custos',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>'
  },
  { 
    id: 'documents', 
    name: 'Documentos',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>'
  }
])

// Funções para formatar dados
function formatDate(dateString?: string) {
  if (!dateString) return 'Não definido'
  return new Date(dateString).toLocaleDateString('pt-BR')
}

function calculateDuration(startDate?: string, endDate?: string) {
  if (!startDate) return 'Não definido'
  
  const start = new Date(startDate)
  const end = endDate ? new Date(endDate) : new Date()
  
  const diffTime = Math.abs(end.getTime() - start.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  return `${diffDays} dias`
}

function calculateRemainingDays(endDate?: string) {
  if (!endDate) return 'Não definido'
  
  const end = new Date(endDate)
  const today = new Date()
  
  const diffTime = end.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return `Atrasado por ${Math.abs(diffDays)} dias`
  } else if (diffDays === 0) {
    return 'Vence hoje'
  } else {
    return `${diffDays} dias restantes`
  }
}

function getRemainingDaysClass(endDate?: string) {
  if (!endDate) return 'text-gray-800 dark:text-gray-200'
  
  const end = new Date(endDate)
  const today = new Date()
  
  const diffTime = end.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) {
    return 'text-red-600 dark:text-red-400'
  } else if (diffDays <= 7) {
    return 'text-yellow-600 dark:text-yellow-400'
  } else {
    return 'text-green-600 dark:text-green-400'
  }
}

function getStatusClass(status?: string) {
  if (!status) return 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
  
  switch (status) {
    case 'PLANEJADO':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
    case 'EM_ANDAMENTO':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
    case 'PAUSADO':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
    case 'CONCLUIDO':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
    case 'CANCELADO':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
    default:
      return 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
  }
}

function getStatusText(status?: string) {
  if (!status) return 'Não definido'
  
  switch (status) {
    case 'PLANEJADO':
      return 'Planejado'
    case 'EM_ANDAMENTO':
      return 'Em Andamento'
    case 'PAUSADO':
      return 'Pausado'
    case 'CONCLUIDO':
      return 'Concluído'
    case 'CANCELADO':
      return 'Cancelado'
    default:
      return status
  }
}

// Funções para carregar dados
async function fetchProjectDetails() {
  if (!props.projectId) return
  
  loading.value = true
  error.value = null
  
  try {
    project.value = await projectService.retrieveProjeto(props.projectId)
    await Promise.all([
      fetchTaskStats(),
      fetchTeamStats(),
      fetchRiskStats()
    ])
  } catch (err: any) {
    error.value = err
    console.error('Erro ao carregar detalhes do projeto:', err)
  } finally {
    loading.value = false
  }
}

async function fetchTaskStats() {
  try {
    const response = await taskService.listTarefas({ projeto: props.projectId })
    const tasks = response.results
    
    taskStats.value = {
      total: tasks.length,
      completed: tasks.filter(t => t.status === 'CONCLUIDO').length,
      inProgress: tasks.filter(t => t.status === 'EM_ANDAMENTO').length,
      pending: tasks.filter(t => t.status === 'PENDENTE').length,
      blocked: tasks.filter(t => t.status === 'BLOQUEADO').length
    }
  } catch (err) {
    console.error('Erro ao carregar estatísticas de tarefas:', err)
  }
}

async function fetchTeamStats() {
  try {
    const response = await teamService.listEquipes({ projeto: props.projectId })
    const teams = response.results
    
    let memberCount = 0
    for (const team of teams) {
      memberCount += team.membros_count || 0
    }
    
    teamStats.value = {
      members: memberCount,
      teams: teams.length
    }
  } catch (err) {
    console.error('Erro ao carregar estatísticas da equipe:', err)
  }
}

async function fetchRiskStats() {
  try {
    const response = await riskService.listRiscos({ projeto: props.projectId })
    const risks = response.results
    
    riskStats.value = {
      total: risks.length,
      active: risks.filter(r => r.status !== 'MITIGADO' && r.status !== 'ACEITO').length,
      mitigated: risks.filter(r => r.status === 'MITIGADO' || r.status === 'ACEITO').length
    }
  } catch (err) {
    console.error('Erro ao carregar estatísticas de riscos:', err)
  }
}

// Carregar dados quando o componente for montado
onMounted(() => {
  fetchProjectDetails()
})

// Recarregar quando o projectId mudar
watch(() => props.projectId, (newId) => {
  if (newId) {
    fetchProjectDetails()
  }
})
</script>

<style scoped>
.project-dashboard {
  min-height: 400px;
}
</style>
