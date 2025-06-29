// Service para gerenciar documentos usando a API Fetch do Nuxt
export const useDocumentService = () => {
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // Buscar documentos com filtros
  const getDocuments = async (filters: any = {}) => {
    try {
      return await $fetch(`${apiBase}documents/`, {
        params: filters,
      });
    } catch (error) {
      console.error("Erro ao buscar documentos:", error);
      throw error;
    }
  };

  // Buscar documento específico
  const getDocumentById = async (id: number) => {
    try {
      return await $fetch(`${apiBase}documents/${id}/`);
    } catch (error) {
      console.error("Erro ao buscar documento:", error);
      throw error;
    }
  };

  // Criar novo documento
  const createDocument = async (documentData: any) => {
    try {
      return await $fetch(`${apiBase}documents/`, {
        method: "POST",
        body: documentData,
      });
    } catch (error) {
      console.error("Erro ao criar documento:", error);
      throw error;
    }
  };

  // Atualizar documento
  const updateDocument = async (id: number, documentData: any) => {
    try {
      return await $fetch(`${apiBase}documents/${id}/`, {
        method: "PUT",
        body: documentData,
      });
    } catch (error) {
      console.error("Erro ao atualizar documento:", error);
      throw error;
    }
  };

  // Atualizar parcialmente documento
  const partialUpdateDocument = async (id: number, documentData: any) => {
    try {
      return await $fetch(`${apiBase}documents/${id}/`, {
        method: "PATCH",
        body: documentData,
      });
    } catch (error) {
      console.error("Erro ao atualizar documento:", error);
      throw error;
    }
  };

  // Deletar documento
  const deleteDocument = async (id: number) => {
    try {
      return await $fetch(`${apiBase}documents/${id}/`, {
        method: "DELETE",
      });
    } catch (error) {
      console.error("Erro ao deletar documento:", error);
      throw error;
    }
  };

  // Upload de arquivo
  const uploadDocument = async (file: File, documentData: any) => {
    try {
      const formData = new FormData();
      formData.append("arquivo", file);

      // Adicionar outros campos do documento
      Object.keys(documentData).forEach((key) => {
        formData.append(key, documentData[key]);
      });

      return await $fetch(`${apiBase}documents/`, {
        method: "POST",
        body: formData,
      });
    } catch (error) {
      console.error("Erro ao fazer upload do documento:", error);
      throw error;
    }
  };

  // Download de documento
  const downloadDocument = async (id: number) => {
    try {
      return await $fetch(`${apiBase}documents/${id}/download/`, {
        method: "GET",
      });
    } catch (error) {
      console.error("Erro ao fazer download do documento:", error);
      throw error;
    }
  };

  // Buscar documentos por projeto
  const getDocumentsByProject = async (
    projectId: number,
    filters: any = {}
  ) => {
    try {
      return await $fetch(`${apiBase}documents/`, {
        params: { projeto: projectId, ...filters },
      });
    } catch (error) {
      console.error("Erro ao buscar documentos por projeto:", error);
      throw error;
    }
  };

  return {
    getDocuments,
    getDocumentById,
    createDocument,
    updateDocument,
    partialUpdateDocument,
    deleteDocument,
    uploadDocument,
    downloadDocument,
    getDocumentsByProject,
  };
};
