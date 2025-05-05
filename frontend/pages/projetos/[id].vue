<template>
  <div class="space-y-6">
    <div v-if="isLoading" class="flex justify-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
    </div>

    <div v-else-if="error" class="bg-destructive/15 p-4 rounded-md text-destructive">
      {{ error }}
    </div>

    <template v-else>
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-2">
            <NuxtLink to="/projetos" class="text-muted-foreground hover:text-foreground">
              ← Voltar para Projetos
            </NuxtLink>
          </div>
          <h1 class="text-3xl font-bold tracking-tight mt-2">{{ project.titulo }}</h1>
        </div>
        <Button variant="outline" @click="editProject">Editar Projeto</Button>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <Card class="md:col-span-2">
          <div class="p-6">
            <h2 class="text-xl font-semibold mb-4">Detalhes do Projeto</h2>
            <div class="space-y-4">
              <div>
                <h3 class="text-sm font-medium text-muted-foreground">Descrição</h3>
                <p class="mt-1">{{ project.descricao }}</p>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <h3 class="text-sm font-medium text-muted-foreground">Status</h3>
                  <p class="mt-1" :class="{
                    'text-green-600': project.status === 'EM_ANDAMENTO',
                    'text-blue-600': project.status === 'PLANEJADO',
                    'text-gray-600': project.status === 'CONCLUIDO',
                    'text-red-600': project.status === 'CANCELADO'
                  }">
                    {{ formatStatus(project.status) }}
                  </p>
                </div>
                <div>
                  <h3 class="text-sm font-medium text-muted-foreground">Responsável</h3>
                  <p class="mt-1">{{ project.responsavel ? project.responsavel.nome : 'Não atribuído' }}</p>
                </div>
                <div>
                  <h3 class="text-sm font-medium text-muted-foreground">Data de Início</h3>
                  <p class="mt-1">{{ formatDate(project.data_inicio) }}</p>
                </div>
                <div>
                  <h3 class="text-sm font-medium text-muted-foreground">Data de Término</h3>
                  <p class="mt-1">{{ project.data_termino ? formatDate(project.data_termino) : 'Em andamento' }}</p>
                </div>
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <div class="p-6">
            <h2 class="text-xl font-semibold mb-4">Progresso</h2>
            <div class="space-y-4">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <span class="text-sm font-medium">Tarefas Concluídas</span>
                  <span class="text-sm font-medium">{{ taskStats.completed }}/{{ taskStats.total }}</span>
                </div>
                <div class="w-full bg-muted rounded-full h-2.5">
                  <div
                    class="bg-primary h-2.5 rounded-full"
                    :style="{ width: `${taskStats.percentage}%` }"
                  ></div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 text-center">
                <div class="bg-muted/50 p-4 rounded-lg">
                  <p class="text-2xl font-bold">{{ taskStats.inProgress }}</p>
                  <p class="text-sm text-muted-foreground">Em Andamento</p>
                </div>
                <div class="bg-muted/50 p-4 rounded-lg">
                  <p class="text-2xl font-bold">{{ taskStats.pending }}</p>
                  <p class="text-sm text-muted-foreground">Pendentes</p>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <div class="grid gap-6 md:grid-cols-2">
        <Card>
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold">Tarefas</h2>
              <Button size="sm" @click="showNewTaskModal = true">Nova Tarefa</Button>
            </div>
            <div v-if="tasks.length === 0" class="text-center py-4">
              <p class="text-muted-foreground">Nenhuma tarefa encontrada para este projeto.</p>
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="task in tasks"
                :key="task.id"
                class="flex items-start justify-between p-3 border rounded-md"
              >
                <div>
                  <div class="flex items-center gap-2">
                    <div
                      :class="{
                        'bg-blue-500': task.status === 'A_FAZER',
                        'bg-yellow-500': task.status === 'EM_ANDAMENTO',
                        'bg-green-500': task.status === 'FEITO'
                      }"
                      class="w-2 h-2 rounded-full"
                    ></div>
                    <h3 class="font-medium">{{ task.titulo }}</h3>
                  </div>
                  <p class="text-sm text-muted-foreground mt-1">{{ task.descricao }}</p>
                </div>
                <div class="flex items-center space-x-2">
                  <button class="text-muted-foreground hover:text-foreground" @click="editTask(task)">
                    ✏️
                  </button>
                  <button class="text-destructive hover:text-destructive/80" @click="deleteTask(task.id)">
                    🗑️
                  </button>
                </div>
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <div class="p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold">Riscos</h2>
              <Button size="sm" @click="showNewRiskModal = true">Novo Risco</Button>
            </div>
            <div v-if="risks.length === 0" class="text-center py-4">
              <p class="text-muted-foreground">Nenhum risco identificado para este projeto.</p>
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="risk in risks"
                :key="risk.id"
                class="flex items-start justify-between p-3 border rounded-md"
              >
                <div>
                  <div class="flex items-center gap-2">
                    <div
                      :class="{
                        'bg-green-500': risk.impacto === 'BAIXO',
                        'bg-yellow-500': risk.impacto === 'MEDIO',
                        'bg-red-500': risk.impacto === 'ALTO'
                      }"
                      class="w-2 h-2 rounded-full"
                    ></div>
                    <h3 class="font-medium">{{ risk.titulo }}</h3>
                  </div>
                  <p class="text-sm text-muted-foreground mt-1">{{ risk.descricao }}</p>
                </div>
                <div class="flex items-center space-x-2">
                  <button class="text-muted-foreground hover:text-foreground" @click="editRisk(risk)">
                    ✏️
                  </button>
                  <button class="text-destructive hover:text-destructive/80" @click="deleteRisk(risk.id)">
                    🗑️
                  </button>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </template>

    <!-- Modal de Nova Tarefa -->
    <div v-if="showNewTaskModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-background rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 class="text-xl font-bold mb-4">{{ editingTask ? 'Editar Tarefa' : 'Nova Tarefa' }}</h2>
        <form @submit.prevent="saveTask">
          <div class="space-y-4">
            <div>
              <label for="titulo" class="block text-sm font-medium mb-1">Título</label>
              <input
                id="titulo"
                v-model="newTask.titulo"
                type="text"
                class="w-full p-2 rounded-md border border-input"
                required
              />
            </div>
            <div>
              <label for="descricao" class="block text-sm font-medium mb-1">Descrição</label>
              <textarea
                id="descricao"
                v-model="newTask.descricao"
                class="w-full p-2 rounded-md border border-input"
                rows="3"
                required
              ></textarea>
            </div>
            <div>
              <label for="status" class="block text-sm font-medium mb-1">Status</label>
              <select
                id="status"
                v-model="newTask.status"
                class="w-full p-2 rounded-md border border-input"
                required
              >
                <option value="A_FAZER">A Fazer</option>
                <option value="EM_ANDAMENTO">Em Andamento</option>
                <option value="FEITO">Feito</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end space-x-2 mt-6">
            <Button variant="outline" type="button" @click="showNewTaskModal = false">Cancelar</Button>
            <Button type="submit" :disabled="isSaving">
              {{ isSaving ? 'Salvando...' : (editingTask ? 'Atualizar' : 'Criar') }}
            </Button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Novo Risco -->
    <div v-if="showNewRiskModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-background rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 class="text-xl font-bold mb-4">{{ editingRisk ? 'Editar Risco' : 'Novo Risco' }}</h2>
        <form @submit.prevent="saveRisk">
          <div class="space-y-4">
            <div>
              <label for="titulo" class="block text-sm font-medium mb-1">Título</label>
              <input
                id="titulo"
                v-model="newRisk.titulo"
                type="text"
                class="w-full p-2 rounded-md border border-input"
                required
              />
            </div>
            <div>
              <label for="descricao" class="block text-sm font-medium mb-1">Descrição</label>
              <textarea
                id="descricao"
                v-model="newRisk.descricao"
                class="w-full p-2 rounded-md border border-input"
                rows="3"
                required
              ></textarea>
            </div>
            <div>
              <label for="impacto" class="block text-sm font-medium mb-1">Impacto</label>
              <select
                id="impacto"
                v-model="newRisk.impacto"
                class="w-full p-2 rounded-md border border-input"
                required
              >
                <option value="BAIXO">Baixo</option>
                <option value="MEDIO">Médio</option>
                <option value="ALTO">Alto</option>
              </select>
            </div>
            <div>
              <label for="probabilidade" class="block text-sm font-medium mb-1">Probabilidade</label>
              <select
                id="probabilidade"
                v-model="newRisk.probabilidade"
                class="w-full p-2 rounded-md border border-input"
                required
              >
                <option value="BAIXA">Baixa</option>
                <option value="MEDIA">Média</option>
                <option value="ALTA">Alta</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end space-x-2 mt-6">
            <Button variant="outline" type="button" @click="showNewRiskModal = false">Cancelar</Button>
            <Button type="submit" :disabled="isSaving">
              {{ isSaving ? 'Salvando...' : (editingRisk ? 'Atualizar' : 'Criar') }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const projectId = route.params.id

const project = ref({})
const tasks = ref([])
const risks = ref([])
const isLoading = ref(true)
const error = ref('')
const isSaving = ref(false)

// Modais
const showNewTaskModal = ref(false)
const showNewRiskModal = ref(false)
const editingTask = ref(null)
const editingRisk = ref(null)

// Formulários
const newTask = ref({
  titulo: '',
  descricao: '',
  status: 'A_FAZER',
  projeto: projectId
})

const newRisk = ref({
  titulo: '',
  descricao: '',
  impacto: 'MEDIO',
  probabilidade: 'MEDIA',
  projeto: projectId
})

// Estatísticas de tarefas
const taskStats = computed(() => {
  const total = tasks.value.length
  const completed = tasks.value.filter(task => task.status === 'FEITO').length
  const inProgress = tasks.value.filter(task => task.status === 'EM_ANDAMENTO').length
  const pending = tasks.value.filter(task => task.status === 'A_FAZER').length
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0
  
  return {
    total,
    completed,
    inProgress,
    pending,
    percentage
  }
})

onMounted(async () => {
  await fetchProjectData()
})

const fetchProjectData = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    const headers = {
      Authorization: `Bearer ${token}`
    }
    
    // Buscar dados do projeto
    const projectResponse = await axios.get(`http://localhost:8001/api/projects/${projectId}/`, { headers })
    project.value = projectResponse.data
    
    // Buscar tarefas do projeto
    const tasksResponse = await axios.get(`http://localhost:8001/api/tasks/?projeto=${projectId}`, { headers })
    tasks.value = tasksResponse.data
    
    // Buscar riscos do projeto
    const risksResponse = await axios.get(`http://localhost:8001/api/risks/?projeto=${projectId}`, { headers })
    risks.value = risksResponse.data
  } catch (err) {
    console.error('Erro ao buscar dados do projeto:', err)
    error.value = 'Não foi possível carregar os dados do projeto. Por favor, tente novamente.'
  } finally {
    isLoading.value = false
  }
}

