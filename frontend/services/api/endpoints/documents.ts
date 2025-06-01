/**
 * Documents API endpoints
 * Direct interface for document-related API calls
 */
import { apiClient } from '../services/apiClient';

// Types
export interface Document {
  id?: number;
  title: string;
  description?: string;
  project_id: number;
  file?: File | null;
  file_url?: string;
  document_type?: string;
  version?: string;
  created_by?: number;
  created_at?: string;
  updated_at?: string;
}

export interface DocumentResponse {
  id: number;
  title: string;
  description: string;
  project_id: number;
  file_url: string;
  file_name: string;
  document_type: string;
  version: string;
  created_by: number;
  created_by_name: string;
  created_at: string;
  updated_at: string;
}

export interface DocumentListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: DocumentResponse[];
}

// API Endpoints

/**
 * Get list of documents
 */
export const listDocuments = async (params?: Record<string, any>): Promise<DocumentListResponse> => {
  return apiClient.get('/api/documents/', { params });
};

/**
 * Get document by ID
 */
export const retrieveDocument = async (id: number): Promise<DocumentResponse> => {
  return apiClient.get(`/api/documents/${id}/`);
};

/**
 * Create a new document
 */
export const createDocument = async (data: Document): Promise<DocumentResponse> => {
  // If data includes a file, use FormData
  if (data.file instanceof File) {
    const formData = new FormData();
    
    // Add all fields to FormData
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'file') {
          formData.append(key, value as File);
        } else {
          formData.append(key, String(value));
        }
      }
    });
    
    return apiClient.post('/api/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
  
  // Otherwise use JSON
  return apiClient.post('/api/documents/', data);
};

/**
 * Update a document
 */
export const updateDocument = async (id: number, data: Partial<Document>): Promise<DocumentResponse> => {
  // If data includes a file, use FormData
  if (data.file instanceof File) {
    const formData = new FormData();
    
    // Add all fields to FormData
    Object.entries(data).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        if (key === 'file') {
          formData.append(key, value as File);
        } else {
          formData.append(key, String(value));
        }
      }
    });
    
    return apiClient.patch(`/api/documents/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
  
  // Otherwise use JSON
  return apiClient.patch(`/api/documents/${id}/`, data);
};

/**
 * Delete a document
 */
export const destroyDocument = async (id: number): Promise<void> => {
  return apiClient.delete(`/api/documents/${id}/`);
};

/**
 * Download a document
 */
export const downloadDocument = async (id: number): Promise<Blob> => {
  return apiClient.get(`/api/documents/${id}/download/`, {
    headers: {
      Accept: '*/*',
    },
  });
};

/**
 * Get document versions
 */
export const getDocumentVersions = async (id: number): Promise<DocumentResponse[]> => {
  return apiClient.get(`/api/documents/${id}/versions/`);
};