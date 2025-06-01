/**
 * Risks API endpoints
 * Direct interface for risk-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface Risk {
  id?: number;
  title: string;
  description?: string;
  project_id: number;
  probability?: string;
  impact?: string;
  status?: string;
  category?: string;
  mitigation_plan?: string;
  contingency_plan?: string;
  owner_id?: number;
  created_by?: number;
  created_at?: string;
  updated_at?: string;
}

export interface RiskResponse {
  id: number;
  title: string;
  description: string;
  project_id: number;
  probability: string;
  impact: string;
  status: string;
  category: string;
  mitigation_plan: string;
  contingency_plan: string;
  owner_id: number;
  owner_name: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  risk_score: number;
}

export interface RiskListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: RiskResponse[];
}

// API Endpoints

/**
 * Get list of risks
 */
export const listRisks = async (params?: Record<string, any>): Promise<RiskListResponse> => {
  return apiClient.get('/api/risks/', { params });
};

/**
 * Get risk by ID
 */
export const retrieveRisk = async (id: number): Promise<RiskResponse> => {
  return apiClient.get(`/api/risks/${id}/`);
};

/**
 * Create a new risk
 */
export const createRisk = async (data: Risk): Promise<RiskResponse> => {
  return apiClient.post('/api/risks/', data);
};

/**
 * Update a risk
 */
export const updateRisk = async (id: number, data: Partial<Risk>): Promise<RiskResponse> => {
  return apiClient.patch(`/api/risks/${id}/`, data);
};

/**
 * Delete a risk
 */
export const destroyRisk = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/risks/${id}/`);
};

/**
 * Update risk status
 */
export const updateRiskStatus = async (id: number, status: string): Promise<RiskResponse> => {
  return apiClient.patch(`/api/risks/${id}/`, { status });
};

/**
 * Get project risk summary
 */
export const getProjectRiskSummary = async (projectId: number): Promise<{
  total: number;
  high: number;
  medium: number;
  low: number;
  mitigated: number;
  by_category: Record<string, number>;
}> => {
  return apiClient.get(`/api/projects/${projectId}/risk-summary/`);
};