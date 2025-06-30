import { useApiClient } from '~/composables/useApiClient';

export const useDocumentService = () => {
  const apiClient = useApiClient();

  /**
   * Obtém a lista de documentos de um projeto
   * @param projectId ID do projeto
   * @param params Parâmetros de paginação e filtros
   */
  const getProjectDocuments = async (projectId: number, params = {}) => {
    const response = await apiClient.get(`documents/`, { 
      params: { 
        projeto_id: projectId,
        ...params 
      } 
    });
    return response.data;
  };

  /**
   * Obtém um documento específico pelo ID
   * @param id ID do documento
   */
  const getDocument = async (id: number) => {
    const response = await apiClient.get(`documents/${id}/`);
    return response.data;
  };

  /**
   * Cria um novo documento
   * @param data Dados do documento
   */
  const createDocument = async (data: any) => {
    // Criar um FormData para envio de arquivos
    const formData = new FormData();
    
    // Adicionar os campos ao FormData
    Object.keys(data).forEach(key => {
      if (key === 'arquivo') {
        formData.append('arquivo', data[key]);
      } else {
        formData.append(key, data[key]);
      }
    });
    
    const response = await apiClient.post('documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  };

  /**
   * Atualiza um documento existente
   * @param id ID do documento
   * @param data Dados do documento
   */
  const updateDocument = async (id: number, data: any) => {
    // Criar um FormData para envio de arquivos
    const formData = new FormData();
    
    // Adicionar os campos ao FormData
    Object.keys(data).forEach(key => {
      if (key === 'arquivo' && data[key]) {
        formData.append('arquivo', data[key]);
      } else if (data[key] !== undefined) {
        formData.append(key, data[key]);
      }
    });
    
    const response = await apiClient.patch(`documents/${id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  };

  /**
   * Exclui um documento
   * @param id ID do documento
   */
  const deleteDocument = async (id: number) => {
    const response = await apiClient.delete(`documents/${id}/`);
    return response.data;
  };

  /**
   * Obtém o histórico de um documento
   * @param documentId ID do documento
   * @param params Parâmetros de paginação e filtros
   */
  const getDocumentHistory = async (documentId: number, params = {}) => {
    const response = await apiClient.get(`documents/${documentId}/history/`, { params });
    return response.data;
  };

  return {
    getProjectDocuments,
    getDocument,
    createDocument,
    updateDocument,
    deleteDocument,
    getDocumentHistory
  };
};
