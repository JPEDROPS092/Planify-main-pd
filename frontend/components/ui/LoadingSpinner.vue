<template>
  <div class="flex items-center justify-center">
    <div
      :class="[
        'animate-spin rounded-full border-solid',
        sizeClasses[size],
        colorClasses[color],
      ]"
    />
    <span v-if="text" :class="['ml-3 text-sm', textColorClasses[color]]">
      {{ text }}
    </span>
  </div>
</template>

<script setup lang="ts">
type SpinnerSize = "xs" | "sm" | "md" | "lg" | "xl";
type SpinnerColor = "primary" | "secondary" | "white" | "gray";

interface Props {
  size?: SpinnerSize;
  color?: SpinnerColor;
  text?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: "md",
  color: "primary",
});

const sizeClasses: Record<SpinnerSize, string> = {
  xs: "h-3 w-3 border-2",
  sm: "h-4 w-4 border-2",
  md: "h-6 w-6 border-2",
  lg: "h-8 w-8 border-[3px]",
  xl: "h-12 w-12 border-4",
};

const colorClasses: Record<SpinnerColor, string> = {
  primary: "border-primary-600 border-t-transparent",
  secondary: "border-gray-600 border-t-transparent",
  white: "border-white border-t-transparent",
  gray: "border-gray-300 border-t-gray-600",
};

const textColorClasses: Record<SpinnerColor, string> = {
  primary: "text-primary-600",
  secondary: "text-gray-600",
  white: "text-white",
  gray: "text-gray-600",
};
</script>
