<!-- filepath: pages/costs/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";

// 1. Importar as funções e tipos corretos do Orval
import {
  useCostsCustosList,
  useCostsCustosCreate,
  useCostsCustosUpdate,
  useCostsCustosDestroy,
} from "@/api/custo/custo";
import { useProjectsProjectsList } from "@/api/projetos/projetos";
import type {
  Custo,
  CustoRequest,
  PaginatedCustoListList,
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
const showModal = ref(false);
const editingCost = ref<Custo | null>(null);

const getInitialFormState = (): CustoRequest => ({
  descricao: "",
  projeto: 0, // Iniciar com um valor inválido para forçar a seleção
  valor: "0.00",
  data: new Date().toISOString().split("T")[0],
  tipo: "VARIAVEL", // Um valor padrão do enum CustoTipoEnum
  tarefa: null,
  categoria: null,
});

const form = ref<CustoRequest>(getInitialFormState());

// --- QUERIES (BUSCA DE DADOS) ---

// 2. Query para buscar a lista de custos com paginação
const {
  data: paginatedCosts,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedCustoListList>({
  queryKey: ["costs", currentPage],
  queryFn: () =>
    useCostsCustosList({ page: currentPage.value, page_size: pageSize }).then(
      (res) => res.data
    ),
});

// 3. Query para buscar a lista de projetos para o modal (apenas os 100 primeiros)
const { data: projectsList } = useQuery<PaginatedProjetoListList>({
  queryKey: ["projectsForCosts"],
  queryFn: () =>
    useProjectsProjectsList({ page_size: 100 }).then((res) => res.data),
  staleTime: 1000 * 60 * 5, // Cache por 5 minutos
});

// Dados computados para a UI
const costs = computed(() => paginatedCosts.value?.results || []);
const totalPages = computed(() => {
  if (!paginatedCosts.value?.count) return 1;
  return Math.ceil(paginatedCosts.value.count / pageSize);
});

// --- MUTAÇÕES (CRIAR, ATUALIZAR, DELETAR) ---

// 4. Mutação para CRIAR um custo
const createCostMutation = useCostsCustosCreate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Custo criado com sucesso!" });
      queryClient.invalidateQueries({ queryKey: ["costs"] });
      closeModal();
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao criar o custo.",
        variant: "destructive",
      });
    },
  },
});

// 5. Mutação para ATUALIZAR um custo
const updateCostMutation = useCostsCustosUpdate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Custo atualizado com sucesso!" });
      queryClient.invalidateQueries({ queryKey: ["costs"] });
      closeModal();
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Falha ao atualizar o custo.",
        variant: "destructive",
      });
    },
  },
});

// 6. Mutação para DELETAR um custo
const deleteCostMutation = useCostsCustosDestroy({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Custo excluído com sucesso!" });
      queryClient.invalidateQueries({ queryKey: ["costs"] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao excluir o custo.",
        variant: "destructive",
      });
    },
  },
});

// --- FUNÇÕES DE MANIPULAÇÃO ---

