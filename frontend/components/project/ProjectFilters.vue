<template>
  <div class="bg-white shadow-sm rounded-lg border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
        <Icon icon="lucide:filter" class="h-5 w-5 text-gray-500" />
        Filtros
      </h3>
      <button
        @click="clearFilters"
        class="text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors flex items-center gap-1"
      >
        <Icon icon="lucide:x" class="h-4 w-4" />
        Limpar Filtros
      </button>
    </div>

    <!-- Filtros Principais -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
      <!-- Busca -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Buscar Projeto
        </label>
        <div class="relative">
          <input
            v-model="localFilters.search"
            type="text"
            placeholder="Nome, descrição..."
            class="block w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg bg-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors text-sm"
          />
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
          >
            <Icon icon="lucide:search" class="h-4 w-4 text-gray-400" />
          </div>
        </div>
      </div>

      <!-- Status -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Status
        </label>
        <div class="relative">
          <select
            v-model="localFilters.status"
            class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm bg-white"
          >
            <option value="">Todos os Status</option>
            <option value="PLANEJADO">📅 Planejado</option>
            <option value="EM_ANDAMENTO">▶️ Em Andamento</option>
            <option value="PAUSADO">⏸️ Pausado</option>
            <option value="CONCLUIDO">✅ Concluído</option>
            <option value="CANCELADO">❌ Cancelado</option>
          </select>
        </div>
      </div>

      <!-- Prioridade -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Prioridade
        </label>
        <div class="relative">
          <select
            v-model="localFilters.prioridade"
            class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm bg-white"
          >
            <option value="">Todas as Prioridades</option>
            <option value="BAIXA">🟢 Baixa</option>
            <option value="MEDIA">🟡 Média</option>
            <option value="ALTA">🟠 Alta</option>
            <option value="CRITICA">🔴 Crítica</option>
          </select>
        </div>
      </div>

      <!-- Arquivado -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Estado
        </label>
        <div class="relative">
          <select
            v-model="localFilters.arquivado"
            class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm bg-white"
          >
            <option value="">Todos</option>
            <option value="false">📁 Ativos</option>
            <option value="true">📦 Arquivados</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Chips de Filtros Ativos -->
    <div
      v-if="hasActiveFilters"
      class="flex flex-wrap gap-2 mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200"
    >
      <span class="text-sm text-blue-700 font-medium">Filtros ativos:</span>

      <span
        v-if="localFilters.search"
        class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
      >
        Busca: "{{ localFilters.search }}"
        <button
          @click="localFilters.search = ''"
          class="hover:bg-blue-200 rounded-full p-0.5"
        >
          <Icon icon="lucide:x" class="h-3 w-3" />
        </button>
      </span>

      <span
        v-if="localFilters.status"
        class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
      >
        Status: {{ getStatusLabel(localFilters.status) }}
        <button
          @click="localFilters.status = ''"
          class="hover:bg-blue-200 rounded-full p-0.5"
        >
          <Icon icon="lucide:x" class="h-3 w-3" />
        </button>
      </span>

      <span
        v-if="localFilters.prioridade"
        class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
      >
        Prioridade: {{ getPriorityLabel(localFilters.prioridade) }}
        <button
          @click="localFilters.prioridade = ''"
          class="hover:bg-blue-200 rounded-full p-0.5"
        >
          <Icon icon="lucide:x" class="h-3 w-3" />
        </button>
      </span>

      <span
        v-if="localFilters.arquivado"
        class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
      >
        Estado:
        {{ localFilters.arquivado === "true" ? "Arquivados" : "Ativos" }}
        <button
          @click="localFilters.arquivado = ''"
          class="hover:bg-blue-200 rounded-full p-0.5"
        >
          <Icon icon="lucide:x" class="h-3 w-3" />
        </button>
      </span>

      <span
        v-if="localFilters.atrasado"
        class="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
      >
        Apenas Atrasados
        <button
          @click="localFilters.atrasado = false"
          class="hover:bg-blue-200 rounded-full p-0.5"
        >
          <Icon icon="lucide:x" class="h-3 w-3" />
        </button>
      </span>
    </div>

    <!-- Filtros Avançados -->
    <div class="border-t border-gray-200 pt-4">
      <button
        @click="showAdvanced = !showAdvanced"
        class="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
      >
        <Icon
          :icon="showAdvanced ? 'lucide:chevron-up' : 'lucide:chevron-down'"
          class="h-4 w-4"
        />
        <span>Filtros Avançados</span>
        <span
          class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full"
        >
          {{ advancedFiltersCount }} ativos
        </span>
      </button>

      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div v-if="showAdvanced" class="mt-4 space-y-4">
          <!-- Datas -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Data de Início (A partir de)
              </label>
              <input
                v-model="localFilters.data_inicio_apos_after"
                type="date"
                class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Data de Início (Até)
              </label>
              <input
                v-model="localFilters.data_inicio_antes_before"
                type="date"
                class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Data de Fim (A partir de)
              </label>
              <input
                v-model="localFilters.data_fim_apos_after"
                type="date"
                class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Data de Fim (Até)
              </label>
              <input
                v-model="localFilters.data_fim_antes_before"
                type="date"
                class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
              />
            </div>
          </div>

          <!-- Outras opções avançadas -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Checkbox para projetos atrasados -->
            <div
              class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg border border-gray-200"
            >
              <input
                v-model="localFilters.atrasado"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label class="text-sm text-gray-900 flex items-center gap-2">
                <Icon
                  icon="lucide:alert-triangle"
                  class="h-4 w-4 text-orange-500"
                />
                Apenas projetos em atraso
              </label>
            </div>

            <!-- Ordenação -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Ordenar por
              </label>
              <select
                v-model="localFilters.ordering"
                class="block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm bg-white"
              >
                <option value="">Ordem Padrão</option>
                <optgroup label="Por Nome">
                  <option value="titulo">📝 Título (A-Z)</option>
                  <option value="-titulo">📝 Título (Z-A)</option>
                </optgroup>
                <optgroup label="Por Data">
                  <option value="data_inicio">
                    📅 Data de Início (Mais Antiga)
                  </option>
                  <option value="-data_inicio">
                    📅 Data de Início (Mais Recente)
                  </option>
                  <option value="data_fim">🏁 Data de Fim (Mais Antiga)</option>
                  <option value="-data_fim">
                    🏁 Data de Fim (Mais Recente)
                  </option>
                  <option value="criado_em">🆕 Criado em (Mais Antigo)</option>
                  <option value="-criado_em">
                    🆕 Criado em (Mais Recente)
                  </option>
                </optgroup>
                <optgroup label="Por Prioridade">
                  <option value="prioridade">
                    🎯 Prioridade (Baixa → Alta)
                  </option>
                  <option value="-prioridade">
                    🎯 Prioridade (Alta → Baixa)
                  </option>
                </optgroup>
              </select>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

