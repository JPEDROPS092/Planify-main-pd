<template>
  <div class="container mx-auto p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Gerenciamento de Custos</h1>
      <button 
        @click="openModal()"
        class="bg-primary hover:bg-primary-700 text-white px-4 py-2 rounded-md flex items-center shadow-sm"
      >
        <Icon icon="lucide:plus" class="mr-2 h-4 w-4" />
        Novo Custo
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-10">
      <Icon icon="svg-spinners:180-ring-with-bg" class="w-12 h-12 mx-auto text-primary" />
      <p class="mt-2 text-gray-600">Carregando custos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 text-center">
      <Icon icon="lucide:alert-triangle" class="w-10 h-10 mx-auto text-red-500" />
      <p class="mt-2 font-semibold text-red-700">Erro ao carregar custos</p>
      <p class="text-sm text-red-600">{{ error.message }}</p>
      <button @click="refetch()" class="mt-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700">Tentar Novamente</button>
    </div>

    <!-- Empty State -->
    <div v-else-if="!costs || costs.results.length === 0" class="text-center py-10 border-2 border-dashed rounded-lg">
      <Icon icon="lucide:dollar-sign" class="w-16 h-16 mx-auto text-gray-400" />
      <h3 class="mt-2 text-xl font-medium text-gray-800">Nenhum custo encontrado</h3>
      <p class="mt-1 text-gray-500">Comece registrando um novo custo para um projeto.</p>
      <button @click="openModal()" class="mt-4 bg-primary hover:bg-primary-700 text-white px-4 py-2 rounded-md">
        <Icon icon="lucide:plus" class="mr-2 h-4 w-4 inline-block" />
        Novo Custo
      </button>
    </div>

    <!-- Costs Table -->
    <div v-else class="bg-white shadow overflow-x-auto sm:rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Projeto</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Valor</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Categoria</th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Ações</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="cost in costs.results" :key="cost.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ cost.descricao }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ cost.projeto_titulo }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatCurrency(cost.valor) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ formatDate(cost.data) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ cost.categoria_display }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="openModal(cost)" class="text-primary hover:text-primary-700 mr-4">Editar</button>
              <button @click="confirmDelete(cost.id)" class="text-red-600 hover:text-red-800">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="costs && costs.total_pages > 1" class="mt-6 flex justify-center">
       <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
        <button @click="currentPage--" :disabled="currentPage === 1" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Anterior
        </button>
        <span class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
          Página {{ currentPage }} de {{ costs.total_pages }}
        </span>
        <button @click="currentPage++" :disabled="currentPage === costs.total_pages" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50">
          Próximo
        </button>
      </nav>
    </div>

    <!-- Cost Form Modal -->
    <div v-if="showModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75" @click="closeModal"></div>
        <div class="bg-white rounded-lg overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full">
          <form @submit.prevent="handleSubmit">
            <div class="px-4 pt-5 pb-4 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900">{{ editingCost ? 'Editar Custo' : 'Novo Custo' }}</h3>
              <div class="mt-4 space-y-4">
                <div>
                  <label for="descricao" class="block text-sm font-medium text-gray-700">Descrição</label>
                  <input type="text" v-model="form.descricao" id="descricao" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required />
                </div>
                <div>
                  <label for="projeto" class="block text-sm font-medium text-gray-700">Projeto</label>
                  <select v-model="form.projeto" id="projeto" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required>
                    <option v-for="proj in projectsList?.results" :key="proj.id" :value="proj.id">{{ proj.titulo }}</option>
                  </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="valor" class="block text-sm font-medium text-gray-700">Valor</label>
                    <input type="number" step="0.01" v-model.number="form.valor" id="valor" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required />
                  </div>
                  <div>
                    <label for="data" class="block text-sm font-medium text-gray-700">Data</label>
                    <input type="date" v-model="form.data" id="data" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3" required />
                  </div>
                </div>
                 <div>
                    <label for="categoria" class="block text-sm font-medium text-gray-700">Categoria</label>
                    <select v-model="form.categoria" id="categoria" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3">
                      <option value="EQUIPAMENTOS">Equipamentos</option>
                      <option value="RECURSOS_HUMANOS">Recursos Humanos</option>
                      <option value="SOFTWARE">Software</option>
                      <option value="TREINAMENTO">Treinamento</option>
                      <option value="OUTROS">Outros</option>
                    </select>
                  </div>
              </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button type="submit" :disabled="costMutation.isLoading.value" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-700 sm:ml-3 sm:w-auto sm:text-sm">
                Salvar
              </button>
              <button type="button" @click="closeModal" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})

import { ref } from 'vue';
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { useCostService } from '~/services/costService';
import { useProjectService } from '~/services/projectService';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { Custo, CustoRequest, PaginatedCustoList, PaginatedProjetoList } from '~/api-types';

const queryClient = useQueryClient();
const costService = useCostService();
const projectService = useProjectService();
const { toast } = useToast();

const currentPage = ref(1);
const showModal = ref(false);
const editingCost = ref<Custo | null>(null);

const getInitialFormState = () => ({
  descricao: '',
  projeto: null as number | null,
  valor: 0,
  data: new Date().toISOString().split('T')[0], // Today's date
  categoria: 'OUTROS',
});

const form = ref<CustoRequest>(getInitialFormState());

// Fetch costs
const { data: costs, isLoading, error, refetch } = useQuery<PaginatedCustoList>({
  queryKey: ['costs', currentPage],
  queryFn: () => costService.getCosts({ page: currentPage.value }),
});

// Fetch projects for select
const { data: projectsList } = useQuery<PaginatedProjetoList>({
    queryKey: ['projectsList'],
    queryFn: () => projectService.getProjects(1, 100)
});

const costMutation = useMutation({
  mutationFn: (data: { id?: number; cost: CustoRequest }) => 
    data.id ? costService.updateCost(data.id, data.cost) : costService.createCost(data.cost),
  onSuccess: () => {
    const action = editingCost.value ? 'atualizado' : 'criado';
    toast({ title: 'Sucesso', description: `Custo ${action} com sucesso!` });
    queryClient.invalidateQueries({ queryKey: ['costs'] });
    closeModal();
  },
  onError: (err: any) => {
    const action = editingCost.value ? 'atualizar' : 'criar';
    toast({ title: 'Erro', description: `Falha ao ${action} o custo.`, variant: 'destructive' });
  },
});

const deleteMutation = useMutation({
  mutationFn: (id: number) => costService.deleteCost(id),
  onSuccess: () => {
    toast({ title: 'Sucesso', description: 'Custo excluído com sucesso!' });
    queryClient.invalidateQueries({ queryKey: ['costs'] });
  },
  onError: (err: any) => {
    toast({ title: 'Erro', description: 'Falha ao excluir o custo.', variant: 'destructive' });
  },
});

const openModal = (cost: Custo | null = null) => {
  if (cost) {
    editingCost.value = cost;
    form.value = {
      descricao: cost.descricao,
      projeto: cost.projeto,
      valor: parseFloat(cost.valor as any),
      data: cost.data,
      categoria: cost.categoria,
    };
  } else {
    editingCost.value = null;
    form.value = getInitialFormState();
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingCost.value = null;
};

const handleSubmit = () => {
  costMutation.mutate({ id: editingCost.value?.id, cost: form.value });
};

const confirmDelete = (id: number) => {
  if (window.confirm('Tem certeza que deseja excluir este custo?')) {
    deleteMutation.mutate(id);
  }
};

const formatCurrency = (value: string | number) => {
  const numberValue = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(numberValue);
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('pt-BR');
};

</script>
