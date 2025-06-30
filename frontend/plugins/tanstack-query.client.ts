import {
  VueQueryPlugin,
  QueryClient,
  type VueQueryPluginOptions,
} from "@tanstack/vue-query";
import { defineNuxtPlugin, useState } from "#app";

export default defineNuxtPlugin((nuxtApp) => {
  // Cria uma instância do QueryClient.
  // As opções de configuração que você já tinha estão ótimas.
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutos de cache "fresco"
        gcTime: 1000 * 60 * 10, // 10 minutos até o cache ser limpo se não for usado
        retry: (failureCount, error: any) => {
          // Não tenta novamente se for um erro de autorização (401) ou não encontrado (404)
          if (
            error?.response?.status === 401 ||
            error?.response?.status === 404
          ) {
            return false;
          }
          // Para outros erros, tenta até 2 vezes (total de 3 tentativas)
          return failureCount < 2;
        },
      },
      mutations: {
        // Mutações (POST, PUT, DELETE) não devem tentar novamente por padrão
        retry: false,
      },
    },
  });

  // Define as opções para o plugin do Vue Query
  const options: VueQueryPluginOptions = {
    queryClient,
  };

  // Instala o plugin na instância do Vue da sua aplicação Nuxt.
  // Isso "injeta" o queryClient no contexto do Vue.
  nuxtApp.vueApp.use(VueQueryPlugin, options);

  // Opcional, mas útil para hydration em SSR (embora este seja um plugin .client)
  // Se você tiver um estado que precisa ser transferido do servidor para o cliente,
  // você usaria useState aqui. Para um plugin client-only, não é estritamente necessário
  // mas não causa problemas.
  const vueQueryState = useState("vue-query");
  if (process.server && nuxtApp.payload.data["vue-query"]) {
    vueQueryState.value = nuxtApp.payload.data["vue-query"];
  }
});
