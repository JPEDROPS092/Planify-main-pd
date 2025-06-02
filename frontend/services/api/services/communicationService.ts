/**
 * Communications Service
 * Provides composable functions for messaging and notifications management in Vue components
 * Refactored to use the new API structure
 */
import { ref, computed } from 'vue';
import * as communicationsApi from '../endpoints/communications';
import type { 
  Message, 
  MessageResponse, 
  MessageListResponse,
  Notification,
  NotificationResponse,
  NotificationListResponse
} from '../endpoints/communications';
import { useApiService } from '~/stores/composables/useApiService';
import { useAuth } from '~/stores/composables/useAuth';

// Message service composable
export const useMessageService = () => {
  const { handleApiError, withLoading } = useApiService();
  const { user } = useAuth();
  
  // State
  const messages = ref<MessageResponse[]>([]);
  const currentMessage = ref<MessageResponse | null>(null);
  const replies = ref<MessageResponse[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const totalMessages = ref(0);
  const hasNextPage = ref(false);
  const hasPreviousPage = ref(false);
  
  // Fetch messages with optional filtering
  const fetchMessages = async (params: Record<string, any> = {}) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await communicationsApi.listMessages(params);
      messages.value = response.results;
      totalMessages.value = response.count;
      hasNextPage.value = !!response.next;
      hasPreviousPage.value = !!response.previous;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch a specific message by ID
  const fetchMessage = async (id: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await communicationsApi.retrieveMessage(id);
      currentMessage.value = response;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Send a new message
  const sendMessage = async (data: Message) => {
    return withLoading(async () => {
      try {
        // Ensure the sender ID is set if not provided
        if (!data.sender_id && user.value) {
          data.sender_id = user.value.id;
        }
        
        const response = await communicationsApi.createMessage(data);
        
        // Add to local state if appropriate
        if (!data.parent_id) {
          messages.value = [response, ...messages.value];
          totalMessages.value++;
        } else if (currentMessage.value && data.parent_id === currentMessage.value.id) {
          replies.value = [...replies.value, response];
          if (currentMessage.value) {
            currentMessage.value.reply_count = (currentMessage.value.reply_count || 0) + 1;
          }
        }
        
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Enviando mensagem...',
      successMessage: 'Mensagem enviada com sucesso!'
    });
  };
  
  // Update an existing message
  const updateMessage = async (id: number, data: Partial<Message>) => {
    return withLoading(async () => {
      try {
        const response = await communicationsApi.updateMessage(id, data);
        
        // Update in local state if found
        const index = messages.value.findIndex(m => m.id === id);
        if (index !== -1) {
          messages.value[index] = response;
        }
        
        // Update current message if it's the one being edited
        if (currentMessage.value && currentMessage.value.id === id) {
          currentMessage.value = response;
        }
        
        // Check if it's in replies
        const replyIndex = replies.value.findIndex(r => r.id === id);
        if (replyIndex !== -1) {
          replies.value[replyIndex] = response;
        }
        
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Atualizando mensagem...',
      successMessage: 'Mensagem atualizada com sucesso!'
    });
  };
  
  // Delete a message
  const deleteMessage = async (id: number) => {
    return withLoading(async () => {
      try {
        await communicationsApi.destroyMessage(id);
        
        // Remove from local state if found
        messages.value = messages.value.filter(m => m.id !== id);
        
        if (currentMessage.value && currentMessage.value.id === id) {
          currentMessage.value = null;
        }
        
        replies.value = replies.value.filter(r => r.id !== id);
        totalMessages.value = Math.max(0, totalMessages.value - 1);
        
        return true;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Excluindo mensagem...',
      successMessage: 'Mensagem excluída com sucesso!'
    });
  };
  
  // Get replies to a message
  const fetchReplies = async (messageId: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await communicationsApi.getMessageReplies(messageId);
      replies.value = response;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Mark a message as read
  const markAsRead = async (id: number) => {
    try {
      // This depends on your API - if there's no specific endpoint, 
      // we can simulate by patching the message
      const response = await communicationsApi.updateMessage(id, { is_read: true });
      
      // Update in local state if found
      const index = messages.value.findIndex(m => m.id === id);
      if (index !== -1) {
        messages.value[index] = {
          ...messages.value[index],
          is_read: true
        };
      }
      
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    }
  };
  
  // Computed properties
  const unreadCount = computed(() => {
    return messages.value.filter(m => !m.is_read).length;
  });
  
  const messagesByProject = computed(() => {
    const grouped: Record<number, MessageResponse[]> = {};
    
    messages.value.forEach(message => {
      if (!message.project_id) return;
      
      if (!grouped[message.project_id]) {
        grouped[message.project_id] = [];
      }
      
      grouped[message.project_id].push(message);
    });
    
    return grouped;
  });
  
  return {
    // State
    messages,
    currentMessage,
    replies,
    isLoading,
    error,
    totalMessages,
    hasNextPage,
    hasPreviousPage,
    
    // Computed
    unreadCount,
    messagesByProject,
    
    // Methods
    fetchMessages,
    fetchMessage,
    sendMessage,
    updateMessage,
    deleteMessage,
    fetchReplies,
    markAsRead
  };
};

// Notification service composable
export const useNotificationService = () => {
  const { handleApiError, withLoading } = useApiService();
  
  // State
  const notifications = ref<NotificationResponse[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const totalNotifications = ref(0);
  const unreadCount = ref(0);
  const hasNextPage = ref(false);
  const hasPreviousPage = ref(false);
  
  // Fetch notifications with optional filtering
  const fetchNotifications = async (params: Record<string, any> = {}) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await communicationsApi.listNotifications(params);
      notifications.value = response.results;
      totalNotifications.value = response.count;
      unreadCount.value = response.unread_count;
      hasNextPage.value = !!response.next;
      hasPreviousPage.value = !!response.previous;
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Fetch a specific notification by ID
  const fetchNotification = async (id: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await communicationsApi.retrieveNotification(id);
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  
  // Mark a notification as read
  const markAsRead = async (id: number) => {
    try {
      const response = await communicationsApi.markNotificationAsRead(id);
      
      // Update in local state if found
      const index = notifications.value.findIndex(n => n.id === id);
      if (index !== -1) {
        notifications.value[index] = response;
        
        // If it was previously unread, decrement the counter
        if (!notifications.value[index].is_read) {
          unreadCount.value = Math.max(0, unreadCount.value - 1);
        }
      }
      
      return response;
    } catch (err) {
      error.value = handleApiError(err);
      throw err;
    }
  };
  
  // Mark all notifications as read
  const markAllAsRead = async () => {
    return withLoading(async () => {
      try {
        const response = await communicationsApi.markAllNotificationsAsRead();
        
        // Update local state
        notifications.value = notifications.value.map(notification => ({
          ...notification,
          is_read: true
        }));
        
        unreadCount.value = 0;
        
        return response;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Marcando notificações como lidas...',
      successMessage: 'Todas as notificações foram marcadas como lidas!'
    });
  };
  
  // Delete a notification
  const deleteNotification = async (id: number) => {
    return withLoading(async () => {
      try {
        await communicationsApi.destroyNotification(id);
        
        // Remove from local state if found
        const notificationToRemove = notifications.value.find(n => n.id === id);
        notifications.value = notifications.value.filter(n => n.id !== id);
        
        // Update counters
        totalNotifications.value = Math.max(0, totalNotifications.value - 1);
        if (notificationToRemove && !notificationToRemove.is_read) {
          unreadCount.value = Math.max(0, unreadCount.value - 1);
        }
        
        return true;
      } catch (err) {
        error.value = handleApiError(err);
        throw err;
      }
    }, {
      loadingMessage: 'Excluindo notificação...',
      successMessage: 'Notificação excluída com sucesso!'
    });
  };
  
  // Computed: Get recent notifications (last 5)
  const recentNotifications = computed(() => {
    return [...notifications.value]
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 5);
  });
  
  // Group notifications by type
  const notificationsByType = computed(() => {
    const grouped: Record<string, NotificationResponse[]> = {};
    
    notifications.value.forEach(notification => {
      const type = notification.related_object_type || 'OTHER';
      
      if (!grouped[type]) {
        grouped[type] = [];
      }
      
      grouped[type].push(notification);
    });
    
    return grouped;
  });
  
  return {
    // State
    notifications,
    isLoading,
    error,
    totalNotifications,
    unreadCount,
    hasNextPage,
    hasPreviousPage,
    
    // Computed
    recentNotifications,
    notificationsByType,
    
    // Methods
    fetchNotifications,
    fetchNotification,
    markAsRead,
    markAllAsRead,
    deleteNotification
  };
};
