<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Componente de notificações -->
    <NotificationContainer />
    
    <!-- Mobile menu button -->
    <button 
      @click="isSidebarOpen = !isSidebarOpen" 
      class="fixed bottom-4 right-4 z-50 flex h-12 w-12 items-center justify-center rounded-full bg-blue-600 text-white shadow-lg md:hidden"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
    
    <!-- Modais -->
    <Modal
      v-model="isNewProjectModalOpen"
      title="Novo Projeto"
      size="lg"
    >
      <ProjectForm
        :loading="isProjectFormLoading"
        @submit="handleProjectSubmit"
        @cancel="isNewProjectModalOpen = false"
      />
    </Modal>
    
    <Modal
      v-model="isNewTaskModalOpen"
      title="Nova Tarefa"
      size="lg"
    >
      <TaskForm
        :loading="isTaskFormLoading"
        @submit="handleTaskSubmit"
        @cancel="isNewTaskModalOpen = false"
      />
    </Modal>
    
    <!-- Sidebar -->
    <aside 
      :class="[
        'fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-gray-200 bg-white transition-all duration-300 ease-in-out dark:border-gray-700 dark:bg-gray-800',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
        isSidebarCollapsed ? 'md:w-16' : 'md:w-64'
      ]"
    >
      <!-- Logo -->
      <div class="flex h-16 items-center justify-between border-b border-gray-200 px-4 dark:border-gray-700">
        <div class="flex items-center">
          <img src="/svg/logop.svg" alt="Planify Logo" class="h-8 w-8" />
          <span 
            :class="[
              'ml-2 text-xl font-semibold text-gray-800 dark:text-white',
              isSidebarCollapsed ? 'md:hidden' : ''
            ]"
          >
            Planify
          </span>
        </div>
        <button 
          @click="isSidebarOpen = false" 
          class="rounded p-1 text-gray-600 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300 md:hidden"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Menu de navegação -->
      <nav class="flex-1 overflow-y-auto p-4">
        <ul class="space-y-2">
          <li>
            <a 
              href="/dashboard" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path === '/dashboard' ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Dashboard</span>
            </a>
          </li>
          <li>
            <a 
              href="/projetos" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/projetos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Projetos</span>
            </a>
          </li>
          <li>
            <a 
              href="/tarefas" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/tarefas') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Tarefas</span>
            </a>
          </li>
          <li>
            <a 
              href="/equipes" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/equipes') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Equipes</span>
            </a>
          </li>
          <li>
            <a 
              href="/comunicacoes" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/comunicacoes') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Comunicações</span>
            </a>
          </li>
          <li>
            <a 
              href="/documentos" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/documentos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Documentos</span>
            </a>
          </li>
          <li>
            <a 
              href="/custos" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/custos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Custos</span>
            </a>
          </li>
          <li>
            <a 
              href="/riscos" 
              :class="[
                'flex items-center rounded-md px-4 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700',
                route.path.startsWith('/riscos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : ''
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span :class="['ml-3', isSidebarCollapsed ? 'md:hidden' : '']">Riscos</span>
            </a>
          </li>
        </ul>
      </nav>
    </aside>
    
    <!-- Conteúdo principal -->
    <div 
      :class="[
        'flex flex-col transition-all duration-300 ease-in-out',
        isSidebarCollapsed ? 'md:ml-16' : 'md:ml-64'
      ]"
    >
      <!-- Header -->
      <header class="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4 dark:border-gray-700 dark:bg-gray-800">
        <!-- Título da página -->
        <div class="flex items-center">
          <button 
            @click="toggleSidebar" 
            class="mr-4 hidden rounded p-1 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300 md:block"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
              <path v-if="isSidebarCollapsed" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
          <h1 class="text-xl font-semibold text-gray-800 dark:text-white">{{ pageTitle }}</h1>
        </div>
        
        <!-- Ações rápidas -->
        <div class="flex items-center space-x-2">
          <button 
            @click="openNewProjectModal" 
            class="flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-700 dark:hover:bg-blue-800"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="mr-1 h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span class="hidden sm:inline">Novo Projeto</span>
            <span class="inline sm:hidden">Projeto</span>
          </button>
          
          <button 
            @click="openNewTaskModal" 
            class="flex items-center rounded-md bg-green-600 px-3 py-2 text-sm font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:bg-green-700 dark:hover:bg-green-800"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="mr-1 h-4 w-4">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span class="hidden sm:inline">Nova Tarefa</span>
            <span class="inline sm:hidden">Tarefa</span>
          </button>
          
          <!-- Tema -->
          <button 
            @click="toggleTheme" 
            class="rounded-full p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300"
          >
            <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-5 w-5">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          
          <!-- Perfil do usuário -->
          <div class="relative" ref="dropdownRef">
            <button 
              @click="isDropdownOpen = !isDropdownOpen" 
              class="flex items-center rounded-full bg-gray-200 text-sm font-medium text-gray-700 focus:outline-none dark:bg-gray-700 dark:text-gray-300"
            >
              <span class="sr-only">Abrir menu do usuário</span>
              <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-white">
                {{ userInitials }}
              </div>
            </button>
            
            <!-- Menu do usuário -->
            <div 
              v-if="isDropdownOpen" 
              class="absolute right-0 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800 dark:ring-gray-700"
            >
              <div class="border-b border-gray-200 px-4 py-2 dark:border-gray-700">
                <p class="text-sm font-medium text-gray-900 dark:text-white">{{ userName }}</p>
                <p class="truncate text-xs text-gray-500 dark:text-gray-400">{{ userRole }}</p>
              </div>
              <a href="/perfil" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">Perfil</a>
              <a href="/configuracoes" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700">Configurações</a>
              <button @click="logout" class="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-gray-100 dark:text-red-400 dark:hover:bg-gray-700">Sair</button>
            </div>
          </div>
        </div>
      </header>
      
      <!-- Conteúdo da página -->
      <main class="flex-1 overflow-auto">
        <div class="container mx-auto p-4">
          <!-- Slot para o conteúdo da página -->
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeMount, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '~/composables/useAuth'
import { useNotification } from '~/composables/useNotification'
import { useProjectService } from '~/services/projectService'
import { useTaskService } from '~/services/taskService'
import Modal from '~/components/Modal.vue'
import ProjectForm from '~/components/ProjectForm.vue'
import TaskForm from '~/components/TaskForm.vue'
import NotificationContainer from '~/components/ui/NotificationContainer.vue'

