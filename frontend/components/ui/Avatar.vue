<template>
  <div class="relative inline-block">
    <div
      :class="[
        'inline-flex items-center justify-center rounded-full bg-gray-100 border-2 border-white shadow-sm',
        sizeClasses[size],
        'transition-all duration-200 hover:scale-105',
      ]"
    >
      <!-- Imagem -->
      <img
        v-if="src"
        :src="src"
        :alt="alt || name"
        :class="['rounded-full object-cover', sizeClasses[size]]"
        @error="showFallback = true"
        v-show="!showFallback"
      />

      <!-- Fallback com iniciais -->
      <span
        v-if="!src || showFallback"
        :class="[
          'font-medium text-white',
          textSizeClasses[size],
          getBackgroundColor(),
        ]"
      >
        {{ initials }}
      </span>
    </div>

    <!-- Indicador de status -->
    <div
      v-if="status"
      :class="[
        'absolute -bottom-0 -right-0 rounded-full border-2 border-white',
        statusSizeClasses[size],
        getStatusColor(),
      ]"
    />
  </div>
</template>

<script setup lang="ts">
type AvatarSize = "xs" | "sm" | "md" | "lg" | "xl";
type AvatarStatus = "online" | "offline" | "away" | "busy";

interface Props {
  src?: string;
  name?: string;
  alt?: string;
  size?: AvatarSize;
  status?: AvatarStatus;
}

const props = withDefaults(defineProps<Props>(), {
  size: "md",
});

const showFallback = ref(false);

const sizeClasses: Record<AvatarSize, string> = {
  xs: "h-6 w-6",
  sm: "h-8 w-8",
  md: "h-10 w-10",
  lg: "h-12 w-12",
  xl: "h-16 w-16",
};

const textSizeClasses: Record<AvatarSize, string> = {
  xs: "text-xs",
  sm: "text-sm",
  md: "text-sm",
  lg: "text-base",
  xl: "text-lg",
};

const statusSizeClasses: Record<AvatarSize, string> = {
  xs: "h-2 w-2",
  sm: "h-2.5 w-2.5",
  md: "h-3 w-3",
  lg: "h-3.5 w-3.5",
  xl: "h-4 w-4",
};

const initials = computed(() => {
  if (!props.name) return "?";
  return props.name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
});

const getBackgroundColor = () => {
  if (!props.name) return "bg-gray-500";

  const colors = [
    "bg-red-500",
    "bg-yellow-500",
    "bg-green-500",
    "bg-blue-500",
    "bg-indigo-500",
    "bg-purple-500",
    "bg-pink-500",
    "bg-orange-500",
  ];

  const hash = props.name.split("").reduce((acc, char) => {
    return char.charCodeAt(0) + ((acc << 5) - acc);
  }, 0);

  return colors[Math.abs(hash) % colors.length];
};

const getStatusColor = () => {
  const colors = {
    online: "bg-green-500",
    offline: "bg-gray-400",
    away: "bg-yellow-500",
    busy: "bg-red-500",
  };
  return colors[props.status!];
};
</script>
