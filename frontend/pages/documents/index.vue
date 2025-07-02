<!-- filepath: pages/documents/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";

// 1. Importar as funções e tipos corretos do Orval
import {
  useDocumentsList,
  useDocumentsCreate,
  useDocumentsDestroy,
} from "@/api/documentos/documentos";
import { useProjectsProjectsList } from "@/api/projects/projects";
import type {
  DocumentoList,
  DocumentoRequest,
  PaginatedDocumentoListList,
  PaginatedProjetoListList,
} from "@/api/schemas";

definePageMeta({
  middleware: "auth",
});

// --- HOOKS E ESTADO INICIAL ---
const queryClient = useQueryClient();
const { toast } = useToast();

const currentPage = ref(1);
const pageSize = 10;
const showUploadModal = ref(false);
const selectedFile = ref<File | null>(null);

const getInitialFormState = (): Omit<
  DocumentoRequest,
  "arquivo" | "versao"
> => ({
  titulo: "",
  descricao: "",
  projeto: 0,
  tipo: "OUTRO",
});

const form = ref(getInitialFormState());

// --- QUERIES ---
const {
  data: paginatedDocs,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedDocumentoListList>({
  queryKey: ["documents", currentPage],
  queryFn: () =>
    useDocumentsList({ page: currentPage.value, page_size: pageSize }).then(
      (res) => res.data
    ),
});

const { data: projectsList } = useQuery<PaginatedProjetoListList>({
  queryKey: ["projectsForDocs"],
  queryFn: () =>
    useProjectsProjectsList({ page_size: 100 }).then((res) => res.data),
  staleTime: 1000 * 60 * 5,
});

const documents = computed(() => paginatedDocs.value?.results || []);
const totalPages = computed(() =>
  paginatedDocs.value?.count
    ? Math.ceil(paginatedDocs.value.count / pageSize)
    : 1
);

// --- MUTAÇÕES ---

// 2. Mutação para UPLOAD (criar) um documento
const uploadMutation = useDocumentsCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Documento enviado com sucesso!",
      });
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      closeModal();
    },
    onError: (err: any) => {
      toast({
        title: "Erro no Upload",
        description:
          err.response?.data?.detail || "Não foi possível enviar o arquivo.",
        variant: "destructive",
      });
    },
  },
});

// 3. Mutação para DELETAR um documento
const deleteMutation = useDocumentsDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Documento excluído com sucesso!",
      });
      queryClient.invalidateQueries({ queryKey: ["documents"] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Falha ao excluir o documento.",
        variant: "destructive",
      });
    },
  },
});

// --- FUNÇÕES DE MANIPULAÇÃO ---

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0];
    if (!form.value.titulo) {
      // Preenche o título com o nome do arquivo (sem extensão) se estiver vazio
      form.value.titulo = selectedFile.value.name.replace(/\.[^/.]+$/, "");
    }
  }
};

const handleUpload = () => {
  if (!selectedFile.value || !form.value.projeto) {
    toast({
      title: "Campos Obrigatórios",
      description: "Por favor, selecione um arquivo e um projeto.",
      variant: "destructive",
    });
    return;
  }

  // 4. Monta o payload para a mutação do Orval
  const payload: DocumentoRequest = {
    ...form.value,
    projeto: form.value.projeto,
    arquivo: selectedFile.value,
    versao: "1.0", // Definir uma versão inicial
  };

  uploadMutation.mutate(
    { data: payload },
    {
      // Importante: O Orval e o Axios cuidam do 'Content-Type: multipart/form-data'
      // quando o corpo da requisição é uma instância de FormData, mas como nosso
      // payload gerado pelo Orval é um objeto, precisamos de um pequeno ajuste no
      // nosso plugin do Axios ou aqui para garantir o header correto.
      // A forma mais fácil é deixar o Axios inferir pelo FormData.
      // Vamos ajustar o Orval para lidar com isso melhor no futuro.
      // Por enquanto, a mutação do Orval deve ser capaz de lidar com Blob.
    }
  );
};

const confirmDelete = (id: number) => {
  if (window.confirm("Tem certeza que deseja excluir este documento?")) {
    deleteMutation.mutate({ id });
  }
};

const closeModal = () => {
  showUploadModal.value = false;
  form.value = getInitialFormState();
  selectedFile.value = null;
};

// --- FUNÇÕES DE UTILIDADE E ESTILO ---

const formatBytes = (bytes: number, decimals = 2) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
};

