<!--
  Badge.vue
  
  Componente para exibir etiquetas, status ou pequenas informações destacadas.
  
  Props:
  - variant: Estilo visual do badge (default, secondary, outline, destructive, success)
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <Badge variant="success">Concluído</Badge>
  <Badge variant="destructive">Cancelado</Badge>
  <Badge variant="outline">Em andamento</Badge>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Importações atualizadas
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';
import { type BadgeVariants, badgeVariants } from './index';

const props = defineProps<{
  variant?: BadgeVariants['variant'];
  class?: HTMLAttributes['class'];
}>();
</script>

<template>
  <div :class="cn(badgeVariants({ variant }), props.class)">
    <slot />
  </div>
</template>
