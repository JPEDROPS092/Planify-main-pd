<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Custos do Projeto
      </h3>
      <Button @click="openCreateCostModal" size="sm" v-if="canManageCosts">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class_name="h-4 w-4 mr-1.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 4v16m8-8H4"
          />
        </svg>
        Novo Custo
      </Button>
    </div>

    <!-- Resumo dos Custos -->
    <div class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
        <h4 class_name="text-sm font-medium text-gray-500 dark:text-gray-400">
          Orçamento Total
        </h4>
        <p class_name="text-2xl font-semibold text-gray-800 dark:text-white">
          {{ formatCurrency(projectDetails?.budget || 0) }}
        </p>
      </div>
      <div class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
        <h4 class_name="text-sm font-medium text-gray-500 dark:text-gray-400">
          Custo Total Realizado
        </h4>
        <p class_name="text-2xl font-semibold text-gray-800 dark:text-white">
          {{ formatCurrency(totalRealizedCost) }}
        </p>
      </div>
      <div class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
        <h4 class_name="text-sm font-medium text-gray-500 dark:text-gray-400">
          Saldo Restante
        </h4>
        <p class_name="text-2xl font-semibold" :class_name="balanceClass">
          {{ formatCurrency(remainingBalance) }}
        </p>
      </div>
    </div>

    <div v-if="loadingCosts" class_name="space-y-4">
      <SkeletonLoader type="table-row" :count="3" />
    </div>
    <div
      v-else-if="costsError"
      class_name="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ costsError.message || 'Erro ao carregar custos.' }}</p>
      <Button variant="outline" size="sm" class_name="mt-2" @click="fetchCosts"
        >Tentar Novamente</Button
      >
    </div>
    <div
      v-else-if="costs.length === 0"
      class_name="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhum custo registrado para este projeto ainda.</p>
      <p class_name="text-sm" v-if="canManageCosts">
        Registre o primeiro custo clicando em "Novo Custo".
      </p>
    </div>
    <div v-else class_name="overflow-x-auto">
      <table
        class_name="min-w-full divide-y divide-gray-200 dark:divide-gray-700"
      >
        <thead class_name="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th
              scope="col"
              class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              Descrição
            </th>
            <th
              scope="col"
              class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              Categoria
            </th>
            <th
              scope="col"
              class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              Valor
            </th>
            <th
              scope="col"
              class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
            >
              Data
            </th>
            <th
              scope="col"
              class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider"
              v-if="canManageCosts"
            >
              Ações
            </th>
          </tr>
        </thead>
        <tbody
          class_name="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700"
        >
          <tr v-for="cost in costs" :key="cost.id">
            <td
              class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white"
            >
              {{ cost.description }}
            </td>
            <td
              class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ cost.category }}
            </td>
            <td
              class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ formatCurrency(cost.amount) }}
            </td>
            <td
              class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300"
            >
              {{ formatDate(cost.date) }}
            </td>
            <td
              class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
              v-if="canManageCosts"
            >
              <div class_name="flex items-center space-x-2">
                <Button
                  variant="ghost"
                  size="icon-sm"
                  @click="openEditCostModal(cost)"
                  title="Editar Custo"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class_name="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                </Button>
                <Button
                  variant="ghost"
                  size="icon-sm"
                  @click="confirmDeleteCost(cost.id)"
                  title="Excluir Custo"
                  class_name="text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class_name="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </Button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para Criar/Editar Custo -->
    <Modal
      :is-open="showCostFormModal"
      @close="closeCostModal"
      :title="editingCost ? 'Editar Custo' : 'Registrar Novo Custo'"
    >
      <CostForm
        :project-id="projectId"
        :cost="editingCost"
        @submit="handleCostFormSubmit"
        @cancel="closeCostModal"
        :key="costFormKey"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, toRefs, computed } from 'vue';
import { useCostService } from '~/services/api/services/costService';
import type { Custo, CustoCreate, CustoUpdate } from '~/services/api/types'; // Tipos atualizados
import { useProjectService } from '~/services/api/services/projectService';
import type { Projeto } from '~/services/api/types';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/stores/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import Modal from '~/components/Modal.vue';
import CostForm from '~/components/CostForm.vue'; // Assumindo que você criará este componente
import SkeletonLoader from '~/components/SkeletonLoader.vue';
import { formatCurrency, formatDate } from '~/utils/formatters'; // Utilitários de formatação

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const { projectId } = toRefs(props);
const costService = useCostService();
const projectService = useProjectService();
const { user: currentUser, hasPermission } = useAuth();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
  confirm,
} = useNotification();

