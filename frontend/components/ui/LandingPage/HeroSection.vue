<template>
  <section class="bg-gradient-to-br from-blue-600 to-blue-800 text-white py-20 md:py-32">
    <div class="container mx-auto px-6 text-center">
      <div class="md:flex md:items-center md:justify-between">
        <div class="md:w-1/2 text-center md:text-left mb-10 md:mb-0">
          <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6">
            Bem-vindo ao <span class="text-blue-300">Planify</span>
          </h1>
          <p class="text-lg sm:text-xl text-blue-100 mb-6">
            Organize projetos, equipes, tarefas, custos e riscos em um só lugar. Gestão visual, dashboards inteligentes e colaboração em tempo real.
          </p>
          <p class="text-base text-blue-200 mb-10">
            Planifique, acompanhe e entregue resultados com mais eficiência.
          </p>
          <div class="flex flex-col sm:flex-row justify-center md:justify-start space-y-4 sm:space-y-0 sm:space-x-4">
            <button
              @click="navigateToLogin"
              class="px-8 py-4 bg-white text-blue-700 font-semibold rounded-lg shadow-md hover:bg-blue-50 transition duration-300 transform hover:scale-105"
            >
              Fazer Login
            </button>
            <button
              @click="navigateToSignup"
              class="px-8 py-4 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-400 transition duration-300 transform hover:scale-105"
            >
              Criar Conta
            </button>
          </div>
        </div>
        <div class="md:w-1/2 flex justify-center">
          <!-- Certifique-se que o caminho da imagem está correto -->
          <img 
            src="https://octodex.github.com/images/neurocats_FULL.png" 
            alt="Planify Dashboard Preview" 
            class="rounded-lg shadow-2xl max-w-sm md:max-w-md lg:max-w-lg"
          >
        </div>
      </div>
    </div>
  </section>
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
/* Estilos específicos para o Hero, se necessário */
</style>