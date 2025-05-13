<template>
  <div class="container mx-auto p-4 md:p-6">
    <div v-if="loadingProject" class="flex justify-center items-center h-64">
      <SkeletonLoader type="article" :count="3" />
    </div>
    <div v-else-if="projectError" class="text-center text-red-500 dark:text-red-400 py-10">
      <h2 class="text-2xl font-semibold mb-2">Erro ao Carregar Projeto</h2>
      <p>{{ projectError.message || 'Não foi possível carregar os detalhes do projeto.' }}</p>
      <Button class="mt-4" @click="fetchProjectDetails">Tentar Novamente</Button>
    </div>
    <div v-else-if="project" class="space-y-8">
      <!-- Cabeçalho do Projeto -->
      <header class="pb-6 border-b border-gray-200 dark:border-gray-700">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h1 class="text-3xl md:text-4xl font-bold text-gray-800 dark:text-white mb-2">{{ project.name }}</h1>
            <p class="text-gray-600 dark:text-gray-400 text-lg">{{ project.description }}</p>
          </div>
          <div class="mt-4 md:mt-0 flex space-x-2">
            <Button variant="outline" @click="navigateToEditProject">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
              </svg>
              Editar
            </Button>
            <!-- Outros botões de ação rápida podem ser adicionados aqui -->
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-sm">
          <div>
            <span class="text-gray-500 dark:text-gray-400 block">Status</span>
            <span class="font-semibold text-gray-700 dark:text-gray-300 py-1 px-2 rounded-full text-xs uppercase tracking-wider" :class="getStatusClass(project.status)">
              {{ project.status }}
            </span>
          </div>
          <div>
            <span class="text-gray-500 dark:text-gray-400 block">Gerente</span>
            <span class="font-semibold text-gray-700 dark:text-gray-300">{{ projectManagerName || 'N/A' }}</span>
          </div>
          <div>
            <span class="text-gray-500 dark:text-gray-400 block">Data de Início</span>
            <span class="font-semibold text-gray-700 dark:text-gray-300">{{ formatDate(project.start_date) }}</span>
          </div>
          <div>
            <span class="text-gray-500 dark:text-gray-400 block">Data de Término</span>
            <span class="font-semibold text-gray-700 dark:text-gray-300">{{ formatDate(project.end_date) }}</span>
          </div>
          <div v-if="project.budget">
            <span class="text-gray-500 dark:text-gray-400 block">Orçamento</span>
            <span class="font-semibold text-gray-700 dark:text-gray-300">{{ formatCurrency(project.budget) }}</span>
          </div>
        </div>
      </header>

      <!-- Tabs para seções de detalhes -->
      <nav class="flex border-b border-gray-200 dark:border-gray-700 -mb-px">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'py-4 px-1 mr-6 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === tab.id 
              ? 'border-blue-500 text-blue-600 dark:border-blue-400 dark:text-blue-300' 
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:border-gray-500'
          ]"
        >
          {{ tab.name }}
        </button>
      </nav>

      <!-- Conteúdo das Tabs -->
      <div class="mt-0">
        <div v-if="activeTab === 'overview'">
          <h2 class="text-xl font-semibold text-gray-700 dark:text-gray-200 mb-4">Visão Geral</h2>
          <p class="text-gray-600 dark:text-gray-400">Gráficos e métricas chave do projeto (a implementar).</p>
          <!-- TODO: Implementar gráficos de progresso, resumo de orçamento, etc. -->
        </div>
        <div v-if="activeTab === 'tasks'">
          <ProjectTasks :project-id="project.id" />
        </div>
        <div v-if="activeTab === 'team'">
          <ProjectTeam :project-id="project.id" />
        </div>
        <div v-if="activeTab === 'risks'">
          <ProjectRisks :project-id="project.id" />
        </div>
        <div v-if="activeTab === 'costs'">
          <ProjectCosts :project-id="project.id" />
        </div>
        <!-- Adicionar mais seções conforme necessário (Documentos, Comunicação, etc.) -->
      </div>
    </div>
    <div v-else class="text-center text-gray-500 dark:text-gray-400 py-10">
      <p>Nenhum projeto encontrado com este ID.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectService } from '~/services/projectService'
import type { Project } from '~/services/projectService'
import { useUserService } from '~/services/userService'
import type { User } from '~/services/userService'
import { useNotification } from '~/composables/useNotification'
import Button from '~/components/ui/Button.vue'
import SkeletonLoader from '~/components/SkeletonLoader.vue'
// Importar componentes para as tabs (a serem criados)
import ProjectTasks from '~/components/project/ProjectTasks.vue'
import ProjectTeam from '~/components/project/ProjectTeam.vue'
import ProjectRisks from '~/components/project/ProjectRisks.vue'
import ProjectCosts from '~/components/project/ProjectCosts.vue'

definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'] // Adicionando middleware de autenticação
})

const route = useRoute()
const router = useRouter()
const projectService = useProjectService()
const userService = useUserService()
const { success: notifySuccess, error: notifyError, showApiError } = useNotification()

const projectId = computed(() => Number(route.params.id))
const project = ref<Project | null>(null)
const projectManager = ref<User | null>(null)
const loadingProject = ref(true)
const projectError = ref<Error | null>(null)

const activeTab = ref('overview')
const tabs = [
  { id: 'overview', name: 'Visão Geral' },
  { id: 'tasks', name: 'Tarefas' },
  { id: 'team', name: 'Equipe' },
  { id: 'risks', name: 'Riscos' },
  { id: 'costs', name: 'Custos' }
]

const projectManagerName = computed(() => {
  if (projectManager.value) {
    return `${projectManager.value.first_name} ${projectManager.value.last_name}`.trim() || projectManager.value.username
  }
  return 'N/A'
})

async function fetchProjectDetails() {
  if (!projectId.value) {
    projectError.value = new Error('ID do projeto inválido.')
    loadingProject.value = false
    return
  }

  loadingProject.value = true
  projectError.value = null
  try {
    const fetchedProject = await projectService.getById(projectId.value)
    project.value = fetchedProject

    if (fetchedProject && fetchedProject.manager) {
      try {
        projectManager.value = await userService.getUserById(fetchedProject.manager)
      } catch (userError) {
        console.warn('Erro ao buscar gerente do projeto:', userError)
        projectManager.value = null // ou algum usuário placeholder
      }
    }
    
  } catch (error: any) {
    projectError.value = error
    showApiError(error)
    project.value = null
  } finally {
    loadingProject.value = false
  }
}

function navigateToEditProject() {
  if (project.value?.id) {
    router.push(`/projetos/editar/${project.value.id}`)
  }
}

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const formatCurrency = (value?: number) => {
  if (value === undefined || value === null) return 'N/A'
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)
}

const getStatusClass = (status: string) => {
  switch (status?.toLowerCase()) {
    case 'planejado': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    case 'em andamento': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    case 'concluído': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    case 'atrasado': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
    case 'cancelado': return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  }
}

onMounted(() => {
  fetchProjectDetails()
})

// Recarregar dados se o ID do projeto na rota mudar
watch(projectId, (newId, oldId) => {
  if (newId !== oldId && newId) {
    fetchProjectDetails()
  }
})
</script>

<style scoped>
/* Estilos adicionais podem ser adicionados aqui, se necessário */
</style>
