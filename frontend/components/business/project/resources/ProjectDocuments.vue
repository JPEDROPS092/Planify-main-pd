<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Documentos do Projeto
      </h3>
      <button
        v-if="canAddDocument"
        @click="showAddDocumentModal = true"
        class="px-3 py-1.5 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:bg-primary-700 dark:hover:bg-primary-600 flex items-center"
      >
        <svg
          class="w-4 h-4 mr-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          ></path>
        </svg>
        Adicionar Documento
      </button>
    </div>

    <div v-if="isLoading" class="py-8">
      <SkeletonLoader :count="3" height="60px" class="mb-3" />
    </div>

    <div v-else-if="documents.length === 0" class="py-8 text-center">
      <svg
        class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
        ></path>
      </svg>
      <p class="mt-2 text-gray-500 dark:text-gray-400">
        Nenhum documento adicionado a este projeto
      </p>
      <button
        v-if="canAddDocument"
        @click="showAddDocumentModal = true"
        class="mt-4 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:bg-primary-700 dark:hover:bg-primary-600"
      >
        Adicionar Primeiro Documento
      </button>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="document in documents"
        :key="document.id"
        class="p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 flex justify-between items-center"
      >
        <div class="flex items-center space-x-3">
          <div class="p-2 bg-gray-100 dark:bg-gray-700 rounded-md">
            <svg
              class="w-6 h-6 text-gray-600 dark:text-gray-300"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              ></path>
            </svg>
          </div>
          <div>
            <h4 class="font-medium text-gray-800 dark:text-gray-200">
              {{ document.title }}
            </h4>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Adicionado por {{ document.created_by?.name || 'Usuário' }} em
              {{ formatDate(document.created_at) }}
            </p>
          </div>
        </div>

        <div class="flex space-x-2">
          <a
            :href="document.file_url"
            target="_blank"
            class="p-1.5 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
            title="Baixar"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              ></path>
            </svg>
          </a>
          <button
            v-if="canDeleteDocument"
            @click="confirmDeleteDocument(document)"
            class="p-1.5 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
            title="Excluir"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              ></path>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal para adicionar documento -->
    <Modal v-model="showAddDocumentModal" title="Adicionar Documento" size="md">
      <form @submit.prevent="uploadDocument" class="space-y-4">
        <div>
          <label
            for="title"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >Título</label
          >
          <input
            id="title"
            v-model="newDocument.title"
            type="text"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
            placeholder="Título do documento"
            required
          />
        </div>

        <div>
          <label
            for="description"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >Descrição</label
          >
          <textarea
            id="description"
            v-model="newDocument.description"
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
            placeholder="Descrição do documento"
          ></textarea>
        </div>

        <div>
          <label
            for="file"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >Arquivo</label
          >
          <input
            id="file"
            ref="fileInput"
            type="file"
            class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100 dark:text-gray-400 dark:file:bg-primary-900 dark:file:text-primary-300"
            required
          />
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600"
            @click="showAddDocumentModal = false"
          >
            Cancelar
          </button>
          <button
            type="submit"
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:bg-primary-700 dark:hover:bg-primary-600"
            :disabled="isUploading"
          >
            <span v-if="isUploading" class="flex items-center">
              <svg
                class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              Enviando...
            </span>
            <span v-else>Enviar Documento</span>
          </button>
        </div>
      </form>
    </Modal>

    <!-- Modal de confirmação para excluir documento -->
    <Modal v-model="showDeleteModal" title="Excluir Documento" size="sm">
      <p class="text-gray-700 dark:text-gray-300">
        Tem certeza que deseja excluir o documento "{{
          documentToDelete?.title
        }}"? Esta ação não pode ser desfeita.
      </p>

      <template #footer>
        <button
          type="button"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-600"
          @click="showDeleteModal = false"
        >
          Cancelar
        </button>
        <button
          type="button"
          class="ml-3 px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 dark:bg-red-700 dark:hover:bg-red-600"
          :disabled="isDeleting"
          @click="deleteDocument"
        >
          <span v-if="isDeleting" class="flex items-center">
            <svg
              class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Excluindo...
          </span>
          <span v-else>Excluir</span>
        </button>
      </template>
    </Modal>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch, toRefs, computed } from 'vue';