// Router e rota atual
const router = useRouter()
const route = useRoute()

// Serviços
const projectService = useProjectService()
const taskService = useTaskService()
const notify = useNotification()

// Estado do sidebar
const isSidebarOpen = ref(false)
const isSidebarCollapsed = ref(false)
const isMobile = ref(false)

// Estado do dropdown do usuário
const isDropdownOpen = ref(false)
const dropdownRef = ref(null)

// Estado do tema
const isDarkMode = ref(false)

// Dados do usuário
const userName = ref('Usuário')
const userRole = ref('Membro')
const userInitials = computed(() => {
  if (!userName.value) return 'U'
  return userName.value
    .split(' ')
    .map(n => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
})

// Estado dos modais
const isNewProjectModalOpen = ref(false)
const isNewTaskModalOpen = ref(false)
const isProjectFormLoading = ref(false)
const isTaskFormLoading = ref(false)

// Título da página
const pageTitles = {
  '/dashboard': 'Dashboard',
  '/projetos': 'Projetos',
  '/tarefas': 'Tarefas',
  '/equipes': 'Equipes',
  '/comunicacoes': 'Comunicações',
  '/documentos': 'Documentos',
  '/custos': 'Custos',
  '/riscos': 'Riscos',
  '/perfil': 'Perfil',
  '/configuracoes': 'Configurações'
}

const pageTitle = computed(() => {
  // Verificar correspondências exatas primeiro
  if (pageTitles[route.path]) {
    return pageTitles[route.path]
  }
  
  // Verificar correspondências parciais
  for (const [path, title] of Object.entries(pageTitles)) {
    if (route.path.startsWith(path) && path !== '/dashboard') {
      // Se temos um ID na rota, adicionar "Detalhes" ao título
      if (route.params.id) {
        return `${title} - Detalhes`
      }
      return title
    }
  }
  
  // Fallback
  return 'Planify'
})

// Verificar se é dispositivo móvel
const checkIfMobile = () => {
  if (process.client) {
    isMobile.value = window.innerWidth < 768
    if (isMobile.value) {
      isSidebarOpen.value = false
    } else {
      isSidebarOpen.value = true
    }
  }
}

onBeforeMount(() => {
  if (process.client) {
    checkIfMobile()
    window.addEventListener('resize', checkIfMobile)
  }
})

onMounted(() => {
  // Carregar dados do usuário
  loadUserData()
  
  // Inicializar tema
  initializeTheme()
  
  // Inicializar dropdown
  initializeDropdown()
  
  // Verificar se é dispositivo móvel
  checkIfMobile()
  
  // Verificar preferência do sidebar
  const savedSidebarState = localStorage.getItem('sidebarCollapsed')
  if (savedSidebarState) {
    isSidebarCollapsed.value = savedSidebarState === 'true'
  }
})

// Carregar dados do usuário
const loadUserData = async () => {
  try {
    const { getCurrentUser } = useAuth()
    const user = await getCurrentUser()
    
    if (user) {
      userName.value = user.name || user.username || 'Usuário'
      userRole.value = user.is_staff ? 'Administrador' : 'Membro'
    }
  } catch (error) {
    console.error('Erro ao carregar dados do usuário:', error)
  }
}

// Inicializar tema
const initializeTheme = () => {
  if (process.client) {
    // Verificar preferência salva
    const savedTheme = localStorage.getItem('theme')
    
    // Verificar preferência do sistema
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    
    // Definir tema inicial
    isDarkMode.value = savedTheme === 'dark' || (!savedTheme && prefersDark)
    
    // Aplicar tema
    applyTheme()
  }
}

// Aplicar tema
const applyTheme = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

// Alternar tema
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  applyTheme()
}

