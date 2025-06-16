// plugins/icons.ts
export default defineNuxtPlugin(() => {
  // Plugin de ícones que utiliza bibliotecas disponíveis
  // Phosphor Icons e Lucide estão disponíveis globalmente
  
  // Mapeamento de ícones comuns para facilitar o uso
  const iconMap = {
    // Ações básicas
    'add': 'ph:plus',
    'close': 'ph:x',
    'check': 'ph:check',
    'edit': 'ph:pencil',
    'delete': 'ph:trash',
    'view': 'ph:eye',
    'hide': 'ph:eye-slash',
    
    // Navegação
    'arrow-left': 'ph:arrow-left',
    'arrow-right': 'ph:arrow-right',
    'home': 'ph:house',
    'chevron-down': 'ph:caret-down',
    'chevron-up': 'ph:caret-up',
    
    // Interface
    'user': 'ph:user',
    'settings': 'ph:gear',
    'notification': 'ph:bell',
    'search': 'ph:magnifying-glass',
    'menu': 'ph:list',
    
    // Conteúdo
    'calendar': 'ph:calendar',
    'clock': 'ph:clock',
    'document': 'ph:file-text',
    'folder': 'ph:folder',
    'chart': 'ph:chart-bar',
    'users': 'ph:users',
    
    // Estados
    'warning': 'ph:warning',
    'info': 'ph:info',
    'success': 'ph:check-circle',
    'error': 'ph:x-circle',
    'loading': 'ph:spinner',
    
    // Ações específicas
    'download': 'ph:download',
    'upload': 'ph:upload',
    'save': 'ph:floppy-disk',
    'copy': 'ph:copy',
    'share': 'ph:share',
  };

  // Função helper para obter o nome do ícone
  const getIconName = (key: string): string => {
    return iconMap[key as keyof typeof iconMap] || 'ph:question';
  };

  // Lista de ícones disponíveis
  const getAvailableIcons = () => {
    return Object.keys(iconMap);
  };

  return {
    provide: {
      iconMap,
      getIconName,
      getAvailableIcons,
    }
  };
});
