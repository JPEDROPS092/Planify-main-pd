<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <div class="mb-6 rounded-full bg-gray-100 p-6 dark:bg-gray-800">
      <slot name="icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-10 w-10 text-gray-400 dark:text-gray-500">
          <rect width="8" height="8" x="3" y="3" rx="2"></rect>
          <rect width="8" height="8" x="13" y="3" rx="2"></rect>
          <rect width="8" height="8" x="3" y="13" rx="2"></rect>
          <rect width="8" height="8" x="13" y="13" rx="2"></rect>
        </svg>
      </slot>
    </div>
    <h3 class="mb-2 text-xl font-bold text-gray-900 dark:text-white">
      <slot name="title">Nenhum dado encontrado</slot>
    </h3>
    <p class="mb-6 max-w-md text-gray-500 dark:text-gray-400">
      <slot name="description">Não encontramos nenhum dado para exibir neste momento.</slot>
    </p>
    <slot name="action">
      <button class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600">
        Criar novo
      </button>
    </slot>
  </div>
</template>
