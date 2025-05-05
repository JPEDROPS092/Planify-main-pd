<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold tracking-tight">Projetos</h1>
      <Button @click="showNewProjectModal = true">Novo Projeto</Button>
    </div>

    <div v-if="isLoading" class="flex justify-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
    </div>

    <div v-else-if="error" class="bg-destructive/15 p-4 rounded-md text-destructive">
      {{ error }}
    </div>

    <div v-else-if="projects.length === 0" class="text-center py-10">
      <p class="text-muted-foreground">Nenhum projeto encontrado. Crie um novo projeto para começar.</p>
    </div>

    <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <Card v-for="project in projects" :key="project.id" class="overflow-hidden">
        <div class="p-6">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="text-lg font-semibold">{{ project.titulo }}</h3>
              <p class="text-sm text-muted-foreground mt-1">{{ project.descricao }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <button class="text-muted-foreground hover:text-foreground" @click="editProject(project)">
                ✏️
              </button>
              <button class="text-destructive hover:text-destructive/80" @click="deleteProject(project.id)">
                🗑️
              </button>
            </div>
          </div>
          <div class="mt-4 space-y-2">
            <div class="flex items-center text-sm">
              <span class="font-medium mr-2">Status:</span>
              <span :class="{
                'text-green-600': project.status === 'EM_ANDAMENTO',
                'text-blue-600': project.status === 'PLANEJADO',
                'text-gray-600': project.status === 'CONCLUIDO',
                'text-red-600': project.status === 'CANCELADO'
              }">
                {{ formatStatus(project.status) }}
              </span>
            </div>
            <div class="flex items-center text-sm">
              <span class="font-medium mr-2">Data de Início:</span>
              <span>{{ formatDate(project.data_inicio) }}</span>
            </div>
            <div class="flex items-center text-sm">
              <span class="font-medium mr-2">Data de Término:</span>
              <span>{{ project.data_termino ? formatDate(project.data_termino) : 'Em andamento' }}</span>
            </div>
          </div>
          <div class="mt-4">
            <NuxtLink :to="`/projetos/${project.id}`">
              <Button variant="outline" class="w-full">Ver Detalhes</Button>
            </NuxtLink>
          </div>
        </div>
      </Card>
    </div>

    <!-- Modal de Novo Projeto -->
    <div v-if="showNewProjectModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-background rounded-lg shadow-lg w-full max-w-md p-6">
        <h2 class="text-xl font-bold mb-4">{{ editingProject ? 'Editar Projeto' : 'Novo Projeto' }}</h2>
        <form @submit.prevent="saveProject">
          <div class="space-y-4">
            <div>
              <label for="titulo" class="block text-sm font-medium mb-1">Título</label>
              <input
                id="titulo"
                v-model="newProject.titulo"
                type="text"
                class="w-full p-2 rounded-md border border-input"
                required
              />
            </div>
            <div>
              <label for="descricao" class="block text-sm font-medium mb-1">Descrição</label>
              <textarea
                id="descricao"
                v-model="newProject.descricao"
                class="w-full p-2 rounded-md border border-input"
                rows="3"
                required
              ></textarea>
            </div>
            <div>
              <label for="status" class="block text-sm font-medium mb-1">Status</label>
              <select
                id="status"
                v-model="newProject.status"
                class="w-full p-2 rounded-md border border-input"
                required
              >
                <option value="PLANEJADO">Planejado</option>
                <option value="EM_ANDAMENTO">Em Andamento</option>
                <option value="CONCLUIDO">Concluído</option>
                <option value="CANCELADO">Cancelado</option>
              </select>
            </div>
            <div>
              <label for="data_inicio" class="block text-sm font-medium mb-1">Data de Início</label>
              <input
                id="data_inicio"
                v-model="newProject.data_inicio"
                type="date"
                class="w-full p-2 rounded-md border border-input"
                required
              />
            </div>
            <div>
              <label for="data_termino" class="block text-sm font-medium mb-1">Data de Término (opcional)</label>
              <input
                id="data_termino"
                v-model="newProject.data_termino"
                type="date"
                class="w-full p-2 rounded-md border border-input"
              />
            </div>
          </div>
          <div class="flex justify-end space-x-2 mt-6">
            <Button variant="outline" type="button" @click="showNewProjectModal = false">Cancelar</Button>
            <Button type="submit" :disabled="isSaving">
              {{ isSaving ? 'Salvando...' : (editingProject ? 'Atualizar' : 'Criar') }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const projects = ref([])
const isLoading = ref(true)
const error = ref('')
const showNewProjectModal = ref(false)
const isSaving = ref(false)
const editingProject = ref(null)

const newProject = ref({
  titulo: '',
  descricao: '',
  status: 'PLANEJADO',
  data_inicio: new Date().toISOString().split('T')[0],
  data_termino: ''
})

onMounted(async () => {
  await fetchProjects()
})

const fetchProjects = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      navigateTo('/login')
      return
    }
    
    const response = await axios.get('http://localhost:8001/api/projects/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    projects.value = response.data
  } catch (err) {
    console.error('Erro ao buscar projetos:', err)
    error.value = 'Não foi possível carregar os projetos. Por favor, tente novamente.'
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

const resetForm = () => {
  newProject.value = {
    titulo: '',
    descricao: '',
    status: 'PLANEJADO',
    data_inicio: new Date().toISOString().split('T')[0],
    data_termino: ''
  }
  editingProject.value = null
}

const editProject = (project) => {
  editingProject.value = project
  newProject.value = {
    titulo: project.titulo,
    descricao: project.descricao,
    status: project.status,
    data_inicio: project.data_inicio,
    data_termino: project.data_termino || ''
  }
  showNewProjectModal.value = true
}

const saveProject = async () => {
  isSaving.value = true
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      navigateTo('/login')
      return
    }
    
    const headers = {
      Authorization: `Bearer ${token}`
    }
    
    if (editingProject.value) {
      // Atualizar projeto existente
      await axios.put(`http://localhost:8001/api/projects/${editingProject.value.id}/`, newProject.value, { headers })
    } else {
      // Criar novo projeto
      await axios.post('http://localhost:8001/api/projects/', newProject.value, { headers })
    }
    
    // Recarregar a lista de projetos
    await fetchProjects()
    
    // Fechar o modal e resetar o formulário
    showNewProjectModal.value = false
    resetForm()
  } catch (err) {
    console.error('Erro ao salvar projeto:', err)
    error.value = 'Não foi possível salvar o projeto. Por favor, tente novamente.'
  } finally {
    isSaving.value = false
  }
}

const deleteProject = async (projectId) => {
  if (!confirm('Tem certeza que deseja excluir este projeto?')) {
    return
  }
  
  try {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      navigateTo('/login')
      return
    }
    
    await axios.delete(`http://localhost:8001/api/projects/${projectId}/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    // Recarregar a lista de projetos
    await fetchProjects()
  } catch (err) {
    console.error('Erro ao excluir projeto:', err)
    error.value = 'Não foi possível excluir o projeto. Por favor, tente novamente.'
  }
}
</script>
