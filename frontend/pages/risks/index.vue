<!-- filepath: pages/risks/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";

// 1. Importar funções e tipos corretos do Orval
// 1. Importar funções e tipos corretos do Orval
import {
  useRisksRiscosList,
  useRisksRiscosCreate,
  useRisksRiscosUpdate,
  useRisksRiscosDestroy,
} from "@/api/riscos/riscos";
import { useProjectsProjectsList } from "@/api/projetos/projetos";
import type {
  Risco,
  RiscoRequest,
  RiscoList,
  PaginatedRiscoList,
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
const editingRisk = ref<RiscoList | null>(null);

const getInitialFormState = (): RiscoRequest => ({
  descricao: "",
  projeto: 0,
  probabilidade: "BAIXA",
  impacto: "BAIXO",
  status: "IDENTIFICADO",
  responsavel_mitigacao: null,
  plano_mitigacao: null,
  plano_contingencia: null,
});

const form = ref<RiscoRequest>(getInitialFormState());

// --- QUERIES ---
// 2. Query para buscar a lista de riscos
const {
  data: paginatedRisks,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedRiscoList>({
  queryKey: ["risks", currentPage],
  queryFn: () =>
    useRisksRiscosList({ page: currentPage.value, page_size: pageSize }).then(
      (res) => res.data
    ),
});

// 3. Query para buscar projetos para o modal
const { data: projectsList } = useQuery<PaginatedProjetoListList>({
  queryKey: ["projectsForRisks"],
  queryFn: () =>
    useProjectsProjectsList({ page_size: 100 }).then((res) => res.data),
  staleTime: 1000 * 60 * 5,
});

const risks = computed(() => paginatedRisks.value?.results || []);
const totalPages = computed(() =>
  paginatedRisks.value?.count
    ? Math.ceil(paginatedRisks.value.count / pageSize)
    : 1
);

// --- MUTAÇÕES ---
// 4. Mutações separadas para cada ação CRUD
const createRiskMutation = useRisksRiscosCreate({
  /* ... onSuccess/onError handlers ... */
});
const updateRiskMutation = useRisksRiscosUpdate({
  /* ... onSuccess/onError handlers ... */
});
const deleteMutation = useRisksRiscosDestroy({
  /* ... onSuccess/onError handlers ... */
});

// --- FUNÇÕES DE MANIPULAÇÃO ---
const openModal = (risk: RiscoList | null = null) => {
  if (risk) {
    editingRisk.value = risk;
    form.value = {
      descricao: risk.descricao,
      projeto: risk.projeto,
      probabilidade: risk.probabilidade,
      impacto: risk.impacto,
      status: risk.status,
      responsavel_mitigacao: (risk as any).responsavel_mitigacao || null,
      plano_mitigacao: (risk as any).plano_mitigacao || null,
      plano_contingencia: (risk as any).plano_contingencia || null,
    };
  } else {
    editingRisk.value = null;
    form.value = getInitialFormState();
  }
  showModal.value = true;
};

const closeModal = () => (showModal.value = false);

const handleSubmit = () => {
  if (editingRisk.value?.id) {
    updateRiskMutation.mutate({ id: editingRisk.value.id, data: form.value });
  } else {
    createRiskMutation.mutate({ data: form.value });
  }
};

const confirmDelete = (id: number) => {
  if (window.confirm("Tem certeza?")) {
    deleteMutation.mutate({ id });
  }
};

// --- FUNÇÕES DE ESTILO ---
const getStatusClass = (status?: RiscoList["status"]) => {
  const classes: Record<string, string> = {
    IDENTIFICADO:
      "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
    EM_ANALISE:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
    MITIGADO:
      "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
    ACEITO:
      "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
    ELIMINADO: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300",
  };
  return classes[status || ""] || "bg-gray-100 text-gray-800";
};

const getNivelRiscoClass = (nivel: string) => {
  const nivelNormalizado = nivel.toUpperCase();
  if (nivelNormalizado.includes("ALTO")) return "text-red-600 font-bold";
  if (nivelNormalizado.includes("MÉDIO"))
    return "text-yellow-600 font-semibold";
  if (nivelNormalizado.includes("BAIXO")) return "text-green-600";
  return "text-gray-600";
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">
        Gerenciamento de Riscos
      </h1>
      <button
        @click="openModal()"
        class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
      >
        <Icon icon="lucide:plus" class="mr-2 h-5 w-5" />
        Novo Risco
      </button>
    </div>

    <!-- Tabela de Riscos -->
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
      Erro ao carregar riscos.
    </div>
    <div
      v-else-if="risks.length === 0"
      class="text-center py-20 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg"
    >
      <Icon
        icon="lucide:shield-off"
        class="w-20 h-20 mx-auto text-gray-400 dark:text-gray-500"
      />
      <h3 class="mt-4 text-xl font-medium text-gray-800 dark:text-gray-200">
        Nenhum risco registrado
      </h3>
      <p class="mt-1 text-gray-500 dark:text-gray-400">
        Excelente! Continue monitorando seus projetos.
      </p>
    </div>

    <div
      v-else
      class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg"
    >
      <table class="min-w-full divide-y divide-gray-300 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th
              scope="col"
              class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 dark:text-gray-100 sm:pl-6"
            >
              Risco
            </th>
            <th
              scope="col"
              class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Projeto
            </th>
            <th
              scope="col"
              class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Nível de Risco
            </th>
            <th
              scope="col"
              class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-100"
            >
              Status
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
            v-for="risk in risks"
            :key="risk.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-700/50"
          >
            <td
              class="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 dark:text-gray-100 sm:w-auto sm:max-w-none sm:pl-6"
            >
              {{ risk.descricao }}
              <dl class="font-normal lg:hidden">
                <dt class="sr-only">Projeto</dt>
                <dd class="mt-1 truncate text-gray-700 dark:text-gray-300">
                  {{ risk.projeto_nome }}
                </dd>
              </dl>
            </td>
            <td
              class="hidden px-3 py-4 text-sm text-gray-500 dark:text-gray-300 lg:table-cell"
            >
              {{ risk.projeto_nome }}
            </td>
            <td
              class="px-3 py-4 text-sm font-medium"
              :class="getNivelRiscoClass(risk.nivel_risco)"
            >
              {{ risk.nivel_risco }}
            </td>
            <td class="px-3 py-4 text-sm">
              <span
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                :class="getStatusClass(risk.status)"
              >
                {{ risk.status_display }}
              </span>
            </td>
            <td class="py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
              <button
                @click.stop="openModal(risk)"
                class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300"
              >
                Editar
              </button>
              <button
                @click.stop="confirmDelete(risk.id)"
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
          :disabled="!paginatedRisks?.previous"
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
          :disabled="!paginatedRisks?.next"
          class="relative inline-flex items-center px-3 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          Próximo
        </button>
      </nav>
    </div>

    <!-- Risk Form Modal -->
    <div v-if="showModal" class="fixed z-50 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen">
        <div
          class="fixed inset-0 bg-gray-500 bg-opacity-75"
          @click="closeModal"
        ></div>
        <div
          class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full"
        >
          <form @submit.prevent="handleSubmit">
            <div class="px-4 pt-5 pb-4 sm:p-6">
              <h3
                class="text-lg leading-6 font-medium text-gray-900 dark:text-gray-100"
              >
                {{ editingRisk ? "Editar Risco" : "Novo Risco" }}
              </h3>
              <div class="mt-4 space-y-4">
                <div>
                  <label
                    for="descricao"
                    class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Descrição</label
                  >
                  <textarea
                    v-model="form.descricao"
                    id="descricao"
                    rows="3"
                    class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                    required
                  ></textarea>
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
                      for="probabilidade"
                      class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                      >Probabilidade</label
                    >
                    <select
                      v-model="form.probabilidade"
                      id="probabilidade"
                      class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                      required
                    >
                      <option value="BAIXA">Baixa</option>
                      <option value="MEDIA">Média</option>
                      <option value="ALTA">Alta</option>
                    </select>
                  </div>
                  <div>
                    <label
                      for="impacto"
                      class="block text-sm font-medium text-gray-700 dark:text-gray-300"
                      >Impacto</label
                    >
                    <select
                      v-model="form.impacto"
                      id="impacto"
                      class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm py-2 px-3 focus:ring-primary-500 focus:border-primary-500 bg-white dark:bg-gray-700"
                      required
                    >
                      <option value="BAIXO">Baixo</option>
                      <option value="MEDIO">Médio</option>
                      <option value="ALTO">Alto</option>
                    </select>
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
                  createRiskMutation.isPending.value ||
                  updateRiskMutation.isPending.value
                "
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                Salvar
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