// Inicializar dropdown
const initializeDropdown = () => {
  if (process.client) {
    const handleClickOutside = (event) => {
      if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        isDropdownOpen.value = false
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside)
    
    // Limpar listener ao desmontar
    onBeforeUnmount(() => {
      document.removeEventListener('mousedown', handleClickOutside)
    })
  }
}

// Logout
const logout = () => {
  const { logout: authLogout } = useAuth()
  authLogout()
}

// Toggle sidebar
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
  localStorage.setItem('sidebarCollapsed', isSidebarCollapsed.value.toString())
}

// Funções para abrir modais
const openNewProjectModal = () => {
  isNewProjectModalOpen.value = true
}

const openNewTaskModal = () => {
  isNewTaskModalOpen.value = true
}

// Funções para manipular submissões de formulários
const handleProjectSubmit = async (projectData) => {
  isProjectFormLoading.value = true
  
  try {
    await notify.withLoading(
      projectService.create(projectData),
      {
        loadingMessage: 'Criando projeto...',
        successMessage: 'Projeto criado com sucesso!',
        errorMessage: 'Erro ao criar projeto'
      }
    )
    
    isNewProjectModalOpen.value = false
    
    // Redirecionar para a página de projetos se não estiver nela
    if (!route.path.startsWith('/projetos')) {
      router.push('/projetos')
    } else {
      // Recarregar a página para mostrar o novo projeto
      router.go()
    }
  } catch (error) {
    console.error('Erro ao criar projeto:', error)
  } finally {
    isProjectFormLoading.value = false
  }
}

const handleTaskSubmit = async (taskData) => {
  isTaskFormLoading.value = true
  
  try {
    await notify.withLoading(
      taskService.create(taskData),
      {
        loadingMessage: 'Criando tarefa...',
        successMessage: 'Tarefa criada com sucesso!',
        errorMessage: 'Erro ao criar tarefa'
      }
    )
    
    isNewTaskModalOpen.value = false
    
    // Redirecionar para a página de tarefas se não estiver nela
    if (!route.path.startsWith('/tarefas')) {
      router.push('/tarefas')
    } else {
      // Recarregar a página para mostrar a nova tarefa
      router.go()
    }
  } catch (error) {
    console.error('Erro ao criar tarefa:', error)
  } finally {
    isTaskFormLoading.value = false
  }
}
</script>

<style scoped>
.dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  right: 0;
  top: 100%;
  z-index: 50;
  min-width: 12rem;
}
</style>
