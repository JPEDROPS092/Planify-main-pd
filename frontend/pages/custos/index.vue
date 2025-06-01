<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1
          class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
        >
          Custos
        </h1>
        <button
          @click="openNewCostModal"
          class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
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
          Novo Custo
        </button>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar custos..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
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
            class="absolute right-3 top-2.5 h-4 w-4 text-gray-400 dark:text-gray-500"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"></path>
            <path d="M12 18V6"></path>
          </svg>
        </div>
        <select
          v-model="categoryFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todas as categorias</option>
          <option value="PESSOAL">Pessoal</option>
          <option value="MATERIAL">Material</option>
          <option value="EQUIPAMENTO">Equipamento</option>
          <option value="SERVICO">Serviço</option>
          <option value="LICENCA">Licença</option>
          <option value="OUTRO">Outro</option>
        </select>
        <select
          v-model="statusFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os status</option>
          <option value="PREVISTO">Previsto</option>
          <option value="APROVADO">Aprovado</option>
          <option value="PAGO">Pago</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
        <select
          v-model="projectFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
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

      <!-- Loading e estados vazios -->
      <div
        v-if="loading"
        class="flex flex-col items-center justify-center py-12"
      >
        <div
          class="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
        ></div>
        <p class="mt-4 text-sm text-gray-500 dark:text-gray-400">
          Carregando custos...
        </p>
      </div>

      <EmptyState
        v-else-if="filteredCosts.length === 0"
        title="Nenhum custo encontrado"
        description="Não encontramos nenhum custo com os filtros atuais. Tente ajustar os filtros ou registre um novo custo."
        icon="dollar-sign"
      >
        <template #action>
          <button
            @click="openNewCostModal"
            class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600"
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
            Criar Custo
          </button>
        </template>
      </EmptyState>

      <div v-else>
        <div class="overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700">
          <div v-if="loading" class="p-4">
            <TableSkeleton :rows="5" :showCheckbox="true" :showDescription="true" :showPagination="true" />
          </div>
          <table class="w-full border-collapse text-left">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Descrição
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Categoria
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Projeto
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Valor
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Status
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Data
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Data
                </th>
                <th
                  scope="col"
                  class="px-4 py-3 text-sm font-medium text-gray-500 dark:text-gray-400"
                >
                  Ações
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
              <tr
                v-for="(custo, index) in custos"
                :key="getUniqueKey(custo, index, 'custo')"
                class="hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                <td class="px-4 py-3 text-sm">
                  <div class="font-medium text-gray-900 dark:text-white">
                    {{ custo.descricao }}
                  </div>
                  <div
                    v-if="custo.observacoes"
                    class="mt-1 line-clamp-1 text-xs text-gray-500 dark:text-gray-400"
                  >
                    {{ custo.observacoes }}
                  </div>
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300':
                        custo.categoria === 'PESSOAL',
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300':
                        custo.categoria === 'MATERIAL',
                      'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300':
                        custo.categoria === 'EQUIPAMENTO',
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300':
                        custo.categoria === 'SERVICO',
                      'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300':
                        custo.categoria === 'LICENCA',
                      'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300':
                        custo.categoria === 'OUTRO',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getCategoryLabel(custo.categoria) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                  {{ getProjectName(custo.projeto) }}
                </td>
                <td
                  class="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white"
                >
                  {{ formatCurrency(custo.valor) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <span
                    :class="{
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300':
                        custo.status === 'PREVISTO',
                      'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300':
                        custo.status === 'APROVADO',
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300':
                        custo.status === 'PAGO',
                      'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300':
                        custo.status === 'CANCELADO',
                    }"
                    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium"
                  >
                    {{ getStatusLabel(custo.status) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                  {{ formatDate(custo.data) }}
                </td>
                <td class="px-4 py-3 text-sm">
                  <div class="flex items-center space-x-2">
                    <button
                      @click="editCost(custo)"
                      class="rounded-md p-1 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
                      title="Editar"
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
                          d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"
                        ></path>
                      </svg>
                    </button>
                    <button
                      @click="viewCost(custo.id)"
                      class="rounded-md p-1 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900"
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
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50 dark:border-gray-700 dark:text-gray-400"
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
              ? 'bg-blue-600 text-white dark:bg-blue-700 dark:text-white'
              : 'border border-gray-300 text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700'
          "
          @click="changePage(page)"
        >
          {{ page }}
        </div>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="inline-flex h-9 w-9 items-center justify-center rounded-md border border-gray-300 text-sm font-medium text-gray-700 disabled:opacity-50 dark:border-gray-700 dark:text-gray-400"
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
    </div>
    
    <!-- Modal para criação/edição de custo -->
    <Modal 
      v-model="showCostModal" 
      title="Gerenciar Custo" 
      size="lg"
    >
      <LazyWrapper type="form">
        <CostForm
          :projectId="selectedProjectId"
          :cost="selectedCost"
          @submit="handleCostSubmit"
          @cancel="showCostModal = false"
        />
      </LazyWrapper>
    </Modal>
  </NuxtLayout>
  <!-- ... -->
</template>

<script setup lang="ts">
  import { ref, computed, watch, onMounted, defineAsyncComponent, shallowRef } from 'vue';
  import { getUniqueKey, debounce, createShallowState } from '~/lib/performance';
  import { useRouter } from 'vue-router';
  import { useCostService } from '~/services/api/services/costService';
  import { useProjectService } from '~/services/api/services/projectService';
  import { useNotification } from '~/composables/useNotification';
  // Lazy loading do componente de formulário de custos para melhorar a performance inicial da página
  const CostForm = defineAsyncComponent(() => import('~/components/ui/cost/CostForm.vue'));
  // Lazy loading do componente Modal para reduzir o bundle inicial
  const Modal = defineAsyncComponent(() => import('~/components/ui/Modal.vue'));
  // Lazy loading do componente TableSkeleton para exibir durante carregamento
  const TableSkeleton = defineAsyncComponent(() => import('~/components/ui/TableSkeleton.vue'));
  // Componente para gerenciar carregamento assíncrono com Suspense
  const LazyWrapper = defineAsyncComponent(() => import('~/components/ui/LazyWrapper.vue'));
  
  const router = useRouter();
  const notify = useNotification();
  const { 
    fetchCustos, 
    getCusto: retrieveCusto, 
    updateCusto, 
    createCusto, 
    deleteCusto: destroyCusto,
    getResumoCustos
  } = useCostService();
  const projectService = useProjectService();
  const { fetchProjects } = projectService;
  
  // Estado
  // Usar shallowRef para grandes listas de dados para melhorar performance
  const custos = createShallowState([]);
  const projects = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const currentPage = ref(1);
  const totalPages = ref(1);
  const totalItems = ref(0);
  const searchQuery = ref('');
  const categoryFilter = ref('');
  const statusFilter = ref('');
  const projectFilter = ref('');
  const showCostModal = ref(false);
  const saving = ref(false);
  const editingCost = ref(null);
  // Usar shallowRef para objetos complexos
  const selectedCost = createShallowState(null);
  const selectedProjectId = ref(null);

  // Abrir modal de novo custo
  function openNewCostModal() {
    selectedCost.value = null;
    selectedProjectId.value = projectFilter.value || (projects.value.length > 0 ? projects.value[0].id : null);
    showCostModal.value = true;
  };

  // Editar custo
  function editCost(custo) {
    selectedCost.value = custo;
    selectedProjectId.value = typeof custo.projeto === 'object' ? custo.projeto.id : custo.projeto;
    showCostModal.value = true;
  }

  // Tratar submissão do formulário de custo
  async function handleCostSubmit(custoData) {
    saving.value = true;

    try {
      if (selectedCost.value) {
        // Atualizar custo existente
        await updateCusto(selectedCost.value.id, custoData);
        notify.success('Custo atualizado com sucesso');
      } else {
        // Criar novo custo
        await createCusto(custoData);
        notify.success('Custo criado com sucesso');
      }

      // Recarregar custos e fechar modal
      await fetchCosts();
      showCostModal.value = false;
    } catch (error) {
      console.error('Erro ao salvar custo:', error);
      notify.error('Erro ao salvar custo');
    } finally {
      saving.value = false;
    }
  };
  // ...
const viewCost = async (id) => {
  try {
    // Buscar detalhes do custo usando o novo serviço de API antes de navegar
    await retrieveCusto(id);
    router.push(`/custos/${id}`);
  } catch (err) {
    console.error('Erro ao buscar detalhes do custo:', err);
    error.value = 'Não foi possível carregar os detalhes do custo.';
  }
};

// Confirmar exclusão de custo
const confirmDeleteCost = (cost) => {
  if (confirm(`Tem certeza que deseja excluir o custo "${cost.descricao}"?`)) {
    deleteCost(cost.id);
  }
};

// Excluir custo
const deleteCost = async (id) => {
  try {
    // Usar o novo serviço de API para excluir o custo
    await destroyCusto(id);
    // Atualizar a lista após a exclusão
    fetchCosts();
  } catch (err) {
    console.error('Erro ao excluir custo:', err);
    error.value =
      'Não foi possível excluir o custo. Por favor, tente novamente.';
  }
};

// Buscar projetos
async function loadProjects() {
  try {
    const response = await projectService.fetchProjects();
    projects.value = response.results || [];
  } catch (err) {
    console.error('Erro ao buscar projetos:', err);
    error.value = 'Não foi possível carregar os projetos.';
    projects.value = [];
  }
}

// Buscar custos com filtros e paginação
async function fetchCosts() {
  loading.value = true;
  error.value = null;
  
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value,
      categoria: categoryFilter.value,
      status: statusFilter.value,
      projeto: projectFilter.value,
    };
    
    const response = await fetchCustos(params);
    
    custos.value = response.results || [];
    totalPages.value = response.total_pages || 1;
    totalItems.value = response.count || 0;
  } catch (err) {
    console.error('Erro ao buscar custos:', err);
    error.value = 'Não foi possível carregar os custos.';
    custos.value = [];
  } finally {
    loading.value = false;
  }
}

// Formatar moeda
function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
}

