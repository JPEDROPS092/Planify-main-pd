
/**
 * Teams API endpoints
 * Direct interface for team-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface TeamMember {
  id?: number;
  user_id: number;
  role: string;
  name?: string;
  email?: string;
  profile_picture?: string;
}

export interface Team {
  id?: number;
  name: string;
  description?: string;
  project_id?: number;
  members: TeamMember[];
  created_at?: string;
  updated_at?: string;
}

export interface TeamResponse {
  id: number;
  name: string;
  description: string;
  project_id: number;
  members: TeamMember[];
  created_at: string;
  updated_at: string;
}

export interface TeamListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: TeamResponse[];
}

// API Endpoints

/**
 * Get list of teams
 */
export const listEquipes = async (params?: Record<string, any>): Promise<TeamListResponse> => {
  return apiClient.get('/api/teams/', { params });
};

/**
 * Get team by ID
 */
export const retrieveEquipe = async (id: number): Promise<TeamResponse> => {
  return apiClient.get(`/api/teams/${id}/`);
};

/**
 * Create a new team
 */
export const createEquipe = async (data: Team): Promise<TeamResponse> => {
  return apiClient.post('/api/teams/', data);
};

/**
 * Update a team
 */
export const updateEquipe = async (id: number, data: Partial<Team>): Promise<TeamResponse> => {
  return apiClient.patch(`/api/teams/${id}/`, data);
};

/**
 * Delete a team
 */
export const destroyEquipe = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/teams/${id}/`);
};

/**
 * Add a member to a team
 */
export const adicionarMembroEquipe = async (
  teamId: number, 
  memberData: TeamMember
): Promise<TeamResponse> => {
  return apiClient.post(`/api/teams/${teamId}/members/`, memberData);
};

/**
 * Remove a member from a team
 */
export const removerMembroEquipe = async (
  teamId: number, 
  memberId: number
): Promise<void> => {
  return apiClient.delete(`/api/teams/${teamId}/members/${memberId}/`);
};