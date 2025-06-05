<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Page header with welcome message -->
    <div class="mb-8">
      <div v-if="user" class="flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
            Bem-vindo, {{ user.full_name || user.username }}!
          </h1>
          <p class="text-gray-600 dark:text-gray-300 mt-1">
            {{ getCurrentDateTime() }} | {{ getCurrentDate() }}
          </p>
        </div>
        
        <!-- Quick actions -->
        <div class="flex space-x-2">
          <button class="inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 hover:bg-purple-200 dark:hover:bg-purple-800 transition-colors">
            <span class="mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
            </span>
            Nova Tarefa
          </button>
          <button class="inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-medium bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors">
            <span class="mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
              </svg>
            </span>
            Agendar Reunião
          </button>
        </div>
      </div>
      
      <!-- Loading state -->
      <div v-else-if="isLoading" class="flex items-center space-x-4">
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-purple-600"></div>
        <p class="text-gray-600 dark:text-gray-300">Carregando informações do usuário...</p>
      </div>
    </div>

    <!-- Display appropriate dashboard based on user role -->
    <RoleBasedDashboard v-if="isAuthenticated && !isLoading" />
    
    <!-- Error state if not authenticated -->
    <div v-else-if="!isLoading && !isAuthenticated" class="bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 flex flex-col items-center justify-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-yellow-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h2 class="text-xl font-bold text-gray-800 dark:text-white mb-2">Sessão Expirada</h2>
      <p class="text-gray-600 dark:text-gray-300 mb-4 text-center">
        Sua sessão pode ter expirado ou você não está autenticado.
      </p>
      <button 
        @click="redirectToLogin"
        class="bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
        Fazer Login Novamente
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '~/composables/useAuth';

// Define page metadata including layout and required middleware
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
  requiresAuth: true
});

const router = useRouter();
const { user, isAuthenticated } = useAuth();
const isLoading = ref(true);

// Get current date and time in user-friendly format
const getCurrentDateTime = () => {
  const now = new Date();
  return now.toLocaleTimeString('pt-BR', { 
    hour: '2-digit', 
    minute: '2-digit'
  });
};

const getCurrentDate = () => {
  const now = new Date();
  return now.toLocaleDateString('pt-BR', { 
    weekday: 'long', 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  });
};

// Redirect to login page
const redirectToLogin = () => {
  router.push('/auth/login?redirect=/dashboard');
};

// Set loading state
onMounted(() => {
  // Simulate a loading delay
  setTimeout(() => {
    isLoading.value = false;
  }, 1000);
});
</script>