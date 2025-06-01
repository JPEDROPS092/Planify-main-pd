<!--
  CardHeader.vue
  
  Componente para o cabeçalho de um Card.
  Geralmente contém CardTitle e CardDescription.
  
  Props:
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <CardHeader>
    <CardTitle>Título do Card</CardTitle>
    <CardDescription>Descrição do card</CardDescription>
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
  <div :class="cn('flex flex-col gap-y-1.5 p-6', props.class)">
    <slot />
  </div>
</template>
