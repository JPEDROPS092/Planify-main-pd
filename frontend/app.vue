<template>
  <div>
    <!-- Splash Screen -->
    <div
      v-if="loading"
      class="fixed inset-0 z-50 flex items-center justify-center bg-white dark:bg-gray-900 transition-opacity duration-1000"
      :class="{ 'opacity-0 pointer-events-none': !loading }"
    >
      <img
        src="/svg/logop.svg"
        alt="Planify Logo"
        class="w-32 h-32 animate-bounce-slow transition-transform duration-1000"
      />
    </div>

    <!-- App Content -->
    <NuxtLayout>
      <!-- Adicionado um wrapper div para aplicar v-show corretamente -->
      <div v-show="!loading" class="h-full"> <!-- Adicionado h-full para manter a altura se necessário -->
        <NuxtPage />
      </div>
    </NuxtLayout>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const loading = ref(true);

// Inicialização de tema e tela de carregamento
onMounted(() => {
  // Aplica tema salvo no localStorage
  const theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  }

  // Aguarda 2 segundos antes de mostrar o conteúdo
  setTimeout(() => {
    loading.value = false;
  }, 2000);
});
</script>

<style scoped>
@keyframes bounceSlow {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-10px) scale(1.05);
  }
}

.animate-bounce-slow {
  animation: bounceSlow 2s infinite;
}
</style>
