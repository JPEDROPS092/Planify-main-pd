/**
 * API Services
 * Exportação central para todos os serviços da API
 */

// Exportar cliente API
export * from './client';

// Exportar autenticação
export * from './auth';

// Exportar todos os serviços
// Explicitly re-exporting non-conflicting members from './services'
export { 
    apiClient, 
    useAuthService, 
    useProjectService, 
    useTaskService, 
    useTeamService, 
    useRiskService, 
    useCostService, 
    useDocumentService, 
    useUserService
} from './services';
