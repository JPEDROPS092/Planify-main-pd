/**
 * Communications API endpoints
 * Direct interface for communication-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface Message {
  id?: number;
  content: string;
  project_id: number;
  sender_id?: number;
  recipient_id?: number | null;
  is_global?: boolean;
  parent_id?: number | null;
  attachments?: File[] | null;
  created_at?: string;
  updated_at?: string;
}

export interface MessageResponse {
  id: number;
  content: string;
  project_id: number;
  sender_id: number;
  sender_name: string;
  sender_avatar: string;
  recipient_id: number | null;
  recipient_name: string | null;
  is_global: boolean;
  parent_id: number | null;
  attachments: string[];
  attachment_files: Array<{
    url: string;
    name: string;
    size: number;
    type: string;
  }>;
  reply_count: number;
  created_at: string;
  updated_at: string;
}

export interface MessageListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: MessageResponse[];
}

export interface Notification {
  id?: number;
  title: string;
  content: string;
  user_id: number;
  related_object_type?: string;
  related_object_id?: number;
  is_read?: boolean;
  created_at?: string;
}

export interface NotificationResponse {
  id: number;
  title: string;
  content: string;
  user_id: number;
  related_object_type: string;
  related_object_id: number;
  related_object_url: string;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: NotificationResponse[];
  unread_count: number;
}

// API Endpoints

/**
 * Get list of messages
 */
export const listMessages = async (params?: Record<string, any>): Promise<MessageListResponse> => {
  return apiClient.get('/api/messages/', { params });
};

/**
 * Get message by ID
 */
export const retrieveMessage = async (id: number): Promise<MessageResponse> => {
  return apiClient.get(`/api/messages/${id}/`);
};

/**
 * Create a new message
 */
export const createMessage = async (data: Message): Promise<MessageResponse> => {
  // If data includes attachments, use FormData
  if (data.attachments && data.attachments.length > 0) {
    const formData = new FormData();
    
    // Add all fields to FormData
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'attachments' && Array.isArray(value)) {
          value.forEach((file, index) => {
            formData.append(`attachments[${index}]`, file);
          });
        } else {
          formData.append(key, String(value));
        }
      }
    });
    
    return apiClient.post('/api/messages/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
  
  // Otherwise use JSON
  return apiClient.post('/api/messages/', data);
};

/**
 * Update a message
 */
export const updateMessage = async (id: number, data: Partial<Message>): Promise<MessageResponse> => {
  return apiClient.patch(`/api/messages/${id}/`, data);
};

/**
 * Delete a message
 */
export const destroyMessage = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/messages/${id}/`);
};

/**
 * Get replies to a message
 */
export const getMessageReplies = async (messageId: number): Promise<MessageResponse[]> => {
  return apiClient.get(`/api/messages/${messageId}/replies/`);
};

/**
 * Get list of notifications
 */
export const listNotifications = async (params?: Record<string, any>): Promise<NotificationListResponse> => {
  return apiClient.get('/api/notifications/', { params });
};

/**
 * Get notification by ID
 */
export const retrieveNotification = async (id: number): Promise<NotificationResponse> => {
  return apiClient.get(`/api/notifications/${id}/`);
};

/**
 * Mark notification as read
 */
export const markNotificationAsRead = async (id: number): Promise<NotificationResponse> => {
  return apiClient.patch(`/api/notifications/${id}/`, { is_read: true });
};

/**
 * Mark all notifications as read
 */
export const markAllNotificationsAsRead = async (): Promise<{ success: boolean }> => {
  return apiClient.post('/api/notifications/mark-all-read/', {});
};

/**
 * Delete a notification
 */
export const destroyNotification = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/notifications/${id}/`);
};