const getFileIcon = (fileType: string | undefined) => {
  if (!fileType) return "lucide:file";
  if (fileType.includes("pdf")) return "lucide:file-type";
  if (fileType.includes("image")) return "lucide:image";
  if (fileType.includes("word")) return "lucide:file-text";
  if (fileType.includes("spreadsheet") || fileType.includes("excel"))
    return "lucide:file-spreadsheet";
  if (fileType.includes("presentation")) return "lucide:file-sliders";
  return "lucide:file-question";
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div
      class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4"
    >
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Gerenciador de Documentos
        </h1>
        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">
          Armazene e organize os arquivos dos seus projetos.
        </p>
      </div>
      <button
        @click="showUploadModal = true"
        class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        <Icon icon="lucide:upload" class="mr-2 h-5 w-5" />
        Novo Upload
      </button>
    </div>

    <!-- Estados da UI -->
    <div v-if="isLoading" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
    </div>
    <div
      v-else-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md"
      role="alert"
    >
      Erro ao carregar documentos.
    </div>
    <div
      v-else-if="documents.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:file-search"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Nenhum documento encontrado
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Comece fazendo o upload do seu primeiro arquivo.
      </p>
    </div>

    <!-- Lista de Documentos -->
    <div v-else class="bg-white dark:bg-gray-800/50 shadow-md rounded-lg">
      <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
        <li
          v-for="doc in documents"
          :key="doc.id"
          class="px-4 py-4 sm:px-6 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center min-w-0">
              <Icon
                :icon="getFileIcon(doc.tipo_arquivo)"
                class="h-10 w-10 text-gray-400 dark:text-gray-500 flex-shrink-0"
              />
              <div class="ml-4 min-w-0">
                <p
                  class="text-sm font-medium text-primary-600 dark:text-primary-400 truncate"
                >
                  {{ doc.titulo }}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                  Projeto: {{ doc.projeto_nome }}
                </p>
                <p class="text-xs text-gray-400 dark:text-gray-500">
                  Versão: {{ doc.versao || "1.0" }}
                </p>
              </div>
            </div>
            <div class="ml-4 flex-shrink-0 flex items-center space-x-4">
              <span
                class="text-sm text-gray-500 dark:text-gray-400 hidden sm:block"
                >{{ formatBytes(doc.tamanho_arquivo) }}</span
              >
              <a
                :href="doc.arquivo"
                target="_blank"
                class="text-gray-500 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400"
                title="Baixar"
              >
                <Icon icon="lucide:download" class="h-5 w-5" />
              </a>
              <button
                @click.stop="confirmDelete(doc.id)"
                class="text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-500"
                title="Excluir"
              >
                <Icon icon="lucide:trash-2" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Paginação -->
    <div v-if="totalPages > 1" class="mt-6 flex justify-center">
      <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
        <button
          @click="currentPage--"
          :disabled="!paginatedDocs?.previous"
          class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
        <span
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-200"
          >Página {{ currentPage }} de {{ totalPages }}</span
        >
        <button
          @click="currentPage++"
          :disabled="!paginatedDocs?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>

    <!-- Modal de Upload -->
    <div v-if="showUploadModal" class="fixed z-50 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full"
        >
          <form @submit.prevent="handleUpload">
            <div class="px-4 pt-5 pb-4 sm:p-6">
              <h3
                class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
              >
                Upload de Novo Documento
              </h3>
              <div class="mt-4 space-y-4">
                <div>
                  <label
                    for="title"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Título</label
                  >
                  <input
                    type="text"
                    v-model="form.titulo"
                    id="title"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                    required
                  />
                </div>
                <div>
                  <label
                    for="project"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Projeto Associado</label
                  >
                  <select
                    v-model="form.projeto"
                    id="project"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                    required
                  >
                    <option disabled :value="0">Selecione um projeto</option>
                    <option
                      v-for="project in projectsList?.results"
                      :key="project.id"
                      :value="project.id"
                    >
                      {{ project.titulo }}
                    </option>
                  </select>
                </div>
                <div>
                  <label
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Arquivo</label
                  >
                  <div
                    class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-md"
                  >
                    <div class="space-y-1 text-center">
                      <Icon
                        icon="lucide:file-up"
                        class="mx-auto h-12 w-12 text-gray-400"
                      />
                      <div
                        class="flex text-sm text-gray-600 dark:text-gray-400"
                      >
                        <label
                          for="file-upload"
                          class="relative cursor-pointer bg-white dark:bg-gray-800 rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none"
                        >
                          <span>Selecione um arquivo</span>
                          <input
                            id="file-upload"
                            type="file"
                            class="sr-only"
                            @change="onFileChange"
                            required
                          />
                        </label>
                      </div>
                      <p v-if="selectedFile" class="text-sm text-gray-500">
                        {{ selectedFile.name }} ({{
                          formatBytes(selectedFile.size)
                        }})
                      </p>
                      <p v-else class="text-xs text-gray-500">
                        PNG, JPG, PDF, DOCX, etc.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div
              class="bg-gray-50 dark:bg-gray-900 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="uploadMutation.isPending.value"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                <Icon
                  v-if="uploadMutation.isPending.value"
                  icon="svg-spinners:180-ring-with-bg"
                  class="mr-2 h-5 w-5"
                />
                Fazer Upload
              </button>
              <button
                type="button"
                @click="closeModal"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-700 text-base font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 sm:mt-0 sm:w-auto sm:text-sm"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
