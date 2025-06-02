<template>
  <NuxtLayout name="error">
    <div class="error-container">
      <h1 class="text-4xl font-bold text-red-600 dark:text-red-400 mb-4">404</h1>
      <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-2">Página não encontrada</h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        A página que você está procurando não existe ou foi movida.
      </p>
      <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
        <NuxtLink
          to="/"
          class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          Voltar para o início
        </NuxtLink>
        <NuxtLink
          to="/dashboard"
          class="px-4 py-2 bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
        >
          Ir para o Dashboard
        </NuxtLink>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
});
</script>

<style scoped>
.error-container {
  text-align: center;
}
</style>