const costs = ref<Cost[]>([]);
const loadingCosts = ref(true);
const costsError = ref<Error | null>(null);
const projectDetails = ref<Project | null>(null);

const showCostFormModal = ref(false);
const editingCost = ref<Cost | null>(null);
const costFormKey = ref(0);

const canManageCosts = computed(() => {
  // Adapte conforme suas regras de permissão (ex: 'manage_project_costs')
  return (
    hasPermission('add_cost') ||
    hasPermission('change_cost') ||
    hasPermission('delete_cost')
  );
});

const totalRealizedCost = computed(() => {
  if (!Array.isArray(costs.value)) {
    return 0;
  }
  return costs.value.reduce((sum, cost) => sum + Number(cost.amount), 0);
});

const remainingBalance = computed(() => {
  return (projectDetails.value?.budget || 0) - totalRealizedCost.value;
});

const balanceClass = computed(() => {
  if (remainingBalance.value < 0) return 'text-red-500 dark:text-red-400';
  if (remainingBalance.value < (projectDetails.value?.budget || 0) * 0.1)
    return 'text-yellow-500 dark:text-yellow-400';
  return 'text-green-500 dark:text-green-400';
});

async function fetchProjectDetails() {
  if (!projectId.value) return;
  try {
    projectDetails.value = await projectService.getById(projectId.value);
  } catch (error) {
    console.error('Falha ao buscar detalhes do projeto para custos:', error);
    // Não necessariamente um erro fatal para a lista de custos, mas impede cálculo de orçamento
  }
}

async function fetchCosts() {
  if (!projectId.value) return;
  loadingCosts.value = true;
  costsError.value = null;
  try {
    const result = await costService.getByProject(projectId.value);
    if (Array.isArray(result)) {
      costs.value = result;
    } else if (result && Array.isArray(result.results)) {
      costs.value = result.results;
    } else {
      costs.value = []; // Fallback para array vazio
      console.warn(
        'ProjectCosts: Resposta inesperada ao buscar custos:',
        result
      );
    }
  } catch (error: any) {
    costsError.value = error;
    showApiError(error, 'Falha ao carregar custos');
    costs.value = []; // Garantir que seja um array em caso de erro
  } finally {
    loadingCosts.value = false;
  }
}

function openCreateCostModal() {
  editingCost.value = null;
  costFormKey.value++;
  showCostFormModal.value = true;
}

function openEditCostModal(cost: Custo) {
  editingCost.value = { ...cost };
  costFormKey.value++;
  showCostFormModal.value = true;
}

function closeCostModal() {
  showCostFormModal.value = false;
  editingCost.value = null;
  costFormKey.value++;
}

async function handleCostFormSubmit(formData: CustoCreate | CustoUpdate) {
  try {
    if (editingCost.value && editingCost.value.id) {
      await costService.update(editingCost.value.id, formData as CustoUpdate);
      notifySuccess('Custo atualizado com sucesso!');
    } else {
      const payload = { ...formData, projeto: projectId.value } as CustoCreate;
      await costService.create(payload);
      notifySuccess('Custo registrado com sucesso!');
    }
    await fetchCosts(); // Recarrega a lista de custos
    await fetchProjectDetails(); // Recarrega detalhes do projeto para atualizar orçamento
    closeCostModal();
  } catch (error: any) {
    showApiError(
      error,
      editingCost.value
        ? 'Falha ao atualizar custo'
        : 'Falha ao registrar custo'
    );
  }
}

async function confirmDeleteCost(costId?: number) {
  if (!costId) return;
  const confirmed = await confirm(
    'Excluir Custo',
    'Tem certeza que deseja excluir este registro de custo? Esta ação não pode ser desfeita.',
    {
      confirmButtonText: 'Excluir',
      cancelButtonText: 'Cancelar',
      type: 'danger',
    }
  );
  if (confirmed) {
    try {
      await costService.remove(costId);
      notifySuccess('Custo excluído com sucesso!');
      await fetchCosts();
      await fetchProjectDetails(); // Recarrega detalhes do projeto para atualizar orçamento
    } catch (error: any) {
      showApiError(error, 'Falha ao excluir custo');
    }
  }
}

watch(
  projectId,
  (newProjectId) => {
    if (newProjectId) {
      fetchProjectDetails();
      fetchCosts();
    }
  },
  { immediate: true }
);
</script>

<style scoped>
/* Estilos específicos para este componente */
</style>
