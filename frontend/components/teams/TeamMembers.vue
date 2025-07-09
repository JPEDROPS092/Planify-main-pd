<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { useQuery } from "@tanstack/vue-query";
import { useToast } from "@/composables/useToast";
// Substitua pelo seu endpoint real:
import { useTeamsEquipesUsuariosDisponiveisList } from "@/api/equipes/equipes";

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
  definingRole: boolean;
  memberId: number;
  teamId: number;
}>();
const emit = defineEmits(["close", "add", "changeRole"]);

const selectedUserId = ref<number | null>(null);
const selectedRole = ref<keyof typeof PapelEnum | "">("");

const teamIdParam = computed(() => props.teamId)

const { data, isLoading, error } = useTeamsEquipesUsuariosDisponiveisList(
  { equipe: teamIdParam.value }, 
  { query: {queryKey: ['membros-disponiveis']} }
);

const userOptions = computed(() =>
  {
    return (data.value?.data || []).map((u: any) => ({
      label: u.full_name || u.username || u.email,
      value: u.id,
    })) || []
  }
);

const papelOptions = Object.entries(PapelEnum).map(([key, value]) => ({
  label: value,
  value: key
}))

function handleChange() {
  console.log(props.memberId, selectedRole.value)
  if (selectedRole.value) {
    emit("changeRole", {
      usuario: props.memberId || 0,
      papel: selectedRole.value
    })
    emit("close");
    selectedUserId.value = null;
  }
}

function handleAdd() {
  if (selectedUserId.value) {
    emit("add", 
      {
        usuario: selectedUserId.value,
        papel: selectedRole.value
      });
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
      <h2 class="text-xl font-bold mb-4">{{!definingRole ? "Adicionar Membro à Equipe" : "Atualizar papel do membro de equipe"}}</h2>

      <div v-if="isLoading" class="py-4 text-center">Carregando usuários...</div>
      <div v-else-if="error" class="py-4 text-center">Erro ao carregar usuários: {{ error }}</div>
      <div v-else-if="!definingRole">
        <select
          v-model="selectedUserId"
          class="w-full border rounded px-3 py-2 mb-4"
          @change="selectedRole = ''"
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
        <select
          v-if="selectedUserId"
          v-model="selectedRole"
          class="w-full border rounded px-3 py-2 mb-4"
        >
          <option value="" disabled>Selecione o novo papel do membro</option>
          <option
            v-for="papel in papelOptions"
            :key="papel.value"
            :value="papel.value"
          >
            {{ papel.label }}
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
            :disabled="!selectedUserId || !selectedRole"
            @click="handleAdd"
            class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            type="button"
          >
            Adicionar
          </button>
        </div>
      </div>
      <div v-else>
        <select
          v-model="selectedRole"
          class="w-full border rounded px-3 py-2 mb-4"
        >
          <option value="" disabled>Selecione o novo papel do membro</option>
          <option
            v-for="papel in papelOptions"
            :key="papel.value"
            :value="papel.value"
          >
            {{ papel.label }}
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
            :disabled="!selectedRole"
            @click="handleChange"
            class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            type="button"
          >
            Atualizar
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