/**
 * Middleware para carregar dados críticos do usuário
 * Usado para pré-carregar dados do usuário antes de exibir a página
 */
export default defineNuxtRouteMiddleware(async () => {
  const { isAuthenticated, isLoadingUser } = useAuth()
  
  // Se não está autenticado ou ainda está carregando, retorna
  if (!isAuthenticated.value || isLoadingUser.value) {
    return
  }
  
  try {
    // Carregar dados de perfil do usuário usando Orval
    const { data: profile } = await useAuthUsersMeRetrieve({
      query: {
        retry: false
      }
    })
    
    // Carregar permissões do usuário
    await useUsersMyPermissionsList()
    
    // Aqui poderia armazenar os dados em um store Pinia
    // const authStore = useAuthStore()
    // authStore.setUser(profile.value)
    
    return
  } catch (error) {
    // Em caso de erro, continuar sem bloquear a navegação
    console.error('Erro ao carregar dados críticos do usuário:', error)
  }
})
