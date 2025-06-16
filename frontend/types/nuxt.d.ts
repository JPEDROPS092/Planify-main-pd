// types/nuxt.d.ts
declare global {
  // Nuxt Configuration
  const defineNuxtConfig: (config: any) => any;
  
  // Nuxt Plugins
  const defineNuxtPlugin: (plugin: any) => any;
  
  // Nuxt App
  const useNuxtApp: () => any;
  const navigateTo: (path: string) => Promise<any>;
  const useCookie: (name: string, options?: any) => any;
  const addRouteMiddleware: (name: string, middleware: any) => void;
  const useRuntimeConfig: () => any;
}

export {};
