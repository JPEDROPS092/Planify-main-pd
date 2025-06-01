<!--
  AvatarFallback.vue
  
  Componente para exibir um fallback quando a imagem do avatar não está disponível.
  Geralmente usado dentro do componente Avatar.
  
  Exemplo de uso:
  <Avatar>
    <AvatarImage src="/path/to/image.jpg" alt="Avatar do usuário" />
    <AvatarFallback>JP</AvatarFallback>
  </Avatar>
-->

<script setup lang="ts">
// [Refatorado para padronização] - Documentação adicionada
import { AvatarFallback, type AvatarFallbackProps } from 'reka-ui';

const props = defineProps<AvatarFallbackProps>();
</script>

<template>
  <AvatarFallback v-bind="props">
    <slot />
  </AvatarFallback>
</template>
