<!-- filepath: layouts/auth.vue -->
<template>
  <div
    class="min-h-screen bg-gray-100 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8"
  >
    <main>
      <!-- 
        O <slot /> é o marcador onde o Nuxt vai injetar a página atual 
        (seja a de login, registro, ou esqueceu a senha).
        O layout apenas fornece o fundo cinza e a centralização.
      -->
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
// O script pode ficar completamente vazio.
// Nenhuma lógica de autenticação, query ou watcher é necessária aqui.
// O middleware 'guest' já cuida do redirecionamento se o usuário estiver logado.
</script>
