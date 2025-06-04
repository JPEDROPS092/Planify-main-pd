<template>
  <!-- Landing Page da aplicação -->
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 text-center">
    <h1 class="text-4xl font-bold text-blue-600 mb-4">Bem-vindo ao Planify</h1>
    <p class="text-lg text-gray-700 mb-4">
      Organize projetos, equipes, tarefas, custos e riscos em um só lugar. Gestão visual, dashboards inteligentes e colaboração em tempo real.
    </p>
    <p class="text-base text-gray-500 mb-8">
      Planifique, acompanhe e entregue resultados com mais eficiência.
    </p>
    <div class="flex space-x-4">
      <button
        @click="navigateToLogin"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        Fazer Login
      </button>
      <button
        @click="navigateToSignup"
        class="px-6 py-3 bg-gray-200 text-blue-600 rounded-lg hover:bg-gray-300"
      >
        Criar Conta
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateToLogin = () => {
  router.push('/auth/login');
};

const navigateToSignup = () => {
  router.push('/auth/registro');
};
</script>

<style scoped>
/* Adicione estilos personalizados, se necessário */
</style>
