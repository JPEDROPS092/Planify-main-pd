<!--
  CardDescription.vue
  
  Componente para a descrição de um Card.
  Geralmente usado dentro de CardHeader.
  
  Props:
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <CardHeader>
    <CardTitle>Título do Card</CardTitle>
    <CardDescription>Esta é uma descrição detalhada do conteúdo do card.</CardDescription>
  </CardHeader>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Documentação adicionada
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';

const props = defineProps<{
  class?: HTMLAttributes['class'];
}>();
</script>

<template>
  <p :class="cn('text-sm text-muted-foreground', props.class)">
    <slot />
  </p>
</template>
