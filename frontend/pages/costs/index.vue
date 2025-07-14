<!-- filepath: pages/costs/index.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { saveAs } from "file-saver";
import { useRouter } from "vue-router";

// Definindo o tipo para o definePageMeta do Nuxt
declare function definePageMeta(meta: { middleware: string }): void;

// 1. Importar as funções e tipos corretos do Orval
import {
  useCostsCustosList,
  useCostsCustosCreate,
  useCostsCustosUpdate,
  useCostsCustosDestroy,
  useCostsCategoriasList,
  useCostsCustosRetrieve,
} from "@/api/custo/custo";
import { useProjectsProjectsMyProjectsList } from "@/api/projetos/projetos";
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
const router = useRouter();
const queryClient = useQueryClient();
const { toast } = useToast();

// Função para inicializar o estado do formulário
const getInitialFormState = (): CustoRequest => ({
  descricao: "",
  projeto: 0, // Iniciar com um valor inválido para forçar a seleção
  valor: "0.00",
  data: new Date().toISOString().split("T")[0],
  tipo: "VARIAVEL", // Um valor padrão do enum CustoTipoEnum
  tarefa: null,
  categoria: null,
});

const currentPage = ref(1);
const pageSize = 10;
const showModal = ref(false);
const editingCost = ref<Custo | null>(null);
// Adicionando a declaração do form que estava faltando
const form = ref<CustoRequest>(getInitialFormState());

// --- ESTADO DOS FILTROS ---
const filterProjeto = ref<number | null>(null);
const filterCategoria = ref<number | null>(null);
const filterDataInicio = ref<string | null>(null);
const filterDataFim = ref<string | null>(null);

// --- BUSCA DE CATEGORIAS ---
const categoriasList = ref<any>(null);
const categoriesQuery = useCostsCategoriasList();
// Configurar os dados quando estiverem disponíveis
onMounted(() => {
  // Observar mudanças nos dados das categorias
  if (categoriesQuery.data.value) {
    categoriasList.value = categoriesQuery.data.value.data;
  }
});

// --- BUSCA DE PROJETOS ---
// Usando a API de "meus projetos" para evitar erro 403
const projectsList = ref<any>(null);
const projectsQuery = useProjectsProjectsMyProjectsList();

// Configurar os dados quando estiverem disponíveis
onMounted(() => {
  // Observar mudanças nos dados dos projetos
  if (projectsQuery.data.value) {
    projectsList.value = projectsQuery.data.value.data;
  }
});

// Definindo o tipo para a resposta paginada de custos
interface PaginatedResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: CostItem[];
}

// --- QUERY DE CUSTOS COM FILTROS ---
const {
  data: paginatedCosts,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedResponse>({
  queryKey: [
    "costs",
    currentPage,
    filterProjeto,
    filterCategoria,
    filterDataInicio,
    filterDataFim,
  ],
  queryFn: async () => {
    // Criar um objeto de parâmetros dinâmico para evitar erros de tipo
    const params: Record<string, any> = {
      page: currentPage.value,
    };
    
    // Adicionar parâmetros opcionais apenas quando existirem
    if (filterProjeto.value) params.projeto = filterProjeto.value;
    if (filterCategoria.value) params.categoria = filterCategoria.value;
    if (filterDataInicio.value) params.data__gte = filterDataInicio.value;
    if (filterDataFim.value) params.data__lte = filterDataFim.value;
    
    const response = await useCostsCustosList(params as any);
    return response.data;
  },
  retry: (failureCount, error: any) => {
    // Não tentar novamente para erros 401, 403 ou 404
    if (error?.response?.status === 401) {
      // Erro de autenticação - redirecionar para login
      router.push('/login');
      return false;
    }
    if ([403, 404].includes(error?.response?.status)) {
      return false;
    }
    return failureCount < 3;
  },
});

// Dados computados para a UI
const costs = computed(() => {
  if (!paginatedCosts) return [];
  return paginatedCosts.results || [];
});

const totalPages = computed(() => {
  if (!paginatedCosts || !paginatedCosts.count) return 1;
  return Math.ceil(paginatedCosts.count / pageSize);
});

// --- MUTAÇÕES (CRIAR, ATUALIZAR, DELETAR) ---

// 4. Mutação para CRIAR um custo
const createCostMutation = useCostsCustosCreate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Custo criado com sucesso!", type: "success" });
      queryClient.invalidateQueries({ queryKey: ["costs"] });
      closeModal();
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao criar o custo.",
        type: "error",
      });
    },
  },
});

