<!--
  Avatar.vue
  
  Componente para exibir avatares de usuários ou entidades.
  
  Props:
  - size: Tamanho do avatar (sm, base, lg)
  - shape: Forma do avatar (circle, square)
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <Avatar size="base" shape="circle">
    <AvatarImage src="/path/to/image.jpg" alt="Avatar do usuário" />
    <AvatarFallback>JP</AvatarFallback>
  </Avatar>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Importações atualizadas
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';
import { AvatarRoot } from 'reka-ui';
import { avatarVariant, type AvatarVariants } from './index';

const props = withDefaults(
  defineProps<{
    class?: HTMLAttributes['class'];
    size?: AvatarVariants['size'];
    shape?: AvatarVariants['shape'];
  }>(),
  {
    size: 'sm',
    shape: 'circle',
  }
);
</script>

<template>
  <AvatarRoot :class="cn(avatarVariant({ size, shape }), props.class)">
    <slot />
  </AvatarRoot>
</template>

<style scoped>
/* Adicione estilos específicos para o componente aqui, se necessário */
</style>
