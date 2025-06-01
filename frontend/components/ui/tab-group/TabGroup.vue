<!--
  TabGroup.vue
  
  Componente para organização de conteúdo em abas.
  Permite alternar entre diferentes seções de conteúdo sem navegar para outra página.
  
  Props:
  - tabs: Array de abas
  - modelValue: Índice ou ID da aba ativa (v-model)
  - variant: Variante de estilo (default, underline, pills)
  - class: Classes CSS adicionais
  
  Eventos:
  - update:modelValue: Emitido quando a aba ativa é alterada
  
  Slots:
  - tab: Slot para personalizar a renderização de cada aba
  - content: Slot para o conteúdo de cada aba
-->

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { cn } from '@/lib/utils';
import { cva } from 'class-variance-authority';

// Definir tipos para as abas
export interface Tab {
  id: string | number;
  label: string;
  icon?: any; // Componente Lucide
  disabled?: boolean;
  content?: any; // Conteúdo da aba (opcional, pode ser usado com slots)
}

// Definir variantes de estilo para as abas
const tabVariants = cva('tab-item', {
  variants: {
    variant: {
      default:
        'inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium rounded-md transition-all',
      underline:
        'inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium border-b-2 border-transparent transition-all',
      pills:
        'inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium rounded-full transition-all',
    },
  },
  defaultVariants: {
    variant: 'default',
  },
});

// Props do componente
const props = withDefaults(
  defineProps<{
    tabs: Tab[];
    modelValue?: string | number;
    variant?: 'default' | 'underline' | 'pills';
    class?: string;
  }>(),
  {
    variant: 'default',
  }
);

const emit = defineEmits<{
  'update:modelValue': [value: string | number];
}>();

// Referência para a aba ativa
const activeTab = ref<string | number | null>(null);

// Observar mudanças no modelValue
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue !== undefined && newValue !== activeTab.value) {
      activeTab.value = newValue;
    }
  }
);

// Inicializar a aba ativa
onMounted(() => {
  // Se o modelValue for fornecido, use-o como aba ativa
  if (props.modelValue !== undefined) {
    activeTab.value = props.modelValue;
  }
  // Caso contrário, use a primeira aba não desabilitada
  else if (props.tabs.length > 0) {
    const firstEnabledTab = props.tabs.find((tab) => !tab.disabled);
    activeTab.value = firstEnabledTab ? firstEnabledTab.id : props.tabs[0].id;
  }
});

// Alternar para uma aba específica
const selectTab = (tabId: string | number) => {
  if (activeTab.value !== tabId) {
    activeTab.value = tabId;
    emit('update:modelValue', tabId);
  }
};

// Verificar se uma aba está ativa
const isTabActive = (tabId: string | number): boolean => {
  return activeTab.value === tabId;
};

// Obter a aba ativa
const currentTab = computed(() => {
  return props.tabs.find((tab) => tab.id === activeTab.value);
});

// Obter classes para uma aba específica
const getTabClasses = (tab: Tab) => {
  return cn(tabVariants({ variant: props.variant }), {
    'bg-primary text-primary-foreground':
      isTabActive(tab.id) && props.variant === 'default',
    'border-primary text-primary':
      isTabActive(tab.id) && props.variant === 'underline',
    'bg-primary text-primary-foreground':
      isTabActive(tab.id) && props.variant === 'pills',
    'hover:bg-muted': !isTabActive(tab.id) && props.variant === 'default',
    'hover:border-muted-foreground':
      !isTabActive(tab.id) && props.variant === 'underline',
    'hover:bg-muted': !isTabActive(tab.id) && props.variant === 'pills',
    'text-muted-foreground': !isTabActive(tab.id),
    'opacity-50 cursor-not-allowed': tab.disabled,
  });
};
</script>

<template>
  <div :class="cn('tab-group', props.class)">
    <!-- Cabeçalho das abas -->
    <div
      class="tab-header flex"
      :class="{
        'border-b': variant === 'underline',
        'gap-1': variant === 'default' || variant === 'pills',
        'gap-0': variant === 'underline',
      }"
    >
      <!-- Renderizar cada aba -->
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="getTabClasses(tab)"
        @click="!tab.disabled && selectTab(tab.id)"
        :disabled="tab.disabled"
        role="tab"
        :aria-selected="isTabActive(tab.id)"
        :tabindex="isTabActive(tab.id) ? 0 : -1"
      >
        <!-- Slot para personalizar a aba -->
        <slot name="tab" :tab="tab" :active="isTabActive(tab.id)">
          <component v-if="tab.icon" :is="tab.icon" class="h-4 w-4 mr-2" />
          <span>{{ tab.label }}</span>
        </slot>
      </button>
    </div>

    <!-- Conteúdo das abas -->
    <div class="tab-content mt-4">
      <template v-for="tab in tabs" :key="tab.id">
        <div
          v-if="isTabActive(tab.id)"
          role="tabpanel"
          :aria-labelledby="`tab-${tab.id}`"
        >
          <!-- Slot para o conteúdo da aba -->
          <slot :name="`content-${tab.id}`" :tab="tab">
            <slot name="content" :tab="tab">
              <div v-if="tab.content">
                {{ tab.content }}
              </div>
            </slot>
          </slot>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
