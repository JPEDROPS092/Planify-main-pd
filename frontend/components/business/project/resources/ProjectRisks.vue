<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Riscos do Projeto
      </h3>
      <Button @click="openCreateRiskModal" size="sm" v-if="canManageRisks">
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
        Novo Risco
      </Button>
    </div>

    <div v-if="loadingRisks" class_name="space-y-4">
      <SkeletonLoader type="list-item-two-line" :count="3" />
    </div>
    <div
      v-else-if="risksError"
      class_name="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ risksError.message || 'Erro ao carregar riscos.' }}</p>
      <Button variant="outline" size="sm" class_name="mt-2" @click="fetchRisks"
        >Tentar Novamente</Button
      >
    </div>
    <div
      v-else-if="risks.length === 0"
      class_name="text-center text-gray-500 dark:text-gray-400 py-6"
    >
      <p>Nenhum risco identificado para este projeto ainda.</p>
      <p class_name="text-sm" v-if="canManageRisks">
        Crie o primeiro risco clicando em "Novo Risco".
      </p>
    </div>
    <div v-else class_name="space-y-3">
      <div
        v-for="risk in risks"
        :key="risk.id"
        class_name="bg-white dark:bg-gray-800 p-4 rounded-lg shadow hover:shadow-md transition-shadow"
      >
        <div class_name="flex justify-between items-start">
          <div>
            <h4 class_name="text-lg font-medium text-gray-800 dark:text-white">
              {{ risk.name }}
            </h4>
            <p class_name="text-sm text-gray-600 dark:text-gray-400 mt-1">
              {{ risk.description }}
            </p>
            <div
              class_name="mt-2 flex items-center space-x-3 text-xs text-gray-500 dark:text-gray-400 flex-wrap"
            >
              <span class_name="mr-2 mb-1"
                >Impacto:
                <span
                  :class_name="getImpactClass(risk.impact)"
                  class_name="font-semibold py-0.5 px-1.5 rounded-full"
                  >{{ risk.impact }}</span
                ></span
              >
              <span class_name="mr-2 mb-1"
                >Probabilidade:
                <span
                  :class_name="getProbabilityClass(risk.probability)"
                  class_name="font-semibold py-0.5 px-1.5 rounded-full"
                  >{{ risk.probability }}</span
                ></span
              >
              <span class_name="mr-2 mb-1"
                >Status:
                <span
                  :class_name="getStatusClass(risk.status)"
                  class_name="font-semibold py-0.5 px-1.5 rounded-full"
                  >{{ risk.status }}</span
                ></span
              >
              <span v-if="risk.assignee_details"
                >Responsável:
                {{
                  risk.assignee_details.first_name ||
                  risk.assignee_details.username
                }}</span
              >
            </div>
            <p
              v-if="risk.mitigation_plan"
              class_name="text-sm text-gray-500 dark:text-gray-300 mt-2"
            >
              <strong class_name="font-medium">Plano de Mitigação:</strong>
              {{ risk.mitigation_plan }}
            </p>
          </div>
          <div class_name="flex space-x-1" v-if="canManageRisks">
            <Button
              variant="ghost"
              size="icon-sm"
              @click="openEditRiskModal(risk)"
              title="Editar Risco"
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
              @click="confirmDeleteRisk(risk.id)"
              title="Excluir Risco"
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
        </div>
      </div>
    </div>

    <!-- Modal para Criar/Editar Risco -->
    <Modal
      :is-open="showRiskFormModal"
      @close="closeRiskModal"
      :title="editingRisk ? 'Editar Risco' : 'Registrar Novo Risco'"
    >
      <RiskForm
        :project-id="projectId"
        :risk="editingRisk"
        @submit="handleRiskFormSubmit"
        @cancel="closeRiskModal"
        :key="riskFormKey"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, defineProps, toRefs, computed } from 'vue';
import { useRiskService } from '~/services/api/services/riskService';
import type { Risco, RiscoCreate, RiscoUpdate } from '~/services/api/types'; // Tipos atualizados
import { useUserService } from '~/services/api/userService';
import type { User } from '~/services/api/types';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/stores/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import Modal from '~/components/Modal.vue';
import RiskForm from '~/components/RiskForm.vue'; // Assumindo que você criará este componente
import SkeletonLoader from '~/components/SkeletonLoader.vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const { projectId } = toRefs(props);
const riskService = useRiskService();
const userService = useUserService();
const { user: currentUser, hasPermission } = useAuth();
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
  confirm,
} = useNotification();

