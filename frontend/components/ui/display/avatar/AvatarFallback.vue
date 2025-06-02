<!--
  AvatarFallback.vue

  Componente de fallback para exibir texto (como iniciais) caso a imagem do avatar falhe ou esteja ausente.

  Uso comum:
  <Avatar>
    <AvatarImage src="/caminho/para/imagem.jpg" alt="Avatar do usuário" />
    <AvatarFallback>JP</AvatarFallback>
  </Avatar>
-->

<script setup lang="ts">
import { AvatarFallback as RekaAvatarFallback } from 'reka-ui'; // Renomeando para evitar conflito de nome
import type { AvatarFallbackProps } from 'reka-ui';

// Recebe todas as props válidas do componente AvatarFallback original
const props = defineProps<AvatarFallbackProps>();
</script>

<template>
  <!-- Renderiza o conteúdo do slot (normalmente iniciais do nome) -->
  <RekaAvatarFallback v-bind="props">
    <slot />
  </RekaAvatarFallback>
</template>
