<template>
  <!-- Este componente é um wrapper para o componente em /components/task/TaskForm.vue -->
  <task-form
    v-bind="$attrs"
    :task="task"
    :project-id="projectId"
    :loading="loading"
    @submit="$emit('submit', $event)"
    @cancel="$emit('cancel')"
  />
</template>

<script setup lang="ts">
// Este componente é um wrapper para o componente TaskForm em /components/task/TaskForm.vue
// Mantido para compatibilidade com código existente
import TaskForm from './task/TaskForm.vue';
import type { Tarefa } from '~/services/api/types';

const props = defineProps({
  task: {
    type: Object as () => Tarefa | null,
    default: null,
  },
  projectId: {
    type: Number,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['submit', 'cancel']);
</script>
