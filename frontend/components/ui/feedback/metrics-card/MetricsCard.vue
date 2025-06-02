<!--
  MetricsCard.vue
  
  Componente para exibição de métricas e estatísticas em dashboards.
  Suporta diferentes formatos de dados, ícones e indicadores de tendência.
  
  Props:
  - title: Título da métrica
  - value: Valor da métrica
  - description: Descrição opcional
  - icon: Ícone a ser exibido (componente Lucide)
  - trend: Objeto com informação de tendência (valor e direção)
  - loading: Estado de carregamento
  - variant: Variante de estilo (default, outline)
  - class: Classes CSS adicionais
  
  Slots:
  - icon: Slot para personalizar o ícone
  - value: Slot para personalizar a exibição do valor
  - trend: Slot para personalizar a exibição da tendência
  - footer: Slot para adicionar conteúdo ao rodapé
-->

<script setup lang="ts">
import { computed } from 'vue';
import { cn } from '@/lib/utils';
import { cva } from 'class-variance-authority';
import { Card, CardContent } from '@/components/ui/display/card';
import {
  ArrowUpIcon,
  ArrowDownIcon,
  ArrowRightIcon,
  MinusIcon,
} from 'lucide-vue-next';

// Definir tipos para a tendência
export interface TrendInfo {
  value: number | string;
  direction: 'up' | 'down' | 'neutral';
  label?: string;
  isPositive?: boolean;
}

// Definir variantes de estilo para o card
const cardVariants = cva('metrics-card', {
  variants: {
    variant: {
      default: '',
      outline: 'border border-border',
    },
  },
  defaultVariants: {
    variant: 'default',
  },
});

// Props do componente
const props = withDefaults(
  defineProps<{
    title: string;
    value: number | string;
    description?: string;
    icon?: any; // Componente Lucide
    trend?: TrendInfo;
    loading?: boolean;
    variant?: 'default' | 'outline';
    class?: string;
  }>(),
  {
    description: '',
    loading: false,
    variant: 'default',
  }
);

// Formatação de valor numérico
const formatValue = (value: number | string): string => {
  if (typeof value === 'number') {
    // Formatar números grandes (K, M, B)
    if (value >= 1000000000) {
      return (value / 1000000000).toFixed(1) + 'B';
    } else if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K';
    } else {
      return value.toString();
    }
  }

  return value.toString();
};

// Obter ícone de tendência
const getTrendIcon = (direction: string) => {
  switch (direction) {
    case 'up':
      return ArrowUpIcon;
    case 'down':
      return ArrowDownIcon;
    case 'neutral':
      return MinusIcon;
    default:
      return ArrowRightIcon;
  }
};

// Obter classe de cor para tendência
const getTrendClass = (trend: TrendInfo) => {
  if (trend.isPositive !== undefined) {
    return trend.isPositive ? 'text-success' : 'text-destructive';
  }

  switch (trend.direction) {
    case 'up':
      return 'text-success';
    case 'down':
      return 'text-destructive';
    default:
      return 'text-muted-foreground';
  }
};

// Classes computadas para o card
const cardClass = computed(() => {
  return cn(cardVariants({ variant: props.variant }), props.class);
});
</script>

<template>
  <Card :class="cardClass">
    <CardContent class="p-6">
      <div class="flex flex-col space-y-3">
        <!-- Cabeçalho com título e ícone -->
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-medium text-muted-foreground">{{ title }}</h3>

          <!-- Slot para ícone personalizado -->
          <slot name="icon" v-if="$slots.icon || icon">
            <component
              v-if="icon"
              :is="icon"
              class="h-5 w-5 text-muted-foreground"
            />
          </slot>
        </div>

        <!-- Valor principal -->
        <div class="flex items-baseline gap-2">
          <!-- Estado de carregamento -->
          <template v-if="loading">
            <div class="h-9 w-24 bg-muted animate-pulse rounded"></div>
          </template>

          <!-- Slot para valor personalizado -->
          <slot name="value" v-else>
            <h2 class="text-3xl font-bold">{{ formatValue(value) }}</h2>
          </slot>

          <!-- Indicador de tendência -->
          <slot name="trend" v-if="trend && !loading">
            <div
              class="flex items-center text-sm font-medium"
              :class="getTrendClass(trend)"
            >
              <component
                :is="getTrendIcon(trend.direction)"
                class="h-4 w-4 mr-1"
              />
              {{ trend.value }}
              <span v-if="trend.label" class="ml-1 text-muted-foreground">{{
                trend.label
              }}</span>
            </div>
          </slot>
        </div>

        <!-- Descrição -->
        <p v-if="description && !loading" class="text-sm text-muted-foreground">
          {{ description }}
        </p>
        <div
          v-else-if="loading"
          class="h-4 w-36 bg-muted animate-pulse rounded"
        ></div>

        <!-- Slot para rodapé -->
        <slot name="footer"></slot>
      </div>
    </CardContent>
  </Card>
</template>

<style scoped>
/* Estilos específicos para o componente, se necessário */
</style>
