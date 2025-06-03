/**
 * Plugin de autenticação para Nuxt
 * Integra o serviço de autenticação com o Nuxt
 */
import { defineNuxtPlugin } from '#app';
import { useAuth } from '~/composables/useAuth';

export default defineNuxtPlugin(async (nuxtApp) => {
  // Garantir que o plugin API seja carregado primeiro
  // Isso é importante porque useAuth depende da instância de API
  await nuxtApp.callHook('app:created');

  // Inicializar o serviço de autenticação
  const auth = useAuth();

  // Verificar autenticação ao iniciar a aplicação
  // Isso só precisa rodar no cliente, pois depende do localStorage e interações de API
  if (process.client) {
    try {
      // Verificar estado de autenticação após a hidratação
      // Usar setTimeout para garantir que a API esteja disponível
      setTimeout(async () => {
        await auth.checkAuth();
        console.log('Estado de autenticação verificado com sucesso pelo plugin.');
      }, 0);
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
