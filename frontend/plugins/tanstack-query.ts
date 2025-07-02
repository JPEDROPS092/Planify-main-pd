// plugins/tanstack-query.ts
import {
  VueQueryPlugin,
  QueryClient,
  type VueQueryPluginOptions,
  type Query,
} from "@tanstack/vue-query";
import { type Ref } from "vue";

// @ts-ignore - These imports are resolved by Nuxt at runtime
import { defineNuxtPlugin, useState, type NuxtApp } from "#imports";

export default defineNuxtPlugin((nuxtApp: NuxtApp) => {
  // Create a new QueryClient instance
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 5 * (60 * 1000), // 5 minutes
        refetchOnWindowFocus: false,
      },
    },
  });

  const options: VueQueryPluginOptions = { queryClient };

  // Install Vue Query's plugin
  nuxtApp.vueApp.use(VueQueryPlugin, options);

  // Handle SSR state transfer
  if (typeof window === "undefined") {
    // server-side
    const state = useState<unknown[]>("vue-query-state", () => []);
    const queries = queryClient.getQueryCache().findAll();
    state.value = queries.map((q) => (q as Query<unknown, unknown>).state);

    nuxtApp.hooks.hook("app:rendered", () => {
      const queries = queryClient.getQueryCache().findAll();
      state.value = queries.map((q) => (q as Query<unknown, unknown>).state);
    });
  } else {
    // client-side
    const state = useState<unknown[]>("vue-query-state");
    if (state.value) {
      const queries = queryClient.getQueryCache().findAll();
      queries.forEach((q, i) => {
        if (state.value && state.value[i]) {
          (q as Query<unknown, unknown>).setState(state.value[i]);
        }
      });
    }
  }

  // Return the configured client
  return {
    provide: {
      queryClient,
    },
  };
});
