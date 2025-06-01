/**
 * Definições de permissões por papel (role)
 * Mapeia papéis de usuário para conjuntos de permissões
 */
import { Permission } from './permissionService';

/**
 * Tipos de papéis (roles) no sistema
 */
export enum Role {
  ADMIN = 'admin',
  PROJECT_MANAGER = 'project_manager',
  TEAM_MEMBER = 'team_member',
  STAKEHOLDER = 'stakeholder',
  GUEST = 'guest'
}

/**
 * Mapeamento de papéis para permissões
 * Define quais permissões cada papel tem acesso
 */
export const ROLE_PERMISSIONS: Record<Role, Permission[]> = {
  // Administrador tem acesso a todas as permissões
  [Role.ADMIN]: [
    Permission.ADMIN,
    // Todas as permissões de projeto
    Permission.VIEW_PROJECT,
    Permission.CREATE_PROJECT,
    Permission.EDIT_PROJECT,
    Permission.DELETE_PROJECT,
    // Todas as permissões de tarefa
    Permission.VIEW_TASK,
    Permission.CREATE_TASK,
    Permission.EDIT_TASK,
    Permission.DELETE_TASK,
    // Todas as permissões de equipe
    Permission.VIEW_TEAM,
    Permission.CREATE_TEAM,
    Permission.EDIT_TEAM,
    Permission.DELETE_TEAM,
    // Todas as permissões de custo
    Permission.VIEW_COST,
    Permission.CREATE_COST,
    Permission.EDIT_COST,
    Permission.DELETE_COST,
    // Todas as permissões de risco
    Permission.VIEW_RISK,
    Permission.CREATE_RISK,
    Permission.EDIT_RISK,
    Permission.DELETE_RISK,
    // Todas as permissões de documento
    Permission.VIEW_DOCUMENT,
    Permission.CREATE_DOCUMENT,
    Permission.EDIT_DOCUMENT,
    Permission.DELETE_DOCUMENT,
    // Todas as permissões de comunicação
    Permission.VIEW_COMMUNICATION,
    Permission.CREATE_COMMUNICATION,
    Permission.EDIT_COMMUNICATION,
    Permission.DELETE_COMMUNICATION
  ],

  // Gerente de projeto tem acesso a quase tudo, exceto excluir certos recursos
  [Role.PROJECT_MANAGER]: [
    // Permissões de projeto
    Permission.VIEW_PROJECT,
    Permission.CREATE_PROJECT,
    Permission.EDIT_PROJECT,
    Permission.DELETE_PROJECT,
    // Permissões de tarefa
    Permission.VIEW_TASK,
    Permission.CREATE_TASK,
    Permission.EDIT_TASK,
    Permission.DELETE_TASK,
    // Permissões de equipe
    Permission.VIEW_TEAM,
    Permission.CREATE_TEAM,
    Permission.EDIT_TEAM,
    Permission.DELETE_TEAM,
    // Permissões de custo
    Permission.VIEW_COST,
    Permission.CREATE_COST,
    Permission.EDIT_COST,
    Permission.DELETE_COST,
    // Permissões de risco
    Permission.VIEW_RISK,
    Permission.CREATE_RISK,
    Permission.EDIT_RISK,
    Permission.DELETE_RISK,
    // Permissões de documento
    Permission.VIEW_DOCUMENT,
    Permission.CREATE_DOCUMENT,
    Permission.EDIT_DOCUMENT,
    Permission.DELETE_DOCUMENT,
    // Permissões de comunicação
    Permission.VIEW_COMMUNICATION,
    Permission.CREATE_COMMUNICATION,
    Permission.EDIT_COMMUNICATION,
    Permission.DELETE_COMMUNICATION
  ],

  // Membro da equipe tem acesso a visualizar tudo, mas só pode editar tarefas e documentos
  [Role.TEAM_MEMBER]: [
    // Permissões de projeto
    Permission.VIEW_PROJECT,
    // Permissões de tarefa
    Permission.VIEW_TASK,
    Permission.CREATE_TASK,
    Permission.EDIT_TASK,
    // Permissões de equipe
    Permission.VIEW_TEAM,
    // Permissões de custo
    Permission.VIEW_COST,
    // Permissões de risco
    Permission.VIEW_RISK,
    Permission.CREATE_RISK,
    Permission.EDIT_RISK,
    // Permissões de documento
    Permission.VIEW_DOCUMENT,
    Permission.CREATE_DOCUMENT,
    Permission.EDIT_DOCUMENT,
    // Permissões de comunicação
    Permission.VIEW_COMMUNICATION,
    Permission.CREATE_COMMUNICATION,
    Permission.EDIT_COMMUNICATION
  ],

  // Stakeholder pode visualizar a maioria dos recursos, mas não pode editar
  [Role.STAKEHOLDER]: [
    // Permissões de projeto
    Permission.VIEW_PROJECT,
    // Permissões de tarefa
    Permission.VIEW_TASK,
    // Permissões de equipe
    Permission.VIEW_TEAM,
    // Permissões de custo
    Permission.VIEW_COST,
    // Permissões de risco
    Permission.VIEW_RISK,
    // Permissões de documento
    Permission.VIEW_DOCUMENT,
    // Permissões de comunicação
    Permission.VIEW_COMMUNICATION,
    Permission.CREATE_COMMUNICATION
  ],

  // Convidado tem acesso mínimo, apenas visualização de projetos e tarefas
  [Role.GUEST]: [
    // Permissões de projeto
    Permission.VIEW_PROJECT,
    // Permissões de tarefa
    Permission.VIEW_TASK,
    // Permissões de comunicação
    Permission.VIEW_COMMUNICATION
  ]
};

/**
 * Verifica se um papel tem uma permissão específica
 * @param role Papel a verificar
 * @param permission Permissão a verificar
 * @returns Verdadeiro se o papel tiver a permissão
 */
export const roleHasPermission = (role: Role, permission: Permission): boolean => {
  return ROLE_PERMISSIONS[role].includes(permission);
};

/**
 * Obtém todas as permissões para um papel
 * @param role Papel para obter permissões
 * @returns Lista de permissões do papel
 */
export const getRolePermissions = (role: Role): Permission[] => {
  return ROLE_PERMISSIONS[role];
};

/**
 * Obtém todos os papéis que têm uma permissão específica
 * @param permission Permissão para verificar
 * @returns Lista de papéis que têm a permissão
 */
export const getRolesWithPermission = (permission: Permission): Role[] => {
  return Object.entries(ROLE_PERMISSIONS)
    .filter(([_, permissions]) => permissions.includes(permission))
    .map(([role]) => role as Role);
};
