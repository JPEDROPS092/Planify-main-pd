/**
 * useTheme.ts
 *
 * Composable para gerenciar o tema da aplicação (claro/escuro)
 * com persistência via localStorage e suporte para preferências do sistema.
 */

import { ref, onMounted, watch } from 'vue';

export type Theme = 'light' | 'dark' | 'system';

export function useTheme() {
  const theme = ref<Theme>('system');
  const isDark = ref(false);

  // Verificar se o sistema prefere tema escuro
  const getSystemPreference = (): boolean => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  };

  // Aplicar o tema ao documento
  const applyTheme = () => {
    const shouldBeDark =
      theme.value === 'dark' ||
      (theme.value === 'system' && getSystemPreference());

    isDark.value = shouldBeDark;

    // Aplicar classe ao elemento HTML
    if (shouldBeDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }

    // Salvar no localStorage
    localStorage.setItem('planify-theme', theme.value);
  };

  // Alternar entre temas
  const toggleTheme = () => {
    theme.value = isDark.value ? 'light' : 'dark';
    applyTheme();
  };

  // Definir tema específico
  const setTheme = (newTheme: Theme) => {
    theme.value = newTheme;
    applyTheme();
  };

  // Observar mudanças na preferência do sistema
  const setupSystemPreferenceListener = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    // Atualizar tema quando a preferência do sistema mudar
    const handleChange = () => {
      if (theme.value === 'system') {
        applyTheme();
      }
    };

    // Adicionar listener com compatibilidade para navegadores antigos
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
    } else {
      // Para navegadores mais antigos
      mediaQuery.addListener(handleChange);
    }
  };

  // Inicializar tema
  const initTheme = () => {
    // Recuperar tema salvo ou usar padrão
    const savedTheme = localStorage.getItem('planify-theme') as Theme | null;

    if (savedTheme && ['light', 'dark', 'system'].includes(savedTheme)) {
      theme.value = savedTheme;
    } else {
      theme.value = 'system';
    }

    applyTheme();
    setupSystemPreferenceListener();
  };

  // Inicializar quando o componente for montado
  onMounted(() => {
    initTheme();
  });

  // Observar mudanças no tema e aplicar
  watch(theme, () => {
    applyTheme();
  });

  return {
    theme,
    isDark,
    toggleTheme,
    setTheme,
  };
}
