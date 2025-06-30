<template>
  <div v-if="show" class="fixed z-50 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="closeModal"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
      
      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            type="button"
            @click="closeModal"
            class="bg-white rounded-md text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <span class="sr-only">Fechar</span>
            <Icon icon="lucide:x" class="h-6 w-6" />
          </button>
        </div>
        
        <div class="sm:flex sm:items-start">
          <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
            <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
              {{ isEditing ? 'Editar Projeto' : 'Novo Projeto' }}
            </h3>
            <div class="mt-4">
              <form @submit.prevent="handleSubmit" class="space-y-6">
                <!-- Informações básicas -->
                <div class="grid grid-cols-1 gap-6">
                  <div>
                    <label for="titulo" class="block text-sm font-medium text-gray-700">
                      Título *
                    </label>
                    <input
                      type="text"
                      id="titulo"
                      v-model="form.titulo"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      placeholder="Título do projeto"
                      required
                    />
                  </div>
                  
                  <div>
                    <label for="descricao" class="block text-sm font-medium text-gray-700">
                      Descrição
                    </label>
                    <textarea
                      id="descricao"
                      v-model="form.descricao"
                      rows="3"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      placeholder="Descrição do projeto"
                    ></textarea>
                  </div>
                </div>

                <!-- Datas -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="data_inicio" class="block text-sm font-medium text-gray-700">
                      Data de Início *
                    </label>
                    <input
                      type="date"
                      id="data_inicio"
                      v-model="form.data_inicio"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      required
                    />
                  </div>
                  
                  <div>
                    <label for="data_fim" class="block text-sm font-medium text-gray-700">
                      Data de Fim *
                    </label>
                    <input
                      type="date"
                      id="data_fim"
                      v-model="form.data_fim"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                      required
                    />
                  </div>
                </div>

                <!-- Status e Prioridade -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="status" class="block text-sm font-medium text-gray-700">
                      Status
                    </label>
                    <select
                      id="status"
                      v-model="form.status"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    >
                      <option value="PLANEJADO">Planejado</option>
                      <option value="EM_ANDAMENTO">Em Andamento</option>
                      <option value="PAUSADO">Pausado</option>
                      <option value="CONCLUIDO">Concluído</option>
                      <option value="CANCELADO">Cancelado</option>
                    </select>
                  </div>
                  
                  <div>
                    <label for="prioridade" class="block text-sm font-medium text-gray-700">
                      Prioridade
                    </label>
                    <select
                      id="prioridade"
                      v-model="form.prioridade"
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    >
                      <option value="BAIXA">Baixa</option>
                      <option value="MEDIA">Média</option>
                      <option value="ALTA">Alta</option>
                      <option value="CRITICA">Crítica</option>
                    </select>
                  </div>
                </div>

                <!-- Arquivado (apenas para edição) -->
                <div v-if="isEditing" class="flex items-center">
                  <input
                    id="arquivado"
                    v-model="form.arquivado"
                    type="checkbox"
                    class="h-4 w-4 text-primary focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <label for="arquivado" class="ml-2 block text-sm text-gray-900">
                    Projeto arquivado
                  </label>
                </div>
                
                <!-- Botões -->
                <div class="mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                  <button
                    type="submit"
                    class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="inline-block mr-2">
                      <Icon icon="lucide:loader-2" class="h-4 w-4 animate-spin" />
                    </span>
                    {{ isEditing ? 'Atualizar' : 'Criar' }}
                  </button>
                  <button
                    type="button"
                    @click="closeModal"
                    class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm"
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue';
import type { Projeto, ProjetoRequest } from '~/api-types';

interface Props {
  show: boolean;
  project?: Projeto;
  loading?: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  close: [];
  submit: [data: ProjetoRequest];
}>();

const isEditing = computed(() => !!props.project);

const form = ref<ProjetoRequest>({
  titulo: '',
  descricao: '',
  data_inicio: '',
  data_fim: '',
  status: 'PLANEJADO',
  prioridade: 'MEDIA',
  arquivado: false
});

// Resetar formulário quando o modal abrir/fechar
watch(() => props.show, (show) => {
  if (show) {
    if (props.project) {
      // Edição - preencher com dados do projeto
      form.value = {
        titulo: props.project.titulo,
        descricao: props.project.descricao || '',
        data_inicio: props.project.data_inicio,
        data_fim: props.project.data_fim,
        status: props.project.status,
        prioridade: props.project.prioridade,
        arquivado: props.project.arquivado
      };
    } else {
      // Novo projeto - resetar formulário
      form.value = {
        titulo: '',
        descricao: '',
        data_inicio: '',
        data_fim: '',
        status: 'PLANEJADO',
        prioridade: 'MEDIA',
        arquivado: false
      };
    }
  }
});

const closeModal = () => {
  emit('close');
};

const handleSubmit = () => {
  emit('submit', { ...form.value });
};

// Fechar modal com ESC
onMounted(() => {
  const handleEsc = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && props.show) {
      closeModal();
    }
  };
  document.addEventListener('keydown', handleEsc);
  
  onUnmounted(() => {
    document.removeEventListener('keydown', handleEsc);
  });
});
</script>
