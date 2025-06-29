import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query'

export default defineNuxtPlugin((nuxtApp) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutos
        gcTime: 1000 * 60 * 10, // 10 minutos
        retry: (failureCount, error: any) => {
          // Não retry em erros de auth
          if (error?.response?.status === 401) return false
          return failureCount < 3
        },
      },
      mutations: {
        retry: false
      }
    }
  })

  nuxtApp.vueApp.use(VueQueryPlugin, { queryClient })
  
  // Disponibilizar queryClient globalmente
  nuxtApp.provide('queryClient', queryClient)
})
