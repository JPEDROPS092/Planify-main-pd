<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useToast } from "@/composables/useToast";
// Substitua pelo seu endpoint real:
import { useTeamsEquipesUsuariosDisponiveisList } from "@/api/equipes/equipes";

const props = defineProps<{
  show: boolean;
}>();
const emit = defineEmits(["close", "add"]);

const selectedUserId = ref<number | null>(null);

const { data, isLoading, error } = useTeamsEquipesUsuariosDisponiveisList();

const userOptions = computed(() =>
  {
    console.log(data.value?.data);
    return (data.value?.data || []).map((u: any) => ({
      label: u.full_name || u.username || u.email,
      value: u.id,
    })) || []
  }
  
);

function handleAdd() {
  if (selectedUserId.value) {
    emit("add", selectedUserId.value);
    emit("close");
    selectedUserId.value = null;
  }
}

watch(
  () => props.show,
  (val) => {
    if (!val) selectedUserId.value = null;
  }
);
</script>

<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40"
  >
    <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6 relative">
      <h2 class="text-xl font-bold mb-4">Adicionar Membro à Equipe</h2>

      <div v-if="isLoading" class="py-4 text-center">Carregando usuários...</div>
      <div v-else-if="error" class="py-4 text-center">Erro ao carregar usuários: {{ error }}</div>
      <div v-else>
        <select
          v-model="selectedUserId"
          class="w-full border rounded px-3 py-2 mb-4"
        >
          <option value="" disabled>Selecione um usuário</option>
          <option
            v-for="user in userOptions"
            :key="user.value"
            :value="user.value"
          >
            {{ user.label }}
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
            :disabled="!selectedUserId"
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
        ×
      </button>
    </div>
  </div>
</template>

<style>

</style>