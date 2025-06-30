<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Documentos</h1>
      <button 
        @click="showUploadModal = true"
        class="bg-primary hover:bg-primary-700 text-white px-4 py-2 rounded-md flex items-center shadow-sm"
      >
        <Icon icon="lucide:upload" class="mr-2 h-4 w-4" />
        Upload de Documento
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-10">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="mt-2 text-gray-600">Carregando documentos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 text-center">
      <Icon icon="lucide:alert-triangle" class="w-10 h-10 mx-auto text-red-500" />
      <p class="mt-2 font-semibold text-red-700">Erro ao carregar documentos</p>
      <p class="text-sm text-red-600">{{ error.message }}</p>
      <button @click="refetch()" class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700">Tentar Novamente</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!documents || documents.results.length === 0" class="text-center py-10 border-2 border-dashed rounded-lg">
      <Icon icon="lucide:file-text" class="w-16 h-16 mx-auto text-gray-400" />
      <h3 class="mt-2 text-xl font-medium text-gray-800">Nenhum documento encontrado</h3>
      <p class="mt-1 text-gray-500">Faça o upload do seu primeiro documento para começar.</p>
      <button @click="showUploadModal = true" class="mt-4 bg-primary hover:bg-primary-700 text-white px-4 py-2 rounded-md"> 
        <Icon icon="lucide:upload" class="mr-2 h-4 w-4 inline-block" />
        Upload de Documento
      </button>
    </div>

    <!-- Documents List -->
    <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul role="list" class="divide-y divide-gray-200">
        <li v-for="doc in documents.results" :key="doc.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <Icon :icon="getFileIcon(doc.tipo_arquivo)" class="h-10 w-10 text-gray-500" />
              <div class="ml-4">
                <p class="text-sm font-medium text-primary truncate">{{ doc.titulo }}</p>
                <p class="text-sm text-gray-500">{{ doc.descricao || 'Sem descrição' }}</p>
                <p class="text-xs text-gray-400">Projeto: {{ doc.projeto_titulo || 'N/A' }}</p>
              </div>
            </div>
            <div class="ml-2 flex-shrink-0 flex items-center space-x-4">
              <p class="text-sm text-gray-500">{{ formatBytes(doc.tamanho_arquivo) }}</p>
              <a :href="doc.arquivo" target="_blank" class="text-primary hover:text-primary-700">
                <Icon icon="lucide:download" class="h-5 w-5" />
              </a>
              <button @click="confirmDelete(doc.id)" class="text-red-500 hover:text-red-700">
                <Icon icon="lucide:trash-2" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Pagination -->
    <div v-if="documents && documents.total_pages > 1" class="mt-6 flex justify-center">
       <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
        <button @click="prevPage" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Anterior
        </button>
        <span class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
          Página {{ currentPage }} de {{ documents.total_pages }}
        </span>
        <button @click="nextPage" :disabled="currentPage === documents.total_pages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Próximo
        </button>
      </nav>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75" @click="closeModal"></div>
        <div class="bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full">
          <form @submit.prevent="handleUpload">
            <div class="px-4 pt-5 pb-4 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Upload de Novo Documento</h3>
              <div class="mt-4 space-y-4">
                <div>
                  <label for="title" class="block text-sm font-medium text-gray-700">Título</label>
                  <input type="text" v-model="newDocument.titulo" id="title" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500" required />
                </div>
                <div>
                  <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
                  <textarea v-model="newDocument.descricao" id="description" rows="3" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"></textarea>
                </div>
                <div>
                  <label for="project" class="block text-sm font-medium text-gray-700">Projeto</label>
                   <select v-model="newDocument.projeto" id="project" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                    <option disabled value="">Selecione um projeto</option>
                    <option v-for="project in projectsList?.results" :key="project.id" :value="project.id">{{ project.titulo }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Arquivo</label>
                  <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                    <div class="space-y-1 text-center">
                      <Icon icon="lucide:file-up" class="mx-auto h-12 w-12 text-gray-400" />
                      <div class="flex text-sm text-gray-600">
                        <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-primary hover:text-primary-500 focus-within:outline-none">
                          <span>Selecione um arquivo</span>
                          <input id="file-upload" name="file-upload" type="file" class="sr-only" @change="onFileChange" required />
                        </label>
                        <p class="pl-1">ou arraste e solte</p>
                      </div>
                      <p v-if="selectedFile" class="text-sm text-gray-500">{{ selectedFile.name }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button type="submit" :disabled="uploadMutation.isLoading.value" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50">
                <Icon v-if="uploadMutation.isLoading.value" icon="svg-spinners:180-ring-with-bg" class="mr-2 h-5 w-5" />
                Upload
              </button>
              <button type="button" @click="closeModal" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { ref, watch } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useDocumentService } from '~/services/documentService';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { Documento, PaginatedDocumentoList, PaginatedProjetoList } from '~/api-types';

const queryClient = useQueryClient();
const documentService = useDocumentService();
const projectService = useProjectService();
const { toast } = useToast();

const currentPage = ref(1);
const showUploadModal = ref(false);
const selectedFile = ref<File | null>(null);
const newDocument = ref({
  titulo: '',
  descricao: '',
  projeto: null as number | null,
});

// Fetch documents
const { data: documents, isLoading, error, refetch } = useQuery<PaginatedDocumentoList>({
  queryKey: ['documents', currentPage],
  queryFn: () => documentService.getDocuments(currentPage.value),
});

// Fetch projects for the select input
const { data: projectsList } = useQuery<PaginatedProjetoList>({
    queryKey: ['projectsList'],
    queryFn: () => projectService.getProjects(1, 100) // Fetch up to 100 projects
});

// Upload mutation
const uploadMutation = useMutation({
  mutationFn: (formData: FormData) => documentService.uploadDocument(formData),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Documento enviado com sucesso!' });
    queryClient.invalidateQueries({ queryKey: ['documents'] });
    closeModal();
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: err.message || 'Falha no upload do documento.', variant: 'destructive' });
  },
});

