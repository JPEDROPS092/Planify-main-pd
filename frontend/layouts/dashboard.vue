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
      class="fixed inset-y-0 left-0 z-50 flex h-full flex-col border-r border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-950 transition-transform duration-300 ease-in-out"
      :class="{ 
        '-translate-x-full': !isSidebarOpen && isMobile, 
        'translate-x-0': isSidebarOpen || !isMobile,
        'w-72': !isSidebarCollapsed,
        'w-20': isSidebarCollapsed && !isMobile
      }"
    >
      <!-- Logo -->
      <div class="flex h-16 items-center justify-between border-b px-6">
        <NuxtLink to="/projetos" class="flex items-center gap-3 font-semibold">
          <div class="flex h-10 w-10 items-center justify-center rounded-md bg-blue-600 text-white">
            <NuxtImg src="public/svg/logop.svg" alt="Logo" class="h-6 w-6" />
          </div>
          <span v-if="!isSidebarCollapsed || isMobile" class="text-xl font-bold text-blue-600 dark:text-blue-400">Planify</span>
        </NuxtLink>
        
        <!-- Theme toggle button (desktop) -->
        <div class="flex items-center">
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
      </div>

      <!-- Toggle sidebar button -->
      <button 
        @click="toggleSidebar" 
        class="absolute -right-3 top-20 hidden h-6 w-6 items-center justify-center rounded-full bg-white border border-gray-200 text-gray-600 shadow-sm hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 md:flex"
      >
        <svg v-if="isSidebarCollapsed" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3 w-3">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-3 w-3">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>

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
          <div v-if="!isSidebarCollapsed || isMobile" class="flex-1">
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
                <span v-if="!isSidebarCollapsed || isMobile">Notificações</span>
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
                <span v-if="!isSidebarCollapsed || isMobile">Perfil</span>
              </button>
              <button 
                class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <span v-if="!isSidebarCollapsed || isMobile">Configurações</span>
              </button>
              <button 
                @click="logout" 
                class="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16 17 21 12 16 7"></polyline>
                  <line x1="21" x2="9" y1="12" y2="12"></line>
                </svg>
                <span v-if="!isSidebarCollapsed || isMobile">Sair</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto p-4">
        <div class="space-y-1">
          <!-- Dashboard -->
          <NuxtLink 
            to="/dashboard" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/dashboard') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <rect width="7" height="9" x="3" y="3" rx="1"></rect>
              <rect width="7" height="5" x="14" y="3" rx="1"></rect>
              <rect width="7" height="9" x="14" y="12" rx="1"></rect>
              <rect width="7" height="5" x="3" y="16" rx="1"></rect>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Dashboard</span>
          </NuxtLink>

          <!-- Projetos -->
          <NuxtLink 
            to="/projetos" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/projetos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"></path>
              <path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"></path>
              <path d="M15 2v5h5"></path>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Projetos</span>
          </NuxtLink>

          <!-- Tarefas -->
          <NuxtLink 
            to="/tarefas" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/tarefas') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <rect width="18" height="18" x="3" y="3" rx="2"></rect>
              <path d="m9 12 2 2 4-4"></path>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Tarefas</span>
          </NuxtLink>

          <!-- Equipes -->
          <NuxtLink 
            to="/equipes" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/equipes') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Equipes</span>
          </NuxtLink>

          <!-- Riscos -->
          <NuxtLink 
            to="/riscos" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/riscos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" x2="12" y1="9" y2="13"></line>
              <line x1="12" x2="12.01" y1="17" y2="17"></line>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Riscos</span>
          </NuxtLink>

          <!-- Custos -->
          <NuxtLink 
            to="/custos" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/custos') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path>
              <path d="M12 18V6"></path>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Custos</span>
          </NuxtLink>

          <!-- Comunicações -->
          <NuxtLink 
            to="/comunicacoes" 
            class="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors"
            :class="$route.path.startsWith('/comunicacoes') ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400' : 'text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Comunicações</span>
          </NuxtLink>
        </div>

        <!-- Quick Actions -->
        <div class="mt-6 space-y-1">
          <h3 class="px-3 text-xs font-medium uppercase text-gray-500 dark:text-gray-400" v-if="!isSidebarCollapsed || isMobile">Ações Rápidas</h3>
          
          <!-- Novo Projeto -->
          <button 
            @click="openNewProjectModal" 
            class="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="12" x2="12" y1="18" y2="12"></line>
              <line x1="9" x2="15" y1="15" y2="15"></line>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Novo Projeto</span>
          </button>
          
          <!-- Nova Tarefa -->
          <button 
            @click="openNewTaskModal" 
            class="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-800"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5">
              <rect width="18" height="18" x="3" y="3" rx="2"></rect>
              <path d="M12 8v8"></path>
              <path d="M8 12h8"></path>
            </svg>
            <span v-if="!isSidebarCollapsed || isMobile">Nova Tarefa</span>
          </button>
        </div>
      </nav>

      <!-- Footer -->
      <div class="mt-auto border-t p-4 text-center text-xs text-gray-500 dark:text-gray-400">
        <p v-if="!isSidebarCollapsed || isMobile">Planify &copy; {{ new Date().getFullYear() }}</p>
        <p v-else class="text-center">&copy;</p>
      </div>
    </aside>

    <!-- Main Content -->
    <main 
      class="transition-all duration-300 ease-in-out min-h-screen p-4 sm:p-6 md:p-8"
      :class="{ 'ml-0': !isSidebarOpen && isMobile, 'ml-72': isSidebarOpen || !isMobile, 'ml-20': isSidebarCollapsed && !isMobile }"
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
const isSidebarCollapsed = ref(false)

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

// Toggle sidebar
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
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
