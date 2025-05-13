import { useApiService } from './api'

export interface Document {
  id?: number
  title: string
  description: string
  project: number
  file: File | string
  category: string
  version: string
  status: string
  owner?: number
  created_at?: string
  updated_at?: string
}

export const useDocumentService = () => {
  const api = useApiService()
  const endpoint = '/api/documents/'

  // Listar todos os documentos
  const getAll = async (params = {}) => {
    try {
      const response = await api.get(endpoint, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter um documento específico
  const getById = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Criar um novo documento
  const create = async (document: Document) => {
    try {
      // Usamos FormData para enviar arquivos
      const formData = new FormData()
      Object.keys(document).forEach(key => {
        if (key === 'file' && document.file instanceof File) {
          formData.append(key, document.file)
        } else {
          formData.append(key, document[key])
        }
      })
      
      const response = await api.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar um documento existente
  const update = async (id: number, document: Document) => {
    try {
      // Usamos FormData para enviar arquivos
      const formData = new FormData()
      Object.keys(document).forEach(key => {
        if (key === 'file' && document.file instanceof File) {
          formData.append(key, document.file)
        } else {
          formData.append(key, document[key])
        }
      })
      
      const response = await api.put(`${endpoint}${id}/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Atualizar parcialmente um documento
  const patch = async (id: number, partialDocument: Partial<Document>) => {
    try {
      // Usamos FormData para enviar arquivos
      if (partialDocument.file && partialDocument.file instanceof File) {
        const formData = new FormData()
        Object.keys(partialDocument).forEach(key => {
          if (key === 'file') {
            formData.append(key, partialDocument.file)
          } else {
            formData.append(key, partialDocument[key])
          }
        })
        
        const response = await api.patch(`${endpoint}${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data
      } else {
        const response = await api.patch(`${endpoint}${id}/`, partialDocument)
        return response.data
      }
    } catch (error) {
      throw error
    }
  }

  // Excluir um documento
  const remove = async (id: number) => {
    try {
      await api.delete(`${endpoint}${id}/`)
      return true
    } catch (error) {
      throw error
    }
  }

  // Aprovar um documento
  const approve = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { status: 'APROVADO' })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Rejeitar um documento
  const reject = async (id: number) => {
    try {
      const response = await api.patch(`${endpoint}${id}/`, { status: 'REJEITADO' })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Obter documentos por projeto
  const getByProject = async (projectId: number) => {
    try {
      const response = await api.get(`${endpoint}`, { 
        params: { project: projectId } 
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Download do arquivo
  const downloadFile = async (id: number) => {
    try {
      const response = await api.get(`${endpoint}${id}/download/`, {
        responseType: 'blob'
      })
      
      // Criar URL para o blob e iniciar download
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', response.headers['content-disposition']?.split('filename=')[1] || `document-${id}`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      return true
    } catch (error) {
      throw error
    }
  }

  return {
    getAll,
    getById,
    create,
    update,
    patch,
    remove,
    approve,
    reject,
    getByProject,
    downloadFile
  }
}
