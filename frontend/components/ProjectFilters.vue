<template>
  <div class="bg-white shadow rounded-lg p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-900">Filtros</h3>
      <button
        @click="clearFilters"
        class="text-sm text-primary hover:text-primary-700 font-medium"
      >
        Limpar Filtros
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Busca -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Buscar
        </label>
        <div class="relative">
          <input
            v-model="localFilters.search"
            type="text"
            placeholder="Título, descrição..."
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon icon="lucide:search" class="h-5 w-5 text-gray-400" />
          </div>
        </div>
      </div>

      <!-- Status -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Status
        </label>
        <select
          v-model="localFilters.status"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
        >
          <option value="">Todos</option>
          <option value="PLANEJADO">Planejado</option>
          <option value="EM_ANDAMENTO">Em Andamento</option>
          <option value="PAUSADO">Pausado</option>
          <option value="CONCLUIDO">Concluído</option>
          <option value="CANCELADO">Cancelado</option>
        </select>
      </div>

      <!-- Prioridade -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Prioridade
        </label>
        <select
          v-model="localFilters.prioridade"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
        >
          <option value="">Todas</option>
          <option value="BAIXA">Baixa</option>
          <option value="MEDIA">Média</option>
          <option value="ALTA">Alta</option>
          <option value="CRITICA">Crítica</option>
        </select>
      </div>

      <!-- Arquivado -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Arquivado
        </label>
        <select
          v-model="localFilters.arquivado"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
        >
          <option value="">Todos</option>
          <option value="false">Ativos</option>
          <option value="true">Arquivados</option>
        </select>
      </div>
    </div>

    <!-- Filtros avançados -->
    <div class="mt-4">
      <button
        @click="showAdvanced = !showAdvanced"
        class="flex items-center text-sm text-gray-600 hover:text-gray-900"
      >
        <Icon 
          :icon="showAdvanced ? 'lucide:chevron-up' : 'lucide:chevron-down'" 
          class="h-4 w-4 mr-1" 
        />
        Filtros Avançados
      </button>

      <div v-if="showAdvanced" class="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <!-- Data de início -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Data de Início (Após)
          </label>
          <input
            v-model="localFilters.data_inicio_apos_after"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Data de Início (Antes)
          </label>
          <input
            v-model="localFilters.data_inicio_antes_before"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          />
        </div>

        <!-- Data de fim -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Data de Fim (Após)
          </label>
          <input
            v-model="localFilters.data_fim_apos_after"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Data de Fim (Antes)
          </label>
          <input
            v-model="localFilters.data_fim_antes_before"
            type="date"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          />
        </div>

        <!-- Projetos atrasados -->
        <div class="flex items-center">
          <input
            v-model="localFilters.atrasado"
            type="checkbox"
            class="h-4 w-4 text-primary focus:ring-primary-500 border-gray-300 rounded"
          />
          <label class="ml-2 block text-sm text-gray-900">
            Apenas projetos atrasados
          </label>
        </div>

        <!-- Ordenação -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Ordenar por
          </label>
          <select
            v-model="localFilters.ordering"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="">Padrão</option>
            <option value="titulo">Título (A-Z)</option>
            <option value="-titulo">Título (Z-A)</option>
            <option value="data_inicio">Data de Início (Mais Antiga)</option>
            <option value="-data_inicio">Data de Início (Mais Recente)</option>
            <option value="data_fim">Data de Fim (Mais Antiga)</option>
            <option value="-data_fim">Data de Fim (Mais Recente)</option>
            <option value="criado_em">Criado em (Mais Antigo)</option>
            <option value="-criado_em">Criado em (Mais Recente)</option>
            <option value="prioridade">Prioridade</option>
            <option value="-prioridade">Prioridade (Decrescente)</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';

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
  'update:filters': [filters: Filters];
}>();

const showAdvanced = ref(false);
const localFilters = ref<Filters>({ ...props.filters });

// Watch para emitir mudanças
watch(localFilters, (newFilters) => {
  emit('update:filters', { ...newFilters });
}, { deep: true });

// Watch para sincronizar com props
watch(() => props.filters, (newFilters) => {
  localFilters.value = { ...newFilters };
}, { deep: true });

const clearFilters = () => {
  localFilters.value = {};
  showAdvanced.value = false;
};
</script>
