/**
 * Middleware para verificar acesso a um projeto específico
 * Verifica se o usuário tem permissão para acessar o projeto
 */
export default defineNuxtRouteMiddleware(async (to) => {
  const projectId = to.params.id
  
  if (!projectId) {
    return
  }
  
  try {
    // Usar composable do Orval para verificar acesso
    const { data: project } = await useProjectsProjectsRetrieveQuery(
      { id: projectId },
      { 
        query: {
          retry: false, // Não tentar novamente se der 403/404
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
        statusMessage: 'Você não tem acesso a este projeto'
      })
    }
    
    if (error.response?.status === 404) {
      throw createError({
        statusCode: 404,
        statusMessage: 'Projeto não encontrado'
      })
    }
    
    // Em caso de outros erros, reportar erro genérico
    throw createError({
      statusCode: 500,
      statusMessage: 'Erro ao carregar dados do projeto'
    })
  }
})
