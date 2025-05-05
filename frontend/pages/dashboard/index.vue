<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <p class="text-gray-500 dark:text-gray-400">Bem-vindo ao seu painel de controle, {{ userName }}</p>
    </div>

    <!-- Resumo -->
    <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div class="flex items-center">
          <div class="mr-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
              <path d="M3 3v18h18"></path>
              <path d="M7 12v5"></path>
              <path d="m14 7 3-3 3 3"></path>
              <path d="M7 19h5"></path>
              <path d="M19 15v4"></path>
              <path d="M11 12v5"></path>
              <path d="M14 12v5"></path>
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Projetos</p>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ projetosCount }}</h3>
          </div>
        </div>
        <div class="mt-4">
          <NuxtLink to="/projetos" class="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">Ver todos →</NuxtLink>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div class="flex items-center">
          <div class="mr-4 flex h-12 w-12 items-center justify-center rounded-lg bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
              <rect width="8" height="8" x="3" y="3" rx="2"></rect>
              <rect width="8" height="8" x="13" y="3" rx="2"></rect>
              <rect width="8" height="8" x="3" y="13" rx="2"></rect>
              <rect width="8" height="8" x="13" y="13" rx="2"></rect>
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Tarefas</p>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ tarefasCount }}</h3>
          </div>
        </div>
        <div class="mt-4">
          <NuxtLink to="/tarefas" class="text-sm font-medium text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300">Ver todas →</NuxtLink>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div class="flex items-center">
          <div class="mr-4 flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Equipes</p>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ equipesCount }}</h3>
          </div>
        </div>
        <div class="mt-4">
          <NuxtLink to="/equipes" class="text-sm font-medium text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300">Ver todas →</NuxtLink>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div class="flex items-center">
          <div class="mr-4 flex h-12 w-12 items-center justify-center rounded-lg bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-300">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
              <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" x2="12" y1="9" y2="13"></line>
              <line x1="12" x2="12.01" y1="17" y2="17"></line>
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Riscos</p>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">{{ riscosCount }}</h3>
          </div>
        </div>
        <div class="mt-4">
          <NuxtLink to="/riscos" class="text-sm font-medium text-yellow-600 hover:text-yellow-700 dark:text-yellow-400 dark:hover:text-yellow-300">Ver todos →</NuxtLink>
        </div>
      </div>
    </div>

    <!-- Projetos Recentes e Tarefas Pendentes -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      <!-- Projetos Recentes -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div class="border-b border-gray-200 px-6 py-4 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Projetos Recentes</h3>
        </div>
        <div v-if="projetos.length > 0" class="divide-y divide-gray-200 dark:divide-gray-700">
          <div v-for="(projeto, index) in projetos.slice(0, 5)" :key="index" class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ projeto.nome }}</h4>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ projeto.status }}</p>
              </div>
              <NuxtLink :to="`/projetos/${projeto.id}`" class="rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
                Detalhes
              </NuxtLink>
            </div>
          </div>
        </div>
        <div v-else class="p-6">
          <EmptyState>
            <template #icon>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-10 w-10 text-gray-400 dark:text-gray-500">
                <path d="M3 3v18h18"></path>
                <path d="M7 12v5"></path>
                <path d="m14 7 3-3 3 3"></path>
                <path d="M7 19h5"></path>
                <path d="M19 15v4"></path>
                <path d="M11 12v5"></path>
                <path d="M14 12v5"></path>
              </svg>
            </template>
            <template #title>Nenhum projeto encontrado</template>
            <template #description>Você ainda não tem projetos. Crie seu primeiro projeto para começar.</template>
            <template #action>
              <button @click="openNewProjectModal" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
                Criar projeto
              </button>
            </template>
          </EmptyState>
        </div>
        <div class="border-t border-gray-200 px-6 py-4 dark:border-gray-700">
          <NuxtLink to="/projetos" class="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">Ver todos os projetos →</NuxtLink>
        </div>
      </div>

      <!-- Tarefas Pendentes -->
      <div class="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-800">
        <div class="border-b border-gray-200 px-6 py-4 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Tarefas Pendentes</h3>
        </div>
        <div v-if="tarefas.length > 0" class="divide-y divide-gray-200 dark:divide-gray-700">
          <div v-for="(tarefa, index) in tarefas.slice(0, 5)" :key="index" class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ tarefa.titulo }}</h4>
                <p class="text-xs text-gray-500 dark:text-gray-400">Prazo: {{ formatDate(tarefa.prazo) }}</p>
              </div>
              <span :class="`rounded-md px-2.5 py-1 text-xs font-medium ${getPrioridadeClass(tarefa.prioridade)}`">
                {{ tarefa.prioridade }}
              </span>
            </div>
          </div>
        </div>
        <div v-else class="p-6">
          <EmptyState>
            <template #icon>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-10 w-10 text-gray-400 dark:text-gray-500">
                <rect width="8" height="8" x="3" y="3" rx="2"></rect>
                <rect width="8" height="8" x="13" y="3" rx="2"></rect>
                <rect width="8" height="8" x="3" y="13" rx="2"></rect>
                <rect width="8" height="8" x="13" y="13" rx="2"></rect>
              </svg>
            </template>
            <template #title>Nenhuma tarefa pendente</template>
            <template #description>Você não tem tarefas pendentes no momento.</template>
            <template #action>
              <button @click="openNewTaskModal" class="inline-flex items-center justify-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-green-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-green-700 dark:bg-green-700 dark:hover:bg-green-600">
                Criar tarefa
              </button>
            </template>
          </EmptyState>
        </div>
        <div class="border-t border-gray-200 px-6 py-4 dark:border-gray-700">
          <NuxtLink to="/tarefas" class="text-sm font-medium text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300">Ver todas as tarefas →</NuxtLink>
        </div>
      </div>
    </div>

    <!-- Notificações Recentes -->
    <div class="mt-8 rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-800">
      <div class="border-b border-gray-200 px-6 py-4 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Notificações Recentes</h3>
      </div>
      <div v-if="notificacoes.length > 0" class="divide-y divide-gray-200 dark:divide-gray-700">
        <div v-for="(notificacao, index) in notificacoes.slice(0, 5)" :key="index" class="px-6 py-4">
          <div class="flex items-start gap-4">
            <div :class="`flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full ${getNotificacaoIconClass(notificacao.tipo)}`">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
                <path v-if="notificacao.tipo === 'MENSAGEM'" d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                <path v-else-if="notificacao.tipo === 'ALERTA'" d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line v-else-if="notificacao.tipo === 'ALERTA'" x1="12" x2="12" y1="9" y2="13"></line>
                <line v-else-if="notificacao.tipo === 'ALERTA'" x1="12" x2="12.01" y1="17" y2="17"></line>
                <path v-else d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ notificacao.titulo }}</h4>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ notificacao.mensagem }}</p>
              <p class="mt-1 text-xs text-gray-400 dark:text-gray-500">{{ formatDate(notificacao.data) }}</p>
            </div>
            <button v-if="!notificacao.lida" @click="marcarComoLida(notificacao.id)" class="rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
              Marcar como lida
            </button>
          </div>
        </div>
      </div>
      <div v-else class="p-6">
        <EmptyState>
          <template #icon>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-10 w-10 text-gray-400 dark:text-gray-500">
              <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"></path>
              <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"></path>
            </svg>
          </template>
          <template #title>Nenhuma notificação</template>
          <template #description>Você não tem notificações no momento.</template>
        </EmptyState>
      </div>
      <div class="border-t border-gray-200 px-6 py-4 dark:border-gray-700">
        <NuxtLink to="/comunicacoes" class="text-sm font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">Ver todas as notificações →</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNuxtApp } from '#app'

