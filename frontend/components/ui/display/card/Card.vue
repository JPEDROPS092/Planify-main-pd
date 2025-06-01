<!--
  Card.vue
  
  Componente de card para agrupar conteúdo relacionado em uma única unidade visual.
  Geralmente usado com outros componentes de card como CardHeader, CardContent, etc.
  
  Props:
  - class: Classes CSS adicionais
  
  Exemplo de uso:
  <Card>
    <CardHeader>
      <CardTitle>Título do Card</CardTitle>
      <CardDescription>Descrição do card</CardDescription>
    </CardHeader>
    <CardContent>
      Conteúdo principal do card
    </CardContent>
    <CardFooter>
      <Button>Ação</Button>
    </CardFooter>
  </Card>
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
  <div
    :class="
      cn('rounded-xl border bg-card text-card-foreground shadow', props.class)
    "
  >
    <slot />
  </div>
</template>

<style scoped>
/* Adicione estilos específicos para o seu componente aqui */
</style>
