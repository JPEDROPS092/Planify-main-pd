<!--
  ThemeToggle.vue
  
  Componente para controle do tema da aplicação (claro/escuro/sistema)
  e ajustes de acessibilidade como tamanho de fonte.
  
  Uso:
  <ThemeToggle />
-->

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useTheme } from '@/stores/composables/useTheme';
import { Button } from '@/components/ui/input/button';
import { Sun, Moon, Monitor, Plus, Minus } from 'lucide-vue-next';

// Obter controles de tema do composable
const { theme, isDark, setTheme, toggleTheme } = useTheme();

// Estado do menu dropdown
const isOpen = ref(false);

// Tamanho da fonte
const fontSize = ref(16); // Default to avoid hydration mismatch

// Only set from localStorage on client-side
onMounted(() => {
  fontSize.value = parseInt(localStorage.getItem('planify-font-size') || '16');
  applyFontSize();
});

// Ícone a ser exibido com base no tema atual
const currentIcon = computed(() => {
  if (theme.value === 'system') return Monitor;
  return isDark.value ? Moon : Sun;
});

// Texto a ser exibido com base no tema atual
const themeText = computed(() => {
  if (theme.value === 'system') return 'Sistema';
  return isDark.value ? 'Escuro' : 'Claro';
});

// Alternar o menu dropdown
const toggleMenu = () => {
  isOpen.value = !isOpen.value;
};

// Fechar o menu dropdown
const closeMenu = () => {
  isOpen.value = false;
};

// Aumentar o tamanho da fonte
const increaseFontSize = () => {
  if (fontSize.value < 24) {
    fontSize.value += 1;
    applyFontSize();
  }
};

// Diminuir o tamanho da fonte
const decreaseFontSize = () => {
  if (fontSize.value > 12) {
    fontSize.value -= 1;
    applyFontSize();
  }
};

// Aplicar o tamanho da fonte
const applyFontSize = () => {
  if (process.client) {
    document.documentElement.style.fontSize = `${fontSize.value}px`;
    localStorage.setItem('planify-font-size', fontSize.value.toString());
  }
};

// Fechar o menu ao clicar fora
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.theme-toggle-container')) {
    closeMenu();
  }
};

// Adicionar e remover event listener
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <div class="theme-toggle-container relative">
    <Button
      variant="ghost"
      size="icon"
      @click="toggleMenu"
      class="relative"
      aria-label="Configurações de tema e acessibilidade"
    >
      <component :is="currentIcon" class="h-5 w-5" />
    </Button>

    <!-- Menu dropdown -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800 dark:ring-gray-700 z-50"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="theme-menu-button"
      tabindex="-1"
    >
      <div class="py-1" role="none">
        <!-- Opções de tema -->
        <div
          class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 font-medium"
        >
          Tema
        </div>

        <button
          @click="
            setTheme('light');
            closeMenu();
          "
          class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
          :class="{ 'bg-gray-100 dark:bg-gray-700': theme === 'light' }"
          role="menuitem"
        >
          <Sun class="mr-2 h-4 w-4" />
          Claro
        </button>

        <button
          @click="
            setTheme('dark');
            closeMenu();
          "
          class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
          :class="{ 'bg-gray-100 dark:bg-gray-700': theme === 'dark' }"
          role="menuitem"
        >
          <Moon class="mr-2 h-4 w-4" />
          Escuro
        </button>

        <button
          @click="
            setTheme('system');
            closeMenu();
          "
          class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
          :class="{ 'bg-gray-100 dark:bg-gray-700': theme === 'system' }"
          role="menuitem"
        >
          <Monitor class="mr-2 h-4 w-4" />
          Sistema
        </button>

        <!-- Separador -->
        <div class="my-1 h-px bg-gray-200 dark:bg-gray-700"></div>

        <!-- Controle de tamanho de fonte -->
        <div
          class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 font-medium"
        >
          Tamanho da fonte
        </div>

        <div class="flex items-center justify-between px-4 py-2">
          <button
            @click="decreaseFontSize"
            class="flex h-8 w-8 items-center justify-center rounded-md border border-gray-300 text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
            aria-label="Diminuir tamanho da fonte"
          >
            <Minus class="h-4 w-4" />
          </button>

          <span class="text-sm text-gray-700 dark:text-gray-300"
            >{{ fontSize }}px</span
          >

          <button
            @click="increaseFontSize"
            class="flex h-8 w-8 items-center justify-center rounded-md border border-gray-300 text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
            aria-label="Aumentar tamanho da fonte"
          >
            <Plus class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
