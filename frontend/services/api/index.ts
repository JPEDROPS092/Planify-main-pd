/**
 * API Services
 * 
 * Este arquivo centraliza a exportação de todos os serviços de API,
 * facilitando a importação em outros arquivos do projeto.
 */

// Serviços de API
export { useProjectService } from './services/projectService';
export { useTaskService } from './services/taskService';
export { useDocumentService } from './services/documentService';
export { useUserService } from './services/userService';
export { useCostService } from './services/costService';
export { useMessageService, useNotificationService } from './services/messageService';
export { useRiskService } from './services/riskService';
export { useAuthService } from './services/authService';

// Tipos de API
export * from './types';

// Configuração e utilitários
export { createApiClient, createFormData } from './config';
