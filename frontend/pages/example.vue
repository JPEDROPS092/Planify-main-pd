<template>
  <div class="container mx-auto p-6">
    <Card>
      <CardHeader>
        <CardTitle>Exemplo de Componentes</CardTitle>
        <CardDescription>Testando os componentes do Shadcn</CardDescription>
      </CardHeader>
      <CardContent>
        <p class="mb-4">Este é um exemplo usando os componentes do Shadcn no Nuxt.</p>
        <Button>Botão Padrão</Button>
        <Button variant="destructive" class="ml-2">Botão Destrutivo</Button>
        <Button variant="outline" class="ml-2">Botão Outline</Button>
      </CardContent>
      <CardFooter>
        <p class="text-sm text-gray-500">Exemplo de rodapé</p>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { Button, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '~/components/ui';
</script>
