<template>
  <!-- Removido o container principal para permitir ocupação total da tela -->
  <div>
    <!-- Slot direto sem containers adicionais -->
    <slot />
    
    <!-- Botão de alternar tema - mantido e reposicionado -->
    <button 
      @click="toggleTheme" 
      class="fixed bottom-4 right-4 z-50 p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
      aria-label="Alternar tema"
    >
      <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
      </svg>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

// Usar o composable nativo do Nuxt para color-mode
const colorMode = useColorMode();

// Derivar o estado de dark mode diretamente da preferência reativa
const isDarkMode = computed(() => colorMode.preference === 'dark');

// Alternar entre tema claro e escuro
const toggleTheme = () => {
  colorMode.preference = colorMode.preference === 'dark' ? 'light' : 'dark';
};
</script>

<style>
/* Estilos globais para remover margens e bordas, garantindo tela cheia */
html, 
body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

/* Garantir que o conteúdo do slot ocupe toda a tela disponível */
#__nuxt {
  height: 100%;
  width: 100%;
}

/* Z-index para o botão toggle */
.fixed {
  z-index: 50;
}
</style>