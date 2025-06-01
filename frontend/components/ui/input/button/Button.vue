<!--
  Button.vue
  
  Componente de botão para ações interativas como submissão de formulários,
  navegação, ou qualquer interação que requeira um botão.
  
  Props:
  - variant: Estilo visual do botão (default, secondary, outline, ghost, link, destructive, success)
  - size: Tamanho do botão (default, sm, lg, icon)
  - as: Elemento HTML a ser renderizado (button, a, div, etc.)
  - asChild: Se verdadeiro, não renderiza um elemento, apenas passa as props para o filho
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <Button variant="default" size="lg">Enviar</Button>
  <Button variant="outline" size="sm">Cancelar</Button>
  <Button variant="ghost" as="a" href="/dashboard">Dashboard</Button>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Importações atualizadas
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';
import { Primitive, type PrimitiveProps } from 'reka-ui';
import { type ButtonVariants, buttonVariants } from './index';

interface Props extends PrimitiveProps {
  variant?: ButtonVariants['variant'];
  size?: ButtonVariants['size'];
  class?: HTMLAttributes['class'];
}

const props = withDefaults(defineProps<Props>(), {
  as: 'button',
});
</script>

<template>
  <Primitive
    :as="as"
    :as-child="asChild"
    :class="cn(buttonVariants({ variant, size }), props.class)"
  >
    <slot />
  </Primitive>
</template>

<style scoped>
/* Adicione estilos específicos para o seu componente aqui */
</style>
