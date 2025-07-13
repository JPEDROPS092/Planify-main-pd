<!-- filepath: pages/communications/index.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: "auth",
});

import { ref, computed, watch } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { useApiErrorHandler } from "@/composables/useApiErrorHandler";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

// 1. Importar funções e tipos do Orval para comunicações
import {
  useCommunicationsList,
  useCommunicationsCreate,
  useCommunicationsUpdate,
  useCommunicationsDestroy,
} from "@/api/communications/communications";
import type {
  PaginatedComunicacaoList,
  Comunicacao,
  ComunicacaoRequest,
  ComunicacaoTipoEnum,
} from "@/api/schemas";

const queryClient = useQueryClient();
const { toast } = useToast();
const { handleApiError } = useApiErrorHandler();

// Estado local para filtros e paginação
const currentPage = ref(1);
const pageSize = 10;
const searchTerm = ref("");
const selectedTipo = ref<ComunicacaoTipoEnum | "">("");
const selectedProjeto = ref<number | "">("");
const dataInicio = ref("");
const dataFim = ref("");

// Estado para modais
const showCreateModal = ref(false);
const showEditModal = ref(false);
const editingCommunication = ref<Comunicacao | null>(null);

// Estado do formulário
const formData = ref<ComunicacaoRequest>({
  projeto: 0,
  tipo: "ATA" as ComunicacaoTipoEnum,
  titulo: "",
  texto: "",
  destinatarios: [],
});

// 2. Query para buscar comunicações com filtros
const {
  data: paginatedCommunications,
  isLoading,
  error,
  refetch,
} = useCommunicationsList(
  computed(() => ({
    page: currentPage.value,
    search: searchTerm.value || undefined,
    tipo: selectedTipo.value || undefined,
    projeto: selectedProjeto.value || undefined,
    data_inicio: dataInicio.value || undefined,
    data_fim: dataFim.value || undefined,
    ordering: "-criada_em", // Mais recentes primeiro
  })),
  {
    query: {
      placeholderData: (previousData) => previousData,
    },
  }
);

// Computed properties para dados
const totalPages = computed(() => {
  if (!paginatedCommunications.value?.data?.count) return 1;
  return Math.ceil(paginatedCommunications.value.data.count / pageSize);
});

const communications = computed(
  () => paginatedCommunications.value?.data?.results || []
);

// 3. Mutações para CRUD
const createMutation = useCommunicationsCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Comunicação criada com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["api", "communications"] });
      showCreateModal.value = false;
      resetForm();
    },
    onError: (error) => {
      handleApiError(error, "Erro ao criar comunicação");
    },
  },
});

const updateMutation = useCommunicationsUpdate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Comunicação atualizada com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["api", "communications"] });
      showEditModal.value = false;
      editingCommunication.value = null;
      resetForm();
    },
    onError: (error) => {
      handleApiError(error, "Erro ao atualizar comunicação");
    },
  },
});

const deleteMutation = useCommunicationsDestroy({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Sucesso",
        description: "Comunicação removida com sucesso.",
        type: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["api", "communications"] });
    },
    onError: (error) => {
      handleApiError(error, "Erro ao remover comunicação");
    },
  },
});

// Funções auxiliares
const resetForm = () => {
  formData.value = {
    projeto: 0,
    tipo: "ATA" as ComunicacaoTipoEnum,
    titulo: "",
    texto: "",
    destinatarios: [],
  };
};

const openCreateModal = () => {
  resetForm();
  showCreateModal.value = true;
};

const openEditModal = (communication: Comunicacao) => {
  editingCommunication.value = communication;
  formData.value = {
    projeto: communication.projeto,
    tipo: communication.tipo,
    titulo: communication.titulo,
    texto: communication.texto,
    destinatarios: communication.destinatarios,
  };
  showEditModal.value = true;
};

const handleCreate = () => {
  if (!formData.value.titulo || !formData.value.texto) {
    toast({
      title: "Erro",
      description: "Título e texto são obrigatórios.",
      type: "error",
    });
    return;
  }
  createMutation.mutate({ data: formData.value });
};

const handleUpdate = () => {
  if (!editingCommunication.value) return;
  updateMutation.mutate({
    id: editingCommunication.value.id,
    data: formData.value,
  });
};

const handleDelete = (id: number) => {
  if (confirm("Tem certeza que deseja remover esta comunicação?")) {
    deleteMutation.mutate({ id });
  }
};

