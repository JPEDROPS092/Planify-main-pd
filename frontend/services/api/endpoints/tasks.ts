/**
 * Tasks API endpoints
 * Direct interface for task-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface Task {
  id?: number;
  title: string;
  description?: string;
  project_id: number;
  assigned_to?: number;
  status?: string;
  priority?: string;
  start_date?: string;
  due_date?: string;
  estimated_hours?: number;
  actual_hours?: number;
  created_by?: number;
  created_at?: string;
  updated_at?: string;
}

export interface TaskResponse {
  id: number;
  title: string;
  description: string;
  project_id: number;
  assigned_to: number;
  status: string;
  priority: string;
  start_date: string;
  due_date: string;
  estimated_hours: number;
  actual_hours: number;
  created_by: number;
  created_at: string;
  updated_at: string;
  assignee_name?: string;
  progress?: number;
}

export interface TaskListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: TaskResponse[];
}

export interface TaskComment {
  id?: number;
  task_id: number;
  user_id: number;
  content: string;
  created_at?: string;
}

// API Endpoints

/**
 * Get list of tasks
 */
export const listTasks = async (params?: Record<string, any>): Promise<TaskListResponse> => {
  return apiClient.get('/api/tasks/', { params });
};

/**
 * Get task by ID
 */
export const retrieveTask = async (id: number): Promise<TaskResponse> => {
  return apiClient.get(`/api/tasks/${id}/`);
};

/**
 * Create a new task
 */
export const createTask = async (data: Task): Promise<TaskResponse> => {
  return apiClient.post('/api/tasks/', data);
};

/**
 * Update a task
 */
export const updateTask = async (id: number, data: Partial<Task>): Promise<TaskResponse> => {
  return apiClient.patch(`/api/tasks/${id}/`, data);
};

/**
 * Delete a task
 */
export const destroyTask = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/tasks/${id}/`);
};

/**
 * Update task status
 */
export const updateTaskStatus = async (id: number, status: string): Promise<TaskResponse> => {
  return apiClient.patch(`/api/tasks/${id}/`, { status });
};

/**
 * Assign task to user
 */
export const assignTask = async (id: number, userId: number): Promise<TaskResponse> => {
  return apiClient.patch(`/api/tasks/${id}/`, { assigned_to: userId });
};

/**
 * Log time on task
 */
export const logTaskTime = async (id: number, hours: number): Promise<TaskResponse> => {
  return apiClient.post(`/api/tasks/${id}/log-time/`, { hours });
};

/**
 * Get task comments
 */
export const getTaskComments = async (taskId: number): Promise<TaskComment[]> => {
  return apiClient.get(`/api/tasks/${taskId}/comments/`);
};

/**
 * Add task comment
 */
export const addTaskComment = async (taskId: number, content: string): Promise<TaskComment> => {
  return apiClient.post(`/api/tasks/${taskId}/comments/`, { content });
};