<script lang="ts" setup>
import { ref, computed, watch } from "vue";

import { useDocumentsList } from "@/api/documentos/documentos";
import type { ComputedRef } from "vue";
import type { DocumentoList } from "@/api/schemas";

import DocumentModal from "./DocumentModal.vue";
import DocumentAssociateModal from "./DocumentAssociateModal.vue";

import { useQueryClient } from "@tanstack/vue-query";

import { useDocumentsAssociarTarefaCreate } from "@/api/documentos/documentos";
import { useToast } from "@/composables/useToast";

const props = defineProps<{
  tarefaId: number;
}>();
const emit = defineEmits(["close", "add", "changeRole"]);
const { toast } = useToast();

const showDocumentModal = ref(false);
const showAssociateModal = ref(false);

const selectedDocumentId = ref(0);

const queryClient = useQueryClient();
const taskIdParam = computed(() => props.tarefaId)

const { data, isLoading, error } = useDocumentsList(
  { tarefa: taskIdParam.value }, 
  { query: {
      queryKey: ['documentos-associados', taskIdParam.value],
      enabled: computed(() => !!taskIdParam.value)
  }}
);

const documentos: ComputedRef<DocumentoList[] | undefined> = computed(() => data.value?.data?.results);

/*watch(
  () => props.tarefaId,
  (tarefaId) => {
    console.log("props.tarefaId", props.tarefaId)
    queryClient.invalidateQueries({queryKey: ['documentos-associados', tarefaId]})
  }
);*/

const documentAssociacaoMutation = useDocumentsAssociarTarefaCreate({
  mutation: {
    onSuccess: () => {
      toast({
        title: "Associação atualizada",
        description: "A associação do documento à tarefa foi atualizada com sucesso.",
        type: "success"
      });
      queryClient.invalidateQueries({ queryKey: ["documentos-associados", taskIdParam.value] });
    },
    onError: (err: any) => {
      toast({
        title: "Erro",
        description:
          err.response?.data?.detail || "Não foi possível associar o documento.",
        variant: "destructive",
      });
    },
  }
})

const handleAddDocumento = (data: {documentoId: number}) => {
  console.log("handleAddDocumento", data)
  documentAssociacaoMutation.mutate({ id: data.documentoId, data: {tarefa_id: taskIdParam.value} });
}

const handleRemoveDocumento = (data: {documentoId: number}) => {
  if (
    window.confirm(
      "Tem certeza que deseja desassociar o documento da tarefa?"
    )
  ) {
      documentAssociacaoMutation.mutate({ id: data.documentoId, data: {tarefa_id: 0} });
  }
}

</script>

<template>
  <div class="bg-white rounded-lg shadow-lg w-full max-w-full p-6 relative">
    <div v-if="isLoading" class="py-4 text-center">Carregando documentos associados...</div>
    <div v-else-if="error" class="py-4 text-center">Erro ao carregar documentos associados: {{ error }}</div>
    <div v-else>
        <h2 class="text-1xl mb-4 font-bold text-gray-900 dark:text-gray-100">
          Documentos associados
        </h2>
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 font-bold dark:text-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-4 py-2 text-left text-xs uppercase">Título</th>
              <th class="px-4 py-2 text-left text-xs uppercase">Tipo</th>
              <th class="px-4 py-2 text-left text-xs uppercase"></th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200 dark:text-gray-50 dark:bg-gray-800">
            <tr v-for="doc in documentos" :key="doc.id">
              <td class="px-4 py-2">{{ doc.titulo }}</td>
              <td class="px-4 py-2">{{ doc.tipo_arquivo }}</td>
              <td class="flex justify-around px-4 py-2">
                  <button
                    @click="() => { showDocumentModal = true; selectedDocumentId = doc.id }"
                    class="inline-flex items-center px-3 py-2 border border-cyan-300 shadow-sm text-sm font-medium rounded-md text-cyan-700 bg-white hover:bg-cyan-50"
                  >
                    <Icon icon="lucide:download" class="h-4 w-4" />
                    Baixar
                  </button>
                  <button
                      @click="() => handleRemoveDocumento({documentoId: doc.id})"
                      class="inline-flex items-center px-3 py-2 m-0 border border-red-300 shadow-sm text-sm font-medium rounded-md text-red-700 bg-white hover:bg-red-50"
                    >
                    <Icon icon="lucide:trash" class="h-4 w-4" />
                      Remover
                    </button>
              </td>
            </tr>
            <tr v-if="!documentos || documentos.length === 0">
              <td colspan="4" class="px-4 py-2 text-center text-gray-400">Nenhum documento associado. Acesse a seção de documentos para associar</td>
            </tr>
            <tr>
                <td colspan="4" class="px-4 py-2 text-center text-gray-400">
                  <button
                    @click="() => {showAssociateModal = true;}"
                    class="flex w-full justify-center items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-50">
                    <Icon icon="lucide:plus"/>
                  </button>
                </td> 
              </tr>
          </tbody>
          
        </table>
    </div>

    <DocumentModal 
      :show="showDocumentModal"
      :documento_id="selectedDocumentId"
      @close="showDocumentModal = false"
    />

    <DocumentAssociateModal 
      :show="showAssociateModal"
      :task-id="taskIdParam"
      @close="showAssociateModal = false"
      @add="(data) => handleAddDocumento(data)"
    />

  </div>
</template>