// 5. Mutação para ATUALIZAR um custo
const updateCostMutation = useCostsCustosUpdate({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Custo atualizado com sucesso!", type: "success" });
      queryClient.invalidateQueries({ queryKey: ["costs"] });
      closeModal();
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Falha ao atualizar o custo.",
        type: "error",
      });
    },
  },
});

// 6. Mutação para DELETAR um custo
const deleteCostMutation = useCostsCustosDestroy({
  mutation: {
    onSuccess: () => {
      toast({ title: "Sucesso", description: "Custo excluído com sucesso!", type: "success" });
      queryClient.invalidateQueries({ queryKey: ["costs"] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description: err.response?.data?.detail || "Falha ao excluir o custo.",
        type: "error",
      });
    },
  },
});

// --- FUNÇÕES DE MANIPULAÇÃO ---

const openModal = async (cost: Custo | null = null) => {
  if (cost) {
    // Buscar detalhes do custo para edição usando o hook corretamente dentro de um try/catch
    try {
      // Chamar a API diretamente em vez de usar o hook Vue Query
      const response = await fetch(`/api/costs/custos/${cost.id}/`, {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        credentials: 'include', // Para enviar cookies de autenticação
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          router.push('/login');
          throw new Error('Não autenticado');
        }
        if (response.status === 403) {
          throw new Error('Acesso negado');
        }
        throw new Error(`Erro ${response.status}`);
      }
      
      const data = await response.json();
      editingCost.value = data as Custo;
      form.value = {
        descricao: data.descricao,
        projeto: data.projeto,
        valor: data.valor,
        data: data.data,
        tipo: data.tipo || "VARIAVEL",
        tarefa: data.tarefa || null,
        categoria: data.categoria || null,
      };
      showModal.value = true;
    } catch (err: any) {
      console.error("Erro ao buscar detalhes do custo:", err);
      toast({
        title: "Erro",
        description: err?.message || "Não foi possível carregar os detalhes do custo.",
        type: "error",
      });
      
      if (err?.message === 'Acesso negado') {
        toast({
          title: "Acesso negado",
          description: "Você não tem permissão para acessar este custo.",
          type: "error",
        });
      }
    }
  } else {
    editingCost.value = null;
    form.value = getInitialFormState();
    showModal.value = true;
  }
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

// --- EXPORTAÇÃO CSV ---
function exportarCSV() {
  const rows = [
    ["Descrição", "Projeto", "Valor", "Data", "Categoria"],
    ...costs.value.map((c: CostItem) => [
      c.descricao,
      c.projeto_nome,
      c.valor,
      formatDate(c.data),
      c.categoria_nome,
    ]),
  ];
  const csv = rows
    .map((r) => r.map((v: any) => `"${String(v || '').replace(/"/g, '""')}"`).join(","))
    .join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  saveAs(blob, `custos_${new Date().toISOString().slice(0, 10)}.csv`);
}

// --- TOASTS AJUSTADOS ---
function showToastSuccess(msg: string) {
  toast({ title: "Sucesso", description: msg, type: "success" });
}
function showToastError(msg: string) {
  toast({ title: "Erro", description: msg, type: "error" });
}

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

// Tipo para os itens da tabela de custos
type CostItem = {
  id: number;
  descricao: string;
  projeto: number;
  projeto_nome: string;
  valor: string;
  data: string;
  categoria?: number | null;
  categoria_nome?: string | null;
  [key: string]: any; // Para permitir outras propriedades
};

// Função para upload de comprovante (mock, ajuste conforme backend)
function onComprovanteChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (!file) return;
  // Aqui você deve fazer upload para o backend e obter a URL
  // Exemplo mock:
  const reader = new FileReader();
  reader.onload = () => {
    // Verificar se comprovante existe no tipo antes de atribuir
    if (form.value) {
      // @ts-ignore - Ignorando erro de tipo aqui já que comprovante pode não estar definido no tipo
      form.value.comprovante = reader.result as string;
    }
  };
  reader.readAsDataURL(file);
}
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <!-- FILTROS -->
    <div class="flex flex-col md:flex-row md:items-end gap-4 mb-6">
      <div class="flex-1">
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Projeto</label
        >
        <select
          v-model="filterProjeto"
          class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
        >
          <option :value="null">Todos</option>
          <option
            v-for="proj in projectsList?.results || []"
            :key="proj.id"
            :value="proj.id"
          >
            {{ proj.titulo }}
          </option>
        </select>
      </div>
      <div class="flex-1">
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Categoria</label
        >
        <select
          v-model="filterCategoria"
          class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
        >
          <option :value="null">Todas</option>
          <option
            v-for="cat in categoriasList?.results || []"
            :key="cat.id"
            :value="cat.id"
          >
            {{ cat.nome }}
          </option>
        </select>
      </div>
      <div class="flex-1">
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Data início</label
        >
        <input
          type="date"
          v-model="filterDataInicio"
          class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
        />
      </div>
      <div class="flex-1">
        <label
          class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Data fim</label
        >
        <input
          type="date"
          v-model="filterDataFim"
          class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
        />
      </div>
      <div class="flex-none">
        <button
          @click="refetch()"
          class="mt-6 px-4 py-2 bg-primary-600 text-white rounded-md shadow-sm hover:bg-primary-700"
        >
          Filtrar
        </button>
      </div>
      <div class="flex-none">
        <button
          @click="exportarCSV"
          class="mt-6 px-4 py-2 bg-green-600 text-white rounded-md shadow-sm hover:bg-green-700"
        >
          Exportar CSV
        </button>
      </div>
    </div>

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
      <table
        class="min-w-full divide-y divide-gray-300 dark:divide-gray-700 text-xs md:text-sm"
      >
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

    <!-- Modal para edição/criação de custo -->
    <transition name="modal">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 overflow-auto bg-black bg-opacity-30 flex items-center justify-center"
      >
        <div
          class="bg-white dark:bg-gray-800 rounded-lg shadow-lg max-w-lg w-full p-6"
        >
          <h2
            class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4"
          >
            {{ editingCost ? "Editar Custo" : "Novo Custo" }}
          </h2>
          <form @submit.prevent="handleSubmit">
            <div class="space-y-4">
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                  >Descrição</label
                >
                <input
                  v-model="form.descricao"
                  required
                  class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
                />
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                  >Projeto</label
                >
                <select
                  v-model="form.projeto"
                  required
                  class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
                >
                  <option value="">Selecione um projeto</option>
                  <option
                    v-for="proj in projectsList?.value?.results"
                    :key="proj.id"
                    :value="proj.id"
                  >
                    {{ proj.titulo }}
                  </option>
                </select>
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                  >Categoria</label
                >
                <select
                  v-model="form.categoria"
                  required
                  class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
                >
                  <option value="">Selecione uma categoria</option>
                  <option
                    v-for="cat in categoriasList?.value?.results"
                    :key="cat.id"
                    :value="cat.id"
                  >
                    {{ cat.nome }}
                  </option>
                </select>
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                  >Valor</label
                >
                <input
                  type="number"
                  v-model.number="form.valor"
                  required
                  class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
                />
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                  >Data</label
                >
                <input
                  type="date"
                  v-model="form.data"
                  required
                  class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
                />
              </div>
              <div>
                <label
                  class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                  >Tipo</label
                >
                <select
                  v-model="form.tipo"
                  class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700"
                >
                  <option value="VARIAVEL">Variável</option>
                  <option value="FIXO">Fixo</option>
                </select>
              </div>
              <!-- CAMPO DE UPLOAD NO MODAL (opcional, mock) -->
              <!--
              <div class="mt-4">
                <label for="comprovante" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Comprovante (opcional)</label>
                <input type="file" id="comprovante" @change="onComprovanteChange" class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 bg-white dark:bg-gray-700" />
                <div v-if="form.comprovante" class="mt-2">
                  <a :href="form.comprovante" target="_blank" class="text-blue-600 hover:underline">Arquivo atual</a>
                </div>
              </div>
              -->
            </div>
            <div class="mt-4 flex justify-end gap-2">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-md shadow-sm hover:bg-gray-300 dark:hover:bg-gray-600"
              >
                Cancelar
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-primary-600 text-white rounded-md shadow-sm hover:bg-primary-700"
              >
                Salvar
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>
