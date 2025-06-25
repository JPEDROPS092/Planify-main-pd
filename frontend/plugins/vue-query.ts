import { VueQueryPlugin, QueryClient, dehydrate, hydrate } from '@tanstack/vue-query';

export default defineNuxtPlugin((nuxtApp) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutos
        retry: 2,
        refetchOnWindowFocus: false,
      },
    },
  });
  
  nuxtApp.vueApp.use(VueQueryPlugin, { queryClient });

  // Suporte para SSR
  if (process.server) {
    nuxtApp.payload.vueQueryState = dehydrate(queryClient);
  }
  
  if (process.client && nuxtApp.payload.vueQueryState) {
    hydrate(queryClient, nuxtApp.payload.vueQueryState);
  }
});
