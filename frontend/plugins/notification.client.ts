// plugins/notification.client.ts
import { useGlobalNotification } from '../composables/useNotification';

export default defineNuxtPlugin(() => {
  // This plugin ensures the notification system is initialized on the client
  const notification = useGlobalNotification();
  
  return {
    provide: {
      notification,
    },
  };
});
