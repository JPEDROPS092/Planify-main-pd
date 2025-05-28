<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-blue-50 dark:from-gray-900 dark:to-gray-800">
    <!-- Header -->
    <header class="container mx-auto px-4 py-6 flex items-center justify-between">
      <div class="flex items-center gap-2">
          <img src="/img/logop.png" alt="Logo" class="h-32 w-22">
      </div>
      <div class="flex items-center gap-4">
        <button @click="toggleTheme" class="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800">
          <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-yellow-400">
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
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-700">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>
        <NuxtLink to="/login" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
          Entrar
        </NuxtLink>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="py-16 md:py-24 lg:py-32">
      <div class="container mx-auto px-4 md:px-6">
        <div class="grid grid-cols-1 gap-8 md:grid-cols-2 items-center">
          <div class="space-y-6">
            <h1 class="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl/none text-gray-900 dark:text-white">
              Gerencie seus projetos de P&D com eficiência
            </h1>
            <p class="text-lg text-gray-600 dark:text-gray-300 md:text-xl max-w-[600px]">
              Simplifique o gerenciamento de seus projetos de Pesquisa e Desenvolvimento com nossa plataforma completa e integrada.
            </p>
            <div class="flex flex-wrap items-center gap-4">
              <NuxtLink to="/login" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-6 py-3 text-base font-medium text-white shadow-lg transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 dark:bg-blue-700 dark:hover:bg-blue-600">
                Começar agora
              </NuxtLink>
              <a href="#recursos" class="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 shadow-sm transition-colors hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-400 focus-visible:ring-offset-2 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700">
                Saiba mais
              </a>
            </div>
          </div>
          <div class="relative hidden md:block">
            <div class="absolute -inset-1 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 opacity-30 blur-xl"></div>
            <div class="relative overflow-hidden rounded-xl border border-gray-200 bg-white p-6 shadow-lg dark:border-gray-800 dark:bg-gray-900">
              <div class="space-y-4">
                <div class="h-2 w-20 rounded bg-blue-600"></div>
                <div class="grid grid-cols-3 gap-2">
                  <div class="h-24 rounded bg-gray-100 dark:bg-gray-800"></div>
                  <div class="h-24 rounded bg-gray-100 dark:bg-gray-800"></div>
                  <div class="h-24 rounded bg-gray-100 dark:bg-gray-800"></div>
                </div>
                <div class="h-2 w-16 rounded bg-gray-200 dark:bg-gray-700"></div>
                <div class="grid grid-cols-2 gap-2">
                  <div class="h-32 rounded bg-gray-100 dark:bg-gray-800"></div>
                  <div class="h-32 rounded bg-gray-100 dark:bg-gray-800"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="recursos" class="py-16 md:py-24 bg-gray-50 dark:bg-gray-900">
      <div class="container mx-auto px-4 md:px-6">
        <div class="flex flex-col items-center justify-center space-y-4 text-center mb-12">
          <div class="space-y-2">
            <h2 class="text-3xl font-bold tracking-tighter md:text-4xl text-gray-900 dark:text-white">
              Recursos Principais
            </h2>
            <p class="mx-auto max-w-[700px] text-gray-600 dark:text-gray-300 md:text-lg">
              Conheça os recursos que tornam o Planify a escolha ideal para gerenciamento de projetos de P&D.
            </p>
          </div>
        </div>
        <div class="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600 dark:bg-blue-900 dark:text-blue-300">
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
            <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Gestão de Projetos</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Organize seus projetos de P&D com facilidade, definindo cronogramas, marcos e objetivos claros.
            </p>
          </div>
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
                <rect width="8" height="8" x="3" y="3" rx="2"></rect>
                <rect width="8" height="8" x="13" y="3" rx="2"></rect>
                <rect width="8" height="8" x="3" y="13" rx="2"></rect>
                <rect width="8" height="8" x="13" y="13" rx="2"></rect>
              </svg>
            </div>
            <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Gestão de Tarefas</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Atribua e acompanhe tarefas com facilidade, garantindo que todos os membros da equipe estejam alinhados.
            </p>
          </div>
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-purple-600 dark:bg-purple-900 dark:text-purple-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Gestão de Equipes</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Gerencie sua equipe de P&D, definindo funções, responsabilidades e acompanhando o desempenho.
            </p>
          </div>
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-yellow-100 text-yellow-600 dark:bg-yellow-900 dark:text-yellow-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
                <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" x2="12" y1="9" y2="13"></line>
                <line x1="12" x2="12.01" y1="17" y2="17"></line>
              </svg>
            </div>
            <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Gestão de Riscos</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Identifique, avalie e mitigue riscos em seus projetos de P&D, garantindo o sucesso das iniciativas.
            </p>
          </div>
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path>
                <path d="M12 18V6"></path>
              </svg>
            </div>
            <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Gestão de Custos</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Controle os custos de seus projetos de P&D, garantindo que estejam dentro do orçamento planejado.
            </p>
          </div>
          <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md dark:border-gray-800 dark:bg-gray-800">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100 text-indigo-600 dark:bg-indigo-900 dark:text-indigo-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-6 w-6">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
            </div>
            <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">Gestão de Documentos</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Organize e compartilhe documentos importantes relacionados aos seus projetos de P&D.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-16 md:py-24">
      <div class="container mx-auto px-4 md:px-6">
        <div class="flex flex-col items-center justify-center space-y-4 text-center">
          <div class="space-y-2">
            <h2 class="text-3xl font-bold tracking-tighter md:text-4xl text-gray-900 dark:text-white">
              Pronto para começar?
            </h2>
            <p class="mx-auto max-w-[600px] text-gray-600 dark:text-gray-300 md:text-lg">
              Comece a gerenciar seus projetos de P&D de forma eficiente com o Planify.
            </p>
          </div>
          <div class="flex flex-wrap items-center justify-center gap-4">
            <NuxtLink to="/login" class="inline-flex items-center justify-center rounded-md bg-blue-600 px-6 py-3 text-base font-medium text-white shadow-lg transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 dark:bg-blue-700 dark:hover:bg-blue-600">
              Começar agora
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-200 bg-white py-8 dark:border-gray-800 dark:bg-gray-900">
      <div class="container mx-auto px-4 md:px-6">
        <div class="flex flex-col items-center justify-between gap-4 md:flex-row">
          <div class="flex items-center gap-2">
            <div class="flex h-8 w-8 items-center justify-center rounded-md bg-blue-600 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                <path d="M2 17a5 5 0 0 0 10 0c0-2.76-2.5-5-5-3-2.5-2-5 .24-5 3Z"></path>
                <path d="M12 17a5 5 0 0 0 10 0c0-2.76-2.5-5-5-3-2.5-2-5 .24-5 3Z"></path>
                <path d="M7 14c3.22-2.91 4.29-8.75 5-12 1.66 2.38 4.94 9 5 12"></path>
                <path d="M22 9c-4.29 0-7.14-2.33-10-7 5.71 0 10 4.67 10 7Z"></path>
              </svg>
            </div>
            <span class="text-sm font-bold text-blue-600 dark:text-blue-400">Planify</span>
          </div>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            &copy; {{ new Date().getFullYear() }} Planify. Todos os direitos reservados.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '~/composables/useAuth'

const router = useRouter()
const isDarkMode = ref(false)
const { isAuthenticated } = useAuth()

// Verificar se o usuário já está autenticado
onMounted(() => {
  // Redirecionar para o dashboard se o usuário estiver autenticado
  if (isAuthenticated.value) {
    router.push('/dashboard')
  }
  
  // Verificar preferência de tema
  if (process.client) {
    // Verificar preferência salva
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
</script>
