<template>
  <NuxtLayout name="dashboard">
    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <h1
          class="text-2xl font-bold tracking-tight text-gray-900 dark:text-white"
        >
          Riscos
        </h1>
        <RoleBasedContent :roles="['admin', 'manager', 'editor']">
          <button
            @click="openNewRiskModal"
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
          Novo Risco
          </button>
        </RoleBasedContent>
      </div>

      <!-- Filtros -->
      <div class="flex flex-wrap gap-4">
        <div class="relative w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar riscos..."
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
            <path d="m21 21-4.3-4.3"></path>
          </svg>
        </div>
        <select
          v-model="probabilityFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todas as probabilidades</option>
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
        </select>
        <select
          v-model="impactFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os impactos</option>
          <option value="BAIXO">Baixo</option>
          <option value="MEDIO">Médio</option>
          <option value="ALTO">Alto</option>
        </select>
        <select
          v-model="statusFilter"
          class="rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
        >
          <option value="">Todos os status</option>
          <option value="IDENTIFICADO">Identificado</option>
          <option value="ANALISADO">Analisado</option>
          <option value="MITIGADO">Mitigado</option>
          <option value="ACEITO">Aceito</option>
          <option value="TRANSFERIDO">Transferido</option>
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
          Carregando riscos...
        </p>
      </div>
      <EmptyState
        v-else-if="filteredRisks.length === 0"
        title="Nenhum risco encontrado"
        description="Não encontramos nenhum risco com os filtros atuais. Tente ajustar os filtros ou crie um novo risco."
        icon="alert-triangle"
      >
        <template #action>
          <button
            @click="openNewRiskModal"
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
            Criar novo risco
          </button>
        </template>
      </EmptyState>
      <div v-else class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="risk in filteredRisks"
          :key="risk.id"
          class="flex flex-col rounded-lg border bg-white shadow-sm transition-all hover:shadow-md dark:bg-gray-800"
        >
          <div class="p-6">
            <div class="flex items-center justify-between">
              <span
                :class="{
                  'bg-yellow-100 text-yellow-800':
                    risk.status === 'IDENTIFICADO',
                  'bg-blue-100 text-blue-800': risk.status === 'ANALISADO',
                  'bg-green-100 text-green-800': risk.status === 'MITIGADO',
                  'bg-gray-100 text-gray-800': risk.status === 'ACEITO',
                  'bg-purple-100 text-purple-800':
                    risk.status === 'TRANSFERIDO',
                }"
                class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium dark:text-white"
              >
                {{ getStatusLabel(risk.status) }}
              </span>
              <div class="flex space-x-2">
                <button
                  @click="editRisk(risk)"
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
                  @click="viewRisk(risk.id)"
                  class="rounded-md p-1 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-600"
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
            </div>
            <h3
              class="mt-2 text-lg font-semibold text-gray-900 dark:text-white"
            >
              {{ risk.titulo }}
            </h3>
            <p
              class="mt-1 line-clamp-2 text-sm text-gray-500 dark:text-gray-400"
            >
              {{ risk.descricao }}
            </p>

            <div class="mt-4 grid grid-cols-2 gap-2">
              <div>
                <h4
                  class="text-xs font-medium uppercase text-gray-500 dark:text-gray-400"
                >
                  Probabilidade
                </h4>
                <span
                  :class="{
                    'text-green-600': risk.probabilidade === 'BAIXA',
                    'text-yellow-600': risk.probabilidade === 'MEDIA',
                    'text-red-600': risk.probabilidade === 'ALTA',
                  }"
                  class="text-sm font-medium dark:text-white"
                >
                  {{ getProbabilityLabel(risk.probabilidade) }}
                </span>
              </div>
              <div>
                <h4
                  class="text-xs font-medium uppercase text-gray-500 dark:text-gray-400"
                >
                  Impacto
                </h4>
                <span
                  :class="{
                    'text-green-600': risk.impacto === 'BAIXO',
                    'text-yellow-600': risk.impacto === 'MEDIO',
                    'text-red-600': risk.impacto === 'ALTO',
                  }"
                  class="text-sm font-medium dark:text-white"
                >
                  {{ getImpactLabel(risk.impacto) }}
                </span>
              </div>
            </div>

            <div
              class="mt-4 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400"
            >
              <div class="flex items-center">
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
                  class="h-4 w-4 mr-1 text-gray-400 dark:text-gray-500"
                >
                  <path d="M3 3v18h18"></path>
                  <path d="M7 12v5"></path>
                  <path d="m14 7 3-3 3 3"></path>
                  <path d="M7 19h5"></path>
                  <path d="M19 15v4"></path>
                  <path d="M11 12v5"></path>
                  <path d="M14 12v5"></path>
                </svg>
                {{ getProjectName(risk.projeto) }}
              </div>
              <div>
                Identificado em {{ formatDate(risk.data_identificacao) }}
              </div>
            </div>
          </div>
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
              ? 'bg-blue-600 text-white'
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

      <!-- Modal para novo risco -->
      <div
        v-if="showRiskModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      >
        <div
          class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-900"
        >
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">
              {{ editingRisk ? 'Editar Risco' : 'Novo Risco' }}
            </h3>
            <button
              @click="showRiskModal = false"
              class="rounded-full p-1 hover:bg-gray-100 dark:hover:bg-gray-700"
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
                class="h-5 w-5"
              >
                <path d="M18 6 6 18"></path>
                <path d="m6 6 12 12"></path>
              </svg>
            </button>
          </div>
          <form @submit.prevent="saveRisk" class="mt-4 space-y-4">
            <div>
              <label
                for="titulo"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Título</label
              >
              <input
                id="titulo"
                v-model="riskForm.titulo"
                type="text"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label
                for="descricao"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Descrição</label
              >
              <textarea
                id="descricao"
                v-model="riskForm.descricao"
                rows="3"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              ></textarea>
            </div>
            <div>
              <label
                for="projeto"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Projeto</label
              >
              <select
                id="projeto"
                v-model="riskForm.projeto"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option
                  v-for="project in projects"
                  :key="project.id"
                  :value="project.id"
                >
                  {{ project.titulo }}
                </option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label
                  for="probabilidade"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                  >Probabilidade</label
                >
                <select
                  id="probabilidade"
                  v-model="riskForm.probabilidade"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
                >
                  <option value="BAIXA">Baixa</option>
                  <option value="MEDIA">Média</option>
                  <option value="ALTA">Alta</option>
                </select>
              </div>
              <div>
                <label
                  for="impacto"
                  class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                  >Impacto</label
                >
                <select
                  id="impacto"
                  v-model="riskForm.impacto"
                  required
                  class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
                >
                  <option value="BAIXO">Baixo</option>
                  <option value="MEDIO">Médio</option>
                  <option value="ALTO">Alto</option>
                </select>
              </div>
            </div>
            <div>
              <label
                for="status"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Status</label
              >
              <select
                id="status"
                v-model="riskForm.status"
                required
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              >
                <option value="IDENTIFICADO">Identificado</option>
                <option value="ANALISADO">Analisado</option>
                <option value="MITIGADO">Mitigado</option>
                <option value="ACEITO">Aceito</option>
                <option value="TRANSFERIDO">Transferido</option>
              </select>
            </div>
            <div>
              <label
                for="plano_mitigacao"
                class="block text-sm font-medium text-gray-700 dark:text-gray-400"
                >Plano de Mitigação</label
              >
              <textarea
                id="plano_mitigacao"
                v-model="riskForm.plano_mitigacao"
                rows="3"
                class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white"
              ></textarea>
            </div>
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="showRiskModal = false"
                class="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-400 dark:hover:bg-gray-700"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="saving"
                class="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-70 dark:bg-blue-700 dark:hover:bg-blue-600"
              >
                <span
                  v-if="saving"
                  class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"
                ></span>
                {{ saving ? 'Salvando...' : editingRisk ? 'Salvar' : 'Criar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useRiskService } from '~/services/api/services/riskService';
import { useProjectService } from '~/services/api/services/projectService';
import { useAuth } from '~/stores/composables/useAuth';
import EmptyState from '~/components/EmptyState.vue';

definePageMeta({
  middleware: ['auth'],
});

const router = useRouter();
const { $api } = useNuxtApp();
const { userRole } = useAuth();

// Propriedades computadas para verificar permissões baseadas no papel do usuário
const userCanCreate = computed(() => ['admin', 'manager', 'editor'].includes(userRole.value));
const userCanEdit = computed(() => ['admin', 'manager', 'editor'].includes(userRole.value));
const userCanDelete = computed(() => ['admin', 'manager'].includes(userRole.value));

// Estado
const risks = ref([]);
const projects = ref([]);
const loading = ref(true);
const error = ref(null);
const currentPage = ref(1);
const totalPages = ref(1);
const searchQuery = ref('');
const probabilityFilter = ref('');
const impactFilter = ref('');
const statusFilter = ref('');
const projectFilter = ref('');
const showRiskModal = ref(false);
const saving = ref(false);
const editingRisk = ref(null);

// Formulário de risco
const riskForm = ref({
  titulo: '',
  descricao: '',
  projeto: '',
  probabilidade: 'MEDIA',
  impacto: 'MEDIO',
  status: 'IDENTIFICADO',
  plano_mitigacao: '',
});

// Filtrar riscos
const filteredRisks = computed(() => {
  return risks.value.filter((risk) => {
    const matchesSearch =
      searchQuery.value === '' ||
      risk.titulo.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      risk.descricao.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesProbability =
      probabilityFilter.value === '' ||
      risk.probabilidade === probabilityFilter.value;
    const matchesImpact =
      impactFilter.value === '' || risk.impacto === impactFilter.value;
    const matchesStatus =
      statusFilter.value === '' || risk.status === statusFilter.value;
    const matchesProject =
      projectFilter.value === '' ||
      risk.projeto === parseInt(projectFilter.value);

    return (
      matchesSearch &&
      matchesProbability &&
      matchesImpact &&
      matchesStatus &&
      matchesProject
    );
  });
});

// Paginação
const paginationRange = computed(() => {
  const range = [];
  const maxVisiblePages = 5;

  if (totalPages.value <= maxVisiblePages) {
    for (let i = 1; i <= totalPages.value; i++) {
      range.push(i);
    }
  } else {
    let start = Math.max(
      1,
      currentPage.value - Math.floor(maxVisiblePages / 2)
    );
    let end = Math.min(totalPages.value, start + maxVisiblePages - 1);

    if (end - start + 1 < maxVisiblePages) {
      start = Math.max(1, end - maxVisiblePages + 1);
    }

    for (let i = start; i <= end; i++) {
      range.push(i);
    }
  }

  return range;
});

// Buscar riscos
const fetchRisks = async () => {
  loading.value = true;
  error.value = null;

  try {
    const params = {
      page: currentPage.value,
      ordering: '-data_identificacao',
    };

    if (probabilityFilter.value) {
      params.probabilidade = probabilityFilter.value;
    }

    if (impactFilter.value) {
      params.impacto = impactFilter.value;
    }

    if (statusFilter.value) {
      params.status = statusFilter.value;
    }

    if (projectFilter.value) {
      params.projeto = projectFilter.value;
    }

    if (searchQuery.value) {
      params.search = searchQuery.value;
    }

    // Usar o novo serviço de API para riscos
    const response = await listRiscos(params);

    risks.value = response.results.map((risk) => ({
      id: risk.id,
      titulo: risk.titulo,
      descricao: risk.descricao,
      projeto: risk.projeto,
      projeto_nome: risk.projeto_nome,
      probabilidade: risk.probabilidade,
      probabilidade_display: risk.probabilidade_display,
      impacto: risk.impacto,
      impacto_display: risk.impacto_display,
      status: risk.status,
      status_display: risk.status_display,
      plano_mitigacao: risk.plano_mitigacao,
      data_identificacao: risk.data_identificacao,
      data_atualizacao: risk.data_atualizacao,
    }));

    totalItems.value = response.count;
    totalPages.value = Math.ceil(response.count / itemsPerPage.value);
  } catch (err) {
    console.error('Erro ao buscar riscos:', err);
    error.value =
      'Não foi possível carregar os riscos. Por favor, tente novamente.';
  } finally {
    loading.value = false;
  }
};

// Buscar projetos
const fetchProjects = async () => {
  try {
    // Usar o novo serviço de API para projetos
    const response = await listProjetos();
    projects.value = response.results.map((project) => ({
      id: project.id,
      titulo: project.nome,
    }));

    if (projects.value.length > 0) {
      riskForm.value.projeto = projects.value[0].id;
    }
  } catch (err) {
    console.error('Erro ao buscar projetos:', err);
  }
};

// Mudar página
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// Formatar data
const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR');
};

// Obter label da probabilidade
const getProbabilityLabel = (probability) => {
  const probabilityMap = {
    BAIXA: 'Baixa',
    MEDIA: 'Média',
    ALTA: 'Alta',
  };
  return probabilityMap[probability] || probability;
};

// Obter label do impacto
const getImpactLabel = (impact) => {
  const impactMap = {
    BAIXO: 'Baixo',
    MEDIO: 'Médio',
    ALTO: 'Alto',
  };
  return impactMap[impact] || impact;
};

// Obter label do status
const getStatusLabel = (status) => {
  const statusMap = {
    IDENTIFICADO: 'Identificado',
    ANALISADO: 'Analisado',
    MITIGADO: 'Mitigado',
    ACEITO: 'Aceito',
    TRANSFERIDO: 'Transferido',
  };
  return statusMap[status] || status;
};

// Obter nome do projeto
const getProjectName = (projectId) => {
  const project = projects.value.find((p) => p.id === projectId);
  return project ? project.titulo : 'Projeto não encontrado';
};

// Abrir modal de novo risco
const openNewRiskModal = () => {
  editingRisk.value = null;
  riskForm.value = {
    titulo: '',
    descricao: '',
    projeto: projects.value.length > 0 ? projects.value[0].id : '',
    probabilidade: 'MEDIA',
    impacto: 'MEDIO',
    status: 'IDENTIFICADO',
    plano_mitigacao: '',
  };
  showRiskModal.value = true;
};

// Editar risco
const editRisk = async (risk) => {
  try {
    // Buscar detalhes completos do risco usando o novo serviço de API
    const riskDetails = await retrieveRisco(risk.id);

    editingRisk.value = riskDetails;
    riskForm.value = {
      titulo: riskDetails.titulo,
      descricao: riskDetails.descricao || '',
      projeto: riskDetails.projeto,
      probabilidade: riskDetails.probabilidade,
      impacto: riskDetails.impacto,
      status: riskDetails.status,
      plano_mitigacao: riskDetails.plano_mitigacao || '',
    };
    showRiskModal.value = true;
  } catch (err) {
    console.error('Erro ao buscar detalhes do risco para edição:', err);
    error.value = 'Não foi possível carregar os detalhes do risco para edição.';
  }
};

// Salvar risco
const saveRisk = async () => {
  if (!riskForm.value.titulo || !riskForm.value.projeto) {
    alert('Preencha os campos obrigatórios');
    return;
  }

  saving.value = true;

  try {
    // Preparar dados do risco
    const riskData = {
      titulo: riskForm.value.titulo,
      descricao: riskForm.value.descricao || '',
      projeto: riskForm.value.projeto,
      probabilidade: riskForm.value.probabilidade,
      impacto: riskForm.value.impacto,
      status: riskForm.value.status,
      plano_mitigacao: riskForm.value.plano_mitigacao || '',
    };

    if (editingRisk.value) {
      // Atualizar risco existente usando o novo serviço de API
      await updateRisco(editingRisk.value.id, riskData);
    } else {
      // Criar novo risco usando o novo serviço de API
      await createRisco(riskData);
    }

    showRiskModal.value = false;
    await fetchRisks();
  } catch (err) {
    console.error('Erro ao salvar risco:', err);
    alert('Não foi possível salvar o risco. Por favor, tente novamente.');
  } finally {
    saving.value = false;
  }
};

// Ver detalhes do risco
const viewRisk = async (id) => {
  try {
    // Buscar detalhes do risco usando o novo serviço de API antes de navegar
    await retrieveRisco(id);
    router.push(`/riscos/${id}`);
  } catch (err) {
    console.error('Erro ao buscar detalhes do risco:', err);
    error.value = 'Não foi possível carregar os detalhes do risco.';
  }
};

// Confirmar exclusão de risco
const confirmDeleteRisk = (risk) => {
  if (confirm(`Tem certeza que deseja excluir o risco "${risk.titulo}"?`)) {
    deleteRisk(risk.id);
  }
};

// Excluir risco
const deleteRisk = async (id) => {
  try {
    // Usar o novo serviço de API para excluir o risco
    await destroyRisco(id);
    // Atualizar a lista após a exclusão
    fetchRisks();
  } catch (err) {
    console.error('Erro ao excluir risco:', err);
    error.value =
      'Não foi possível excluir o risco. Por favor, tente novamente.';
  }
};

// Observar mudanças nos filtros e página
watch(
  [
    currentPage,
    searchQuery,
    probabilityFilter,
    impactFilter,
    statusFilter,
    projectFilter,
  ],
  () => {
    fetchRisks();
  }
);

// Carregar dados ao montar o componente
onMounted(async () => {
  await fetchProjects();
  await fetchRisks();
});
</script>
