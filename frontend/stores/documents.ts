// frontend/stores/documents.ts
import { defineStore } from 'pinia';
import { ref } from 'vue';
// Ex: import type { Documento } from '~/services/utils/types';

export const useDocumentsStore = defineStore('documents', () => {
  // State
  const documents = ref<any[]>([]); // Substituir 'any' pelo tipo Documento[]
  const currentDocument = ref<any | null>(null); // Substituir 'any' pelo tipo Documento | null
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Actions
  async function fetchDocumentsForProject(projectId: number | string) {
    isLoading.value = true;
    error.value = null;
    try {
      // TODO: Chamar API para buscar documentos de um projeto
      console.warn(`fetchDocumentsForProject(${projectId}): Mock implementation.`);
      // documents.value = [{ id: 1, titulo: 'Documento Mock 1', projeto: projectId }];
    } catch (e:any) {
      error.value = e.message || `Falha ao buscar documentos para o projeto ${projectId}.`;
    } finally {
      isLoading.value = false;
    }
  }
  
  // TODO: Adicionar actions para CRUD e versionamento

  return {
    documents,
    currentDocument,
    isLoading,
    error,
    fetchDocumentsForProject,
  };
});