const formatStatus = (status) => {
  const statusMap = {
    'PLANEJADO': 'Planejado',
    'EM_ANDAMENTO': 'Em Andamento',
    'CONCLUIDO': 'Concluído',
    'CANCELADO': 'Cancelado'
  }
  return statusMap[status] || status
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('pt-BR')
}

// Funções para tarefas
const resetTaskForm = () => {
  newTask.value = {
    titulo: '',
    descricao: '',
    status: 'A_FAZER',
    projeto: projectId
  }
  editingTask.value = null
}

const editTask = (task) => {
  editingTask.value = task
  newTask.value = {
    titulo: task.titulo,
    descricao: task.descricao,
    status: task.status,
    projeto: projectId
  }
  showNewTaskModal.value = true
}

const saveTask = async () => {
  isSaving.value = true
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    const headers = {
      Authorization: `Bearer ${token}`
    }
    
    if (editingTask.value) {
      // Atualizar tarefa existente
      await axios.put(`http://localhost:8001/api/tasks/${editingTask.value.id}/`, newTask.value, { headers })
    } else {
      // Criar nova tarefa
      await axios.post('http://localhost:8001/api/tasks/', newTask.value, { headers })
    }
    
    // Recarregar as tarefas
    const tasksResponse = await axios.get(`http://localhost:8001/api/tasks/?projeto=${projectId}`, { headers })
    tasks.value = tasksResponse.data
    
    // Fechar o modal e resetar o formulário
    showNewTaskModal.value = false
    resetTaskForm()
  } catch (err) {
    console.error('Erro ao salvar tarefa:', err)
    error.value = 'Não foi possível salvar a tarefa. Por favor, tente novamente.'
  } finally {
    isSaving.value = false
  }
}

