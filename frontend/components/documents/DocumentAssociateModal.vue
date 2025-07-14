<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useToast } from "@/composables/useToast";
// Substitua pelo seu endpoint real:
import { useDocumentsList } from "@/api/documentos/documentos";

const PapelEnum = {
  PO: "Product Owner",
  SM: "Scrum Master",
  DEV: "Desenvolvedor",
  QA: "Analista de Qualidade",
  DESIGN: "Designer",
  ANALISTA: "Analista de Sistemas",
};

const props = defineProps<{
  show: boolean;
  taskId: number;
}>();
const emit = defineEmits(["close", "add", "changeRole"]);

const currentPage = ref(1);
const pageSize = 10;

const selectedDocumentoId = ref<number | null>(null);

const taskIdParam = computed(() => props.taskId);

const { data, isLoading, error } = useDocumentsList(
  { page: currentPage.value, page_size: pageSize },
  { query: {queryKey: ['documentos-disponiveis', { page: currentPage.value, page_size: pageSize }]} }
);

const documentsOptions = computed(() =>
  {
    return (data.value?.data?.results || []).map((u: any) => ({
      label: u.titulo,
      value: u.id,
    })) || []
  }
);

const papelOptions = Object.entries(PapelEnum).map(([key, value]) => ({
  label: value,
  value: key
}))

function handleAdd() {
  if (selectedDocumentoId.value) {
    emit("add", 
      {
        documentoId: selectedDocumentoId.value
      });
    emit("close");
    selectedDocumentoId.value = null;
  }
}

watch(
  () => props.show,
  (val) => {
    if (!val) selectedDocumentoId.value = null;
  }
);
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40"
  >
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6 relative">
      <h2 class="text-xl font-bold mb-4">Associar documento à tarefa</h2>

      <div v-if="isLoading" class="py-4 text-center">Carregando documentos...</div>
      <div v-else-if="error" class="py-4 text-center">Erro ao carregar documentos: {{ error }}</div>
      <div v-else>
        <select
          v-model="selectedDocumentoId"
          class="w-full border rounded px-3 py-2 mb-4"
        >
          <option value="" disabled>Selecione um documento</option>
          <option
            v-for="doc in documentsOptions"
            :key="doc.value"
            :value="doc.value"
          >
            {{ doc.label }}
          </option>
        </select>
        <div class="flex justify-end space-x-2">
          <button
            @click="emit('close')"
            class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300"
            type="button"
          >
            Cancelar
          </button>
          <button
            :disabled="!selectedDocumentoId"
            @click="handleAdd"
            class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            type="button"
          >
            Adicionar
          </button>
        </div>
      </div>
      <button
        class="absolute top-2 right-2 text-gray-400 hover:text-gray-600 text-xl"
        @click="emit('close')"
        aria-label="Fechar"
        type="button"
      >
      </button>
    </div>
  </div>
</template>

<style>

</style>