import { useDocumentService } from '~/services/api/documentService';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/composables/useNotification';
import SkeletonLoader from '~/components/SkeletonLoader.vue';
import Modal from '~/components/ui/Modal.vue';

export default defineComponent({
  name: 'ProjectDocuments',

  components: {
    SkeletonLoader,
    Modal,
  },

  props: {
    projectId: {
      type: [Number, String],
      required: true,
    },
  },

  setup(props) {
    const { projectId } = toRefs(props);
    const documentService = useDocumentService();
    const { user, hasPermission } = useAuth();
    const notification = useNotification();

    const documents = ref([]);
    const isLoading = ref(false);
    const isUploading = ref(false);
    const isDeleting = ref(false);
    const showAddDocumentModal = ref(false);
    const showDeleteModal = ref(false);
    const documentToDelete = ref(null);
    const fileInput = ref(null);

    const newDocument = ref({
      title: '',
      description: '',
      project: projectId,
    });

    // Verificar permissões
    const canAddDocument = computed(() => {
      return hasPermission('document', 'create');
    });

    const canDeleteDocument = computed(() => {
      return hasPermission('document', 'delete');
    });

    // Carregar documentos do projeto
    const loadDocuments = async () => {
      isLoading.value = true;

      try {
        documents.value = await documentService.fetchDocuments(projectId.value);
      } catch (error) {
        notification.error('Erro ao carregar documentos');
        console.error('Erro ao carregar documentos:', error);
      } finally {
        isLoading.value = false;
      }
    };

    // Enviar novo documento
    const uploadDocument = async () => {
      if (!fileInput.value.files || fileInput.value.files.length === 0) {
        notification.error('Selecione um arquivo para enviar');
        return;
      }

      isUploading.value = true;

      try {
        const formData = new FormData();
        formData.append('title', newDocument.value.title);
        formData.append('description', newDocument.value.description || '');
        formData.append('project', projectId.value);
        formData.append('file', fileInput.value.files[0]);

        await documentService.createDocument(formData);

        notification.success('Documento enviado com sucesso');
        showAddDocumentModal.value = false;

        // Limpar formulário
        newDocument.value = {
          title: '',
          description: '',
          project: projectId.value,
        };

        // Recarregar documentos
        loadDocuments();
      } catch (error) {
        notification.error('Erro ao enviar documento');
        console.error('Erro ao enviar documento:', error);
      } finally {
        isUploading.value = false;
      }
    };

    // Confirmar exclusão de documento
    const confirmDeleteDocument = (document) => {
      documentToDelete.value = document;
      showDeleteModal.value = true;
    };

    // Excluir documento
    const deleteDocument = async () => {
      if (!documentToDelete.value) return;

      isDeleting.value = true;

      try {
        await documentService.deleteDocument(documentToDelete.value.id);

        notification.success('Documento excluído com sucesso');
        showDeleteModal.value = false;

        // Recarregar documentos
        loadDocuments();
      } catch (error) {
        notification.error('Erro ao excluir documento');
        console.error('Erro ao excluir documento:', error);
      } finally {
        isDeleting.value = false;
        documentToDelete.value = null;
      }
    };

    // Formatar data
    const formatDate = (dateString) => {
      if (!dateString) return '';

      const date = new Date(dateString);
      return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      }).format(date);
    };

    // Carregar documentos quando o componente for montado
    onMounted(() => {
      loadDocuments();
    });

    // Recarregar documentos quando o ID do projeto mudar
    watch(projectId, () => {
      loadDocuments();
    });

    return {
      documents,
      isLoading,
      isUploading,
      isDeleting,
      showAddDocumentModal,
      showDeleteModal,
      documentToDelete,
      newDocument,
      fileInput,
      canAddDocument,
      canDeleteDocument,
      loadDocuments,
      uploadDocument,
      confirmDeleteDocument,
      deleteDocument,
      formatDate,
    };
  },
});
</script>
