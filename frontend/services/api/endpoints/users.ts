/**
 * Users API endpoints
 * Direct interface for user-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface User {
  id?: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role?: string;
  profile_picture?: File | string | null;
  is_active?: boolean;
  date_joined?: string;
  last_login?: string;
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: string;
  profile_picture_url: string;
  is_active: boolean;
  date_joined: string;
  last_login: string;
  permissions: string[];
}

export interface UserListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: UserResponse[];
}

export interface UserCredentials {
  username: string;
  password: string;
}

export interface TokenResponse {
  access: string;
  refresh: string;
  user: UserResponse;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordChangeRequest {
  old_password: string;
  new_password: string;
}

export interface PasswordResetConfirmRequest {
  token: string;
  password: string;
}

// API Endpoints

/**
 * Get list of users
 */
export const listUsers = async (params?: Record<string, any>): Promise<UserListResponse> => {
  return apiClient.get('/api/users/', { params });
};

/**
 * Get user by ID
 */
export const retrieveUser = async (id: number): Promise<UserResponse> => {
  return apiClient.get(`/api/users/${id}/`);
};

/**
 * Get current user profile
 */
export const getCurrentUser = async (): Promise<UserResponse> => {
  return apiClient.get('/api/users/me/');
};

/**
 * Update user profile
 */
export const updateUserProfile = async (data: Partial<User>): Promise<UserResponse> => {
  // If data includes a profile picture, use FormData
  if (data.profile_picture instanceof File) {
    const formData = new FormData();
    
    // Add all fields to FormData
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'profile_picture') {
          formData.append(key, value as File);
        } else {
          formData.append(key, String(value));
        }
      }
    });
    
    return apiClient.patch('/api/users/me/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
  
  // Otherwise use JSON
  return apiClient.patch('/api/users/me/', data);
};

/**
 * Login user
 */
export const login = async (credentials: UserCredentials): Promise<TokenResponse> => {
  return apiClient.post('/api/auth/login/', credentials, { withAuth: false });
};

/**
 * Refresh token
 */
export const refreshToken = async (refresh: string): Promise<{ access: string }> => {
  return apiClient.post('/api/auth/token/refresh/', { refresh }, { withAuth: false });
};

/**
 * Request password reset
 */
export const requestPasswordReset = async (data: PasswordResetRequest): Promise<{ detail: string }> => {
  return apiClient.post('/api/auth/password-reset/', data, { withAuth: false });
};

/**
 * Confirm password reset
 */
export const confirmPasswordReset = async (data: PasswordResetConfirmRequest): Promise<{ detail: string }> => {
  return apiClient.post('/api/auth/password-reset/confirm/', data, { withAuth: false });
};

/**
 * Change password
 */
export const changePassword = async (data: PasswordChangeRequest): Promise<{ detail: string }> => {
  return apiClient.post('/api/auth/password/change/', data);
};