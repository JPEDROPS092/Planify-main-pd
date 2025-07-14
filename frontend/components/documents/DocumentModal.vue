<script lang="ts" setup>
import { Icon } from '@iconify/vue';
import type { Documento, DocumentoRequest } from '@/api/schemas';
import { ref, computed, onMounted, onUnmounted, type ComputedRef } from "vue";
import { useQueryClient } from "@tanstack/vue-query";

import { useDocumentsRetrieve } from "@/api/documentos/documentos";
import PDFThumbnail from './PDFThumbnail.vue'

interface Props {
  show: boolean;
  documento_id: number;
  loading?: boolean;
}

const queryClient = useQueryClient();
const props = defineProps<Props>();
const emit = defineEmits<{
  close: [];
  submit: [data: DocumentoRequest];
}>();

const documentoIdParam = computed(() => props.documento_id)

console.log("documentoIdParam.value:", documentoIdParam.value)

const { data, isLoading, error } = useDocumentsRetrieve(documentoIdParam,  { 
  query: {
    enabled: computed(() => !!documentoIdParam.value && !isNaN(documentoIdParam.value)),
    queryKey: ['document-retrieve', documentoIdParam]
  } 
});

const documento: ComputedRef<Documento> = computed(() => {
  console.log(data.value)
  return data.value?.data
});

watch(() => props.show, (show) => {
  if (show) {
    queryClient.invalidateQueries({ queryKey: ["document-retrieve", documentoIdParam.value] });
  }
})

onMounted(() => {
  const handleEsc = (e: KeyboardEvent) => {
    if (e.key === 'Escape' && props.show) {
      emit('close');
    }
  };
  document.addEventListener('keydown', handleEsc);
  
  onUnmounted(() => {
    document.removeEventListener('keydown', handleEsc);
  });
});

const handleDownload = () => {

}

</script>

<template>
  <div v-if="show" class="fixed z-50 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="emit('close')"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button
            type="button"
            @click="emit('close')"
            class="bg-white rounded-md text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <span class="sr-only">Fechar</span>
            <Icon icon="lucide:x" class="h-6 w-6" />
          </button>
        </div>
        
        <div>
          <div v-if="isLoading" class="text-center py-8">
            <pre>{{ documentoIdParam }}</pre>
            Carregando documento...
          </div>
          <div v-else-if="error" class="text-center py-8 text-red-500">
            Erro ao carregar o documento.
            <pre>{{ error }}</pre>
          </div>
          <div v-else-if="documento">
            <pre>{{ console.log(documento) }}</pre>
            <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <h3 class="text-lg text-center leading-6 font-medium text-gray-900" id="modal-title">
                Informações do Documento
              </h3>
              <div class="mt-4">
                <div class="space-y-6 text-center">
                  <!-- Informações básicas -->
                   <p class="text-lg">{{ documento.titulo }}</p>
                  <div v-if="documento.arquivo" div class="flex justify-center">
                    <PDFThumbnail 
                      :file-url="documento.arquivo"
                    />
                  </div>
                  <div v-else class="text-center text-bold text-red-600">Arquivo não encontrado</div>
                  <p class="text-sm font-light">{{ documento.descricao || "Sem descrição"}}</p>
                  <!-- Botões -->
                  <div class="mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                    <button
                      type="button"
                      @click="handleDownload"
                      class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:col-start-2 sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed bg-gray-800"
                      :disabled="loading"
                    >
                      Baixar
                    </button>
                    <button
                      type="button"
                      @click="emit('close')"
                      class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:col-start-1 sm:text-sm"
                    >
                      Fechar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>