const router = useRouter()
const userName = ref('Usuário')
const projetosCount = ref(0)
const tarefasCount = ref(0)
const equipesCount = ref(0)
const riscosCount = ref(0)
const projetos = ref([])
const tarefas = ref([])
const notificacoes = ref([])

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return 'Sem data'
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  }).format(date)
}

// Obter classe CSS para prioridade
const getPrioridadeClass = (prioridade) => {
  switch (prioridade?.toUpperCase()) {
    case 'ALTA':
      return 'bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-400'
    case 'MÉDIA':
      return 'bg-yellow-50 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'BAIXA':
      return 'bg-green-50 text-green-600 dark:bg-green-900/30 dark:text-green-400'
    default:
      return 'bg-gray-50 text-gray-600 dark:bg-gray-900/30 dark:text-gray-400'
  }
}

// Obter classe CSS para ícone de notificação
const getNotificacaoIconClass = (tipo) => {
  switch (tipo?.toUpperCase()) {
    case 'MENSAGEM':
      return 'bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300'
    case 'ALERTA':
      return 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-300'
    case 'SISTEMA':
      return 'bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-300'
    default:
      return 'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300'
  }
}

// Marcar notificação como lida
const marcarComoLida = async (id) => {
  try {
    const { $api } = useNuxtApp()
    await $api.patch(`/api/communications/${id}/`, {
      status: 'LIDA'
    })
    
    // Atualizar a lista de notificações
    notificacoes.value = notificacoes.value.map(n => {
      if (n.id === id) {
        return { ...n, lida: true }
      }
      return n
    })
  } catch (error) {
    console.error('Erro ao marcar notificação como lida:', error)
  }
}

// Abrir modal de novo projeto
const openNewProjectModal = () => {
  router.push('/projetos?new=true')
}

