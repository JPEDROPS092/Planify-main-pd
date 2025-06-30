<script setup lang="ts">
import { onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";
// Importe componentes globais que devem aparecer em todas as páginas,
// como o container de toasts.
import ToastContainer from "~/components/ToastContainer.vue";
import AuthLoadingScreen from "~/components/AuthLoadingScreen.vue";

// Use um nome descritivo para a instância da store
const authStore = useAuthStore();

// onMounted garante que este código só rode no cliente,
// após a hidratação inicial. É o lugar perfeito para restaurar a sessão.
onMounted(() => {
  // Tenta carregar a sessão do usuário a partir do localStorage.
  // Isso é crucial para manter o usuário logado ao recarregar a página.
  authStore.tryToLoadSession();
});
</script>

<template>
  <div>
    <!-- Envolver em um único div raiz é uma boa prática -->
    <!-- 
      Mostra uma tela de carregamento inicial enquanto a store de autenticação 
      verifica se há uma sessão válida. Isso previne um "flash" de conteúdo
      público antes do redirecionamento para o dashboard.
    -->
    <AuthLoadingScreen v-if="authStore.isAuthLoading" />

    <!-- 
      O layout principal e a página só são renderizados após a verificação inicial.
      Você pode usar v-else se preferir.
    -->
    <NuxtLayout v-show="!authStore.isAuthLoading">
      <NuxtPage />
    </NuxtLayout>

    <!-- 
      O ToastContainer é colocado aqui para estar disponível globalmente.
      Ele ficará acima de todos os layouts e páginas.
    -->
    <ToastContainer />
  </div>
</template>
