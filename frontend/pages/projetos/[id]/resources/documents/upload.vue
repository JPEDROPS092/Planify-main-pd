<template>
  <div class="document-upload-container">
    <h1 class="text-2xl font-bold mb-4">Upload de Documentos</h1>
    <div class="card bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div class="file-uploader">
        <div class="upload-area" 
             :class="{ 'drag-active': isDragging }" 
             @dragover.prevent="isDragging = true" 
             @dragleave.prevent="isDragging = false" 
             @drop.prevent="onFileDrop">
          <div class="upload-icon">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p class="text-center text-gray-600 dark:text-gray-300 mt-4">
            Arraste e solte arquivos aqui ou
          </p>
          <button 
            class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            @click="triggerFileInput">
            Selecionar Arquivos
          </button>
          <input 
            type="file" 
            ref="fileInput" 
            multiple 
            class="hidden" 
            @change="onFileSelect" />
        </div>
        
        <div v-if="selectedFiles.length > 0" class="mt-6">
          <h3 class="text-lg font-semibold mb-3">Arquivos Selecionados</h3>
          <ul class="space-y-2">
            <li v-for="(file, index) in selectedFiles" :key="index" class="flex items-center justify-between p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="text-sm">{{ file.name }}</span>
              </div>
              <button 
                @click="removeFile(index)" 
                class="text-red-500 hover:text-red-700">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </li>
          </ul>
          
          <div class="mt-6">
            <button 
              :disabled="isUploading" 
              @click="uploadFiles" 
              class="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed">
              <span v-if="isUploading">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Enviando...
              </span>
              <span v-else>Enviar Arquivos</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProjectService } from '@/composables/useProjectService';
import { useNotification } from '~/composables/useNotification';
import { useDocumentService } from '@/composables/useDocumentService';

export default defineComponent({
  name: 'DocumentUploadPage',
  middleware: 'auth',
  layout: 'dashboard',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const projectId = String(route.params.id);
    const { getProject } = useProjectService();
    const { uploadDocumento } = useDocumentService();
    const { showSuccess, showError } = useNotification();
    
    const fileInput = ref<HTMLInputElement | null>(null);
    const selectedFiles = ref<File[]>([]);
    const isDragging = ref(false);
    const isUploading = ref(false);

    // Validar que o projeto existe
    getProject(projectId).catch(error => {
      showError('Erro ao carregar projeto', error.message || 'Não foi possível carregar os dados do projeto');
    });

    const triggerFileInput = () => {
      fileInput.value?.click();
    };

    const onFileSelect = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files) {
        for (let i = 0; i < input.files.length; i++) {
          selectedFiles.value.push(input.files[i]);
        }
      }
    };

    const onFileDrop = (event: DragEvent) => {
      isDragging.value = false;
      if (event.dataTransfer?.files) {
        for (let i = 0; i < event.dataTransfer.files.length; i++) {
          selectedFiles.value.push(event.dataTransfer.files[i]);
        }
      }
    };

    const removeFile = (index: number) => {
      selectedFiles.value.splice(index, 1);
    };

    const uploadFiles = async () => {
      if (selectedFiles.value.length === 0) {
        showError('Erro', 'Nenhum arquivo selecionado para upload');
        return;
      }

      isUploading.value = true;
      
      try {
        const uploadPromises = selectedFiles.value.map(file => {
          const formData = new FormData();
          formData.append('arquivo', file);
          formData.append('projeto_id', projectId);
          formData.append('nome', file.name);
          formData.append('tipo', file.type);
          
          return uploadDocumento(formData);
        });
        
        await Promise.all(uploadPromises);
        
        showSuccess('Sucesso', 'Arquivos enviados com sucesso');
        selectedFiles.value = [];
        
        // Redirecionar para a página de documentos
        router.push(`/projetos/${projectId}/resources/documents`);
      } catch (error: any) {
        showError('Erro no upload', error.message || 'Não foi possível enviar os arquivos');
      } finally {
        isUploading.value = false;
      }
    };

    return {
      projectId,
      fileInput,
      selectedFiles,
      isDragging,
      isUploading,
      triggerFileInput,
      onFileSelect,
      onFileDrop,
      removeFile,
      uploadFiles
    };
  }
});
</script>

<style scoped>
.document-upload-container {
  padding: 1rem;
}

.upload-area {
  border: 2px dashed #cbd5e0;
  border-radius: 0.5rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.2s ease;
}

.upload-area.drag-active {
  border-color: #4299e1;
  background-color: rgba(66, 153, 225, 0.1);
}

.upload-icon {
  margin: 0 auto;
  width: 3rem;
}
</style>
