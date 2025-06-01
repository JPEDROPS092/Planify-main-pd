/**
 * API Client for Planify
 * Central utility for making API requests with proper authentication and error handling
 */
import { $fetch } from 'ofetch';
import { useRuntimeConfig } from '#app';
import { useState } from '#imports';
import { getAuthToken, ApiError, formatQueryParams } from '../config';

// Define our own FetchOptions type since it's not exported by ofetch
interface FetchOptions {
  method?: string;
  headers?: Record<string, string>;
  baseURL?: string;
  body?: any;
  [key: string]: any;
}

// Types for API requests
export type ApiResponse<T = any> = {
  status: number;
  data: T;
  response: any;
};

export type ApiRequestConfig = {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  params?: Record<string, any>;
  data?: any;
  headers?: Record<string, string>;
  withAuth?: boolean;
};

/**
 * Creates a configured API client instance
 */
const createApiClient = () => {
  const getBaseUrl = () => {
    const config = useRuntimeConfig();
    return process.client ? config.public.apiBaseUrl : '';
  };

  /**
   * Makes an API request with proper error handling
   */
  const request = async <T = any>(
    endpoint: string,
    config: ApiRequestConfig = {}
  ): Promise<T> => {
    const {
      method = 'GET',
      params = {},
      data = null,
      headers = {},
      withAuth = true,
    } = config;

    // Build request URL with query parameters
    let url = endpoint;
    const queryString = formatQueryParams(params);
    if (queryString) {
      url = `${url}?${queryString}`;
    }

    // Prepare headers
    const requestHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      ...headers,
    };

    // Add auth token if needed
    if (withAuth) {
      const token = getAuthToken();
      if (token) {
        requestHeaders['Authorization'] = `Bearer ${token}`;
      }
    }

    // Prepare fetch options
    const fetchOptions: FetchOptions = {
      method,
      headers: requestHeaders,
      baseURL: getBaseUrl(),
    };

    // Add body for non-GET requests
    if (method !== 'GET' && data !== null) {
      if (data instanceof FormData) {
        // Let the browser set the correct content type with boundary
        delete requestHeaders['Content-Type'];
        fetchOptions.body = data;
      } else {
        fetchOptions.body = data;
      }
    }

    try {
      // Make the request
      const response = await $fetch(url, fetchOptions);
      return response as T;
    } catch (error: any) {
      // Handle fetch errors
      if (error.response) {
        const { status, statusText } = error.response;
        const responseData = await error.response._data;
        
        const message = 
          responseData?.detail || 
          responseData?.message || 
          statusText || 
          'Erro na requisição';
          
        throw new ApiError(message, status, responseData);
      }
      
      // Network or other errors
      throw new ApiError(
        error.message || 'Erro de conexão',
        0,
        null
      );
    }
  };

  /**
   * HTTP methods shortcuts
   */
  return {
    get: <T = any>(endpoint: string, config: Omit<ApiRequestConfig, 'method' | 'data'> = {}) => 
      request<T>(endpoint, { ...config, method: 'GET' }),
      
    post: <T = any>(endpoint: string, data?: any, config: Omit<ApiRequestConfig, 'method' | 'data'> = {}) => 
      request<T>(endpoint, { ...config, method: 'POST', data }),
      
    put: <T = any>(endpoint: string, data?: any, config: Omit<ApiRequestConfig, 'method' | 'data'> = {}) => 
      request<T>(endpoint, { ...config, method: 'PUT', data }),
      
    patch: <T = any>(endpoint: string, data?: any, config: Omit<ApiRequestConfig, 'method' | 'data'> = {}) => 
      request<T>(endpoint, { ...config, method: 'PATCH', data }),
      
    delete: <T = any>(endpoint: string, config: Omit<ApiRequestConfig, 'method'> = {}) => 
      request<T>(endpoint, { ...config, method: 'DELETE' }),
  };
};

// Export the API client instance
export const apiClient = createApiClient();