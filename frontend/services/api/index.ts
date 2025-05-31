/**
 * Índice de serviços da API do Planify
 * Centraliza todas as exportações de serviços da API para facilitar o uso
 */

// Configurações e utilitários da API
export * from './config'

// Tipos e interfaces para tipagem forte
export * from './types'

// Serviços de autenticação e usuários
export * from './auth'

// Serviços de gerenciamento de projetos
export * from './projects'

// Serviços de gerenciamento de tarefas
export * from './tasks'

// Serviços de comunicação
export * from './communications'

// Serviços de gerenciamento de documentos
export * from './documents'

// Serviços de gerenciamento de riscos
export * from './risks'

// Serviços de gerenciamento de custos
export * from './costs'

// Serviços de gerenciamento de equipes
export * from './teams'

// Serviços adaptadores (composables)
export { useProjectService } from './projectService'
export { useTaskService } from './taskService'
export { useTeamService } from './teamService'
export { useDocumentService } from './documentService'
export { useRiskService } from './riskService'
export { useCostService } from './costService'
export { useUserService } from './userService'
export { useChatService, useNotificationService } from './communicationService'
export { permissionService } from './permissionService'

// Composable de autenticação para uso em componentes Vue
export { useAuth } from '~/composables/useAuth'