// Formatação e utilitários
const formatDate = (dateString: string) => {
  if (!dateString) return "";
  return format(new Date(dateString), "dd/MM/yyyy 'às' HH:mm", {
    locale: ptBR,
  });
};

const getTipoIcon = (tipo: ComunicacaoTipoEnum) => {
  const icons: Record<ComunicacaoTipoEnum, string> = {
    ATA: "lucide:file-text",
    MEMORANDO: "lucide:mail",
    RELATORIO: "lucide:file-bar-chart",
    OFICIO: "lucide:scroll",
    COMUNICADO: "lucide:megaphone",
    OUTRO: "lucide:file-plus",
  };
  return icons[tipo] || "lucide:file";
};

const getTipoColor = (tipo: ComunicacaoTipoEnum) => {
  const colors: Record<ComunicacaoTipoEnum, string> = {
    ATA: "bg-blue-500",
    MEMORANDO: "bg-green-500",
    RELATORIO: "bg-purple-500",
    OFICIO: "bg-yellow-500",
    COMUNICADO: "bg-red-500",
    OUTRO: "bg-gray-500",
  };
  return colors[tipo] || "bg-gray-500";
};

const tipoOptions = [
  { value: "ATA", label: "Ata de Reunião" },
  { value: "MEMORANDO", label: "Memorando" },
  { value: "RELATORIO", label: "Relatório" },
  { value: "OFICIO", label: "Ofício" },
  { value: "COMUNICADO", label: "Comunicado Geral" },
  { value: "OUTRO", label: "Outro" },
];

// Limpar filtros
const clearFilters = () => {
  searchTerm.value = "";
  selectedTipo.value = "";
  selectedProjeto.value = "";
  dataInicio.value = "";
  dataFim.value = "";
  currentPage.value = 1;
};

