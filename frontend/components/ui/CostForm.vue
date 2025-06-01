<template>
  <form @submit.prevent="submitForm" class_name="space-y-6">
    <div>
      <label
        for="cost-description"
        class_name="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Descrição do Custo</label
      >
      <input
        type="text"
        id="cost-description"
        v-model="form.description"
        required
        class_name="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
      />
      <span v-if="errors.description" class_name="text-xs text-red-500">{{
        errors.description
      }}</span>
    </div>

    <div class_name="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <label
          for="cost-amount"
          class_name="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Valor (R$)</label
        >
        <input
          type="number"
          id="cost-amount"
          v-model.number="form.amount"
          required
          step="0.01"
          min="0"
          class_name="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        />
        <span v-if="errors.amount" class_name="text-xs text-red-500">{{
          errors.amount
        }}</span>
      </div>
      <div>
        <label
          for="cost-date"
          class_name="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >Data do Custo</label
        >
        <input
          type="date"
          id="cost-date"
          v-model="form.date"
          required
          class_name="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        />
        <span v-if="errors.date" class_name="text-xs text-red-500">{{
          errors.date
        }}</span>
      </div>
    </div>

    <div>
      <label
        for="cost-category"
        class_name="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >Categoria</label
      >
      <select
        id="cost-category"
        v-model="form.category"
        required
        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
      >
        <option value="" disabled>Selecione uma categoria</option>
        <option value="EQUIPAMENTOS">Equipamentos</option>
        <option value="RECURSOS_HUMANOS">Recursos Humanos</option>
        <option value="SOFTWARE">Software/Licenças</option>
        <option value="MARKETING">Marketing</option>
        <option value="VIAGENS">Viagens</option>
        <option value="TREINAMENTO">Treinamento</option>
        <option value="CONSULTORIA">Consultoria</option>
        <option value="INFRAESTRUTURA">Infraestrutura</option>
        <option value="OUTROS">Outros</option>
      </select>
      <span v-if="errors.category" class_name="text-xs text-red-500">{{
        errors.category
      }}</span>
    </div>

    <div class_name="flex justify-end space-x-3 pt-4">
      <Button type="button" variant="outline" @click="cancelForm"
        >Cancelar</Button
      >
      <LoadingButton
        type="submit"
        :loading="isSubmitting"
        :disabled="!isFormValid || isSubmitting"
      >
        {{ cost && cost.id ? 'Salvar Alterações' : 'Registrar Custo' }}
      </LoadingButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits, computed, onMounted } from 'vue';
import type { Cost, CostCreate, CostUpdate } from '~/services/costService';
import Button from '~/components/ui/Button.vue';
import LoadingButton from '~/components/LoadingButton.vue';
import { z } from 'zod';

const props = defineProps({
  projectId: {
    type: Number,
    required: true,
  },
  cost: {
    type: Object as () => Cost | null,
    default: null,
  },
});

const emit = defineEmits(['submit', 'cancel']);

const costCategories = [
  'EQUIPAMENTOS',
  'RECURSOS_HUMANOS',
  'SOFTWARE',
  'MARKETING',
  'VIAGENS',
  'TREINAMENTO',
  'CONSULTORIA',
  'INFRAESTRUTURA',
  'OUTROS',
] as const;

const costSchema = z.object({
  description: z.string().min(1, 'A descrição é obrigatória.'),
  amount: z.number().positive('O valor deve ser positivo.'),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, 'Data inválida.'),
  category: z.enum(costCategories, {
    errorMap: () => ({ message: 'Selecione uma categoria válida.' }),
  }),
  project: z.number(),
  id: z.number().optional(),
});

const initialFormState: CostCreate = {
  description: '',
  amount: 0,
  date: new Date().toISOString().split('T')[0], // Data atual por padrão
  category: 'OUTROS',
  project: props.projectId,
};

const form = ref({ ...initialFormState });
const errors = ref<Partial<Record<keyof CostCreate | 'id', string>>>({});
const isSubmitting = ref(false);

const isFormValid = computed(() => {
  const result = costSchema.safeParse(form.value);
  return result.success;
});

watch(
  () => props.cost,
  (newCost) => {
    if (newCost) {
      form.value = {
        description: newCost.description,
        amount: Number(newCost.amount), // Certifique-se de que é um número
        date: newCost.date, // Assumindo que a data já está no formato YYYY-MM-DD
        category: newCost.category,
        project: newCost.project || props.projectId,
      };
      if (newCost.id) {
        (form.value as CostUpdate).id = newCost.id;
      }
    } else {
      form.value = { ...initialFormState, project: props.projectId };
    }
    errors.value = {};
  },
  { immediate: true, deep: true }
);

function validateForm(): boolean {
  const result = costSchema.safeParse(form.value);
  if (!result.success) {
    errors.value = result.error.issues.reduce(
      (acc, issue) => {
        const path = issue.path.join('.') as keyof CostCreate;
        acc[path] = issue.message;
        return acc;
      },
      {} as Partial<Record<keyof CostCreate, string>>
    );
    return false;
  }
  errors.value = {};
  return true;
}

async function submitForm() {
  if (!validateForm()) {
    return;
  }
  isSubmitting.value = true;
  try {
    // Certificar que amount é um número antes de enviar
    const payload = { ...form.value, amount: Number(form.value.amount) };
    emit('submit', payload);
  } catch (error) {
    console.error('Erro ao submeter formulário de custo:', error);
  } finally {
    isSubmitting.value = false;
  }
}

function cancelForm() {
  emit('cancel');
}

onMounted(() => {
  if (!props.cost) {
    form.value.project = props.projectId;
  }
});
</script>
