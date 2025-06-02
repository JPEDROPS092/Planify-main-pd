import { useNotification } from '@/stores/composables/useNotification';

export default defineNuxtPlugin((nuxtApp) => {
  const notification = useNotification();

  // Interceptar erros globais não tratados
  nuxtApp.hook('vue:error', (err) => {
    console.error('Erro não tratado:', err);
    notification.showApiError(err);
  });

  // Disponibilizar o serviço de notificação globalmente
  return {
    provide: {
      notification,
    },
  };
});
