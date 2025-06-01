<!--
  Timeline.vue
  
  Componente para exibição de eventos em ordem cronológica.
  Útil para históricos de projetos, atividades e marcos.
  
  Props:
  - items: Array de itens da timeline
  - variant: Variante de estilo (default, condensed)
  - class: Classes CSS adicionais
  
  Slots:
  - item: Slot para personalizar a renderização de cada item
  - icon: Slot para personalizar o ícone de cada item
-->

<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';
import { cva } from 'class-variance-authority';
import { Circle, CheckCircle2, AlertCircle, Clock } from 'lucide-vue-next';

// Definir tipos para os itens da timeline
export interface TimelineItem {
  id: string | number;
  title: string;
  description?: string;
  date: string | Date;
  status?: 'pending' | 'completed' | 'warning' | 'info';
  icon?: string;
  metadata?: Record<string, any>;
}

// Definir variantes de estilo para a timeline
const timelineVariants = cva('timeline', {
  variants: {
    variant: {
      default: 'space-y-6',
      condensed: 'space-y-3',
    },
  },
  defaultVariants: {
    variant: 'default',
  },
});

// Props do componente
const props = withDefaults(
  defineProps<{
    items: TimelineItem[];
    variant?: 'default' | 'condensed';
    class?: string;
  }>(),
  {
    variant: 'default',
  }
);

// Formatação de data
const formatDate = (date: string | Date): string => {
  if (!date) return '';

  const dateObj = typeof date === 'string' ? new Date(date) : date;

  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(dateObj);
};

// Obter ícone com base no status
const getStatusIcon = (status?: string) => {
  switch (status) {
    case 'completed':
      return CheckCircle2;
    case 'warning':
      return AlertCircle;
    case 'pending':
      return Clock;
    default:
      return Circle;
  }
};

// Obter classe de cor com base no status
const getStatusClass = (status?: string) => {
  switch (status) {
    case 'completed':
      return 'text-success';
    case 'warning':
      return 'text-warning';
    case 'pending':
      return 'text-muted-foreground';
    default:
      return 'text-primary';
  }
};

// Classes computadas para a timeline
const timelineClass = computed(() => {
  return cn(timelineVariants({ variant: props.variant }), props.class);
});
</script>

<template>
  <div :class="timelineClass">
    <div
      v-for="(item, index) in items"
      :key="item.id"
      class="timeline-item relative"
      :class="{ 'pb-6': index !== items.length - 1 }"
    >
      <!-- Linha conectora -->
      <div
        v-if="index !== items.length - 1"
        class="absolute left-3.5 top-5 bottom-0 w-px bg-border"
        :class="{ 'left-2.5': variant === 'condensed' }"
      ></div>

      <div class="flex gap-3">
        <!-- Ícone / Indicador -->
        <div
          class="timeline-icon z-10 flex-shrink-0 mt-1"
          :class="[
            variant === 'condensed' ? 'mt-0.5' : 'mt-1',
            getStatusClass(item.status),
          ]"
        >
          <!-- Slot para ícone personalizado -->
          <slot name="icon" :item="item">
            <component
              :is="getStatusIcon(item.status)"
              :class="[variant === 'condensed' ? 'h-5 w-5' : 'h-7 w-7']"
            />
          </slot>
        </div>

        <!-- Conteúdo -->
        <div class="timeline-content flex-1">
          <!-- Slot para conteúdo personalizado -->
          <slot name="item" :item="item">
            <div class="space-y-1">
              <div
                class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1"
              >
                <h4
                  class="font-medium leading-none"
                  :class="[variant === 'condensed' ? 'text-sm' : 'text-base']"
                >
                  {{ item.title }}
                </h4>
                <span
                  class="text-muted-foreground"
                  :class="[variant === 'condensed' ? 'text-xs' : 'text-sm']"
                >
                  {{ formatDate(item.date) }}
                </span>
              </div>

              <p
                v-if="item.description"
                class="text-muted-foreground"
                :class="[variant === 'condensed' ? 'text-xs' : 'text-sm']"
              >
                {{ item.description }}
              </p>
            </div>
          </slot>
        </div>
      </div>
    </div>

    <!-- Mensagem quando não há itens -->
    <div
      v-if="items.length === 0"
      class="py-4 text-center text-sm text-muted-foreground"
    >
      Nenhum item para exibir na timeline.
    </div>
  </div>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
