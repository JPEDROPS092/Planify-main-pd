<script setup lang="ts">
import { Icon } from '@iconify/vue';
import { buttonVariants } from './index';

// Props do componente
const props = withDefaults(
  defineProps<{
    type?: 'button' | 'submit' | 'reset';
    variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
    size?: 'default' | 'sm' | 'lg' | 'icon';
    disabled?: boolean;
    loading?: boolean;
    icon?: string;
  }>(),
  {
    type: 'button',
    variant: 'default',
    size: 'default',
    disabled: false,
    loading: false,
    icon: '',
  }
);

// Emits
const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void;
}>();

// Computeds
const buttonClasses = computed(() => {
  return buttonVariants({ variant: props.variant, size: props.size });
});
</script>

<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="emit('click', $event)"
  >
    <Icon v-if="loading" icon="lucide:loader-2" class="h-4 w-4 mr-2 animate-spin" />
    <Icon v-else-if="icon" :icon="icon" class="h-4 w-4" :class="{ 'mr-2': $slots.default }" />
    <slot />
  </button>
</template>
