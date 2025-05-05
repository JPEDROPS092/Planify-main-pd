<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Equipes</h1>
        <button @click="openNewTeamModal" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2">
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Nova Equipe
        </button>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-8">
        <div class="h-8 w-8 animate-spin rounded-full border-2 border-blue-600 border-t-transparent dark:border-blue-500"></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4 text-red-700 dark:bg-red-900/30 dark:text-red-400">
        <p>{{ error }}</p>
        <button @click="fetchTeams" class="mt-2 text-sm font-medium underline">Tentar novamente</button>
      </div>

      <!-- Empty state -->
      <div v-else-if="teams.length === 0" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <EmptyState>
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-10 w-10 text-gray-400 dark:text-gray-500">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </template>
          <template #title>Nenhuma equipe encontrada</template>
          <template #description>Comece criando sua primeira equipe para organizar os membros do projeto.</template>
          <template #action>
            <button
              @click="openNewTeamModal"
              class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4 mr-2">
                <path d="M5 12h14"></path>
                <path d="M12 5v14"></path>
              </svg>
              Nova Equipe
            </button>
          </template>
        </EmptyState>
      </div>

      <!-- Teams list -->
      <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="team in teams" :key="team.id" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ team.nome }}</h3>
            <div class="flex items-center space-x-2">
              <button @click="editTeam(team)" class="rounded-full p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"></path>
                  <path d="m15 5 4 4"></path>
                </svg>
              </button>
              <button @click="viewTeam(team.id)" class="rounded-full p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
              </button>
            </div>
          </div>
          <p class="mb-4 text-sm text-gray-500 dark:text-gray-400">{{ team.descricao || 'Sem descrição' }}</p>
          <div class="mb-4">
            <div class="text-xs font-medium text-gray-500 dark:text-gray-400">Membros</div>
            <div class="mt-2 flex -space-x-2 overflow-hidden">
              <div v-for="(member, index) in team.membros?.slice(0, 5) || []" :key="index" class="inline-flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-gray-200 text-xs font-medium text-gray-700 dark:border-gray-800 dark:bg-gray-700 dark:text-gray-300">
                {{ getMemberInitials(member) }}
              </div>
              <div v-if="(team.membros?.length || 0) > 5" class="inline-flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-gray-200 text-xs font-medium text-gray-700 dark:border-gray-800 dark:bg-gray-700 dark:text-gray-300">
                +{{ team.membros.length - 5 }}
              </div>
              <div v-if="!team.membros?.length" class="text-sm text-gray-500 dark:text-gray-400">
                Nenhum membro
              </div>
            </div>
          </div>
          <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <div>Criada em: {{ formatDate(team.data_criacao) }}</div>
            <div class="rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-700 dark:bg-green-900/30 dark:text-green-400">
              {{ team.status || 'Ativa' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Team Modal -->
      <div v-if="showTeamModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ editingTeam ? 'Editar Equipe' : 'Nova Equipe' }}</h3>
            <button @click="showTeamModal = false" class="rounded-full p-1 hover:bg-gray-100 dark:hover:bg-gray-700">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-gray-500 dark:text-gray-400">
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="saveTeam" class="mt-4 space-y-4">
            <div>
              <label for="nome" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nome da Equipe</label>
              <input
                id="nome"
                v-model="teamForm.nome"
                type="text"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label for="descricao" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Descrição</label>
              <textarea
                id="descricao"
                v-model="teamForm.descricao"
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              ></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Membros</label>
              <p class="text-xs text-gray-500 dark:text-gray-400">Funcionalidade de adicionar membros será implementada em breve.</p>
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showTeamModal = false"
                class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-700 dark:hover:bg-blue-600"
                :disabled="saving"
              >
                <svg v-if="saving" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 inline-block h-4 w-4 animate-spin">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
                </svg>
                {{ saving ? 'Salvando...' : 'Salvar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNuxtApp } from '#app'

const router = useRouter()
const { $api } = useNuxtApp()

// Estados
const teams = ref([])
const loading = ref(true)
const error = ref('')
const showTeamModal = ref(false)
const saving = ref(false)
const editingTeam = ref(null)
const teamForm = ref({
  nome: '',
  descricao: '',
  membros: []
})

// Buscar equipes
const fetchTeams = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await $api.get('/api/teams/')
    teams.value = response.data.results || response.data || []
  } catch (err) {
    console.error('Erro ao buscar equipes:', err)
    error.value = 'Não foi possível carregar as equipes. Por favor, tente novamente.'
    
    // Dados de exemplo para demonstração
    teams.value = [
      { id: 1, nome: 'Equipe de Desenvolvimento', descricao: 'Responsável pelo desenvolvimento do software', membros: [{nome: 'João Silva'}, {nome: 'Maria Santos'}], data_criacao: '2025-04-15', status: 'Ativa' },
      { id: 2, nome: 'Equipe de Design', descricao: 'Responsável pelo design da interface', membros: [{nome: 'Pedro Alves'}, {nome: 'Ana Oliveira'}], data_criacao: '2025-04-20', status: 'Ativa' },
      { id: 3, nome: 'Equipe de Testes', descricao: 'Responsável pelos testes e garantia de qualidade', membros: [{nome: 'Carlos Mendes'}, {nome: 'Lúcia Ferreira'}], data_criacao: '2025-04-25', status: 'Ativa' }
    ]
  } finally {
    loading.value = false
  }
}

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return 'Data não informada'
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date)
}

// Obter iniciais do membro
const getMemberInitials = (member) => {
  if (!member || !member.nome) return '?'
  
  return member.nome
    .split(' ')
    .map(name => name[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}

// Abrir modal de nova equipe
const openNewTeamModal = () => {
  editingTeam.value = null
  teamForm.value = {
    nome: '',
    descricao: '',
    membros: []
  }
  showTeamModal.value = true
}

// Editar equipe
const editTeam = (team) => {
  editingTeam.value = team
  teamForm.value = {
    nome: team.nome,
    descricao: team.descricao || '',
    membros: team.membros || []
  }
  showTeamModal.value = true
}

// Salvar equipe
const saveTeam = async () => {
  saving.value = true
  
  try {
    if (editingTeam.value) {
      // Atualizar equipe existente
      await $api.put(`/api/teams/${editingTeam.value.id}/`, teamForm.value)
      
      // Atualizar a lista de equipes
      teams.value = teams.value.map(team => {
        if (team.id === editingTeam.value.id) {
          return { ...team, ...teamForm.value }
        }
        return team
      })
    } else {
      // Criar nova equipe
      const response = await $api.post('/api/teams/', teamForm.value)
      teams.value.push(response.data)
    }
    
    showTeamModal.value = false
  } catch (err) {
    console.error('Erro ao salvar equipe:', err)
    alert('Erro ao salvar equipe. Por favor, tente novamente.')
  } finally {
    saving.value = false
  }
}

// Ver detalhes da equipe
const viewTeam = (id) => {
  router.push(`/equipes/${id}`)
}

// Carregar dados ao montar o componente
onMounted(() => {
  fetchTeams()
})
</script>
