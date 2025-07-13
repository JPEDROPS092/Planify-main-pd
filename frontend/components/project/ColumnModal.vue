<!-- filepath: components/project/ColumnModal.vue -->
<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
  >
    <div
      class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
    >
      <div class="mt-3">
        <!-- Header -->
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ column ? "Editar Coluna" : "Nova Coluna" }}
          </h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600"
          >
            <Icon icon="lucide:x" class="h-6 w-6" />
          </button>
        </div>

        <!-- Formulário -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Nome da Coluna -->
          <div>
            <label
              for="name"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Nome da Coluna
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Ex: Em Desenvolvimento"
            />
          </div>

          <!-- Cor da Coluna -->
          <div>
            <label
              for="color"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Cor da Coluna
            </label>
            <div class="flex items-center space-x-2">
              <input
                id="color"
                v-model="form.color"
                type="color"
                class="w-12 h-10 border border-gray-300 rounded cursor-pointer"
              />
              <input
                v-model="form.color"
                type="text"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="#3B82F6"
              />
            </div>
            <p class="text-xs text-gray-500 mt-1">
              Escolha uma cor para identificar visualmente esta coluna
            </p>
          </div>

          <!-- Cores Predefinidas -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Cores Sugeridas
            </label>
            <div class="flex space-x-2">
              <button
                v-for="color in predefinedColors"
                :key="color.value"
                type="button"
                @click="form.color = color.value"
                :title="color.name"
                class="w-8 h-8 rounded-full border-2 hover:scale-110 transition-transform"
                :class="
                  form.color === color.value
                    ? 'border-gray-800'
                    : 'border-gray-300'
                "
                :style="{ backgroundColor: color.value }"
              ></button>
            </div>
          </div>

          <!-- Descrição (opcional) -->
          <div>
            <label
              for="description"
              class="block text-sm font-medium text-gray-700 mb-1"
            >
              Descrição <span class="text-gray-400">(opcional)</span>
            </label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Descreva o propósito desta coluna..."
            ></textarea>
          </div>

          <!-- Preview -->
          <div class="p-3 bg-gray-50 rounded-md">
            <label class="block text-sm font-medium text-gray-700 mb-2"
              >Preview</label
            >
            <div
              class="p-3 bg-white rounded border-l-4 flex items-center justify-between"
              :style="{
                borderLeftColor: form.color,
                backgroundColor: form.color + '10',
              }"
            >
              <div class="flex items-center space-x-2">
                <div
                  class="w-3 h-3 rounded-full"
                  :style="{ backgroundColor: form.color }"
                ></div>
                <span class="font-medium">{{
                  form.name || "Nome da Coluna"
                }}</span>
              </div>
              <span class="text-xs bg-gray-100 px-2 py-1 rounded-full">0</span>
            </div>
          </div>

          <!-- Botões -->
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
            >
              {{ column ? "Atualizar" : "Criar" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { Icon } from "@iconify/vue";

const props = defineProps<{
  show: boolean;
  column?: any;
}>();

const emit = defineEmits(["close", "save"]);

const form = ref({
  name: "",
  color: "#3B82F6",
  description: "",
});

const predefinedColors = [
  { name: "Azul", value: "#3B82F6" },
  { name: "Verde", value: "#10B981" },
  { name: "Vermelho", value: "#EF4444" },
  { name: "Amarelo", value: "#F59E0B" },
  { name: "Roxo", value: "#8B5CF6" },
  { name: "Rosa", value: "#EC4899" },
  { name: "Índigo", value: "#6366F1" },
  { name: "Cinza", value: "#6B7280" },
];

// Preencher formulário quando coluna for passada
watch(
  () => props.column,
  (newColumn) => {
    if (newColumn) {
      form.value = {
        name: newColumn.name || "",
        color: newColumn.color || "#3B82F6",
        description: newColumn.description || "",
      };
    } else {
      form.value = {
        name: "",
        color: "#3B82F6",
        description: "",
      };
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  if (!form.value.name.trim()) {
    return;
  }

  emit("save", { ...form.value });
};
</script>
