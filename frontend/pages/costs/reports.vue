<!-- filepath: pages/costs/reports.vue -->
<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Relatórios de Custos
      </h1>
      <p class="text-gray-600">
        Visualize e analise os custos do seu projeto através de diferentes
        perspectivas
      </p>
    </div>

    <!-- Navigation Tabs -->
    <div class="mb-6">
      <nav class="flex space-x-8" aria-label="Tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            activeTab === tab.id
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
            'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm',
          ]"
        >
          <Icon :icon="tab.icon" class="w-5 h-5 mr-2 inline" />
          {{ tab.name }}
        </button>
      </nav>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div
        class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"
      ></div>
      <span class="ml-3 text-gray-600">Carregando relatórios...</span>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-50 border border-red-200 rounded-md p-4 mb-6"
    >
      <div class="flex">
        <Icon
          icon="heroicons:exclamation-triangle"
          class="h-5 w-5 text-red-400"
        />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">
            Erro ao carregar relatórios
          </h3>
          <p class="mt-1 text-sm text-red-700">
            {{
              error?.value?.message ||
              error?.message ||
              "Ocorreu um erro inesperado"
            }}
          </p>
          <button
            @click="refetchData"
            class="mt-2 text-sm bg-red-100 text-red-800 px-3 py-1 rounded hover:bg-red-200"
          >
            Tentar novamente
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div v-else class="space-y-6">
      <!-- Relatório Mensal -->
      <div
        v-if="activeTab === 'monthly'"
        class="bg-white rounded-lg shadow p-6"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-gray-900">Relatório Mensal</h2>
          <button
            @click="exportReport('monthly')"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <Icon icon="heroicons:arrow-down-tray" class="w-4 h-4 mr-2" />
            Exportar
          </button>
        </div>

        <div
          v-if="monthlyReport.value && monthlyReport.value.data"
          class="space-y-6"
        >
          <!-- Resumo Geral -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-blue-50 p-4 rounded-lg">
              <div class="flex items-center">
                <Icon
                  icon="heroicons:currency-dollar"
                  class="h-8 w-8 text-blue-600"
                />
                <div class="ml-3">
                  <p class="text-sm font-medium text-blue-600">Total Gasto</p>
                  <p class="text-2xl font-bold text-blue-900">
                    {{
                      formatCurrency(monthlyReport.value.data.total_gasto || 0)
                    }}
                  </p>
                </div>
              </div>
            </div>
            <div class="bg-green-50 p-4 rounded-lg">
              <div class="flex items-center">
                <Icon
                  icon="heroicons:chart-bar"
                  class="h-8 w-8 text-green-600"
                />
                <div class="ml-3">
                  <p class="text-sm font-medium text-green-600">
                    Número de Custos
                  </p>
                  <p class="text-2xl font-bold text-green-900">
                    {{ monthlyReport.value.data.total_custos || 0 }}
                  </p>
                </div>
              </div>
            </div>
            <div class="bg-purple-50 p-4 rounded-lg">
              <div class="flex items-center">
                <Icon
                  icon="heroicons:calendar"
                  class="h-8 w-8 text-purple-600"
                />
                <div class="ml-3">
                  <p class="text-sm font-medium text-purple-600">Período</p>
                  <p class="text-lg font-bold text-purple-900">
                    {{ getCurrentMonth() }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Gráfico Mensal -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Gastos por Mês
            </h3>
            <div class="h-64 flex items-center justify-center">
              <MonthlyChart
                v-if="monthlyReport.value.data.gastos_por_mes"
                :data="monthlyReport.value.data.gastos_por_mes"
              />
              <p v-else class="text-gray-500">
                Nenhum dado disponível para exibir
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Relatório por Categoria -->
      <div
        v-if="activeTab === 'category'"
        class="bg-white rounded-lg shadow p-6"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-gray-900">
            Relatório por Categoria
          </h2>
          <button
            @click="exportReport('category')"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <Icon icon="heroicons:arrow-down-tray" class="w-4 h-4 mr-2" />
            Exportar
          </button>
        </div>

        <div
          v-if="categoryReport.value && categoryReport.value.data"
          class="space-y-6"
        >
          <!-- Tabela de Categorias -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Categoria
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Total Gasto
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Número de Custos
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Percentual
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="item in categoryReport.value.data.gastos_por_categoria"
                  :key="item.categoria_nome"
                >
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                  >
                    {{ item.categoria_nome || "Sem categoria" }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatCurrency(item.total_gasto) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ item.total_custos }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center">
                      <div class="w-16 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          class="bg-blue-600 h-2 rounded-full"
                          :style="{ width: `${item.percentual || 0}%` }"
                        ></div>
                      </div>
                      {{ (item.percentual || 0).toFixed(1) }}%
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Gráfico de Pizza -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Distribuição por Categoria
            </h3>
            <div class="h-64 flex items-center justify-center">
              <CategoryChart
                v-if="categoryReport.value.data.gastos_por_categoria"
                :data="categoryReport.value.data.gastos_por_categoria"
              />
              <p v-else class="text-gray-500">
                Nenhum dado disponível para exibir
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Relatório por Projeto -->
      <div
        v-if="activeTab === 'project'"
        class="bg-white rounded-lg shadow p-6"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-semibold text-gray-900">
            Relatório por Projeto
          </h2>
          <button
            @click="exportReport('project')"
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          >
            <Icon icon="heroicons:arrow-down-tray" class="w-4 h-4 mr-2" />
            Exportar
          </button>
        </div>

        <div
          v-if="projectReport.value && projectReport.value.data"
          class="space-y-6"
        >
          <!-- Tabela de Projetos -->
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Projeto
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Total Gasto
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Orçamento
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Utilização
                  </th>
                  <th
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Status
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="item in projectReport.value.data.gastos_por_projeto"
                  :key="item.projeto_nome"
                >
                  <td
                    class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                  >
                    {{ item.projeto_nome }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatCurrency(item.total_gasto) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatCurrency(item.orcamento || 0) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <div class="flex items-center">
                      <div class="w-16 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          class="h-2 rounded-full"
                          :class="
                            getUtilizationColor(item.percentual_utilizado)
                          "
                          :style="{
                            width: `${Math.min(item.percentual_utilizado || 0, 100)}%`,
                          }"
                        ></div>
                      </div>
                      {{ (item.percentual_utilizado || 0).toFixed(1) }}%
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                      :class="getStatusColor(item.percentual_utilizado)"
                    >
                      {{ getStatusText(item.percentual_utilizado) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Gráfico de Barras -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              Gastos por Projeto
            </h3>
            <div class="h-64 flex items-center justify-center">
              <ProjectChart
                v-if="projectReport.value.data.gastos_por_projeto"
                :data="projectReport.value.data.gastos_por_projeto"
              />
              <p v-else class="text-gray-500">
                Nenhum dado disponível para exibir
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { Icon } from "@iconify/vue";
import { useToast } from "@/composables/useToast";
import { saveAs } from "file-saver";
import { definePageMeta } from "#imports";

// Importar as funções de relatório da API
import {
  useCostsCustosRelatorioMensalRetrieve,
  useCostsCustosRelatorioPorCategoriaRetrieve,
  useCostsCustosRelatorioPorProjetoRetrieve,
} from "@/api/custo/custo";

// Importar componentes de gráfico (você precisará criar estes)
import MonthlyChart from "@/components/charts/MonthlyChart.vue";
import CategoryChart from "@/components/charts/CategoryChart.vue";
import ProjectChart from "@/components/charts/ProjectChart.vue";

// Definir metadata da página
definePageMeta({
  middleware: "auth",
});

const { toast } = useToast();
const activeTab = ref("monthly");
const tabs = [
  { id: "monthly", name: "Mensal", icon: "heroicons:calendar-days" },
  { id: "category", name: "Por Categoria", icon: "heroicons:tag" },
  { id: "project", name: "Por Projeto", icon: "heroicons:folder" },
];

const {
  data: monthlyReport,
  isLoading: isLoadingMonthly,
  error: errorMonthly,
  refetch: refetchMonthly,
} = useCostsCustosRelatorioMensalRetrieve();
const {
  data: categoryReport,
  isLoading: isLoadingCategory,
  error: errorCategory,
  refetch: refetchCategory,
} = useCostsCustosRelatorioPorCategoriaRetrieve();
const {
  data: projectReport,
  isLoading: isLoadingProject,
  error: errorProject,
  refetch: refetchProject,
} = useCostsCustosRelatorioPorProjetoRetrieve();

const isLoading = computed(() => {
  switch (activeTab.value) {
    case "monthly":
      return isLoadingMonthly.value;
    case "category":
      return isLoadingCategory.value;
    case "project":
      return isLoadingProject.value;
    default:
      return false;
  }
});
const error = computed(() => {
  switch (activeTab.value) {
    case "monthly":
      return errorMonthly.value;
    case "category":
      return errorCategory.value;
    case "project":
      return errorProject.value;
    default:
      return null;
  }
});

const formatCurrency = (value: number | string) => {
  const numberValue = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(numberValue)) return "R$ 0,00";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(numberValue);
};
const getCurrentMonth = () => {
  return new Date().toLocaleDateString("pt-BR", {
    month: "long",
    year: "numeric",
  });
};
const getUtilizationColor = (percentage: number) => {
  if (percentage >= 90) return "bg-red-500";
  if (percentage >= 75) return "bg-yellow-500";
  return "bg-green-500";
};
const getStatusColor = (percentage: number) => {
  if (percentage >= 90) return "bg-red-100 text-red-800";
  if (percentage >= 75) return "bg-yellow-100 text-yellow-800";
  return "bg-green-100 text-green-800";
};
const getStatusText = (percentage: number) => {
  if (percentage >= 100) return "Excedido";
  if (percentage >= 90) return "Crítico";
  if (percentage >= 75) return "Atenção";
  return "Normal";
};
const refetchData = () => {
  switch (activeTab.value) {
    case "monthly":
      refetchMonthly();
      break;
    case "category":
      refetchCategory();
      break;
    case "project":
      refetchProject();
      break;
  }
};
const exportReport = (type: string) => {
  let data: any;
  let filename: string;
  switch (type) {
    case "monthly":
      data = monthlyReport.value?.data;
      filename = `relatorio_mensal_${new Date().toISOString().slice(0, 10)}.json`;
      break;
    case "category":
      data = categoryReport.value?.data;
      filename = `relatorio_categoria_${new Date().toISOString().slice(0, 10)}.json`;
      break;
    case "project":
      data = projectReport.value?.data;
      filename = `relatorio_projeto_${new Date().toISOString().slice(0, 10)}.json`;
      break;
    default:
      return;
  }
  if (data) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    saveAs(blob, filename);
    toast({
      title: "Sucesso",
      description: "Relatório exportado com sucesso!",
      type: "success",
    });
  } else {
    toast({
      title: "Erro",
      description: "Nenhum dado disponível para exportar.",
      type: "error",
    });
  }
};
</script>

<style scoped>
/* Estilos adicionais se necessário */
</style>