// Delete mutation
const deleteMutation = useMutation({
  mutationFn: (id: number) => documentService.deleteDocument(id),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Documento excluído com sucesso!' });
    queryClient.invalidateQueries({ queryKey: ['documents'] });
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: err.message || 'Falha ao excluir o documento.', variant: 'destructive' });
  },
});

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0];
  }
};

const handleUpload = () => {
  if (!selectedFile.value || !newDocument.value.projeto) {
    toast({ title: 'Erro', description: 'Por favor, preencha todos os campos obrigatórios.', variant: 'destructive' });
    return;
  }
  const formData = new FormData();
  formData.append('titulo', newDocument.value.titulo);
  formData.append('descricao', newDocument.value.descricao);
  formData.append('projeto', newDocument.value.projeto.toString());
  formData.append('arquivo', selectedFile.value);

  uploadMutation.mutate(formData);
};

const confirmDelete = (id: number) => {
  if (window.confirm('Tem certeza que deseja excluir este documento?')) {
    deleteMutation.mutate(id);
  }
};

const closeModal = () => {
  showUploadModal.value = false;
  newDocument.value = { titulo: '', descricao: '', projeto: null };
  selectedFile.value = null;
};

const nextPage = () => {
  if (documents.value && currentPage.value < documents.value.total_pages) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const formatBytes = (bytes: number, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

const getFileIcon = (fileType: string | undefined) => {
  if (!fileType) return 'lucide:file';
  if (fileType.includes('pdf')) return 'lucide:file-type-pdf';
  if (fileType.includes('image')) return 'lucide:file-image';
  if (fileType.includes('word')) return 'lucide:file-type-word';
  if (fileType.includes('excel') || fileType.includes('spreadsheet')) return 'lucide:file-type-excel';
  return 'lucide:file-text';
};

watch(currentPage, () => {
  refetch();
});

</script>