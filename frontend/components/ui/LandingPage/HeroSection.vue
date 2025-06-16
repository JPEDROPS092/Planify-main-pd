<template>
  <section class="relative overflow-hidden py-20 md:py-32">
    <!-- Background com gradiente e padrão animado -->
    <div class="absolute inset-0 bg-gradient-to-br from-blue-700 via-blue-600 to-blue-900 dark:from-blue-900 dark:via-blue-800 dark:to-gray-900 opacity-90"></div>
    <div class="absolute inset-0 pattern-dots opacity-10"></div>
    
    <div class="container mx-auto px-6 relative z-10">
      <div class="md:flex md:items-center md:justify-between">
      <div class="md:w-1/2 text-center md:text-left mb-10 md:mb-0">
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold leading-tight mb-6 text-white">
        Bem-vindo ao <span class="bg-gradient-to-r from-blue-200 to-blue-100 text-transparent bg-clip-text">Planify</span>
        </h1>
        <p class="text-lg sm:text-xl text-blue-100 mb-6 animate__animated animate__fadeIn animate__delay-1s">
        Organize projetos, equipes, tarefas, custos e riscos em um só lugar. Gestão visual, dashboards inteligentes e colaboração em tempo real.
        </p>
        <p class="text-base text-blue-200 mb-10 animate__animated animate__fadeIn animate__delay-2s">
        Planifique, acompanhe e entregue resultados com mais eficiência.
        </p>
        <div class="flex flex-col sm:flex-row justify-center md:justify-start space-y-4 sm:space-y-0 sm:space-x-4">
        <button
          @click="checkAuthAndNavigate"
          class="px-8 py-4 bg-white text-blue-700 font-semibold rounded-lg shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105 hover:bg-blue-50 animate__animated animate__fadeInUp animate__delay-3s"
        >
          <Icon name="ph:sign-in-bold" class="inline-block mr-2" /> Fazer Login
        </button>
        <button
          @click="navigateToSignup"
          class="px-8 py-4 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition duration-300 transform hover:scale-105 animate__animated animate__fadeInUp animate__delay-4s"
        >
          <Icon name="ph:user-plus-bold" class="inline-block mr-2" /> Criar Conta
        </button>
        </div>
      </div>
      <div class="md:w-1/2 flex justify-center animate__animated animate__fadeInRight animate__delay-3s">
        <img 
        src="public/svg/logop.svg" 
        alt="Planify Dashboard Preview" 
        class="rounded-full shadow-2xl w-120 h-80 transform hover:rotate-2 transition-transform duration-500 object-cover"
        style="background: none;"
          >
      </div>
      </div>
      </div>
 
    
    <!-- Ondas decorativas no fundo -->
    <div class="absolute bottom-0 left-0 right-0">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" class="w-full h-auto">
        <path fill="#ffffff" fill-opacity="1" d="M0,160L48,144C96,128,192,96,288,106.7C384,117,480,171,576,186.7C672,203,768,181,864,154.7C960,128,1056,96,1152,101.3C1248,107,1344,149,1392,170.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';
// import { useAuth } from '~/composables/useAuth';
import { getCurrentInstance } from 'vue';
import 'animate.css';

const router = useRouter();
// const { isAuthenticated } = useAuth();

// Busca o método definido no componente pai (index.vue)
const parent = getCurrentInstance()?.parent;

// Verifica autenticação e navega para o dashboard ou login
const checkAuthAndNavigate = () => {
  if (parent?.exposed?.redirectToDashboardOrLogin) {
    // Usa o método do componente pai se estiver disponível
    parent.exposed.redirectToDashboardOrLogin();
  } else {
    // Fallback - verifica autenticação localmente
    // if (isAuthenticated.value) {
    //   router.push('/dashboard');
    // } else {
      router.push('/auth/login');
    // }
  }
};

const navigateToSignup = () => {
  router.push('/auth/registro');
};
</script>

<style scoped>
.pattern-dots {
  background-image: radial-gradient(rgba(255, 255, 255, 0.4) 2px, transparent 2px);
  background-size: 30px 30px;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.floating {
  animation: float 6s ease-in-out infinite;
}
</style>