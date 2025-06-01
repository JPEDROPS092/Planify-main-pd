<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h3 class="text-xl font-semibold text-gray-700 dark:text-gray-200">
        Exportar Dados do Projeto
      </h3>
    </div>

    <div v-if="loading" class="space-y-4">
      <SkeletonLoader type="list-item-two-line" :count="3" />
    </div>
    <div
      v-else-if="error"
      class="text-center text-red-500 dark:text-red-400 py-6"
    >
      <p>{{ error.message || 'Erro ao carregar opções de exportação.' }}</p>
      <Button variant="outline" size="sm" class="mt-2" @click="initialize"
        >Tentar Novamente</Button
      >
    </div>
    <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Opções de exportação -->
        <div class="space-y-4">
          <h4 class="font-medium text-gray-700 dark:text-gray-300">
            Selecione os dados a exportar:
          </h4>

          <div class="space-y-2">
            <div class="flex items-center">
              <input
                type="checkbox"
                id="export-project-details"
                v-model="exportOptions.projectDetails"
                class="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="export-project-details"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                Detalhes do Projeto
              </label>
            </div>

            <div class="flex items-center">
              <input
                type="checkbox"
                id="export-tasks"
                v-model="exportOptions.tasks"
                class="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="export-tasks"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                Tarefas
              </label>
            </div>

            <div class="flex items-center">
              <input
                type="checkbox"
                id="export-team"
                v-model="exportOptions.team"
                class="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="export-team"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                Equipe
              </label>
            </div>

            <div class="flex items-center">
              <input
                type="checkbox"
                id="export-risks"
                v-model="exportOptions.risks"
                class="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="export-risks"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                Riscos
              </label>
            </div>

            <div class="flex items-center">
              <input
                type="checkbox"
                id="export-costs"
                v-model="exportOptions.costs"
                class="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="export-costs"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                Custos
              </label>
            </div>
          </div>
        </div>

        <!-- Formato de exportação -->
        <div class="space-y-4">
          <h4 class="font-medium text-gray-700 dark:text-gray-300">
            Formato de exportação:
          </h4>

          <div class="space-y-2">
            <div class="flex items-center">
              <input
                type="radio"
                id="format-csv"
                value="csv"
                v-model="exportFormat"
                class="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="format-csv"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                CSV (Excel, LibreOffice Calc)
              </label>
            </div>

            <div class="flex items-center">
              <input
                type="radio"
                id="format-json"
                value="json"
                v-model="exportFormat"
                class="h-4 w-4 text-blue-600 border-gray-300 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
              />
              <label
                for="format-json"
                class="ml-2 text-sm text-gray-700 dark:text-gray-300"
              >
                JSON (Formato de dados estruturado)
              </label>
            </div>
          </div>

          <div class="mt-6">
            <Button
              @click="exportData"
              :disabled="!isAnyOptionSelected || exporting"
              :loading="exporting"
              class="w-full md:w-auto"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              {{ exporting ? 'Exportando...' : 'Exportar Dados' }}
            </Button>
          </div>
        </div>
      </div>

      <div
        class="mt-6 text-sm text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700 pt-4"
      >
        <p class="mb-2">Notas:</p>
        <ul class="list-disc pl-5 space-y-1">
          <li>
            Os arquivos CSV podem ser abertos diretamente no Excel ou outros
            aplicativos de planilha.
          </li>
          <li>
            Os arquivos JSON são úteis para integração com outros sistemas ou
            para backup de dados.
          </li>
          <li>Selecione pelo menos uma opção para habilitar a exportação.</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, defineProps, toRefs } from 'vue';
import { useNotification } from '~/composables/useNotification';
import Button from '~/components/ui/Button.vue';
import SkeletonLoader from '~/components/SkeletonLoader.vue';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
});

const { projectId } = toRefs(props);
const {
  success: notifySuccess,
  error: notifyError,
  showApiError,
} = useNotification();

const loading = ref(false);
const exporting = ref(false);
const error = ref<Error | null>(null);
const exportFormat = ref('csv');

const exportOptions = ref({
  projectDetails: true,
  tasks: true,
  team: false,
  risks: false,
  costs: false,
});

const isAnyOptionSelected = computed(() => {
  return Object.values(exportOptions.value).some((value) => value === true);
});

// Inicializa o componente
async function initialize() {
  loading.value = true;
  error.value = null;

  try {
    // Aqui poderíamos carregar configurações de exportação do usuário, se necessário
    loading.value = false;
  } catch (err: any) {
    error.value = err;
    loading.value = false;
  }
}

// Função para exportar dados
async function exportData() {
  if (!isAnyOptionSelected.value) {
    notifyError('Selecione pelo menos uma opção para exportar.');
    return;
  }

  exporting.value = true;

  try {
    // Construir a URL com os parâmetros de exportação
    const params = new URLSearchParams();
    params.append('format', exportFormat.value);

    if (exportOptions.value.projectDetails)
      params.append('include_project', 'true');
    if (exportOptions.value.tasks) params.append('include_tasks', 'true');
    if (exportOptions.value.team) params.append('include_team', 'true');
    if (exportOptions.value.risks) params.append('include_risks', 'true');
    if (exportOptions.value.costs) params.append('include_costs', 'true');

    // Criar a URL completa
    const exportUrl = `/api/projects/projetos/${projectId.value}/export/?${params.toString()}`;

    // Iniciar o download
    const link = document.createElement('a');
    link.href = exportUrl;
    link.target = '_blank';
    link.download = `projeto_${projectId.value}_export.${exportFormat.value}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    notifySuccess('Exportação iniciada. O download começará em breve.');
  } catch (err: any) {
    showApiError(err);
  } finally {
    exporting.value = false;
  }
}

onMounted(() => {
  initialize();
});
</script>
