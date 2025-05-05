<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Mobile menu button -->
    <button 
      @click="isSidebarOpen = !isSidebarOpen" 
      class="fixed bottom-4 right-4 z-50 flex h-12 w-12 items-center justify-center rounded-full bg-blue-600 text-white shadow-lg md:hidden"
    >
      <svg v-if="isSidebarOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
        <path d="M18 6 6 18"></path>
        <path d="m6 6 12 12"></path>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
        <line x1="3" x2="21" y1="6" y2="6"></line>
        <line x1="3" x2="21" y1="12" y2="12"></line>
        <line x1="3" x2="21" y1="18" y2="18"></line>
      </svg>
    </button>

    <!-- Theme toggle button (mobile) -->
    <button 
      @click="toggleTheme" 
      class="fixed bottom-4 left-4 z-50 flex h-12 w-12 items-center justify-center rounded-full bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-yellow-400 shadow-lg md:hidden"
    >
      <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" x2="12" y1="1" y2="3"></line>
        <line x1="12" x2="12" y1="21" y2="23"></line>
        <line x1="4.22" x2="5.64" y1="4.22" y2="5.64"></line>
        <line x1="18.36" x2="19.78" y1="18.36" y2="19.78"></line>
        <line x1="1" x2="3" y1="12" y2="12"></line>
        <line x1="21" x2="23" y1="12" y2="12"></line>
        <line x1="4.22" x2="5.64" y1="19.78" y2="18.36"></line>
        <line x1="18.36" x2="19.78" y1="5.64" y2="4.22"></line>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </button>

    <!-- Sidebar backdrop for mobile -->
    <div 
      v-if="isSidebarOpen" 
      @click="isSidebarOpen = false"
      class="fixed inset-0 z-40 bg-black bg-opacity-50 md:hidden"
    ></div>

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-50 flex h-full w-72 flex-col border-r border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-950 transition-transform duration-300 ease-in-out"
      :class="{ '-translate-x-full': !isSidebarOpen && isMobile, 'translate-x-0': isSidebarOpen || !isMobile }"
    >
      <!-- Logo -->
      <div class="flex h-16 items-center justify-between border-b px-6">
        <NuxtLink to="/projetos" class="flex items-center gap-3 font-semibold">
          <div class="flex h-10 w-10 items-center justify-center rounded-md bg-blue-600 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
              <path d="M2 17a5 5 0 0 0 10 0c0-2.76-2.5-5-5-3-2.5-2-5 .24-5 3Z"></path>
              <path d="M12 17a5 5 0 0 0 10 0c0-2.76-2.5-5-5-3-2.5-2-5 .24-5 3Z"></path>
              <path d="M7 14c3.22-2.91 4.29-8.75 5-12 1.66 2.38 4.94 9 5 12"></path>
              <path d="M22 9c-4.29 0-7.14-2.33-10-7 5.71 0 10 4.67 10 7Z"></path>
            </svg>
          </div>
          <span class="text-xl font-bold text-blue-600 dark:text-blue-400">Planify</span>
        </NuxtLink>
        
        <!-- Theme toggle button (desktop) -->
        <button 
          @click="toggleTheme" 
          class="hidden md:flex p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-yellow-400"
        >
          <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" x2="12" y1="1" y2="3"></line>
            <line x1="12" x2="12" y1="21" y2="23"></line>
            <line x1="4.22" x2="5.64" y1="4.22" y2="5.64"></line>
            <line x1="18.36" x2="19.78" y1="18.36" y2="19.78"></line>
            <line x1="1" x2="3" y1="12" y2="12"></line>
            <line x1="21" x2="23" y1="12" y2="12"></line>
            <line x1="4.22" x2="5.64" y1="19.78" y2="18.36"></line>
            <line x1="18.36" x2="19.78" y1="5.64" y2="4.22"></line>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
      </div>

      <!-- User Profile -->
      <div class="border-b border-gray-200 dark:border-gray-800 px-6 py-4">
        <div class="flex items-center gap-4">
          <div class="relative">
            <div class="flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300">
              <span class="text-sm font-medium">{{ userInitials }}</span>
            </div>
            <div v-if="unreadNotifications > 0" class="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs font-medium text-white">
              {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-gray-900 dark:text-white">{{ userName }}</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ userRole }}</p>
          </div>
          <div class="dropdown" ref="dropdownRef">
            <button 
              @click="isDropdownOpen = !isDropdownOpen" 
              class="flex h-8 w-8 items-center justify-center rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-gray-500 dark:text-gray-400">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="12" cy="5" r="1"></circle>
                <circle cx="12" cy="19" r="1"></circle>
              </svg>
            </button>
            <div 
              v-if="isDropdownOpen" 
              class="dropdown-menu mt-2 rounded-md border border-gray-200 bg-white p-1 shadow-lg dark:border-gray-700 dark:bg-gray-800"
            >
              <NuxtLink 
                to="/comunicacoes" 
                class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                Notificações
                <span v-if="unreadNotifications > 0" class="ml-auto flex h-5 min-w-5 items-center justify-center rounded-full bg-red-500 px-1 text-xs font-medium text-white">
                  {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
                </span>
              </NuxtLink>
              <button 
                class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Perfil
              </button>
              <button 
                class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                Configurações
              </button>
              <button 
                @click="logout" 
                class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                Sair
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-auto py-6 px-3">
        <div class="space-y-1">
          <NuxtLink
            to="/dashboard"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <rect width="7" height="9" x="3" y="3" rx="1"></rect>
              <rect width="7" height="5" x="14" y="3" rx="1"></rect>
              <rect width="7" height="9" x="14" y="12" rx="1"></rect>
              <rect width="7" height="5" x="3" y="16" rx="1"></rect>
            </svg>
            Dashboard
          </NuxtLink>
          <NuxtLink
            to="/projetos"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M3 3v18h18"></path>
              <path d="M7 12v5"></path>
              <path d="m14 7 3-3 3 3"></path>
              <path d="M7 19h5"></path>
              <path d="M19 15v4"></path>
              <path d="M11 12v5"></path>
              <path d="M14 12v5"></path>
            </svg>
            Projetos
          </NuxtLink>
          <NuxtLink
            to="/tarefas"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <rect width="8" height="8" x="3" y="3" rx="2"></rect>
              <rect width="8" height="8" x="13" y="3" rx="2"></rect>
              <rect width="8" height="8" x="3" y="13" rx="2"></rect>
              <rect width="8" height="8" x="13" y="13" rx="2"></rect>
            </svg>
            Tarefas
          </NuxtLink>
          <NuxtLink
            to="/equipes"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M22 9c-4.29 0-7.14-2.33-10-7 5.71 0 10 4.67 10 7Z"></path>
            </svg>
            Equipes
          </NuxtLink>
          <NuxtLink
            to="/documentos"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            Documentos
          </NuxtLink>
          <NuxtLink
            to="/riscos"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" x2="12" y1="9" y2="13"></line>
              <line x1="12" x2="12.01" y1="17" y2="17"></line>
            </svg>
            Riscos
          </NuxtLink>
          <NuxtLink
            to="/custos"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path>
              <path d="M12 18V6"></path>
            </svg>
            Custos
          </NuxtLink>
          <NuxtLink
            to="/comunicacoes"
            class="flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
            active-class="bg-blue-50 text-blue-600 dark:bg-blue-950 dark:text-blue-400"
            @click="isMobile && (isSidebarOpen = false)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            Comunicações
          </NuxtLink>
          
          <div class="py-2 my-2 border-t border-gray-200 dark:border-gray-700"></div>
          
          <div class="px-4 py-2">
            <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              Atalhos
            </h2>
          </div>
          
          <button 
            @click="openNewProjectModal" 
            class="flex w-full items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-green-600">
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Novo Projeto
          </button>
          
          <button 
            @click="openNewTaskModal" 
            class="flex w-full items-center gap-3 rounded-md px-4 py-3 text-sm font-medium text-gray-900 hover:bg-gray-100 dark:text-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-blue-600">
              <path d="M11 12H3"></path>
              <path d="M16 6H3"></path>
              <path d="M16 18H3"></path>
              <path d="M18 9v6"></path>
              <path d="M21 12h-6"></path>
            </svg>
            Nova Tarefa
          </button>
        </div>
      </nav>

      <!-- Footer -->
      <div class="mt-auto border-t p-4 text-center text-xs text-gray-500 dark:text-gray-400">
        <p>Planify &copy; {{ new Date().getFullYear() }}</p>
        <button @click="logout" class="mt-2 text-xs text-red-600 hover:underline">Sair da conta</button>
      </div>
    </aside>

    <!-- Main Content -->
    <main 
      class="transition-all duration-300 ease-in-out min-h-screen p-4 sm:p-6 md:p-8"
      :class="{ 'ml-0': !isSidebarOpen && isMobile, 'ml-72': isSidebarOpen || !isMobile }"
    >
      <slot />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useNuxtApp } from '#app'

const router = useRouter()
const userName = ref('Usuário')
const userRole = ref('Usuário')
const unreadNotifications = ref(0)
const isSidebarOpen = ref(true)
const isMobile = ref(false)
const isDropdownOpen = ref(false)
const dropdownRef = ref(null)
const isDarkMode = ref(false)

// Verificar se o usuário está autenticado
const isLoggedIn = computed(() => {
  if (process.client) {
    return !!localStorage.getItem('auth_token')
  }
  return false
})

// Calcular iniciais do usuário
const userInitials = computed(() => {
  if (!userName.value) return 'U'
  return userName.value
    .split(' ')
    .map(name => name[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
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
    
    // Verificar preferência de tema
    const savedTheme = localStorage.getItem('theme')
    
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      isDarkMode.value = true
      document.documentElement.classList.add('dark')
    } else {
      isDarkMode.value = false
      document.documentElement.classList.remove('dark')
    }
  }
})

onMounted(async () => {
  // Verificar se o usuário está autenticado
  if (!isLoggedIn.value) {
    router.push('/login')
    return
  }

  // Inicializar dropdown
  initializeDropdown()
  
  try {
    // Buscar informações do usuário
    const { $api } = useNuxtApp()
    const response = await $api.get('/api/auth/users/me/')
    userName.value = response.data.full_name || response.data.username
    
    // Definir função do usuário com base em permissões
    if (response.data.is_staff) {
      userRole.value = 'Administrador'
    } else {
      userRole.value = 'Gerente de Projetos'
    }
    
    // Buscar notificações não lidas
    try {
      const notificationsResponse = await $api.get('/api/communications/', {
        params: {
          status: 'NAO_LIDA'
        }
      })
      
      if (notificationsResponse.data.count) {
        unreadNotifications.value = notificationsResponse.data.count
      } else if (Array.isArray(notificationsResponse.data)) {
        unreadNotifications.value = notificationsResponse.data.filter(msg => msg.status === 'NAO_LIDA').length
      }
    } catch (err) {
      console.error('Erro ao buscar notificações:', err)
    }
  } catch (error) {
    console.error('Erro ao carregar informações do usuário:', error)
  }
  
  return () => {
    if (process.client) {
      window.removeEventListener('resize', checkIfMobile)
    }
  }
})

// Alternar tema
const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
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

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }
}

// Logout
const logout = () => {
  localStorage.removeItem('auth_token')
  router.push('/login')
}

// Funções para abrir modais
const openNewProjectModal = () => {
  // Fechar o sidebar em dispositivos móveis
  if (isMobile.value) {
    isSidebarOpen.value = false
  }
  
  // Navegar para a página de projetos com parâmetro para abrir o modal
  router.push('/projetos?new=true')
}

const openNewTaskModal = () => {
  // Fechar o sidebar em dispositivos móveis
  if (isMobile.value) {
    isSidebarOpen.value = false
  }
  
  // Navegar para a página de tarefas com parâmetro para abrir o modal
  router.push('/tarefas?new=true')
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
