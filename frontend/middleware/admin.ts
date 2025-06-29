/**
 * Middleware para proteger rotas de administração
 * Verifica se o usuário tem perfil de administrador
 * Utiliza as permissões retornadas pela API para verificação mais precisa
 */

/**
 * Função auxiliar para determinar quais permissões são necessárias
 * para acessar uma determinada rota
 */
function getRequiredPermissionsForRoute(path: string): string[] {
  // Mapeamento de rotas para permissões necessárias
  // Ajuste conforme as permissões reais do seu sistema
  const routePermissionsMap: Record<string, string[]> = {
    '/users': ['user.view', 'user.add', 'user.edit'],
    '/users/add': ['user.add'],
    '/users/edit': ['user.edit'],
    '/settings/roles': ['role.view', 'role.add', 'role.edit'],
    '/settings/permissions': ['permission.view', 'permission.add', 'permission.edit'],
    // Adicione mais mapeamentos conforme necessário
  }
  
  // Encontrar a rota mais específica que corresponde ao caminho atual
  const matchingRoutes = Object.keys(routePermissionsMap)
    .filter(route => path.startsWith(route))
    .sort((a, b) => b.length - a.length) // Ordenar do mais específico para o menos específico
  
  if (matchingRoutes.length > 0) {
    return routePermissionsMap[matchingRoutes[0]]
  }
  
  return []
}

/**
 * Função auxiliar para verificar se o usuário tem todas as permissões necessárias
 */
function hasRequiredPermissions(userPermissions: any, requiredPermissions: string[]): boolean {
  if (!userPermissions || !Array.isArray(userPermissions)) {
    return false
  }
  
  // Verificar se o usuário tem todas as permissões necessárias
  return requiredPermissions.every(permission => 
    userPermissions.some((p: any) => 
      p.codename === permission || p.name === permission
    )
  )
}

export default defineNuxtRouteMiddleware(async (to) => {
  const { user, isLoadingUser } = useAuth()
  
  // Se ainda está carregando, aguarda
  if (isLoadingUser.value) {
    return
  }
  
  try {
    // Verificar se usuário tem perfil de admin pelo is_staff
    if (!user.value?.is_staff) {
      throw createError({
        statusCode: 403,
        statusMessage: 'Acesso negado: Você não tem permissão de administrador'
      })
    }
    
    // Adicionalmente, carregar permissões específicas do usuário
    const { data: permissions } = await useUsersMyPermissionsList({
      query: {
        retry: false,
        throwOnError: true
      }
    })
    
    // Verificar se o usuário tem todas as permissões necessárias
    // com base na rota que está tentando acessar
    const requiredPermissions = getRequiredPermissionsForRoute(to.path)
    
    if (requiredPermissions.length > 0 && !hasRequiredPermissions(permissions.value, requiredPermissions)) {
      throw createError({
        statusCode: 403,
        statusMessage: 'Acesso negado: Você não tem as permissões necessárias para acessar esta página'
      })
    }
  } catch (error: any) {
    // Se ocorrer um erro na verificação de permissões específicas
    // mas o usuário tem is_staff, permitir o acesso
    if (user.value?.is_staff && error.message !== 'Acesso negado: Você não tem permissão de administrador') {
      return
    }
    
    // Caso contrário, propagar o erro
    throw error
  }
})

/**
 * Função auxiliar para determinar quais permissões são necessárias
 * para acessar uma determinada rota
 */
function getRequiredPermissionsForRoute(path: string): string[] {
  // Mapeamento de rotas para permissões necessárias
  // Ajuste conforme as permissões reais do seu sistema
  const routePermissionsMap: Record<string, string[]> = {
    '/users': ['user.view', 'user.add', 'user.edit'],
    '/users/add': ['user.add'],
    '/users/edit': ['user.edit'],
    '/settings/roles': ['role.view', 'role.add', 'role.edit'],
    '/settings/permissions': ['permission.view', 'permission.add', 'permission.edit'],
    // Adicione mais mapeamentos conforme necessário
  }
  
  // Encontrar a rota mais específica que corresponde ao caminho atual
  const matchingRoutes = Object.keys(routePermissionsMap)
    .filter(route => path.startsWith(route))
    .sort((a, b) => b.length - a.length) // Ordenar do mais específico para o menos específico
  
  if (matchingRoutes.length > 0) {
    return routePermissionsMap[matchingRoutes[0]]
  }
  
  return []
}

/**
 * Função auxiliar para verificar se o usuário tem todas as permissões necessárias
 */
function hasRequiredPermissions(userPermissions: any, requiredPermissions: string[]): boolean {
  if (!userPermissions || !Array.isArray(userPermissions)) {
    return false
  }
  
  // Verificar se o usuário tem todas as permissões necessárias
  return requiredPermissions.every(permission => 
    userPermissions.some((p: any) => 
      p.codename === permission || p.name === permission
    )
  )
}
