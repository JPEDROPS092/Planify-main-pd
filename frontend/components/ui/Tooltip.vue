<template>
  <div class="relative inline-block">
    <!-- Trigger -->
    <div
      ref="triggerRef"
      @mouseenter="show"
      @mouseleave="hide"
      @focus="show"
      @blur="hide"
    >
      <slot name="trigger">
        <button
          class="inline-flex items-center text-gray-400 hover:text-gray-600"
        >
          <Icon icon="lucide:help-circle" class="h-4 w-4" />
        </button>
      </slot>
    </div>

    <!-- Tooltip -->
    <Teleport to="body">
      <div
        v-if="isVisible"
        ref="tooltipRef"
        :class="[
          'absolute z-50 px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm',
          'transition-opacity duration-200',
          'pointer-events-none',
          'max-w-xs break-words',
        ]"
        :style="tooltipStyle"
        role="tooltip"
      >
        <slot>{{ content }}</slot>

        <!-- Seta -->
        <div
          :class="[
            'absolute w-2 h-2 bg-gray-900 transform rotate-45',
            arrowClasses[placement],
          ]"
        />
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

type TooltipPlacement = "top" | "bottom" | "left" | "right";

interface Props {
  content?: string;
  placement?: TooltipPlacement;
  delay?: number;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  placement: "top",
  delay: 100,
  disabled: false,
});

const isVisible = ref(false);
const triggerRef = ref<HTMLElement>();
const tooltipRef = ref<HTMLElement>();
let showTimeout: NodeJS.Timeout;
let hideTimeout: NodeJS.Timeout;

const tooltipStyle = ref({});

const arrowClasses: Record<TooltipPlacement, string> = {
  top: "-bottom-1 left-1/2 transform -translate-x-1/2",
  bottom: "-top-1 left-1/2 transform -translate-x-1/2",
  left: "-right-1 top-1/2 transform -translate-y-1/2",
  right: "-left-1 top-1/2 transform -translate-y-1/2",
};

const show = () => {
  if (props.disabled) return;

  clearTimeout(hideTimeout);
  showTimeout = setTimeout(() => {
    isVisible.value = true;
    nextTick(() => updatePosition());
  }, props.delay);
};

const hide = () => {
  clearTimeout(showTimeout);
  hideTimeout = setTimeout(() => {
    isVisible.value = false;
  }, 100);
};

const updatePosition = () => {
  if (!triggerRef.value || !tooltipRef.value) return;

  const trigger = triggerRef.value.getBoundingClientRect();
  const tooltip = tooltipRef.value.getBoundingClientRect();
  const viewport = {
    width: window.innerWidth,
    height: window.innerHeight,
  };

  let top = 0;
  let left = 0;

  switch (props.placement) {
    case "top":
      top = trigger.top - tooltip.height - 8;
      left = trigger.left + trigger.width / 2 - tooltip.width / 2;
      break;
    case "bottom":
      top = trigger.bottom + 8;
      left = trigger.left + trigger.width / 2 - tooltip.width / 2;
      break;
    case "left":
      top = trigger.top + trigger.height / 2 - tooltip.height / 2;
      left = trigger.left - tooltip.width - 8;
      break;
    case "right":
      top = trigger.top + trigger.height / 2 - tooltip.height / 2;
      left = trigger.right + 8;
      break;
  }

  // Ajustar para não sair da viewport
  if (left < 8) left = 8;
  if (left + tooltip.width > viewport.width - 8) {
    left = viewport.width - tooltip.width - 8;
  }
  if (top < 8) top = 8;
  if (top + tooltip.height > viewport.height - 8) {
    top = viewport.height - tooltip.height - 8;
  }

  tooltipStyle.value = {
    top: `${top}px`,
    left: `${left}px`,
  };
};

onUnmounted(() => {
  clearTimeout(showTimeout);
  clearTimeout(hideTimeout);
});
</script>