const risks = ref<Risk[]>([]);
const loadingRisks = ref(true);
const risksError = ref<Error | null>(null);
const showRiskFormModal = ref(false);
const editingRisk = ref<Risk | null>(null);
const riskFormKey = ref(0);

const canManageRisks = computed(() => {
  // Adapte conforme suas regras de permissão (ex: 'manage_project_risks')
  return (
    hasPermission('add_risk') ||
    hasPermission('change_risk') ||
    hasPermission('delete_risk')
  );
});

async function fetchRisks() {
  if (!projectId.value) return;
  loadingRisks.value = true;
  risksError.value = null;
  try {
    const result = await riskService.getByProject(projectId.value);
    let riskListToProcess: Risk[] = [];
    if (Array.isArray(result)) {
      riskListToProcess = result;
    } else if (result && Array.isArray(result.results)) {
      riskListToProcess = result.results;
    } else {
      // riskListToProcess já é [], mas adiciona um log para depuração
      console.warn(
        'ProjectRisks: Resposta inesperada ao buscar riscos:',
        result
      );
    }

    risks.value = await Promise.all(
      riskListToProcess.map(async (risk: any) => {
        let assigneeDetails: User | null = null;
        if (risk.assignee) {
          try {
            assigneeDetails = await userService.getUserById(risk.assignee);
          } catch (e) {
            console.warn(
              `Falha ao buscar detalhes do usuário ${risk.assignee}`,
              e
            );
          }
        }
        return { ...risk, assignee_details: assigneeDetails };
      })
    );
  } catch (error: any) {
    risksError.value = error;
    showApiError(error, 'Falha ao carregar riscos');
  } finally {
    loadingRisks.value = false;
  }
}

function openCreateRiskModal() {
  editingRisk.value = null;
  riskFormKey.value++;
  showRiskFormModal.value = true;
}

function openEditRiskModal(risk: Risk) {
  editingRisk.value = { ...risk };
  riskFormKey.value++;
  showRiskFormModal.value = true;
}

function closeRiskModal() {
  showRiskFormModal.value = false;
  editingRisk.value = null;
  riskFormKey.value++;
}

async function handleRiskFormSubmit(formData: RiskCreate | RiskUpdate) {
  try {
    if (editingRisk.value && editingRisk.value.id) {
      await riskService.update(editingRisk.value.id, formData as RiskUpdate);
      notifySuccess('Risco atualizado com sucesso!');
    } else {
      const payload = { ...formData, project: projectId.value } as RiskCreate;
      await riskService.create(payload);
      notifySuccess('Risco registrado com sucesso!');
    }
    await fetchRisks();
    closeRiskModal();
  } catch (error: any) {
    showApiError(
      error,
      editingRisk.value
        ? 'Falha ao atualizar risco'
        : 'Falha ao registrar risco'
    );
  }
}

async function confirmDeleteRisk(riskId?: number) {
  if (!riskId) return;
  const confirmed = await confirm(
    'Excluir Risco',
    'Tem certeza que deseja excluir este risco? Esta ação não pode ser desfeita.',
    {
      confirmButtonText: 'Excluir',
      cancelButtonText: 'Cancelar',
      type: 'danger',
    }
  );
  if (confirmed) {
    try {
      await riskService.remove(riskId);
      notifySuccess('Risco excluído com sucesso!');
      await fetchRisks();
    } catch (error: any) {
      showApiError(error, 'Falha ao excluir risco');
    }
  }
}

// Funções de formatação para classes CSS (exemplo)
const getImpactClass = (impact?: string) => {
  switch (impact?.toLowerCase()) {
    case 'alto':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
    case 'médio':
    case 'medio':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    case 'baixo':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  }
};

const getProbabilityClass = (probability?: string) => {
  switch (probability?.toLowerCase()) {
    case 'alta':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
    case 'média':
    case 'media':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    case 'baixa':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  }
};

const getStatusClass = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'aberto':
    case 'identificado':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
    case 'em progresso':
    case 'em andamento':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
    case 'mitigado':
    case 'resolvido':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
    case 'fechado':
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
  }
};

watch(
  projectId,
  (newProjectId) => {
    if (newProjectId) {
      fetchRisks();
    }
  },
  { immediate: true }
);
</script>

<style scoped>
/* Estilos específicos para este componente */
</style>
