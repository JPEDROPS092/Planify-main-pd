<template>
  <span
    :class="[
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
      variantClasses[variant],
      sizeClasses[size],
      'transition-colors duration-200',
    ]"
  >
    <Icon v-if="icon" :icon="icon" :class="iconSizeClasses[size]" />
    <slot />
  </span>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

type BadgeVariant =
  | "default"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "secondary"
  | "status-planejado"
  | "status-andamento"
  | "status-pausado"
  | "status-concluido"
  | "status-cancelado"
  | "priority-baixa"
  | "priority-media"
  | "priority-alta"
  | "priority-critica";

type BadgeSize = "sm" | "md" | "lg";

interface Props {
  variant?: BadgeVariant;
  size?: BadgeSize;
  icon?: string;
}

const props = withDefaults(defineProps<Props>(), {
  variant: "default",
  size: "md",
});

const variantClasses: Record<BadgeVariant, string> = {
  default: "bg-gray-100 text-gray-800 hover:bg-gray-200",
  success: "bg-green-100 text-green-800 hover:bg-green-200",
  warning: "bg-yellow-100 text-yellow-800 hover:bg-yellow-200",
  danger: "bg-red-100 text-red-800 hover:bg-red-200",
  info: "bg-blue-100 text-blue-800 hover:bg-blue-200",
  secondary: "bg-purple-100 text-purple-800 hover:bg-purple-200",

  // Status específicos
  "status-planejado": "bg-blue-100 text-blue-800 border border-blue-200",
  "status-andamento": "bg-green-100 text-green-800 border border-green-200",
  "status-pausado": "bg-yellow-100 text-yellow-800 border border-yellow-200",
  "status-concluido":
    "bg-emerald-100 text-emerald-800 border border-emerald-200",
  "status-cancelado": "bg-red-100 text-red-800 border border-red-200",

  // Prioridades específicas
  "priority-baixa": "bg-gray-100 text-gray-700 border border-gray-200",
  "priority-media": "bg-blue-100 text-blue-700 border border-blue-200",
  "priority-alta": "bg-orange-100 text-orange-700 border border-orange-200",
  "priority-critica": "bg-red-100 text-red-700 border border-red-200",
};

const sizeClasses: Record<BadgeSize, string> = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-2.5 py-0.5 text-xs",
  lg: "px-3 py-1 text-sm",
};

const iconSizeClasses: Record<BadgeSize, string> = {
  sm: "h-3 w-3 mr-1",
  md: "h-3 w-3 mr-1.5",
  lg: "h-4 w-4 mr-1.5",
};
</script>
