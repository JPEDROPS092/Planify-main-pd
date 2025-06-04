<template>
  <section class="py-20 relative overflow-hidden">
    <!-- Fundo com gradiente -->
    <div class="absolute inset-0 bg-gradient-to-br from-blue-100 to-blue-50 dark:from-gray-800 dark:to-gray-900"></div>
    
    <!-- Formas decorativas -->
    <div class="absolute inset-0">
      <div class="shape-blob shape-blob-1"></div>
      <div class="shape-blob shape-blob-2"></div>
      <div class="shape-blob shape-blob-3"></div>
    </div>
    
    <div class="container mx-auto px-6 relative z-10">
      <div class="max-w-4xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
        <div class="md:flex">
          <div class="md:w-3/5 p-10">
            <h2 class="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-600 text-transparent bg-clip-text">
              Pronto para transformar sua gestão de projetos?
            </h2>
            <p class="text-gray-600 dark:text-gray-300 mb-8">
              Junte-se a milhares de profissionais e equipes que já estão elevando seus projetos de P&D a um novo patamar com o Planify.
            </p>
            <button
              @click="navigateToSignup"
              class="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
            >
              Começar Gratuitamente
            </button>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-4">
              Não é necessário cartão de crédito. Plano gratuito disponível.
            </p>
          </div>
          <div class="md:w-2/5 bg-gradient-to-br from-blue-500 to-blue-700 dark:from-blue-600 dark:to-blue-900 flex items-center justify-center p-10">
            <div class="text-center">
              <div class="text-white text-5xl font-bold mb-4">+ 500</div>
              <div class="text-blue-100 text-xl">Projetos gerenciados</div>
              <div class="border-t border-blue-400 my-4"></div>
              <div class="text-white text-5xl font-bold mb-4">+ 2000</div>
              <div class="text-blue-100 text-xl">Usuários satisfeitos</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const navigateToSignup = () => {
  router.push('/auth/registro');
};
</script>

<style scoped>
.shape-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.4;
}

.shape-blob-1 {
  width: 300px;
  height: 300px;
  background: rgba(59, 130, 246, 0.4);
  top: -150px;
  left: 10%;
  animation: blob-move-1 15s infinite alternate;
}

.shape-blob-2 {
  width: 350px;
  height: 350px;
  background: rgba(37, 99, 235, 0.4);
  bottom: -100px;
  right: 20%;
  animation: blob-move-2 20s infinite alternate;
}

.shape-blob-3 {
  width: 250px;
  height: 250px;
  background: rgba(96, 165, 250, 0.3);
  bottom: 30%;
  left: 5%;
  animation: blob-move-3 18s infinite alternate;
}

@keyframes blob-move-1 {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(50px, 20px) scale(1.1); }
}

@keyframes blob-move-2 {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-30px, -50px) scale(1.15); }
}

@keyframes blob-move-3 {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(20px, 40px) scale(1.05); }
}
</style>