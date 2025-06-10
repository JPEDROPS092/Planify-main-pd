/**
 * Theme Plugin
 *
 * Plugin para configurar o tema e acessibilidade globalmente na aplicação.
 * Aplica o tema salvo no localStorage ou a preferência do sistema.
 */

export default defineNuxtPlugin((nuxtApp) => {
  // Função para aplicar o tema inicial antes do Vue ser montado
  // Isso evita o flash de tema incorreto durante o carregamento
  const applyInitialTheme = () => {
    // Verificar tema salvo
    const savedTheme = localStorage.getItem('planify-theme');

    // Verificar preferência do sistema
    const prefersDark = window.matchMedia(
      '(prefers-color-scheme: dark)'
    ).matches;

    // Determinar se deve usar tema escuro
    const shouldUseDark =
      savedTheme === 'dark' ||
      ((savedTheme === 'system' || !savedTheme) && prefersDark);

    // Aplicar tema ao HTML
    if (shouldUseDark) {
      document.documentElement.classList.add('dark');
    }
  };

  // Configurar variáveis CSS para acessibilidade
  const setupAccessibilityVariables = () => {
    // Obter configurações de acessibilidade salvas
    const fontSize = localStorage.getItem('planify-font-size') || '16';

    // Aplicar tamanho de fonte base (afeta todos os rem/em)
    document.documentElement.style.fontSize = `${fontSize}px`;
  };

  // Executar apenas no cliente
  if (process.client) {
    // Aplicar tema inicial antes do Vue montar
    applyInitialTheme();

    // Configurar variáveis de acessibilidade
    setupAccessibilityVariables();

    // Adicionar atributos de acessibilidade ao body
    nuxtApp.hook('app:mounted', () => {
      // Garantir que o documento tenha lang definido
      document.documentElement.lang = document.documentElement.lang || 'pt-BR';

      // Adicionar atributos para melhorar acessibilidade
      const main = document.querySelector('main');
      if (main && !main.hasAttribute('id')) {
        main.setAttribute('id', 'main-content');
      }

      // Adicionar skip link para acessibilidade de teclado se não existir
      if (!document.querySelector('.skip-link')) {
        const skipLink = document.createElement('a');
        skipLink.className = 'skip-link sr-only focus:not-sr-only';
        skipLink.href = '#main-content';
        skipLink.innerText = 'Pular para o conteúdo principal';
        skipLink.style.position = 'absolute';
        skipLink.style.top = '0';
        skipLink.style.left = '0';
        skipLink.style.padding = '0.5rem';
        skipLink.style.zIndex = '9999';
        skipLink.style.background = 'white';
        skipLink.style.color = 'black';
        skipLink.style.textDecoration = 'none';
        document.body.insertBefore(skipLink, document.body.firstChild);
      }
    });
  }
});
