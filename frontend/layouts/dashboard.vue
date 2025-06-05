<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
    <!-- Barra de navegação superior -->
    <nav class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo e título -->
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <img class="h-8 w-auto" src="/img/logop.png" alt="Planify" />
              <span class="ml-2 text-xl font-bold text-gray-900 dark:text-white"
                >Planify</span
              >
            </div>
          </div>

          <!-- Navegação superior -->
          <div class="hidden sm:ml-6 sm:flex sm:items-center sm:space-x-4">
            <!-- Notificações -->
            <button
              class="p-1 rounded-full text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              <span class="sr-only">Ver notificações</span>
              <svg
                class="h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                />
              </svg>
            </button>

            <!-- Menu de perfil -->
            <div class="ml-3 relative">
              <div>
                <button class="flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                  <span class="sr-only">Abrir menu de usuário</span>
                  <img
                    class="h-8 w-8 rounded-full"
                    src="https://ui-avatars.com/api/?name=User&background=6366F1&color=fff"
                    alt=""
                  />
                </button>
              </div>
            </div>

            <!-- Botão de alternar tema -->
            <button
              @click="toggleTheme"
              class="p-1 rounded-full text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              aria-label="Alternar tema"
            >
              <!-- Fixed SVG paths to ensure consistency between server and client rendering -->
              <svg
                v-if="isDarkMode"
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                />
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd" 
                  d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 2a6 6 0 100 12 6 6 0 000-12zm0 1a5 5 0 11-4.7 3.3c-.1-.3.1-.5.4-.6l.3-.1a.5.5 0 01.5.8 4 4 0 105.4-5.4.5.5 0 01-.8-.5l.1-.3a.5.5 0 01.6-.4A5 5 0 0110 5z"
                />
              </svg>
            </button>
          </div>

          <!-- Botão de menu mobile -->
          <div class="-mr-2 flex items-center sm:hidden">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-purple-500"
            >
              <span class="sr-only">Abrir menu principal</span>
              <svg
                class="h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  v-if="!mobileMenuOpen"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
                <path
                  v-else
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Menu mobile -->
      <div v-show="mobileMenuOpen" class="sm:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <NuxtLink
            to="/dashboard"
            class="bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 block px-3 py-2 rounded-md text-base font-medium"
            >Dashboard</NuxtLink
          >
          <NuxtLink
            to="/projetos"
            class="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium"
            >Projetos</NuxtLink
          >
          <NuxtLink
            to="/tarefas"
            class="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium"
            >Tarefas</NuxtLink
          >
          <NuxtLink
            to="/equipes"
            class="text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium"
            >Equipes</NuxtLink
          >
        </div>
        <div class="pt-4 pb-3 border-t border-gray-200 dark:border-gray-700">
          <div class="flex items-center px-3">
            <div class="flex-shrink-0">
              <img
                class="h-10 w-10 rounded-full"
                src="https://ui-avatars.com/api/?name=User&background=6366F1&color=fff"
                alt=""
              />
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800 dark:text-white">
                Usuário
              </div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400">
                usuario@exemplo.com
              </div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <a
              href="#"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >Seu Perfil</a
            >
            <a
              href="#"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >Configurações</a
            >
            <a
              href="#"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >Sair</a
            >
          </div>
        </div>
      </div>
    </nav>

    <!-- Notificação de erro de login (se existir) -->
    <div v-if="loginError" class="bg-red-50 dark:bg-red-900/30 border-b border-red-200 dark:border-red-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <svg class="h-5 w-5 text-red-500 dark:text-red-400 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <p class="text-sm font-medium text-red-700 dark:text-red-300">
              {{ loginError }}
            </p>
          </div>
          <button @click="clearLoginError" class="ml-auto text-red-500 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300">
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="flex flex-grow">
      <!-- Barra lateral -->
      <aside class="hidden md:flex md:flex-shrink-0">
        <div class="flex flex-col w-64 border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <div class="h-0 flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <nav class="mt-5 flex-1 px-2 space-y-1">
              <NuxtLink
                to="/dashboard"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300"
              >
                <svg
                  class="mr-3 h-6 w-6 text-purple-500 dark:text-purple-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                  />
                </svg>
                Dashboard
              </NuxtLink>

              <NuxtLink
                to="/projetos"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"
                  />
                </svg>
                Projetos
              </NuxtLink>

              <NuxtLink
                to="/tarefas"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                  />
                </svg>
                Tarefas
              </NuxtLink>

              <NuxtLink
                to="/equipes"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
                Equipes
              </NuxtLink>

              <NuxtLink
                to="/riscos"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
                Riscos
              </NuxtLink>

              <NuxtLink
                to="/custos"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                Custos
              </NuxtLink>

              <NuxtLink
                to="/documentos"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2"
                  />
                </svg>
                Documentos
              </NuxtLink>

              <NuxtLink
                to="/comunicacoes"
                class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <svg
                  class="mr-3 h-6 w-6 text-gray-500 dark:text-gray-400"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"
                  />
                </svg>
                Comunicações
              </NuxtLink>
            </nav>
          </div>
        </div>
      </aside>

      <!-- Conteúdo principal -->
      <main class="flex-1 flex flex-col min-h-0 overflow-hidden">
        <div class="flex-1 relative z-0 overflow-y-auto focus:outline-none">
          <div class="py-6 px-4 sm:px-6 lg:px-8">
            <slot />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeMount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuth } from '~/composables/useAuth';

// Usar o composable nativo do Nuxt para color-mode
const colorMode = useColorMode();
const isDarkMode = ref(false);

// Para controle do menu mobile
const mobileMenuOpen = ref(false);

// Para exibição de erros de login
const route = useRoute();
const router = useRouter();
const { isAuthenticated, user, checkAuth } = useAuth();
const loginError = ref('');
const isChecking = ref(true);

// Obter mensagens de erro das query params da rota ou localStorage
const updateLoginError = () => {
  // Check URL query params first
  if (route.query.error) {
    loginError.value = decodeURIComponent(route.query.error as string);
    return;
  }
  
  // Then check localStorage for persistent errors
  if (process.client) {
    const storedError = localStorage.getItem('last_auth_error');
    if (storedError) {
      try {
        const errorData = JSON.parse(storedError);
        loginError.value = errorData.message;
      } catch (e) {
        console.error('Failed to parse stored error:', e);
        localStorage.removeItem('last_auth_error');
      }
    } else {
      loginError.value = '';
    }
  }
};

// Limpar mensagem de erro
const clearLoginError = () => {
  loginError.value = '';
  // Clear from URL
  if (route.query.error) {
    router.replace({ query: { ...route.query, error: undefined } });
  }
  // Clear from localStorage
  if (process.client) {
    localStorage.removeItem('last_auth_error');
  }
};

// Verificar autenticação ao carregar
onBeforeMount(async () => {
  isChecking.value = true;
  await checkAuth();
  
  // Verificar login após checkAuth
  if (!isAuthenticated.value) {
    console.log('User not authenticated, redirecting to login');
    router.push('/auth/login?redirect=/dashboard');
  }
  
  isChecking.value = false;
});

// Observar mudanças na rota para atualizar mensagens de erro
watch(() => route.query, updateLoginError, { immediate: true });

// Inicializar o tema
onMounted(() => {
  isDarkMode.value = colorMode.preference === 'dark';
  updateLoginError();
});

// Alternar entre tema claro e escuro
const toggleTheme = () => {
  colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark';
  isDarkMode.value = colorMode.preference === 'dark';
};
</script>

<style scoped>
/* Estilos para garantir que o conteúdo ocupe toda a altura da tela */
:deep(html),
:deep(body) {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}
</style>
