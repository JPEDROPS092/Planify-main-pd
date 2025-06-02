/**
 * Plugin de autenticação para Nuxt
 * Integra o serviço de autenticação com o Nuxt
 */
import { defineNuxtPlugin } from '#app'; // Importe defineNuxtPlugin de #app
import { useAuth } from '~/stores/composables/useAuth';

export default defineNuxtPlugin(async (nuxtApp) => { // nuxtApp é opcional se não usado
  // Inicializar o serviço de autenticação
  const auth = useAuth();

  // Verificar autenticação ao iniciar a aplicação
  // Isso só precisa rodar no cliente, pois depende do localStorage e interações de API
  // que são melhor tratadas no lado do cliente após a hidratação inicial.
  if (process.client) {
    try {
      await auth.checkAuth();
      console.log('Estado de autenticação verificado com sucesso pelo plugin.');
    } catch (error) {
      console.error('Erro ao verificar estado de autenticação no plugin:', error);
    }
  }

  // Disponibilizar o serviço globalmente como $auth
  return {
    provide: {
      auth,
    },
  };
});