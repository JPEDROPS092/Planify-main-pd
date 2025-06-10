/**
 * Serviço de documentos
 * Implementação completa com suporte para feedback visual e associação automática com usuário logado
 */
import { ref } from 'vue';
import { useApiService } from '~/stores/composables/useApiService';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/stores/composables/useNotification';
import { ApiError } from '../services/api/client/config';
import { apiClient } from './apiClient';

// Definição dos tipos de documento
interface Documento {
  id: number;
  nome: string;
  arquivo: string;
  projeto?: number;
  risco?: number;
  custo?: number;
  criado_por?: number;
  criado_em: string;
  atualizado_em: string;
}

// Interfaces para criação e atualização de documentos
interface DocumentoCreateDTO {
  nome: string;
  arquivo: File | string;
  projeto?: number;
  risco?: number;
  custo?: number;
  criado_por?: number;
}

interface DocumentoUpdateDTO {
  nome?: string;
  arquivo?: File | string;
  projeto?: number;
  risco?: number;
  custo?: number;
}

// Interface para parâmetros de consulta
interface DocumentoQueryParams {
  projeto?: number;
  risco?: number;
  custo?: number;
  ordering?: string;
  page?: number;
  search?: string;
}

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Função para obter a instância do cliente fetch apenas quando necessário
const getApi = () => {
  return apiClient;
};

// Utilitário para processar erros da API
const parseApiError = (error: any, defaultMessage: string): string => {
  if (error instanceof ApiError) {
    return error.friendlyMessage;
  }
  return error.message || defaultMessage;
};

// Utilitário para processar payloads com FormData
const processPayload = <T>(payload: T, path: string, method: 'post' | 'put', id?: number): Promise<Documento> => {
  const url = id ? `${path}/${id}/` : `${path}/`;

  // Se for FormData, usar como está
  if (payload instanceof FormData) {
    return getApi()[method]<Documento>(url, payload, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => response.data);
  }

  // Se for objeto comum, enviar como JSON
  return getApi()[method]<Documento>(url, payload)
    .then(response => response.data);
};

// Composable para envolver operações com feedback de carregamento
const withLoading = (promise: Promise<any>, loadingMessage: string, successMessage?: string) => {
  const notification = useNotification();
  const notificationId = notification.notify('loading', loadingMessage);

  return promise
    .then(result => {
      if (successMessage) {
        notification.notify('success', successMessage);
      } else {
        notification.remove(notificationId);
      }
      return result;
    })
    .catch(error => {
      notification.notify('error', parseApiError(error, 'Ocorreu um erro'));
      throw error;
    });
};

export const useDocumentService = () => {
  const { user, hasPermission } = useAuth();
  const { handleApiError } = useApiService();

  const documents = ref<Documento[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  // Carregar todos os documentos
  const fetchDocuments = async (projectId?: number | null) => {
    isLoading.value = true;
    error.value = null;

    try {
      const params: DocumentoQueryParams = {};
      if (projectId) {
        params.projeto = projectId;
      }

      const response = await withLoading(
        listDocumentos(params),
        projectId ? 'Carregando documentos do projeto...' : 'Carregando documentos...',
        'Documentos carregados com sucesso'
      );

      documents.value = response.results;
      return documents.value;
    } catch (err: any) {
      error.value = parseApiError(err, 'Erro ao carregar documentos');
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
      error.value = parseApiError(err, `Erro ao carregar documento ${documentId}`);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Criar um novo documento
  const createDocument = async (documentData: DocumentoCreateDTO | FormData) => {
    isLoading.value = true;
    error.value = null;

    try {
      // Se documentData não for FormData, associar automaticamente o usuário atual como criador
      if (!(documentData instanceof FormData) && !documentData.criado_por && user.value?.id) {
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
      error.value = parseApiError(err, 'Erro ao criar documento');
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Atualizar um documento
  const updateDocument = async (documentId: number, documentData: DocumentoUpdateDTO | FormData) => {
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
      error.value = parseApiError(err, `Erro ao atualizar documento ${documentId}`);
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
      error.value = parseApiError(err, `Erro ao excluir documento ${documentId}`);
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
      error.value = parseApiError(err, `Erro ao baixar documento ${documentId}`);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Obter documentos por risco ou custo usando uma função comum
  const getDocumentosByFilter = async (
    filterType: 'risco' | 'custo',
    filterId: number,
    loadingMessage: string,
    errorMessage: string
  ) => {
    isLoading.value = true;
    error.value = null;

    try {
      const params: DocumentoQueryParams = {};
      params[filterType] = filterId;

      const response = await withLoading(
        listDocumentos(params),
        loadingMessage,
        'Documentos carregados com sucesso'
      );
      return response;
    } catch (err: any) {
      error.value = parseApiError(err, errorMessage);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  // Obter documentos por risco
  const getDocumentosByRisco = async (riscoId: number) => {
    return getDocumentosByFilter(
      'risco',
      riscoId,
      'Carregando documentos do risco...',
      `Erro ao carregar documentos do risco ${riscoId}`
    );
  };

  // Obter documentos por custo
  const getDocumentosByCusto = async (custoId: number) => {
    return getDocumentosByFilter(
      'custo',
      custoId,
      'Carregando documentos do custo...',
      `Erro ao carregar documentos do custo ${custoId}`
    );
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
export async function listDocumentos(params: DocumentoQueryParams = {}): Promise<PaginatedResponse<Documento>> {
  const queryParams = new URLSearchParams();

  if (params.projeto) queryParams.append('projeto', params.projeto.toString());
  if (params.risco) queryParams.append('risco', params.risco.toString());
  if (params.custo) queryParams.append('custo', params.custo.toString());
  if (params.ordering) queryParams.append('ordering', params.ordering);
  if (params.page) queryParams.append('page', params.page.toString());
  if (params.search) queryParams.append('search', params.search);

  const queryString = queryParams.toString();
  const url = `/api/documents/documentos/${queryString ? `?${queryString}` : ''}`;

  return getApi().get<PaginatedResponse<Documento>>(url)
    .then(response => response.data);
}

/**
 * Criar um novo documento
 * @param payload Dados do documento
 */
export async function createDocumento(payload: DocumentoCreateDTO | FormData): Promise<Documento> {
  return processPayload(payload, '/api/documents/documentos', 'post');
}

/**
 * Obter detalhes de um documento
 * @param id ID do documento
 */
export async function retrieveDocumento(id: number): Promise<Documento> {
  return getApi().get<Documento>(`/api/documents/documentos/${id}/`)
    .then(response => response.data);
}

/**
 * Atualizar um documento
 * @param id ID do documento
 * @param payload Dados do documento
 */
export async function updateDocumento(id: number, payload: DocumentoUpdateDTO | FormData): Promise<Documento> {
  return processPayload(payload, '/api/documents/documentos', 'put', id);
}

/**
 * Excluir um documento
 * @param id ID do documento
 */
export async function destroyDocumento(id: number): Promise<void> {
  return getApi().delete(`/api/documents/documentos/${id}/`)
    .then(() => undefined);
}

/**
 * Baixar um documento
 * @param id ID do documento
 */
export async function downloadDocumento(id: number): Promise<string> {
  return getApi().get<{ url: string }>(`/api/documents/documentos/${id}/download/`)
    .then(response => response.data.url);
}
