<!--
  CardTitle.vue
  
  Componente para o título de um Card.
  Geralmente usado dentro de CardHeader.
  
  Props:
  - as: Elemento HTML a ser renderizado (h1, h2, h3, etc.)
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <CardHeader>
    <CardTitle as="h2">Título do Card</CardTitle>
    <CardDescription>Descrição do card</CardDescription>
  </CardHeader>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Documentação adicionada
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';

const props = withDefaults(
  defineProps<{
    as?: string;
    class?: HTMLAttributes['class'];
  }>(),
  {
    as: 'h3',
  }
);
</script>

<template>
  <component
    :is="props.as"
    :class="cn('font-semibold leading-none tracking-tight', props.class)"
  >
    <slot />
  </component>
</template>
