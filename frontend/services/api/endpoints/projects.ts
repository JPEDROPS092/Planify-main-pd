/**
 * Projects API endpoints
 * Direct interface for project-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface Project {
  id?: number;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  status?: string;
  owner_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface ProjectResponse {
  id: number;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  status: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
  metrics?: ProjectMetrics;
  team_count?: number;
  task_count?: number;
}

export interface ProjectMetrics {
  progress: number;
  delayed_tasks: number;
  total_tasks: number;
  completed_tasks: number;
  budget_total?: number;
  budget_spent?: number;
  team_members?: number;
}

export interface ProjectListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: ProjectResponse[];
}

// API Endpoints

/**
 * Get list of projects
 */
export const listProjects = async (params?: Record<string, any>): Promise<ProjectListResponse> => {
  return apiClient.get('/api/projects/', { params });
};

/**
 * Get project by ID
 */
export const retrieveProject = async (id: number): Promise<ProjectResponse> => {
  return apiClient.get(`/api/projects/${id}/`);
};

/**
 * Create a new project
 */
export const createProject = async (data: Project): Promise<ProjectResponse> => {
  return apiClient.post('/api/projects/', data);
};

/**
 * Update a project
 */
export const updateProject = async (id: number, data: Partial<Project>): Promise<ProjectResponse> => {
  return apiClient.patch(`/api/projects/${id}/`, data);
};

/**
 * Delete a project
 */
export const destroyProject = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/projects/${id}/`);
};

/**
 * Get project dashboard data
 */
export const getProjectDashboard = async (id: number): Promise<any> => {
  return apiClient.get(`/api/projects/${id}/dashboard/`);
};

/**
 * Export project data
 */
export const exportProject = async (id: number, format: 'pdf' | 'excel'): Promise<Blob> => {
  return apiClient.get(`/api/projects/${id}/export/?format=${format}`, {
    headers: {
      Accept: format === 'pdf' ? 'application/pdf' : 'application/vnd.ms-excel',
    },
  });
};