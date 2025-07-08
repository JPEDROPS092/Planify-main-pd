<template>
  <div class="relative">
    <!-- Item do Dropdown -->
    <component
      :is="href ? 'a' : 'button'"
      :href="href"
      :target="external ? '_blank' : undefined"
      :rel="external ? 'noopener noreferrer' : undefined"
      @click="handleClick"
      :disabled="disabled"
      :class="[
        'group flex items-center w-full px-4 py-2 text-sm text-left transition-colors duration-200',
        disabled
          ? 'text-gray-400 cursor-not-allowed'
          : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900',
        danger &&
          !disabled &&
          'text-red-600 hover:bg-red-50 hover:text-red-700',
      ]"
      role="menuitem"
    >
      <!-- Ícone -->
      <Icon
        v-if="icon"
        :icon="icon"
        :class="[
          'mr-3 h-4 w-4',
          disabled
            ? 'text-gray-400'
            : 'text-gray-400 group-hover:text-gray-500',
          danger && !disabled && 'text-red-500 group-hover:text-red-600',
        ]"
      />

      <!-- Conteúdo -->
      <div class="flex-1">
        <div class="flex items-center justify-between">
          <span>{{ label }}</span>
          <Icon
            v-if="external"
            icon="lucide:external-link"
            class="ml-2 h-3 w-3 opacity-50"
          />
        </div>
        <p v-if="description" class="text-xs text-gray-500 mt-0.5">
          {{ description }}
        </p>
      </div>

      <!-- Indicador de carregamento -->
      <Icon
        v-if="loading"
        icon="lucide:loader"
        class="ml-2 h-4 w-4 animate-spin text-gray-400"
      />

      <!-- Seta para submenu -->
      <Icon
        v-if="hasSubmenu"
        icon="lucide:chevron-right"
        class="ml-2 h-4 w-4 text-gray-400"
      />
    </component>

    <!-- Divisor -->
    <hr v-if="divider" class="my-1 border-gray-200" />
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

interface Props {
  label: string;
  description?: string;
  icon?: string;
  href?: string;
  external?: boolean;
  disabled?: boolean;
  danger?: boolean;
  loading?: boolean;
  divider?: boolean;
  hasSubmenu?: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  click: [event: Event];
}>();

const handleClick = (event: Event) => {
  if (props.disabled || props.loading) {
    event.preventDefault();
    return;
  }

  emit("click", event);
};
</script>
