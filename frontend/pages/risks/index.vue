<!-- filepath: pages/risks/index.vue -->
<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery, useMutation, useQueryClient } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import {
  risksRiscosList,
  risksRiscosCreate,
  risksRiscosUpdate,
  risksRiscosDestroy,
  risksRiscosRetrieve,
} from "@/api/riscos/riscos";
import { projectsProjectsList } from "@/api/projetos/projetos";
import type {
  Risco,
  RiscoRequest,
  RiscoList,
  PaginatedRiscoList,
  PaginatedProjetoListList,
} from "@/api/schemas";

// --- HOOKS E ESTADO INICIAL ---
const queryClient = useQueryClient();
const { toast } = useToast();
const currentPage = ref(1);
const pageSize = 10;
const showModal = ref(false);
const editingRisk = ref<Risco | null>(null);

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

// Query para buscar a lista de riscos
const {
  data: paginatedRisks,
  isLoading,
  error,
  refetch,
} = useQuery<PaginatedRiscoList>({
  queryKey: ["risks", currentPage],
  queryFn: () =>
    risksRiscosList({ page: currentPage.value }).then((res) => res.data),
});

// Query para buscar projetos
const { data: projectsList } = useQuery<PaginatedProjetoListList>({
  queryKey: ["projectsForRisks"],
  queryFn: () => projectsProjectsList({ page: 1 }).then((res) => res.data),
  staleTime: 1000 * 60 * 5,
});

const risks = computed(() => paginatedRisks.value?.results || []);
const totalPages = computed(() =>
  paginatedRisks.value?.count
    ? Math.ceil(paginatedRisks.value.count / pageSize)
    : 1
);

// --- MUTAÇÕES ---
const createRiskMutation = useMutation({
  mutationFn: (payload: { data: RiscoRequest }) =>
    risksRiscosCreate(payload.data),
  onSuccess: () => {
    toast({
      title: "Sucesso",
      description: "Risco criado com sucesso!",
      type: "success",
    });
    queryClient.invalidateQueries({ queryKey: ["risks"] });
    closeModal();
  },
  onError: (err: any) => {
    toast({
      title: "Erro",
      description: err?.response?.data?.detail || "Falha ao criar risco.",
      type: "error",
    });
  },
});
const updateRiskMutation = useMutation({
  mutationFn: (payload: { id: number; data: RiscoRequest }) =>
    risksRiscosUpdate(payload.id, payload.data),
  onSuccess: () => {
    toast({
      title: "Sucesso",
      description: "Risco atualizado com sucesso!",
      type: "success",
    });
    queryClient.invalidateQueries({ queryKey: ["risks"] });
    closeModal();
  },
  onError: (err: any) => {
    toast({
      title: "Erro",
      description: err?.response?.data?.detail || "Falha ao atualizar risco.",
      type: "error",
    });
  },
});
const deleteMutation = useMutation({
  mutationFn: (payload: { id: number }) => risksRiscosDestroy(payload.id),
  onSuccess: () => {
    toast({
      title: "Sucesso",
      description: "Risco excluído com sucesso!",
      type: "success",
    });
    queryClient.invalidateQueries({ queryKey: ["risks"] });
  },
  onError: (err: any) => {
    toast({
      title: "Erro",
      description: err?.response?.data?.detail || "Falha ao excluir risco.",
      type: "error",
    });
  },
});

const openModal = async (risk: RiscoList | null = null) => {
  if (risk) {
    const res = await risksRiscosRetrieve(risk.id);
    const data = res.data;
    editingRisk.value = data;
    form.value = {
      descricao: data.descricao,
      projeto: data.projeto,
      probabilidade: data.probabilidade,
      impacto: data.impacto,
      status: data.status,
      responsavel_mitigacao: data.responsavel_mitigacao || null,
      plano_mitigacao: data.plano_mitigacao || null,
      plano_contingencia: data.plano_contingencia || null,
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
        class="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
      >
        <Icon icon="lucide:plus" class="h-5 w-5" />
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
                class="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
              >
                > Salvar
              </button>
              <button
                type="button"
                @click="closeModal"
                class="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 text-white text-sm font-semibold shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
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