// Abrir modal de nova tarefa
const openNewTaskModal = () => {
  router.push('/tarefas?new=true')
}

onMounted(async () => {
  try {
    const { $api } = useNuxtApp()
    
    // Buscar informações do usuário
    const userResponse = await $api.get('/api/auth/users/me/')
    userName.value = userResponse.data.full_name || userResponse.data.username
    
    // Buscar contagens
    try {
      const projetosResponse = await $api.get('/api/projects/')
      if (projetosResponse.data.count !== undefined) {
        projetosCount.value = projetosResponse.data.count
        projetos.value = projetosResponse.data.results || []
      } else if (Array.isArray(projetosResponse.data)) {
        projetosCount.value = projetosResponse.data.length
        projetos.value = projetosResponse.data
      }
    } catch (err) {
      console.error('Erro ao buscar projetos:', err)
      // Dados de exemplo para demonstração
      projetosCount.value = 5
      projetos.value = [
        { id: 1, nome: 'Sistema de Gestão Integrada', status: 'Em andamento' },
        { id: 2, nome: 'Aplicativo Mobile', status: 'Planejamento' },
        { id: 3, nome: 'Plataforma de E-commerce', status: 'Em andamento' },
        { id: 4, nome: 'Inteligência Artificial para Previsão', status: 'Concluído' },
        { id: 5, nome: 'Blockchain para Rastreabilidade', status: 'Em andamento' }
      ]
    }
    
    try {
      const tarefasResponse = await $api.get('/api/tasks/')
      if (tarefasResponse.data.count !== undefined) {
        tarefasCount.value = tarefasResponse.data.count
        tarefas.value = tarefasResponse.data.results || []
      } else if (Array.isArray(tarefasResponse.data)) {
        tarefasCount.value = tarefasResponse.data.length
        tarefas.value = tarefasResponse.data
      }
    } catch (err) {
      console.error('Erro ao buscar tarefas:', err)
      // Dados de exemplo para demonstração
      tarefasCount.value = 8
      tarefas.value = [
        { id: 1, titulo: 'Desenvolver API REST', prazo: '2025-05-15', prioridade: 'ALTA' },
        { id: 2, titulo: 'Criar interface de usuário', prazo: '2025-05-20', prioridade: 'MÉDIA' },
        { id: 3, titulo: 'Implementar autenticação', prazo: '2025-05-10', prioridade: 'ALTA' },
        { id: 4, titulo: 'Realizar testes de integração', prazo: '2025-05-25', prioridade: 'MÉDIA' },
        { id: 5, titulo: 'Documentar API', prazo: '2025-05-30', prioridade: 'BAIXA' }
      ]
    }
    
    try {
      const equipesResponse = await $api.get('/api/teams/')
      if (equipesResponse.data.count !== undefined) {
        equipesCount.value = equipesResponse.data.count
      } else if (Array.isArray(equipesResponse.data)) {
        equipesCount.value = equipesResponse.data.length
      }
    } catch (err) {
      console.error('Erro ao buscar equipes:', err)
      equipesCount.value = 3
    }
    
    try {
      const riscosResponse = await $api.get('/api/risks/')
      if (riscosResponse.data.count !== undefined) {
        riscosCount.value = riscosResponse.data.count
      } else if (Array.isArray(riscosResponse.data)) {
        riscosCount.value = riscosResponse.data.length
      }
    } catch (err) {
      console.error('Erro ao buscar riscos:', err)
      riscosCount.value = 2
    }
    
    try {
      const notificacoesResponse = await $api.get('/api/communications/')
      if (notificacoesResponse.data.count !== undefined) {
        notificacoes.value = notificacoesResponse.data.results || []
      } else if (Array.isArray(notificacoesResponse.data)) {
        notificacoes.value = notificacoesResponse.data.map(n => ({
          ...n,
          lida: n.status === 'LIDA'
        }))
      }
    } catch (err) {
      console.error('Erro ao buscar notificações:', err)
      // Dados de exemplo para demonstração
      notificacoes.value = [
        { id: 1, tipo: 'MENSAGEM', titulo: 'Nova mensagem', mensagem: 'Você recebeu uma nova mensagem de João Silva', data: '2025-05-04', lida: false },
        { id: 2, tipo: 'ALERTA', titulo: 'Prazo próximo', mensagem: 'A tarefa "Desenvolver API REST" está com o prazo se aproximando', data: '2025-05-03', lida: true },
        { id: 3, tipo: 'SISTEMA', titulo: 'Atualização do sistema', mensagem: 'O sistema foi atualizado para a versão 2.0', data: '2025-05-02', lida: false }
      ]
    }
  } catch (error) {
    console.error('Erro ao carregar dados do dashboard:', error)
  }
})
</script>
