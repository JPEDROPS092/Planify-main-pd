<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-2xl font-bold text-gray-800 dark:text-white">{{ project?.name || 'Carregando...' }}</h2>
        <p class="text-gray-600 dark:text-gray-400 mt-1">Visualização Kanban e Gerenciamento de Sprints</p>
      </div>
      <div class="flex space-x-2">
        <Button variant="outline" size="sm" @click="$router.push(`/projetos/${projectId}`)">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Voltar ao Projeto
        </Button>
        <Button variant="outline" size="sm" @click="activeTab = 'kanban'" :class="{ 'bg-blue-50 dark:bg-blue-900': activeTab === 'kanban' }">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
          Quadro Kanban
        </Button>
        <Button variant="outline" size="sm" @click="activeTab = 'sprint'" :class="{ 'bg-blue-50 dark:bg-blue-900': activeTab === 'sprint' }">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Sprints
        </Button>
        <Button variant="outline" size="sm" @click="activeTab = 'list'" :class="{ 'bg-blue-50 dark:bg-blue-900': activeTab === 'list' }">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
          </svg>
          Lista Reordenável
        </Button>
      </div>
    </div>

    <div v-if="loading" class="space-y-4">
      <SkeletonLoader type="list-item-avatar" :count="3" />
    </div>
    <div v-else-if="error" class="text-center text-red-500 dark:text-red-400 py-6">
      <p>{{ error.message || 'Erro ao carregar projeto.' }}</p>
      <Button variant="outline" size="sm" class="mt-2" @click="fetchProject">Tentar Novamente</Button>
    </div>
    <div v-else>
      <!-- Conteúdo baseado na aba ativa -->
      <div v-if="activeTab === 'kanban'">
        <KanbanBoard :project-id="projectId" @tasks-updated="handleTasksUpdated" />
      </div>
      <div v-else-if="activeTab === 'sprint'">
        <SprintManagement :project-id="projectId" @sprints-updated="handleSprintsUpdated" />
      </div>
      <div v-else-if="activeTab === 'list'">
        <DraggableTaskList :project-id="projectId" @tasks-reordered="handleTasksReordered" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectService } from '~/services/api/projects'
import { useNotification } from '~/composables/useNotification'
import KanbanBoard from '~/components/project/KanbanBoard.vue'
import SprintManagement from '~/components/project/SprintManagement.vue'
import DraggableTaskList from '~/components/project/DraggableTaskList.vue'

const route = useRoute()
const projectService = useProjectService()
const { showApiError } = useNotification()

// Estado
const projectId = computed(() => route.params.id as string)
const project = ref<any>(null)
const loading = ref(true)
const error = ref<Error | null>(null)
const activeTab = ref('kanban') // 'kanban' ou 'sprint'

// Funções
async function fetchProject() {
  if (!projectId.value) return
  
  loading.value = true
  error.value = null
  
  try {
    project.value = await projectService.retrieveProjeto(Number(projectId.value))
    // Mapear campos para o formato esperado pelo componente
    project.value = {
      ...project.value,
      name: project.value.titulo,
      description: project.value.descricao,
      start_date: project.value.data_inicio,
      end_date: project.value.data_fim
    }
  } catch (err: any) {
    error.value = err
    showApiError(err, 'Erro ao carregar projeto')
  } finally {
    loading.value = false
  }
}

function handleTasksUpdated(tasks: any[]) {
  console.log('Tarefas atualizadas:', tasks.length)
  // Aqui você pode implementar lógica adicional se necessário
}

function handleSprintsUpdated(sprints: any[]) {
  console.log('Sprints atualizadas:', sprints.length)
  // Aqui você pode implementar lógica adicional se necessário
}

function handleTasksReordered(tasks: any[]) {
  console.log('Tarefas reordenadas:', tasks.length)
  // Aqui você pode implementar lógica adicional se necessário
}

// Inicialização
onMounted(() => {
  fetchProject()
})
</script>

<style scoped>
/* Estilos específicos para esta página */
</style>
