<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo e título -->
      <div class="text-center">
        <img class="mx-auto h-16 w-auto" src="/img/logop.png" alt="Planify Logo" />
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">Planify</h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Gerenciamento de Projetos de Pesquisa e Desenvolvimento
        </p>
      </div>
      
      <!-- Conteúdo da página -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6 sm:p-8">
        <slot />
      </div>
      
      <!-- Rodapé -->
      <div class="text-center mt-4">
        <p class="text-sm text-gray-500 dark:text-gray-400">
          &copy; {{ new Date().getFullYear() }} Planify. Todos os direitos reservados.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Componente de layout para páginas de autenticação
</script>
