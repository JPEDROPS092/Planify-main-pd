<template>
  <div class="performance-report-container">
    <h1 class="text-2xl font-bold mb-4">Relatório de Performance</h1>
    <p>Conteúdo do relatório de performance será exibido aqui.</p>
  </div>
</template>

<script setup>
const route = useRoute();
const projectId = route.params.id;
</script>