// Formatar data
function formatDate(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('pt-BR');
}

// Obter nome do projeto
function getProjectName(projectId) {
  if (!projectId) return '';
  const project = projects.value.find(p => p.id === projectId);
  return project ? project.titulo : '';
}

// Obter label da categoria
function getCategoryLabel(category) {
  const labels = {
    'PESSOAL': 'Pessoal',
    'MATERIAL': 'Material',
    'EQUIPAMENTO': 'Equipamento',
    'SERVICO': 'Serviço',
    'LICENCA': 'Licença',
    'OUTRO': 'Outro'
  };
  return labels[category] || category;
}

// Obter label do status
function getStatusLabel(status) {
  const labels = {
    'PREVISTO': 'Previsto',
    'APROVADO': 'Aprovado',
    'PAGO': 'Pago',
    'CANCELADO': 'Cancelado'
  };
  return labels[status] || status;
}

// Mudar página
function changePage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

// Computar range de paginação
const paginationRange = computed(() => {
  const range = [];
  const maxVisiblePages = 5;
  const halfVisiblePages = Math.floor(maxVisiblePages / 2);
  
  let startPage = Math.max(1, currentPage.value - halfVisiblePages);
  let endPage = Math.min(totalPages.value, startPage + maxVisiblePages - 1);
  
  if (endPage - startPage + 1 < maxVisiblePages) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }
  
  for (let i = startPage; i <= endPage; i++) {
    range.push(i);
  }
  
  return range;
});

// Filtrar custos
const filteredCosts = computed(() => {
  return custos.value;
});

  // Debounce da busca para evitar múltiplas chamadas durante digitação
  const debouncedSearch = debounce(() => {
    currentPage.value = 1; // Reset para primeira página ao buscar
    fetchCosts();
  }, 300);

  // Observar mudanças nos filtros e paginação com otimizações
  watch(selectedProjectId, () => {
    currentPage.value = 1; // Reset para primeira página ao mudar projeto
    fetchCosts(); // Não usar cache ao mudar de projeto
  });

  watch([currentPage, searchQuery, categoryFilter, statusFilter, projectFilter], () => {
    fetchCosts();
  });

// Carregar dados ao montar o componente
onMounted(async () => {
  await loadProjects();
  await fetchCosts();
})
</script>
