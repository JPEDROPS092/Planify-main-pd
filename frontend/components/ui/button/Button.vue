<template>
  <button
    @click="(event) => props.onClick(event)"
    :disabled="props.disabled"
    class="inline-flex items-center px-4 py-2 border border-blue-400 text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
  >
    <Icon v-if="icon" :icon="icon" class="h-4 w-4 mr-2" />
    <span>{{ label }}</span>
  </button>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

const props = defineProps<{
  label?: string;
  icon?: string;
  disabled?: boolean;
  onClick: (event: MouseEvent) => void;
}>();
</script>
