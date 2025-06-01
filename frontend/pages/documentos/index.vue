<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold tracking-tight">Documentos</h1>
        <button
          @click="openNewDocumentModal"
          class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4 mr-2"
          >
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Novo Documento
        </button>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar documentos..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="absolute right-3 top-2.5 h-4 w-4 text-gray-400"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="m21 21-4.3-4.3"></path>
          </svg>
        </div>
        <select
          v-model="typeFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todos os tipos</option>
          <option value="REQUISITO">Requisito</option>
          <option value="DESIGN">Design</option>
          <option value="MANUAL">Manual</option>
          <option value="RELATORIO">Relatório</option>
          <option value="ATA">Ata de Reunião</option>
          <option value="OUTRO">Outro</option>
        </select>
        <select
          v-model="projectFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          <option value="">Todos os projetos</option>
          <option
            v-for="project in projects"
            :key="project.id"
            :value="project.id"
          >
            {{ project.titulo }}
          </option>
        </select>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-8">
        <div
          class="h-8 w-8 animate-spin rounded-full border-2 border-blue-600 border-t-transparent"
        ></div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4 text-red-700">
        <p>{{ error }}</p>
        <button
          @click="fetchDocuments"
          class="mt-2 text-sm font-medium underline"
        >
          Tentar novamente
        </button>
      </div>

      <!-- Empty state -->
      <div
        v-else-if="filteredDocuments.length === 0"
        class="flex flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 bg-gray-50 p-12 text-center"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-12 w-12 text-gray-400"
        >
          <path
            d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
          ></path>
          <polyline points="14 2 14 8 20 8"></polyline>
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">
          Nenhum documento encontrado
        </h3>
        <p class="mt-1 text-sm text-gray-500">
          {{
            documents.length === 0
              ? 'Comece fazendo upload do seu primeiro documento.'
              : 'Nenhum documento corresponde aos filtros aplicados.'
          }}
        </p>
        <button
          v-if="documents.length === 0"
          @click="openNewDocumentModal"
          class="mt-4 inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4 mr-2"
          >
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Adicionar Documento
        </button>
      </div>

      <!-- Documents list -->
      <div v-else>
        <div class="overflow-hidden rounded-lg border bg-white shadow">
          <table class="w-full border-collapse text-left">
            <thead class="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Título
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Tipo
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Projeto
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Versão
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Enviado por
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Data
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500"
                >
                  Ações
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr
                v-for="doc in filteredDocuments"
                :key="doc.id"
                class="hover:bg-gray-50"
              >
                <td class="px-4 py-3 text-sm">
                  <div class="font-medium text-gray-900">{{ doc.titulo }}</div>
                  <div class="mt-1 line-clamp-1 text-xs text-gray-500">
                    {{ doc.descricao }}
                  </div>
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-blue-100 text-blue-800': doc.tipo === 'REQUISITO',
                      'bg-purple-100 text-purple-800': doc.tipo === 'DESIGN',
                      'bg-green-100 text-green-800': doc.tipo === 'MANUAL',
                      'bg-yellow-100 text-yellow-800': doc.tipo === 'RELATORIO',
                      'bg-orange-100 text-orange-800': doc.tipo === 'ATA',
                      'bg-gray-100 text-gray-800': doc.tipo === 'OUTRO',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getTypeLabel(doc.tipo) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">
                  {{ getProjectName(doc.projeto) }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">
                  {{ doc.versao }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">
                  {{ doc.enviado_por?.username || 'Desconhecido' }}
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">
                  {{ formatDate(doc.data_upload) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <div class="flex items-center space-x-2">
                    <button
                      @click="downloadDocument(doc)"
                      class="rounded-md p-1 text-blue-600 hover:bg-blue-50"
                      title="Download"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-4 w-4"
                      >
                        <path
                          d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
                        ></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" x2="12" y1="15" y2="3"></line>
                      </svg>
                    </button>
                    <button
                      @click="viewDocument(doc.id)"
                      class="rounded-md p-1 text-gray-600 hover:bg-gray-100"
                      title="Ver detalhes"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        class="h-4 w-4"
                      >
                        <path
                          d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"
                        ></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="totalPages > 1"
        class="flex items-center justify-center space-x-2 pt-4"
      >
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="m15 18-6-6 6-6"></path>
          </svg>
        </button>
        <div
          v-for="page in paginationRange"
          :key="page"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md text-sm font-medium"
          :class="
            page === currentPage
              ? 'bg-blue-600 text-white'
              : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
          "
          @click="changePage(page)"
        >
          {{ page }}
        </div>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="h-4 w-4"
          >
            <path d="m9 18 6-6-6-6"></path>
          </svg>
        </button>
      </div>

      <!-- Modal para novo documento -->
      <div
        v-if="showDocumentModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      >
        <div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium">Novo Documento</h3>
            <button
              @click="showDocumentModal = false"
              class="rounded-full p-1 hover:bg-gray-100"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-5 w-5"
              >
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="uploadDocument" class="mt-4 space-y-4">
            <div>
              <label
                for="titulo"
                class="block text-sm font-medium text-gray-700"
                >Título</label
              >
              <input
                id="titulo"
                v-model="documentForm.titulo"
                type="text"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div>
              <label
                for="descricao"
                class="block text-sm font-medium text-gray-700"
                >Descrição</label
              >
              <textarea
                id="descricao"
                v-model="documentForm.descricao"
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              ></textarea>
            </div>
            <div>
              <label
                for="projeto"
                class="block text-sm font-medium text-gray-700"
                >Projeto</label
              >
              <select
                id="projeto"
                v-model="documentForm.projeto"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option
                  v-for="project in projects"
                  :key="project.id"
                  :value="project.id"
                >
                  {{ project.titulo }}
                </option>
              </select>
            </div>
            <div>
              <label for="tipo" class="block text-sm font-medium text-gray-700"
                >Tipo</label
              >
              <select
                id="tipo"
                v-model="documentForm.tipo"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="REQUISITO">Requisito</option>
                <option value="DESIGN">Design</option>
                <option value="MANUAL">Manual</option>
                <option value="RELATORIO">Relatório</option>
                <option value="ATA">Ata de Reunião</option>
                <option value="OUTRO">Outro</option>
              </select>
            </div>
            <div>
              <label
                for="arquivo"
                class="block text-sm font-medium text-gray-700"
                >Arquivo</label
              >
              <input
                id="arquivo"
                ref="fileInput"
                type="file"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showDocumentModal = false"
                class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="uploading"
                class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70"
              >
                <span
                  v-if="uploading"
                  class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
                ></span>
                {{ uploading ? 'Enviando...' : 'Enviar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import {
  listDocumentos,
  createDocumento,
  retrieveDocumento,
  downloadDocumento,
} from '~/services/api/documents';
import { listProjetos } from '~/services/api/projects';
import { useAuth } from '~/services/api/auth';
import { createFormData } from '~/services/api/config';

definePageMeta({
  middleware: ['auth'],
});

const router = useRouter();
const { $api } = useNuxtApp();
const fileInput = ref(null);

// Estado
const documents = ref([]);
const projects = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const searchQuery = ref('');
const typeFilter = ref('');
const projectFilter = ref('');
const showDocumentModal = ref(false);
const uploading = ref(false);

// Formulário de documento
const documentForm = ref({
  titulo: '',
  descricao: '',
  projeto: '',
  tipo: 'OUTRO',
  versao: '1.0',
});

// Filtrar documentos
const filteredDocuments = computed(() => {
  return documents.value.filter((doc) => {
    const matchesSearch =
      searchQuery.value === '' ||
      doc.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (doc.descricao &&
        doc.descricao.toLowerCase().includes(searchQuery.value.toLowerCase()));

    const matchesType =
      typeFilter.value === '' || doc.tipo === typeFilter.value;
    const matchesProject =
      projectFilter.value === '' ||
      doc.projeto === parseInt(projectFilter.value);

    return matchesSearch && matchesType && matchesProject;
  });
});

// Paginação
const paginationRange = computed(() => {
  const range = [];
  const maxVisiblePages = 5;

  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) {
      range.push(i);
    }
  } else {
    let start = Math.max(
      1,
      currentPage.value - Math.floor(maxVisiblePages / 2)
    );
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1);

    if (end - start + 1 < maxVisiblePages) {
      start = Math.max(1, end - maxVisiblePages + 1);
    }

    for (let i = start; i <= end; i++) {
      range.push(i);
    }
  }

  return range;
});

// Buscar documentos
const fetchDocuments = async () => {
  loading.value = true;
  error.value = null;

  try {
    const params = {
      page: currentPage.value,
      ordering: '-data_upload',
    };

    if (typeFilter.value) {
      params.tipo = typeFilter.value;
    }

    if (projectFilter.value) {
      params.projeto = projectFilter.value;
    }

    if (searchQuery.value) {
      params.search = searchQuery.value;
    }

    // Usar o novo serviço de API para documentos
    const response = await listDocumentos(params);

    documents.value = response.results.map((doc) => ({
      id: doc.id,
      titulo: doc.titulo,
      descricao: doc.descricao,
      projeto: doc.projeto,
      projeto_nome: doc.projeto_nome,
      tipo: doc.tipo,
      tipo_display: doc.tipo_display,
      versao: doc.versao,
      arquivo: doc.arquivo,
      arquivo_nome: doc.arquivo_nome,
      data_upload: doc.data_upload,
      tamanho: doc.tamanho,
    }));

    totalItems.value = response.count;
    totalPages.value = Math.ceil(response.count / itemsPerPage.value);
  } catch (err) {
    console.error('Erro ao buscar documentos:', err);
    error.value =
      'Não foi possível carregar os documentos. Por favor, tente novamente.';
  } finally {
    loading.value = false;
  }
};

// Buscar projetos
const fetchProjects = async () => {
  try {
    // Usar o novo serviço de API para projetos
    const response = await listProjetos();
    projects.value = response.results.map((project) => ({
      id: project.id,
      titulo: project.nome,
    }));

    if (projects.value.length > 0) {
      documentForm.value.projeto = projects.value[0].id;
    }
  } catch (err) {
    console.error('Erro ao buscar projetos:', err);
  }
};

// Mudar página
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

// Obter label do tipo
const getTypeLabel = (type) => {
  const typeMap = {
    REQUISITO: 'Requisito',
    DESIGN: 'Design',
    MANUAL: 'Manual',
    RELATORIO: 'Relatório',
    ATA: 'Ata de Reunião',
    OUTRO: 'Outro',
  };
  return typeMap[type] || type;
};

// Obter nome do projeto
const getProjectName = (projectId) => {
  const project = projects.value.find((p) => p.id === projectId);
  return project ? project.titulo : 'Projeto não encontrado';
};

// Abrir modal de novo documento
const openNewDocumentModal = () => {
  documentForm.value = {
    titulo: '',
    descricao: '',
    projeto: projects.value.length > 0 ? projects.value[0].id : '',
    tipo: 'OUTRO',
    versao: '1.0',
  };
  showDocumentModal.value = true;
};

// Upload de documento
const uploadDocument = async () => {
  if (!fileInput.value.files || fileInput.value.files.length === 0) {
    alert('Por favor, selecione um arquivo para upload.');
    return;
  }

  uploading.value = true;

  try {
    // Preparar dados do documento
    const documentData = {
      titulo: documentForm.value.titulo,
      descricao: documentForm.value.descricao || '',
      projeto: documentForm.value.projeto,
      tipo: documentForm.value.tipo,
      versao: documentForm.value.versao || '1.0',
      arquivo: fileInput.value.files[0],
    };

    // Usar o helper createFormData para criar o FormData corretamente
    const formData = createFormData(documentData);

    // Usar o novo serviço de API para criar documentos
    await createDocumento(formData);

    showDocumentModal.value = false;
    await fetchDocuments();
  } catch (err) {
    console.error('Erro ao fazer upload do documento:', err);
    alert(
      'Não foi possível fazer o upload do documento. Por favor, tente novamente.'
    );
  } finally {
    uploading.value = false;
  }
};

// Download de documento
const downloadDocument = async (doc) => {
  try {
    // Usar o novo serviço de API para download de documentos
    const url = await downloadDocumento(doc.id);
    window.open(url, '_blank');
  } catch (err) {
    console.error('Erro ao fazer download do documento:', err);
    error.value =
      'Não foi possível fazer o download do documento. Por favor, tente novamente.';
  }
};

// Ver detalhes do documento
const viewDocument = async (id) => {
  try {
    // Buscar detalhes do documento usando o novo serviço de API antes de navegar
    await retrieveDocumento(id);
    router.push(`/documentos/${id}`);
  } catch (err) {
    console.error('Erro ao buscar detalhes do documento:', err);
    error.value = 'Não foi possível carregar os detalhes do documento.';
  }
};

// Observar mudanças nos filtros e página
watch([currentPage, searchQuery, typeFilter, projectFilter], () => {
  fetchDocuments();
});

// Carregar dados ao montar o componente
onMounted(async () => {
  await fetchProjects();
  await fetchDocuments();
});
</script>
