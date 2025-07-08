<template>
  <div class="w-full">
    <!-- Barra de progresso -->
    <div
      :class="[
        'relative overflow-hidden rounded-full',
        sizeClasses[size],
        'transition-all duration-300',
      ]"
      :style="{ backgroundColor: trackColor }"
    >
      <!-- Barra de preenchimento -->
      <div
        :class="[
          'h-full rounded-full transition-all duration-500 ease-out',
          getProgressColor(),
        ]"
        :style="{ width: `${clampedValue}%` }"
      />

      <!-- Brilho animado (opcional) -->
      <div
        v-if="animated"
        class="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-20 -skew-x-12 animate-pulse"
      />
    </div>

    <!-- Label e valor (opcional) -->
    <div
      v-if="showLabel || showValue"
      class="flex justify-between items-center mt-1"
    >
      <span
        v-if="showLabel && label"
        :class="labelSizeClasses[size]"
        class="text-gray-600"
      >
        {{ label }}
      </span>
      <span
        v-if="showValue"
        :class="labelSizeClasses[size]"
        class="text-gray-800 font-medium"
      >
        {{ Math.round(clampedValue) }}{{ unit }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
type ProgressSize = "xs" | "sm" | "md" | "lg" | "xl";
type ProgressVariant = "default" | "success" | "warning" | "danger" | "info";

interface Props {
  value: number;
  max?: number;
  size?: ProgressSize;
  variant?: ProgressVariant;
  label?: string;
  showLabel?: boolean;
  showValue?: boolean;
  unit?: string;
  animated?: boolean;
  trackColor?: string;
}

const props = withDefaults(defineProps<Props>(), {
  max: 100,
  size: "md",
  variant: "default",
  unit: "%",
  animated: false,
  trackColor: "#f3f4f6",
});

const clampedValue = computed(() => {
  const percentage = (props.value / props.max) * 100;
  return Math.min(Math.max(percentage, 0), 100);
});

const sizeClasses: Record<ProgressSize, string> = {
  xs: "h-1",
  sm: "h-2",
  md: "h-3",
  lg: "h-4",
  xl: "h-6",
};

const labelSizeClasses: Record<ProgressSize, string> = {
  xs: "text-xs",
  sm: "text-xs",
  md: "text-sm",
  lg: "text-sm",
  xl: "text-base",
};

const getProgressColor = () => {
  // Cor baseada na variante
  if (props.variant !== "default") {
    const variantColors = {
      success: "bg-green-500",
      warning: "bg-yellow-500",
      danger: "bg-red-500",
      info: "bg-blue-500",
    };
    return variantColors[props.variant];
  }

  // Cor baseada na porcentagem (semáforo)
  if (clampedValue.value >= 80) return "bg-green-500";
  if (clampedValue.value >= 60) return "bg-blue-500";
  if (clampedValue.value >= 40) return "bg-yellow-500";
  if (clampedValue.value >= 20) return "bg-orange-500";
  return "bg-red-500";
};
</script>
