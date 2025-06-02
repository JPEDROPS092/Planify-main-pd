<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 text-center">
      <!-- Logo -->
      <div>
        <img class="mx-auto h-16 w-auto" src="/img/logop.png" alt="Planify Logo" />
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">Oops!</h2>
      </div>
      
      <!-- Conteúdo do erro -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-8">
        <slot />
        
        <!-- Botão de voltar -->
        <div class="mt-6">
          <button 
            @click="goBack" 
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Voltar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

// Função para voltar à página anterior ou para o dashboard
const goBack = () => {
  if (window.history.length > 2) {
    router.go(-1);
  } else {
    router.push('/dashboard');
  }
};
</script>
