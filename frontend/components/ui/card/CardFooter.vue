<!--
  CardFooter.vue
  
  Componente para o rodapé de um Card.
  Geralmente contém ações relacionadas ao card.
  
  Props:
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <CardFooter>
    <Button variant="outline">Cancelar</Button>
    <Button>Salvar</Button>
  </CardFooter>
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
  <div :class="cn('flex items-center p-6 pt-0', props.class)">
    <slot />
  </div>
</template>
