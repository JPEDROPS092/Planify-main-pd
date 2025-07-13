<!-- components/ui/Toast.vue -->
<template>
  <Teleport to="body">
    <div
      v-if="show"
      class="fixed top-4 right-4 z-50 min-w-[300px] max-w-md"
    >
      <div
        :class="[
          'bg-white rounded-lg shadow-lg border p-4 transition-all duration-300',
          typeClasses,
          show ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'
        ]"
      >
        <div class="flex items-start">
          <div class="flex-shrink-0">
            <Icon :icon="typeIcon" class="h-5 w-5" />
          </div>
          <div class="ml-3 w-0 flex-1">
            <p class="text-sm font-medium" v-if="title">{{ title }}</p>
            <p class="text-sm" :class="title ? 'mt-1' : ''">{{ description }}</p>
          </div>
          <div class="ml-4 flex-shrink-0 flex">
            <button
              @click="close"
              class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <Icon icon="lucide:x" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { Icon } from '@iconify/vue';

interface Props {
  show: boolean;
  type?: 'success' | 'error' | 'warning' | 'info';
  title?: string;
  description: string;
  duration?: number;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 5000,
});

const emit = defineEmits<{
  close: [];
}>();

const typeClasses = computed(() => {
  const classes = {
    success: 'border-green-200 text-green-800',
    error: 'border-red-200 text-red-800',
    warning: 'border-yellow-200 text-yellow-800',
    info: 'border-blue-200 text-blue-800',
  };
  return classes[props.type];
});

const typeIcon = computed(() => {
  const icons = {
    success: 'lucide:check-circle',
    error: 'lucide:x-circle',
    warning: 'lucide:alert-triangle',
    info: 'lucide:info',
  };
  return icons[props.type];
});

const close = () => {
  emit('close');
};

// Auto close
watch(() => props.show, (newShow) => {
  if (newShow && props.duration > 0) {
    setTimeout(() => {
      close();
    }, props.duration);
  }
});
</script>
</script>
