/**
 * Costs API endpoints
 * Direct interface for cost-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface Cost {
  id?: number;
  title: string;
  description?: string;
  project_id: number;
  amount: number;
  category?: string;
  status?: string;
  date?: string;
  created_by?: number;
  created_at?: string;
  updated_at?: string;
}

export interface CostResponse {
  id: number;
  title: string;
  description: string;
  project_id: number;
  amount: number;
  category: string;
  status: string;
  date: string;
  created_by: number;
  created_by_name?: string;
  created_at: string;
  updated_at: string;
}

export interface CostListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: CostResponse[];
}

export interface CostCategory {
  id?: number;
  name: string;
  description?: string;
  color?: string;
  project_id?: number;
}

export interface CostCategoryResponse {
  id: number;
  name: string;
  description: string;
  color: string;
  project_id: number;
  count: number;
  total: number;
}

export interface BudgetSummary {
  budget_total: number;
  budget_spent: number;
  budget_remaining: number;
  percentage_used: number;
  by_category: Record<string, {
    total: number;
    percentage: number;
  }>;
  by_status: Record<string, {
    total: number;
    percentage: number;
  }>;
  recent_costs: CostResponse[];
}

// API Endpoints

/**
 * Get list of costs
 */
export const listCosts = async (params?: Record<string, any>): Promise<CostListResponse> => {
  return apiClient.get('/api/costs/', { params });
};

/**
 * Get cost by ID
 */
export const retrieveCost = async (id: number): Promise<CostResponse> => {
  return apiClient.get(`/api/costs/${id}/`);
};

/**
 * Create a new cost
 */
export const createCost = async (data: Cost): Promise<CostResponse> => {
  return apiClient.post('/api/costs/', data);
};

/**
 * Update a cost
 */
export const updateCost = async (id: number, data: Partial<Cost>): Promise<CostResponse> => {
  return apiClient.patch(`/api/costs/${id}/`, data);
};

/**
 * Delete a cost
 */
export const destroyCost = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/costs/${id}/`);
};

/**
 * Get list of cost categories
 */
export const listCostCategories = async (params?: Record<string, any>): Promise<CostCategoryResponse[]> => {
  return apiClient.get('/api/cost-categories/', { params });
};

/**
 * Get cost category by ID
 */
export const retrieveCostCategory = async (id: number): Promise<CostCategoryResponse> => {
  return apiClient.get(`/api/cost-categories/${id}/`);
};

/**
 * Create a new cost category
 */
export const createCostCategory = async (data: CostCategory): Promise<CostCategoryResponse> => {
  return apiClient.post('/api/cost-categories/', data);
};

/**
 * Update a cost category
 */
export const updateCostCategory = async (id: number, data: Partial<CostCategory>): Promise<CostCategoryResponse> => {
  return apiClient.patch(`/api/cost-categories/${id}/`, data);
};

/**
 * Delete a cost category
 */
export const destroyCostCategory = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/cost-categories/${id}/`);
};

/**
 * Get project budget summary
 */
export const getProjectBudgetSummary = async (projectId: number): Promise<BudgetSummary> => {
  return apiClient.get(`/api/projects/${projectId}/budget-summary/`);
};