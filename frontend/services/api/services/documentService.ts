/**
 * Serviço de documentos
 * Implementação completa com suporte para feedback visual e associação automática com usuário logado
 */
import { ref } from 'vue';
import { useState } from '#imports';
import { useApiService } from '~/composables/useApiService';
import { useAuth } from '~/composables/useAuth';
import { createFetchClient } from './auth';
import { createFormData } from './config';
import { useNotification } from '~/composables/useNotification';
import type { Documento, PaginatedResponse } from './types';

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return createFetchClient();
};

// Composable para envolver operações com feedback de carregamento
const withLoading = (promise: Promise<any>, loadingMessage: string, successMessage?: string) => {
  const { showNotification, updateNotification } = useNotification();
  const notificationId = showNotification({
    title: loadingMessage,
    type: 'loading'
  });

  return promise
    .then(result => {
      if (successMessage) {
        updateNotification(notificationId, {
          title: successMessage,
          type: 'success',
          timeout: 3000
        });
      } else {
        updateNotification(notificationId, { remove: true });
      }
      return result;
    })
    .catch(error => {
      updateNotification(notificationId, {
        title: error.message || 'Ocorreu um erro',
        type: 'error',
        timeout: 5000
      });
      throw error;
    });
};

export const useDocumentService = () => {
  const { user, hasPermission } = useAuth();
  const { handleApiError } = useApiService();

  const documents = useState<Documento[]>('documents', () => []);
  const isLoading = useState<boolean>('documents.loading', () => false);
  const error = useState<string | null>('documents.error', () => null);

  // Carregar todos os documentos
  const fetchDocuments = async (projectId = null) => {
    isLoading.value = true;
    error.value = null;

    try {
      if (projectId) {
        const response = await withLoading(
          listDocumentos({ projeto: projectId }),
          'Carregando documentos do projeto...',
          'Documentos carregados com sucesso'
        );
        documents.value = response.results;
      } else {
        const response = await withLoading(
          listDocumentos(),
          'Carregando documentos...',
          'Documentos carregados com sucesso'
        );
        documents.value = response.results;
      }
      return documents.value;
    } catch (err: any) {
      error.value = err.message || 'Erro ao carregar documentos';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Obter um documento pelo ID
  const getDocument = async (documentId: number) => {
    isLoading.value = true;
    error.value = null;

    try {
      const document = await withLoading(
        retrieveDocumento(documentId),
        'Carregando documento...',
        'Documento carregado com sucesso'
      );
      return document;
    } catch (err: any) {
      error.value = err.message || `Erro ao carregar documento ${documentId}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Criar um novo documento
  const createDocument = async (documentData: any) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      // Se documentData não for FormData, associar automaticamente o usuário atual como criador
      if (!(documentData instanceof FormData) && !documentData.criado_por && user.value) {
        documentData.criado_por = user.value.id;
      }

      const newDocument = await withLoading(
        createDocumento(documentData),
        'Criando documento...',
        'Documento criado com sucesso'
      );
      documents.value = [...documents.value, newDocument];
      return newDocument;
    } catch (err: any) {
      error.value = err.message || 'Erro ao criar documento';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Atualizar um documento
  const updateDocument = async (documentId: number, documentData: any) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      // Verificar permissão
      if (!hasPermission('document', 'update')) {
        throw new Error('Você não tem permissão para atualizar este documento');
      }
      
      const updatedDocument = await withLoading(
        updateDocumento(documentId, documentData),
        'Atualizando documento...',
        'Documento atualizado com sucesso'
      );

      // Atualizar a lista local
      documents.value = documents.value.map((document) =>
        document.id === documentId ? updatedDocument : document
      );

      return updatedDocument;
    } catch (err: any) {
      error.value = err.message || `Erro ao atualizar documento ${documentId}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Excluir um documento
  const deleteDocument = async (documentId: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      // Verificar permissão
      if (!hasPermission('document', 'delete')) {
        throw new Error('Você não tem permissão para excluir este documento');
      }

      await withLoading(
        destroyDocumento(documentId),
        'Excluindo documento...',
        'Documento excluído com sucesso'
      );

      // Remover da lista local
      documents.value = documents.value.filter(
        (document) => document.id !== documentId
      );

      return true;
    } catch (err: any) {
      error.value = err.message || `Erro ao excluir documento ${documentId}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Baixar um documento
  const downloadDocument = async (documentId: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const url = await withLoading(
        downloadDocumento(documentId),
        'Preparando download...',
        'Download iniciado'
      );

      // Abrir o URL em uma nova aba
      if (process.client) {
        window.open(url, '_blank');
      }

      return url;
    } catch (err: any) {
      error.value = err.message || `Erro ao baixar documento ${documentId}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Obter documentos por risco
  const getDocumentosByRisco = async (riscoId: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await withLoading(
        listDocumentos({ risco: riscoId }),
        'Carregando documentos do risco...',
        'Documentos carregados com sucesso'
      );
      return response;
    } catch (err: any) {
      error.value = err.message || `Erro ao carregar documentos do risco ${riscoId}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Obter documentos por custo
  const getDocumentosByCusto = async (custoId: number) => {
    isLoading.value = true;
    error.value = null;
    
    try {
      const response = await withLoading(
        listDocumentos({ custo: custoId }),
        'Carregando documentos do custo...',
        'Documentos carregados com sucesso'
      );
      return response;
    } catch (err: any) {
      error.value = err.message || `Erro ao carregar documentos do custo ${custoId}`;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    documents,
    isLoading,
    error,
    fetchDocuments,
    getDocument,
    createDocument,
    updateDocument,
    deleteDocument,
    downloadDocument,
    getDocumentosByRisco,
    getDocumentosByCusto,
  };
};

/**
 * Listar documentos
 * @param params Parâmetros de paginação e filtro
 */
export async function listDocumentos(params?: {
  projeto?: number;
  risco?: number;
  custo?: number;
  ordering?: string;
  page?: number;
  search?: string;
}): Promise<PaginatedResponse<Documento>> {
  const queryParams = new URLSearchParams();

  if (params?.projeto) queryParams.append('projeto', params.projeto.toString());
  if (params?.risco) queryParams.append('risco', params.risco.toString());
  if (params?.custo) queryParams.append('custo', params.custo.toString());
  if (params?.ordering) queryParams.append('ordering', params.ordering);
  if (params?.page) queryParams.append('page', params.page.toString());
  if (params?.search) queryParams.append('search', params.search);

  const queryString = queryParams.toString();
  const url = `/api/documents/documentos/${queryString ? `?${queryString}` : ''}`;

  return getApi()<PaginatedResponse<Documento>>(url, {
    method: 'GET',
  });
}

/**
 * Criar um novo documento
 * @param payload Dados do documento
 */
export async function createDocumento(payload: any): Promise<Documento> {
  // Se for FormData, usar como está
  if (payload instanceof FormData) {
    return getApi()<Documento>('/api/documents/documentos/', {
      method: 'POST',
      body: payload,
      formData: true
    });
  }
  
  // Se for objeto comum, converter para JSON
  return getApi()<Documento>('/api/documents/documentos/', {
    method: 'POST',
    body: payload,
  });
}

/**
 * Obter detalhes de um documento
 * @param id ID do documento
 */
export async function retrieveDocumento(id: number): Promise<Documento> {
  return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
    method: 'GET',
  });
}

/**
 * Atualizar um documento
 * @param id ID do documento
 * @param payload Dados do documento
 */
export async function updateDocumento(id: number, payload: any): Promise<Documento> {
  // Se for FormData, usar como está
  if (payload instanceof FormData) {
    return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
      method: 'PUT',
      body: payload,
      formData: true
    });
  }
  
  // Se for objeto comum, converter para JSON
  return getApi()<Documento>(`/api/documents/documentos/${id}/`, {
    method: 'PUT',
    body: payload,
  });
}

/**
 * Excluir um documento
 * @param id ID do documento
 */
export async function destroyDocumento(id: number): Promise<void> {
  return getApi()<void>(`/api/documents/documentos/${id}/`, {
    method: 'DELETE',
  });
}

/**
 * Baixar um documento
 * @param id ID do documento
 */
export async function downloadDocumento(id: number): Promise<string> {
  return getApi()<string>(`/api/documents/documentos/${id}/download/`, {
    method: 'GET',
  });
}
