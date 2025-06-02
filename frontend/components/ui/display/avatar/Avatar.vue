<!--
  Avatar.vue

  Componente reutilizável para exibir avatares de usuários ou entidades.
  Suporta variações de tamanho e formato, e aceita conteúdo via slot.

  Props:
  - size: Tamanho do avatar ('sm', 'base', 'lg') — padrão: 'sm'
  - shape: Forma do avatar ('circle', 'square') — padrão: 'circle'
  - class: Classes CSS adicionais para personalização

  Exemplo de uso:
  <Avatar size="base" shape="circle">
    <AvatarImage src="/caminho/para/imagem.jpg" alt="Avatar do usuário" />
    <AvatarFallback>JP</AvatarFallback>
  </Avatar>
-->

<script setup lang="ts">
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils'; // Combina classes de forma segura
import { AvatarRoot } from 'reka-ui'; // Componente base do Avatar
import { avatarVariant } from '~/components/ui/display/avatar/variants'; // Variantes do avatar definidas em outro arquivo
import { withDefaults } from 'vue'; // Função para definir valores padrão     
import type { AvatarVariants } from '~/components/ui/display/avatar/variants';

// Definição das props com valores padrão
const props = withDefaults(
  defineProps<{
    class?: HTMLAttributes['class'];
    size?: AvatarVariants['size'];   // ✅ Correto agora
    shape?: AvatarVariants['shape']; // ✅ Correto agora
  }>(),
  {
    size: 'sm',
    shape: 'circle',
  }
);
</script>

<template>
  <!-- Componente raiz com variantes aplicadas dinamicamente -->
  <AvatarRoot :class="cn(avatarVariant({ size, shape }), props.class)">
    <slot />
  </AvatarRoot>
</template>

<style scoped>
/* Estilos adicionais podem ser aplicados aqui se necessário */
</style>
