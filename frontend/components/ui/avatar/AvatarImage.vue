<!--
  AvatarImage.vue
  
  Componente para exibir a imagem do avatar.
  Geralmente usado dentro do componente Avatar.
  
  Props:
  - src: URL da imagem
  - alt: Texto alternativo para acessibilidade
  
  Exemplo de uso:
  <Avatar>
    <AvatarImage src="/path/to/image.jpg" alt="Avatar do usuário" />
    <AvatarFallback>JP</AvatarFallback>
  </Avatar>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Documentação adicionada
import type { AvatarImageProps } from 'reka-ui';
import { AvatarImage } from 'reka-ui';

const props = defineProps<AvatarImageProps>();
</script>

<template>
  <AvatarImage v-bind="props" class="h-full w-full object-cover">
    <slot />
  </AvatarImage>
</template>
