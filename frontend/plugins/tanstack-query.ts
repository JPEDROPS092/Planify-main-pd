// plugins/vue-query.ts
import {
  VueQueryPlugin,
  QueryClient,
  type VueQueryPluginOptions,
} from "@tanstack/vue-query";
import { defineNuxtPlugin } from "#app";

export default defineNuxtPlugin((nuxtApp) => {
  // 1. Crie uma instância do QueryClient
  const queryClient = new QueryClient({
    // Opcional: defina configurações padrão para todas as suas queries
    defaultOptions: {
      queries: {
        staleTime: 5 * (60 * 1000), // 5 minutos
        refetchOnWindowFocus: false, // Opcional: desativa o refetch ao focar na janela
      },
    },
  });

  // 2. Crie as opções para o plugin
  const options: VueQueryPluginOptions = { queryClient };

  // 3. Use o plugin do Vue Query na sua aplicação Vue
  nuxtApp.vueApp.use(VueQueryPlugin, options);
});
