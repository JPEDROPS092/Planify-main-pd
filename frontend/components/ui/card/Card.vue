<script setup lang="ts">
import { cardVariants } from './index';

// Props do componente
const props = withDefaults(
  defineProps<{
    variant?: 'default' | 'destructive' | 'success';
  }>(),
  {
    variant: 'default',
  }
);

// Computeds
const cardClasses = computed(() => {
  return cardVariants({ variant: props.variant });
});
</script>

<template>
  <div :class="cardClasses">
    <slot />
  </div>
</template>
