<!--
  CardContent.vue
  
  Componente para o conteúdo principal de um Card.
  
  Props:
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <CardContent>
    <p>Este é o conteúdo principal do card.</p>
  </CardContent>
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
  <div :class="cn('p-6 pt-0', props.class)">
    <slot />
  </div>
</template>
