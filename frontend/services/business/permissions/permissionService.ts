/**
 * Serviço de permissões
 * Gerencia verificações de permissões e regras de acesso
 */
import { useState } from '#imports';
import { UserProfile } from '../../api/endpoints/auth';

/**
 * Tipos de permissões disponíveis no sistema
 */
export enum Permission {
  // Permissões de projeto
  VIEW_PROJECT = 'view_project',
  CREATE_PROJECT = 'create_project',
  EDIT_PROJECT = 'edit_project',
  DELETE_PROJECT = 'delete_project',
  
  // Permissões de tarefa
  VIEW_TASK = 'view_task',
  CREATE_TASK = 'create_task',
  EDIT_TASK = 'edit_task',
  DELETE_TASK = 'delete_task',
  
  // Permissões de equipe
  VIEW_TEAM = 'view_team',
  CREATE_TEAM = 'create_team',
  EDIT_TEAM = 'edit_team',
  DELETE_TEAM = 'delete_team',
  
  // Permissões de custo
  VIEW_COST = 'view_cost',
  CREATE_COST = 'create_cost',
  EDIT_COST = 'edit_cost',
  DELETE_COST = 'delete_cost',
  
  // Permissões de risco
  VIEW_RISK = 'view_risk',
  CREATE_RISK = 'create_risk',
  EDIT_RISK = 'edit_risk',
  DELETE_RISK = 'delete_risk',
  
  // Permissões de documento
  VIEW_DOCUMENT = 'view_document',
  CREATE_DOCUMENT = 'create_document',
  EDIT_DOCUMENT = 'edit_document',
  DELETE_DOCUMENT = 'delete_document',
  
  // Permissões de comunicação
  VIEW_COMMUNICATION = 'view_communication',
  CREATE_COMMUNICATION = 'create_communication',
  EDIT_COMMUNICATION = 'edit_communication',
  DELETE_COMMUNICATION = 'delete_communication',
  
  // Permissões administrativas
  ADMIN = 'admin'
}

/**
 * Hook para gerenciar permissões do usuário
 * @returns Métodos para verificar permissões
 */
export const usePermissionService = () => {
  const user = useState<UserProfile | null>('auth.user');
  
  /**
   * Verifica se o usuário tem uma permissão específica
   * @param permission Permissão a ser verificada
   * @returns Verdadeiro se o usuário tiver a permissão
   */
  const hasPermission = (permission: Permission | string): boolean => {
    if (!user.value || !user.value.permissions) return false;
    
    // Verificar se o usuário é admin (tem todas as permissões)
    if (user.value.permissions.includes(Permission.ADMIN)) return true;
    
    return user.value.permissions.includes(permission);
  };
  
  /**
   * Verifica se o usuário tem todas as permissões especificadas
   * @param permissions Lista de permissões a verificar
   * @returns Verdadeiro se o usuário tiver todas as permissões
   */
  const hasAllPermissions = (permissions: (Permission | string)[]): boolean => {
    return permissions.every(permission => hasPermission(permission));
  };
  
  /**
   * Verifica se o usuário tem pelo menos uma das permissões especificadas
   * @param permissions Lista de permissões a verificar
   * @returns Verdadeiro se o usuário tiver pelo menos uma das permissões
   */
  const hasAnyPermission = (permissions: (Permission | string)[]): boolean => {
    return permissions.some(permission => hasPermission(permission));
  };
  
  /**
   * Verifica se o usuário é o criador de um recurso
   * @param resource Recurso a verificar
   * @returns Verdadeiro se o usuário for o criador
   */
  const isResourceOwner = (resource: { criado_por?: number }): boolean => {
    if (!user.value || !resource.criado_por) return false;
    return resource.criado_por === user.value.id;
  };
  
  /**
   * Verifica se o usuário pode editar um recurso
   * @param resource Recurso a verificar
   * @param editPermission Permissão de edição necessária
   * @returns Verdadeiro se o usuário puder editar o recurso
   */
  const canEditResource = (resource: { criado_por?: number }, editPermission: Permission | string): boolean => {
    // Usuário pode editar se tiver permissão de edição ou for o criador do recurso
    return hasPermission(editPermission) || isResourceOwner(resource);
  };
  
  /**
   * Verifica se o usuário pode excluir um recurso
   * @param resource Recurso a verificar
   * @param deletePermission Permissão de exclusão necessária
   * @returns Verdadeiro se o usuário puder excluir o recurso
   */
  const canDeleteResource = (resource: { criado_por?: number }, deletePermission: Permission | string): boolean => {
    // Usuário pode excluir se tiver permissão de exclusão ou for o criador do recurso
    return hasPermission(deletePermission) || isResourceOwner(resource);
  };
  
  return {
    hasPermission,
    hasAllPermissions,
    hasAnyPermission,
    isResourceOwner,
    canEditResource,
    canDeleteResource
  };
};
