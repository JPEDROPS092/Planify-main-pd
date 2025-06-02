<!--
  AvatarImage.vue

  Componente para renderizar a imagem principal do avatar.
  Aplica estilo para cobrir completamente o espaço disponível.

  Props:
  - src: Caminho da imagem
  - alt: Texto alternativo (acessibilidade)

  Uso comum:
  <Avatar>
    <AvatarImage src="/caminho/para/imagem.jpg" alt="Avatar do usuário" />
    <AvatarFallback>JP</AvatarFallback>
  </Avatar>
-->

<script setup lang="ts">
import { AvatarImage as RekaAvatarImage } from 'reka-ui'; // Renomeado para evitar conflito
import type { AvatarImageProps } from 'reka-ui';

// Recebe as props da imagem
const props = defineProps<AvatarImageProps>();
</script>

<template>
  <!-- Imagem com preenchimento total e corte adequado -->
  <RekaAvatarImage
    v-bind="props"
    class="h-full w-full object-cover"
  />
</template>
