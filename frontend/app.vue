<!-- filepath: app.vue -->
<template>
  <div>
    <!-- 
      NuxtLayout é o componente mestre que escolhe o layout apropriado
      (default.vue, auth.vue, etc.) com base na rota atual.
    -->
    <NuxtLayout>
      <!-- 
        NuxtPage renderiza o componente da página atual (ex: /dashboard -> Dashboard.vue)
        DENTRO do espaço fornecido pelo <slot /> do layout ativo.
        Este componente é essencial e substitui o <router-view>.
      -->
      <NuxtPage />
    </NuxtLayout>

    <!-- Componentes globais como Toasts devem ficar aqui, fora do layout. -->
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
// Geralmente, o script do app.vue pode ficar vazio, a menos que você tenha
// uma lógica global de SEO ou outra configuração de alto nível.
import ToastContainer from "@/components/ToastContainer.vue";
</script>
