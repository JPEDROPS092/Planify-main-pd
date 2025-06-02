<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded-md px-4 py-2 font-medium transition-colors',
      'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
      disabled || loading ? 'cursor-not-allowed opacity-70' : 'cursor-pointer',
      variant === 'primary' ? 'bg-blue-600 text-white hover:bg-blue-700' : '',
      variant === 'secondary'
        ? 'bg-gray-200 text-gray-800 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
        : '',
      variant === 'danger' ? 'bg-red-600 text-white hover:bg-red-700' : '',
      variant === 'success' ? 'bg-green-600 text-white hover:bg-green-700' : '',
      variant === 'warning'
        ? 'bg-yellow-600 text-white hover:bg-yellow-700'
        : '',
      variant === 'outline'
        ? 'border border-gray-300 bg-transparent text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800'
        : '',
      size === 'sm' ? 'text-xs' : '',
      size === 'md' ? 'text-sm' : '',
      size === 'lg' ? 'text-base' : '',
      fullWidth ? 'w-full' : '',
      className,
    ]"
    :disabled="disabled || loading"
    :type="type"
    @click="onClick"
  >
    <span v-if="loading" class="mr-2">
      <svg
        class="h-4 w-4 animate-spin"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </span>
    <slot />
  </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'LoadingButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      validator: (value: string) =>
        [
          'primary',
          'secondary',
          'danger',
          'success',
          'warning',
          'outline',
        ].includes(value),
    },
    size: {
      type: String,
      default: 'md',
      validator: (value: string) => ['sm', 'md', 'lg'].includes(value),
    },
    loading: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String as () => 'submit' | 'reset' | 'button' | undefined,
      default: 'button',
    },
    fullWidth: {
      type: Boolean,
      default: false,
    },
    className: {
      type: String,
      default: '',
    },
  },
  emits: ['click'],
  setup(props, { emit }) {
    const onClick = (event: MouseEvent) => {
      if (!props.loading && !props.disabled) {
        emit('click', event);
      }
    };

    return {
      onClick,
    };
  },
});
</script>