const deleteTask = async (taskId) => {
  if (!confirm('Tem certeza que deseja excluir esta tarefa?')) {
    return
  }
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    await axios.delete(`http://localhost:8001/api/tasks/${taskId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    // Recarregar as tarefas
    const tasksResponse = await axios.get(`http://localhost:8001/api/tasks/?projeto=${projectId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    tasks.value = tasksResponse.data
  } catch (err) {
    console.error('Erro ao excluir tarefa:', err)
    error.value = 'Não foi possível excluir a tarefa. Por favor, tente novamente.'
  }
}

// Funções para riscos
const resetRiskForm = () => {
  newRisk.value = {
    titulo: '',
    descricao: '',
    impacto: 'MEDIO',
    probabilidade: 'MEDIA',
    projeto: projectId
  }
  editingRisk.value = null
}

const editRisk = (risk) => {
  editingRisk.value = risk
  newRisk.value = {
    titulo: risk.titulo,
    descricao: risk.descricao,
    impacto: risk.impacto,
    probabilidade: risk.probabilidade,
    projeto: projectId
  }
  showNewRiskModal.value = true
}

const saveRisk = async () => {
  isSaving.value = true
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    const headers = {
      Authorization: `Bearer ${token}`
    }
    
    if (editingRisk.value) {
      // Atualizar risco existente
      await axios.put(`http://localhost:8001/api/risks/${editingRisk.value.id}/`, newRisk.value, { headers })
    } else {
      // Criar novo risco
      await axios.post('http://localhost:8001/api/risks/', newRisk.value, { headers })
    }
    
    // Recarregar os riscos
    const risksResponse = await axios.get(`http://localhost:8001/api/risks/?projeto=${projectId}`, { headers })
    risks.value = risksResponse.data
    
    // Fechar o modal e resetar o formulário
    showNewRiskModal.value = false
    resetRiskForm()
  } catch (err) {
    console.error('Erro ao salvar risco:', err)
    error.value = 'Não foi possível salvar o risco. Por favor, tente novamente.'
  } finally {
    isSaving.value = false
  }
}

const deleteRisk = async (riskId) => {
  if (!confirm('Tem certeza que deseja excluir este risco?')) {
    return
  }
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    await axios.delete(`http://localhost:8001/api/risks/${riskId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    // Recarregar os riscos
    const risksResponse = await axios.get(`http://localhost:8001/api/risks/?projeto=${projectId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    risks.value = risksResponse.data
  } catch (err) {
    console.error('Erro ao excluir risco:', err)
    error.value = 'Não foi possível excluir o risco. Por favor, tente novamente.'
  }
}

// Editar projeto
const editProject = () => {
  router.push(`/projetos/editar/${projectId}`)
}
</script>
