/**
 * Utilitários
 * Exporta todas as funções utilitárias para uso em toda a aplicação
 */

// Exportar todos os utilitários
// A linha './notifications' foi removida pois o arquivo notifications.ts foi excluído.
// useNotification e tipos relacionados devem ser auto-importados de stores/composables/useNotification.ts
export * from './formatters';
export * from './formValidation';
export * from './fileHandlers';

// Exportar todos os tipos para evitar dependências circulares
export * from './types';

// Re-exportar o tema como um plugin nomeado
export { default as themePlugin } from './theme';
