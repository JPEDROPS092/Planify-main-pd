<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-b from-slate-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-950 dark:to-gray-800">
    <!-- Navbar com gradiente e efeito de glassmorphism -->
    <header class="w-full sticky top-0 z-50 transition-all duration-300 bg-white/70 dark:bg-gray-900/70 backdrop-blur-md shadow-sm">
      <nav class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- Logo e Marca -->
          <div class="flex items-center space-x-2">
            <img src="/img/logop.png" alt="Planify Logo" class="h-8 w-auto" />
            <span class="font-bold text-xl bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-600 text-transparent bg-clip-text">Planify</span>
          </div>
          
          <!-- Links de Navegação - Visíveis apenas em telas médias e grandes -->
          <div class="hidden md:flex items-center space-x-8">
            <a href="#features" class="hover-link text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">Funcionalidades</a>
            <a href="#mission" class="hover-link text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">Missão</a>
            <a href="#contato" class="hover-link text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300">Contato</a>
          </div>
          
          <!-- Botões de Ação -->
          <div class="flex items-center space-x-4">
            <NuxtLink to="/auth/login" class="px-4 py-2 rounded-md text-sm font-medium text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-800 transition-colors duration-300">Entrar</NuxtLink>
            <NuxtLink to="/auth/registro" class="px-4 py-2 rounded-md text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">Registrar</NuxtLink>
          </div>
        </div>
      </nav>
    </header>

    <!-- Conteúdo Principal -->
    <main class="flex-grow">
      <slot /> <!-- O conteúdo da página (pages/index.vue) será renderizado aqui -->
    </main>

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import AppFooter from '~/components/ui/LandingPage/AppFooter.vue'; // Add this import

// Estado para controlar a aparência do navbar ao rolar
const isScrolled = ref(false);

// Função para detectar rolagem e ajustar a aparência do navbar
const handleScroll = () => {
  isScrolled.value = window.scrollY > 10;
};

// Adiciona e remove o event listener para o evento de scroll
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style>
/* Animação de scroll suave */
html {
  scroll-behavior: smooth;
}

/* Animações globais que podem ser usadas em toda a landing page */
.fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

.slide-up {
  animation: slideUp 0.5s ease-in-out;
}

.scale-in {
  animation: scaleIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Estilização para links com hover effect */
.hover-link {
  position: relative;
}

.hover-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: -2px;
  left: 0;
  background: linear-gradient(to right, #3b82f6, #1d4ed8);
  transition: width 0.3s ease;
}

.hover-link:hover::after {
  width: 100%;
}

/* Estilização para cards com hover effect */
.hover-card {
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>