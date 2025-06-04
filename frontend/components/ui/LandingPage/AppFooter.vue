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
    <footer class="bg-gray-100 dark:bg-gray-800 py-10">
      <div class="container mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <img src="/img/logop.png" alt="Planify Logo" class="h-8 w-auto" />
              <span class="font-bold text-xl bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-600 text-transparent bg-clip-text">Planify</span>
            </div>
            <p class="text-gray-600 dark:text-gray-400 text-sm">Gerenciamento de projetos simplificado para equipes modernas.</p>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">Produto</h3>
            <ul class="space-y-2">
              <li><a href="#features" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">Funcionalidades</a></li>
              <li><a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">Preços</a></li>
              <li><a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">FAQ</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">Empresa</h3>
            <ul class="space-y-2">
              <li><a href="#mission" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">Sobre nós</a></li>
              <li><a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">Carreiras</a></li>
              <li><a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">Blog</a></li>
            </ul>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-800 dark:text-gray-200 mb-4">Contato</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">Suporte</a></li>
              <li><a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 text-sm">contato@planify.com</a></li>
            </ul>
          </div>
        </div>
        
        <div class="border-t border-gray-200 dark:border-gray-700 mt-8 pt-8 flex flex-col md:flex-row md:justify-between">
          <p class="text-gray-600 dark:text-gray-400 text-sm">© 2025 Planify. Todos os direitos reservados.</p>
          <div class="flex space-x-6 mt-4 md:mt-0">
            <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">
              <span class="sr-only">Twitter</span>
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"></path>
              </svg>
            </a>
            <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">
              <span class="sr-only">LinkedIn</span>
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fill-rule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clip-rule="evenodd"></path>
              </svg>
            </a>
            <a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">
              <span class="sr-only">GitHub</span>
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

// Use SSR-safe approach
const isScrolled = ref(false);

// Only attach scroll handlers on client-side
onMounted(() => {
  handleScroll(); // Initial check
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

// Scroll handler function
const handleScroll = () => {
  if (process.client) {
    isScrolled.value = window.scrollY > 10;
  }
};
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

/* For animation on scroll */
.slide-up, .fade-in, .scale-in {
  opacity: 0;
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.slide-up {
  transform: translateY(30px);
}

.scale-in {
  transform: scale(0.95);
}

.animate {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Add scroll margin for anchor links to account for fixed header */
.scroll-mt-20 {
  scroll-margin-top: 5rem;
}
</style>