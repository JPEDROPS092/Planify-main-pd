<template>
  <!-- Esta página serve como redirecionamento da rota raiz para o dashboard ou login -->
  <div class="flex items-center justify-center min-h-screen">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '~/stores/composables/useAuth';

const router = useRouter();
const auth = useAuth();

onMounted(async () => {
  try {
    // Verifica se o usuário está autenticado
    await auth.checkAuth();
    
    if (auth.isAuthenticated) {
      // Se autenticado, redireciona para o dashboard
      router.push('/dashboard');
    } else {
      // Se não autenticado, redireciona para a página de login
      router.push('/auth/login');
    }
  } catch (error) {
    console.error('Erro ao verificar autenticação:', error);
    // Em caso de erro, redireciona para a página de login
    router.push('/auth/login');
  }
});
</script>