interface Filters {
  search?: string;
  status?: string;
  prioridade?: string;
  arquivado?: string;
  atrasado?: boolean;
  data_inicio_apos_after?: string;
  data_inicio_antes_before?: string;
  data_fim_apos_after?: string;
  data_fim_antes_before?: string;
  ordering?: string;
}

interface Props {
  filters: Filters;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  "update:filters": [filters: Filters];
}>();

const showAdvanced = ref(false);
const localFilters = ref<Filters>({ ...props.filters });

// Watch para emitir mudanças
watch(
  localFilters,
  (newFilters: Filters) => {
    emit("update:filters", { ...newFilters });
  },
  { deep: true }
);

// Watch para sincronizar com props
watch(
  () => props.filters,
  (newFilters: Filters) => {
    localFilters.value = { ...newFilters };
  },
  { deep: true }
);

// Computed properties
const hasActiveFilters = computed(() => {
  return Object.values(localFilters.value).some(
    (value) => value !== undefined && value !== "" && value !== false
  );
});

const advancedFiltersCount = computed(() => {
  const advancedFields = [
    "data_inicio_apos_after",
    "data_inicio_antes_before",
    "data_fim_apos_after",
    "data_fim_antes_before",
    "atrasado",
    "ordering",
  ];

  return advancedFields.filter((field) => {
    const value = localFilters.value[field as keyof Filters];
    return value !== undefined && value !== "" && value !== false;
  }).length;
});

// Helper functions
const getStatusLabel = (status: string) => {
  const labels = {
    PLANEJADO: "Planejado",
    EM_ANDAMENTO: "Em Andamento",
    PAUSADO: "Pausado",
    CONCLUIDO: "Concluído",
    CANCELADO: "Cancelado",
  };
  return labels[status as keyof typeof labels] || status;
};

const getPriorityLabel = (priority: string) => {
  const labels = {
    BAIXA: "Baixa",
    MEDIA: "Média",
    ALTA: "Alta",
    CRITICA: "Crítica",
  };
  return labels[priority as keyof typeof labels] || priority;
};

const clearFilters = () => {
  localFilters.value = {};
  showAdvanced.value = false;
};
</script>
