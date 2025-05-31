/**
 * Serviço de documentos - adaptador para o novo sistema de API
 */
import { ref } from 'vue'
import * as documentsApi from '~/services/api/documents'
import { useApiService } from '~/composables/useApiService'
import { useAuth } from '~/composables/useAuth'

export const useDocumentService = () => {
  const { user, hasPermission } = useAuth()
  const { handleApiError, withLoading } = useApiService()
  
  const documents = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Carregar todos os documentos
  const fetchDocuments = async (projectId = null) => {
    isLoading.value = true
    error.value = null
    
    try {
      if (projectId) {
        documents.value = await documentsApi.listDocumentsByProject(projectId)
      } else {
        documents.value = await documentsApi.listDocuments()
      }
      return documents.value
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Obter um documento pelo ID
  const getDocument = async (documentId) => {
    isLoading.value = true
    error.value = null
    
    try {
      const document = await documentsApi.retrieveDocument(documentId)
      return document
    } catch (err) {
      error.value = handleApiError(err)
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Criar um novo documento
  const createDocument = async (documentData) => {
    return withLoading(async () => {
      try {
        // Se documentData não for FormData, associar automaticamente o usuário atual como criador
        if (!(documentData instanceof FormData) && !documentData.created_by) {
          documentData.created_by = user.value?.id
        }
        
        const newDocument = await documentsApi.createDocument(documentData)
        documents.value = [...documents.value, newDocument]
        return newDocument
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Atualizar um documento
  const updateDocument = async (documentId, documentData) => {
    return withLoading(async () => {
      try {
        const updatedDocument = await documentsApi.updateDocument(documentId, documentData)
        
        // Atualizar a lista local
        documents.value = documents.value.map(document => 
          document.id === documentId ? updatedDocument : document
        )
        
        return updatedDocument
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Excluir um documento
  const deleteDocument = async (documentId) => {
    return withLoading(async () => {
      try {
        // Verificar permissão
        if (!hasPermission('document', 'delete')) {
          throw new Error('Você não tem permissão para excluir este documento')
        }
        
        await documentsApi.destroyDocument(documentId)
        
        // Remover da lista local
        documents.value = documents.value.filter(document => document.id !== documentId)
        
        return true
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  // Baixar um documento
  const downloadDocument = async (documentId) => {
    return withLoading(async () => {
      try {
        const url = await documentsApi.getDocumentDownloadUrl(documentId)
        
        // Abrir o URL em uma nova aba
        if (process.client) {
          window.open(url, '_blank')
        }
        
        return url
      } catch (err) {
        error.value = handleApiError(err)
        throw err
      }
    })
  }
  
  return {
    documents,
    isLoading,
    error,
    fetchDocuments,
    getDocument,
    createDocument,
    updateDocument,
    deleteDocument,
    downloadDocument
  }
}
