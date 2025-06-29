/**
 * Middleware para verificar se o usuário pertence a uma equipe específica
 * Usado para proteger rotas relacionadas a equipes
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const teamId = to.params.id
  
  if (!teamId) {
    return
  }
  
  try {
    // Verificar se o usuário tem acesso à equipe
    // Usando o composable do Orval para equipes
    const { data: team } = await useEquipesEquipesRetrieveQuery(
      { id: teamId },
      { 
        query: {
          retry: false,
          throwOnError: true
        }
      }
    )
    
    // Se chegou até aqui, usuário tem acesso
    return
  } catch (error: any) {
    if (error.response?.status === 403) {
      throw createError({
        statusCode: 403,
        statusMessage: 'Você não tem acesso a esta equipe'
      })
    }
    
    if (error.response?.status === 404) {
      throw createError({
        statusCode: 404,
        statusMessage: 'Equipe não encontrada'
      })
    }
    
    // Em caso de outros erros, reportar erro genérico
    throw createError({
      statusCode: 500,
      statusMessage: 'Erro ao carregar dados da equipe'
    })
  }
})