// Watch para resetar página quando filtros mudarem
watch([searchTerm, selectedTipo, selectedProjeto, dataInicio, dataFim], () => {
  currentPage.value = 1;
});
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Comunicações Formais
      </h1>
      <button
        @click="openCreateModal"
        class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md font-medium transition-colors flex items-center gap-2"
      >
        <Icon icon="lucide:plus" class="w-4 h-4" />
        Nova Comunicação
      </button>
    </div>

    <!-- Filtros -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Buscar
          </label>
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Título ou texto..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          />
        </div>

        <div>
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Tipo
          </label>
          <select
            v-model="selectedTipo"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          >
            <option value="">Todos os tipos</option>
            <option
              v-for="tipo in tipoOptions"
              :key="tipo.value"
              :value="tipo.value"
            >
              {{ tipo.label }}
            </option>
          </select>
        </div>

        <div>
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Data início
          </label>
          <input
            v-model="dataInicio"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          />
        </div>

        <div>
          <label
            class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            Data fim
          </label>
          <input
            v-model="dataFim"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          />
        </div>
      </div>

      <div class="mt-4 flex justify-end">
        <button
          @click="clearFilters"
          class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
        >
          Limpar filtros
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !communications.length" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
      <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
        Carregando comunicações...
      </p>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md"
      role="alert"
    >
      <p class="font-bold">Erro ao carregar comunicações</p>
      <p>{{ (error as any).message }}</p>
      <button
        @click="refetch()"
        class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
      >
        Tentar Novamente
      </button>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="communications.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:file-text"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Nenhuma comunicação encontrada
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Comece criando uma nova comunicação formal.
      </p>
    </div>

    <!-- Communications List -->
    <div
      v-else
      class="bg-white dark:bg-gray-800 shadow overflow-hidden rounded-lg"
    >
      <ul role="list" class="divide-y divide-gray-200 dark:divide-gray-700">
        <li
          v-for="communication in communications"
          :key="communication.id"
          class="p-4 sm:p-6 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-start flex-1">
              <div
                class="flex-shrink-0 h-12 w-12 rounded-full flex items-center justify-center"
                :class="getTipoColor(communication.tipo)"
              >
                <Icon
                  :icon="getTipoIcon(communication.tipo)"
                  class="h-6 w-6 text-white"
                />
              </div>
              <div class="ml-4 flex-1">
                <div class="flex items-center justify-between">
                  <h3
                    class="text-lg font-medium text-gray-900 dark:text-gray-100"
                  >
                    {{ communication.titulo }}
                  </h3>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200"
                  >
                    {{ communication.tipo_display }}
                  </span>
                </div>
                <p
                  class="text-sm text-gray-600 dark:text-gray-300 mt-1 line-clamp-2"
                >
                  {{ communication.texto }}
                </p>
                <div
                  class="mt-3 flex items-center text-sm text-gray-500 dark:text-gray-400 space-x-4"
                >
                  <span>
                    <Icon icon="lucide:user" class="w-4 h-4 inline mr-1" />
                    {{ communication.remetente_nome }}
                  </span>
                  <span>
                    <Icon icon="lucide:folder" class="w-4 h-4 inline mr-1" />
                    {{ communication.projeto_nome }}
                  </span>
                  <span>
                    <Icon icon="lucide:calendar" class="w-4 h-4 inline mr-1" />
                    {{ formatDate(communication.criada_em) }}
                  </span>
                  <span v-if="communication.destinatarios_info?.length">
                    <Icon icon="lucide:users" class="w-4 h-4 inline mr-1" />
                    {{ communication.destinatarios_info.length }} destinatários
                  </span>
                </div>
              </div>
            </div>
            <div class="ml-4 flex-shrink-0 flex items-center space-x-2">
              <button
                @click="openEditModal(communication)"
                class="text-indigo-600 hover:text-indigo-500"
                title="Editar comunicação"
              >
                <Icon icon="lucide:edit" class="h-5 w-5" />
              </button>
              <button
                @click="handleDelete(communication.id)"
                class="text-red-600 hover:text-red-500"
                title="Remover comunicação"
                :disabled="deleteMutation.isPending"
              >
                <Icon icon="lucide:trash-2" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-8 flex justify-center">
      <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
        <button
          @click="currentPage--"
          :disabled="!paginatedCommunications?.data?.previous"
          class="relative inline-flex items-center px-3 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Anterior
        </button>
        <span
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-200"
        >
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button
          @click="currentPage++"
          :disabled="!paginatedCommunications?.data?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>

    <!-- Modal para Criar Comunicação -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showCreateModal = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white dark:bg-gray-800"
        @click.stop
      >
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
            Nova Comunicação
          </h3>
          <button
            @click="showCreateModal = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <Icon icon="lucide:x" class="w-6 h-6" />
          </button>
        </div>

        <form @submit.prevent="handleCreate" class="space-y-4">
          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Tipo *
            </label>
            <select
              v-model="formData.tipo"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              <option
                v-for="tipo in tipoOptions"
                :key="tipo.value"
                :value="tipo.value"
              >
                {{ tipo.label }}
              </option>
            </select>
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Título *
            </label>
            <input
              v-model="formData.titulo"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Conteúdo *
            </label>
            <textarea
              v-model="formData.texto"
              rows="4"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            ></textarea>
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Projeto ID *
            </label>
            <input
              v-model.number="formData.projeto"
              type="number"
              required
              min="1"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="showCreateModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="createMutation.isPending"
              class="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 disabled:opacity-50"
            >
              {{ createMutation.isPending ? "Criando..." : "Criar" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal para Editar Comunicação -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showEditModal = false"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white dark:bg-gray-800"
        @click.stop
      >
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">
            Editar Comunicação
          </h3>
          <button
            @click="showEditModal = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <Icon icon="lucide:x" class="w-6 h-6" />
          </button>
        </div>

        <form @submit.prevent="handleUpdate" class="space-y-4">
          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Tipo *
            </label>
            <select
              v-model="formData.tipo"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              <option
                v-for="tipo in tipoOptions"
                :key="tipo.value"
                :value="tipo.value"
              >
                {{ tipo.label }}
              </option>
            </select>
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Título *
            </label>
            <input
              v-model="formData.titulo"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Conteúdo *
            </label>
            <textarea
              v-model="formData.texto"
              rows="4"
              required
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            ></textarea>
          </div>

          <div>
            <label
              class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
            >
              Projeto ID *
            </label>
            <input
              v-model.number="formData.projeto"
              type="number"
              required
              min="1"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
          </div>

          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="showEditModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-600 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500"
            >
              Cancelar
            </button>
            <button
              type="submit"
              :disabled="updateMutation.isPending"
              class="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 disabled:opacity-50"
            >
              {{ updateMutation.isPending ? "Atualizando..." : "Atualizar" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
