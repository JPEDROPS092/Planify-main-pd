import { computed } from 'vue';
import { useAuthStore } from '../modules/auth';

/**
 * Composable para gerenciamento de permissões
 * Fornece funções para verificar permissões do usuário em diferentes contextos
 */
export function usePermissions() {
  const authStore = useAuthStore();
  
  /**
   * Verifica se o usuário tem uma permissão específica
   */
  const can = computed(() => (permission: string) => {
    return authStore.hasPermission(permission);
  });
  
  /**
   * Verifica se o usuário é o proprietário de um recurso
   * @param resource O recurso a ser verificado
   * @param userIdField Nome do campo que contém o ID do usuário no recurso (padrão: 'criado_por')
   */
  const isOwner = (resource: any, userIdField: string = 'criado_por') => {
    if (!resource || !authStore.getUserId) return false;
    
    // Verificar se o campo é um objeto (relação) ou um ID
    const ownerId = typeof resource[userIdField] === 'object' 
      ? resource[userIdField]?.id 
      : resource[userIdField];
      
    return ownerId === authStore.getUserId;
  };
  
  /**
   * Verifica se o usuário pode editar um recurso
   * (é proprietário ou tem permissão de edição)
   */
  const canEdit = (resource: any, resourceType: string = 'item') => {
    // Administradores podem editar qualquer coisa
    if (authStore.getUserRole === 'admin') return true;
    
    // Gerentes podem editar qualquer recurso do projeto
    if (authStore.getUserRole === 'manager' && 
        ['project', 'task', 'risk', 'cost', 'document'].includes(resourceType)) {
      return true;
    }
    
    // Verificar permissão específica de escrita
    if (authStore.hasPermission(`write:${resourceType}s`)) {
      return true;
    }
    
    // Proprietários podem editar seus próprios recursos
    return isOwner(resource);
  };
  
  /**
   * Verifica se o usuário pode excluir um recurso
   * (é proprietário ou tem permissão de exclusão)
   */
  const canDelete = (resource: any, resourceType: string = 'item') => {
    // Administradores podem excluir qualquer coisa
    if (authStore.getUserRole === 'admin') return true;
    
    // Verificar permissão específica de exclusão
    if (authStore.hasPermission(`delete:${resourceType}s`)) {
      return true;
    }
    
    // Proprietários podem excluir seus próprios recursos
    return isOwner(resource);
  };
  
  /**
   * Verifica se o usuário tem acesso a um projeto
   * (é membro, proprietário ou administrador)
   */
  const hasProjectAccess = (projectId: number, members: any[] = []) => {
    // Administradores têm acesso a todos os projetos
    if (authStore.getUserRole === 'admin') return true;
    
    // Verificar se o usuário é o proprietário do projeto
    if (isOwner({ projeto_id: projectId })) return true;
    
    // Verificar se o usuário é membro do projeto
    if (members.length > 0) {
      return members.some(member => 
        member.usuario_id === authStore.getUserId
      );
    }
    
    return false;
  };
  
  /**
   * Verifica se o usuário pode convidar membros para um projeto
   */
  const canInviteMembers = (projectId: number) => {
    // Administradores e gerentes podem convidar
    if (['admin', 'manager'].includes(authStore.getUserRole as string)) return true;
    
    // Verificar permissão específica
    if (authStore.hasPermission('invite:members')) return true;
    
    return false;
  };
  
  /**
   * Verifica se o usuário pode gerenciar permissões de um projeto
   */
  const canManagePermissions = (projectId: number) => {
    // Apenas administradores e gerentes podem gerenciar permissões
    if (['admin', 'manager'].includes(authStore.getUserRole as string)) return true;
    
    return false;
  };
  
  return {
    can,
    isOwner,
    canEdit,
    canDelete,
    hasProjectAccess,
    canInviteMembers,
    canManagePermissions
  };
}
