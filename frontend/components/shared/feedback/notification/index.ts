/**
 * Componentes de Notificação
 *
 * Componentes para exibir notificações e alertas ao usuário.
 */

// Importação direta para evitar duplicação de componentes no registro automático do Nuxt
import Notification from './Notification.vue';
import NotificationContainer from './NotificationContainer.vue';

// Exportação explícita dos componentes
export {
  Notification,
  NotificationContainer
};

// Exportação padrão para uso com importações default
export default {
  Notification,
  NotificationContainer
};
