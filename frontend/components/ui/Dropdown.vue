<template>
  <div class="relative inline-block text-left">
    <!-- Trigger -->
    <div>
      <button
        ref="triggerRef"
        @click="toggle"
        :class="[
          'inline-flex justify-center items-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700',
          'hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500',
          'transition-colors duration-200',
          isOpen && 'ring-2 ring-primary-500',
        ]"
        :disabled="disabled"
      >
        <slot name="trigger">
          <span>{{ triggerText }}</span>
          <Icon
            :icon="isOpen ? 'lucide:chevron-up' : 'lucide:chevron-down'"
            class="ml-2 h-4 w-4"
          />
        </slot>
      </button>
    </div>

    <!-- Dropdown Menu -->
    <Teleport to="body">
      <div
        v-if="isOpen"
        ref="menuRef"
        :class="[
          'absolute z-50 mt-2 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5',
          'focus:outline-none',
          'transform transition-all duration-200 ease-out',
          widthClasses[width],
        ]"
        :style="menuStyle"
        role="menu"
      >
        <div class="py-1" role="none">
          <slot />
        </div>
      </div>
    </Teleport>

    <!-- Overlay para fechar ao clicar fora -->
    <div v-if="isOpen" class="fixed inset-0 z-40" @click="close" />
  </div>
</template>

<script setup lang="ts">
import { Icon } from "@iconify/vue";

type DropdownWidth = "auto" | "trigger" | "sm" | "md" | "lg" | "xl";

interface Props {
  triggerText?: string;
  disabled?: boolean;
  width?: DropdownWidth;
}

const props = withDefaults(defineProps<Props>(), {
  triggerText: "Opções",
  width: "auto",
});

const emit = defineEmits<{
  open: [];
  close: [];
}>();

const isOpen = ref(false);
const triggerRef = ref<HTMLElement>();
const menuRef = ref<HTMLElement>();
const menuStyle = ref({});

const widthClasses: Record<DropdownWidth, string> = {
  auto: "min-w-max",
  trigger: "w-auto",
  sm: "w-48",
  md: "w-56",
  lg: "w-64",
  xl: "w-72",
};

const toggle = () => {
  if (props.disabled) return;
  isOpen.value ? close() : open();
};

const open = () => {
  isOpen.value = true;
  emit("open");
  nextTick(() => updatePosition());
};

const close = () => {
  isOpen.value = false;
  emit("close");
};

const updatePosition = () => {
  if (!triggerRef.value || !menuRef.value) return;

  const trigger = triggerRef.value.getBoundingClientRect();
  const menu = menuRef.value.getBoundingClientRect();
  const viewport = {
    width: window.innerWidth,
    height: window.innerHeight,
  };

  let top = trigger.bottom + 8;
  let left = trigger.left;

  // Se o menu sair da viewport na direita, alinhar à direita
  if (left + menu.width > viewport.width - 16) {
    left = trigger.right - menu.width;
  }

  // Se o menu sair da viewport embaixo, mostrar acima
  if (top + menu.height > viewport.height - 16) {
    top = trigger.top - menu.height - 8;
  }

  // Garantir que não saia da viewport à esquerda
  if (left < 16) left = 16;

  // Se width é 'trigger', igualar a largura do trigger
  const width = props.width === "trigger" ? `${trigger.width}px` : undefined;

  menuStyle.value = {
    top: `${top}px`,
    left: `${left}px`,
    ...(width && { width }),
  };
};

// Fechar com ESC
onMounted(() => {
  const handleKeydown = (e: KeyboardEvent) => {
    if (e.key === "Escape" && isOpen.value) {
      close();
    }
  };

  document.addEventListener("keydown", handleKeydown);

  onUnmounted(() => {
    document.removeEventListener("keydown", handleKeydown);
  });
});
</script>
