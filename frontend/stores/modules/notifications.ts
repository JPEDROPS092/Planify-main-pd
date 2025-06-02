import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timeout?: number;
  timestamp: number;
  read: boolean;
  persistent?: boolean;
}

/**
 * Store para gerenciamento de notificações do sistema
 * Permite exibir, gerenciar e persistir notificações para o usuário
 */
export const useNotificationStore = defineStore('notifications', () => {
  // Estado
  const notifications = ref<Notification[]>([]);
  const maxNotifications = ref(50); // Limite para evitar sobrecarga de memória
  
  // Getters
  const getNotifications = computed(() => notifications.value);
  
  const getUnreadCount = computed(() => {
    return notifications.value.filter(n => !n.read).length;
  });
  
  const getByType = computed(() => (type: Notification['type']) => {
    return notifications.value.filter(n => n.type === type);
  });
  
  const getLatestNotifications = computed(() => (count: number = 5) => {
    return [...notifications.value]
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, count);
  });
  
  // Actions
  function addNotification(notification: Omit<Notification, 'id' | 'timestamp' | 'read'>) {
    const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const timestamp = Date.now();
    
    const newNotification: Notification = {
      id,
      timestamp,
      read: false,
      ...notification
    };
    
    // Adicionar ao início da lista
    notifications.value = [newNotification, ...notifications.value];
    
    // Limitar o número de notificações
    if (notifications.value.length > maxNotifications.value) {
      // Remover as notificações mais antigas que não são persistentes
      const toRemove = notifications.value.length - maxNotifications.value;
      const nonPersistentIndices = notifications.value
        .map((n, index) => ({ index, persistent: !!n.persistent }))
        .filter(item => !item.persistent)
        .map(item => item.index)
        .slice(-toRemove);
      
      if (nonPersistentIndices.length > 0) {
        notifications.value = notifications.value.filter((_, index) => 
          !nonPersistentIndices.includes(index)
        );
      }
    }
    
    return id;
  }
  
  function removeNotification(id: string) {
    notifications.value = notifications.value.filter(n => n.id !== id);
  }
  
  function markAsRead(id: string) {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value[index].read = true;
    }
  }
  
  function markAllAsRead() {
    notifications.value = notifications.value.map(n => ({ ...n, read: true }));
  }
  
  function clearAll(keepPersistent: boolean = true) {
    if (keepPersistent) {
      notifications.value = notifications.value.filter(n => n.persistent);
    } else {
      notifications.value = [];
    }
  }
  
  function updateNotification(id: string, updates: Partial<Notification>) {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value[index] = {
        ...notifications.value[index],
        ...updates
      };
    }
  }
  
  function setMaxNotifications(max: number) {
    maxNotifications.value = max;
  }
  
  return {
    // Estado
    notifications,
    maxNotifications,
    
    // Getters
    getNotifications,
    getUnreadCount,
    getByType,
    getLatestNotifications,
    
    // Actions
    addNotification,
    removeNotification,
    markAsRead,
    markAllAsRead,
    clearAll,
    updateNotification,
    setMaxNotifications
  };
});