const openModal = (cost: Custo | null = null) => {
  if (cost) {
    editingCost.value = cost;
    form.value = {
      descricao: cost.descricao,
      projeto: cost.projeto,
      valor: cost.valor, // API espera string, então mantemos como string
      data: cost.data,
      tipo: cost.tipo || "VARIAVEL",
      tarefa: cost.tarefa || null,
      categoria: cost.categoria || null,
    };
  } else {
    editingCost.value = null;
    form.value = getInitialFormState();
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleSubmit = () => {
  if (editingCost.value?.id) {
    updateCostMutation.mutate({ id: editingCost.value.id, data: form.value });
  } else {
    createCostMutation.mutate({ data: form.value });
  }
};

const confirmDelete = (id: number) => {
  if (
    window.confirm(
      "Tem certeza que deseja excluir este custo? A ação não pode ser desfeita."
    )
  ) {
    deleteCostMutation.mutate({ id });
  }
};

// Funções de formatação
const formatCurrency = (value: string | number) => {
  const numberValue = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(numberValue)) return "R$ 0,00";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(numberValue);
};

const formatDate = (dateString: string) => {
  if (!dateString) return "-";
  // Adiciona um horário para evitar problemas de fuso horário
  return new Date(`${dateString}T12:00:00`).toLocaleDateString("pt-BR");
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Gerenciamento de Custos
      </h1>
      <button
        @click="openModal()"
        class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        <Icon icon="lucide:plus" class="mr-2 h-5 w-5" />
        Novo Custo
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-20">
      <Icon
        icon="svg-spinners:180-ring-with-bg"
        class="w-16 h-16 mx-auto text-primary-600"
      />
      <p class="mt-4 text-lg text-gray-600 dark:text-gray-400">
        Carregando custos...
      </p>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md"
      role="alert"
    >
      <p class="font-bold">Ocorreu um erro</p>
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
      v-else-if="costs.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:dollar-sign"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Nenhum custo registrado
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Comece adicionando o primeiro custo para seus projetos.
      </p>
    </div>

    <!-- Costs Table -->
    <div
      v-else
      class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg"
    >
      <table class="min-w-full divide-y divide-gray-300 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th
              scope="col"
              class="px-6 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Descrição
            </th>
            <th
              scope="col"
              class="px-6 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Projeto
            </th>
            <th
              scope="col"
              class="px-6 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Valor
            </th>
            <th
              scope="col"
              class="px-6 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Data
            </th>
            <th
              scope="col"
              class="px-6 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Categoria
            </th>
            <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
              <span class="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody
          class="divide-y divide-gray-200 dark:divide-gray-700 bg-white dark:bg-gray-800/50"
        >
          <tr
            v-for="cost in costs"
            :key="cost.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-700/50"
          >
            <td
              class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100"
            >
              {{ cost.descricao }}
            </td>
            <td
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ cost.projeto_nome }}
            </td>
            <td
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ formatCurrency(cost.valor) }}
            </td>
            <td
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ formatDate(cost.data) }}
            </td>
            <td
              class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ cost.categoria_nome || "-" }}
            </td>
            <td
              class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6"
            >
              <button
                @click.stop="openModal(cost)"
                class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300"
              >
                Editar
              </button>
              <button
                @click.stop="confirmDelete(cost.id)"
                class="ml-4 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
              >
                Excluir
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-6 flex justify-center">
      <nav
        class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
        aria-label="Pagination"
      >
        <button
          @click="currentPage--"
          :disabled="!paginatedCosts?.previous"
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
          :disabled="!paginatedCosts?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>

    <!-- Cost Form Modal -->
    <div v-if="showModal" class="fixed z-50 inset-0 overflow-y-auto">
      <div
        class="flex items-end sm:items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
      >
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
          @click="closeModal"
        ></div>
        <div
          class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
          <form @submit.prevent="handleSubmit">
            <div
              class="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4"
            >
              <h3
                class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
              >
                {{ editingCost ? "Editar Custo" : "Adicionar Novo Custo" }}
              </h3>
              <div class="mt-5 space-y-4">
                <div>
                  <label
                    for="descricao"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Descrição</label
                  >
                  <input
                    type="text"
                    v-model="form.descricao"
                    id="descricao"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                    required
                  />
                </div>
                <div>
                  <label
                    for="projeto"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Projeto</label
                  >
                  <select
                    v-model="form.projeto"
                    id="projeto"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                    required
                  >
                    <option disabled :value="0">Selecione um projeto</option>
                    <option
                      v-for="proj in projectsList?.results"
                      :key="proj.id"
                      :value="proj.id"
                    >
                      {{ proj.titulo }}
                    </option>
                  </select>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label
                      for="valor"
                      class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                      >Valor (R$)</label
                    >
                    <input
                      type="number"
                      step="0.01"
                      v-model="form.valor"
                      id="valor"
                      class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                      required
                    />
                  </div>
                  <div>
                    <label
                      for="data"
                      class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                      >Data</label
                    >
                    <input
                      type="date"
                      v-model="form.data"
                      id="data"
                      class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                      required
                    />
                  </div>
                </div>
              </div>
            </div>
            <div
              class="bg-gray-50 dark:bg-gray-900 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse"
            >
              <button
                type="submit"
                :disabled="
                  createCostMutation.isPending.value ||
                  updateCostMutation.isPending.value
                "
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                Salvar Custo
              </button>
              <button
                type="button"
                @click="closeModal"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-700 text-base font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:w-auto sm:text-sm"
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
