<template>
  <header class="border-b bg-background">
    <div class="container flex h-16 items-center justify-between">
      <div class="flex items-center gap-6">
        <NuxtLink to="/" class="flex items-center space-x-2">
          <span class="text-xl font-bold">Planify</span>
        </NuxtLink>
        <nav class="hidden md:flex gap-6">
          <NuxtLink to="/projetos" class="text-sm font-medium transition-colors hover:text-primary">
            Projetos
          </NuxtLink>
          <NuxtLink to="/tarefas" class="text-sm font-medium transition-colors hover:text-primary">
            Tarefas
          </NuxtLink>
          <NuxtLink to="/equipes" class="text-sm font-medium transition-colors hover:text-primary">
            Equipes
          </NuxtLink>
          <NuxtLink to="/riscos" class="text-sm font-medium transition-colors hover:text-primary">
            Riscos
          </NuxtLink>
          <NuxtLink to="/custos" class="text-sm font-medium transition-colors hover:text-primary">
            Custos
          </NuxtLink>
          <NuxtLink to="/documentos" class="text-sm font-medium transition-colors hover:text-primary">
            Documentos
          </NuxtLink>
        </nav>
      </div>
      <div class="flex items-center gap-4">
        <button
          class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background border border-input hover:bg-accent hover:text-accent-foreground h-9 px-3 rounded-md"
          @click="toggleTheme"
        >
          <span v-if="isDarkMode">☀️</span>
          <span v-else>🌙</span>
        </button>
        <NuxtLink 
          v-if="!isAuthenticated" 
          to="/login"
          class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-3 rounded-md"
        >
          Login
        </NuxtLink>
        <button 
          v-else
          class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background bg-destructive text-destructive-foreground hover:bg-destructive/90 h-9 px-3 rounded-md"
          @click="logout"
        >
          Sair
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDarkMode = ref(false)
const isAuthenticated = ref(false)

onMounted(() => {
  // Verificar se o usuário está autenticado
  const token = localStorage.getItem('auth_token')
  isAuthenticated.value = !!token
  
  // Verificar o tema atual
  const theme = localStorage.getItem('theme')
  isDarkMode.value = theme === 'dark'
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  }
})

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

const logout = () => {
  localStorage.removeItem('auth_token')
  isAuthenticated.value = false
  navigateTo('/login')
}
</script>
