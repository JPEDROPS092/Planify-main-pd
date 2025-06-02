<template>
  <NuxtLayout name="auth">
    <div class="flex flex-col space-y-2 text-center mb-6">
      <h1 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Recuperação de senha</h1>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Informe seu e-mail para receber instruções de recuperação
      </p>
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="space-y-2">
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          E-mail
        </label>
        <input
          id="email"
          v-model="email"
          type="email"
          class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
          placeholder="nome@exemplo.com"
          required
        />
      </div>
      
      <div v-if="error" class="text-sm text-red-600 dark:text-red-400 mt-2">
        {{ error }}
      </div>
      
      <div v-if="success" class="text-sm text-green-600 dark:text-green-400 mt-2">
        Enviamos instruções para recuperar sua senha. Por favor, verifique seu e-mail.
      </div>
      
      <button
        type="submit"
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading"
      >
        <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>{{ loading ? 'Processando...' : 'Enviar instruções' }}</span>
      </button>
    </form>
    
    <div class="mt-6">
      <div class="relative">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
            Ou
          </span>
        </div>
      </div>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Lembrou sua senha?
          <NuxtLink
            to="/auth/login"
            class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
          >
            Voltar para o login
          </NuxtLink>
        </p>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/stores/composables/useNotification';

// Definir metadados da página
definePageMeta({
  layout: false,
  middleware: ['guest-only']
});

// Composables
const router = useRouter();
const auth = useAuth();
const notification = useNotification();

// Estado do formulário
const email = ref('');
const loading = ref(false);
const error = ref('');
const success = ref(false);

const handleSubmit = async () => {
  if (!email.value) {
    notification.error('Por favor, informe seu e-mail');
    error.value = 'Por favor, informe seu e-mail';
    return;
  }

  try {
    loading.value = true;
    error.value = '';
    success.value = false;

    // Usar o método withLoading para gerenciar automaticamente as notificações
    const response = await notification.withLoading(
      auth.requestPasswordReset(email.value),
      {
        loadingMessage: 'Processando solicitação...',
        loadingTitle: 'Recuperação de Senha',
        successMessage: 'Enviamos instruções para recuperar sua senha. Por favor, verifique seu e-mail.',
        errorMessage: 'Não foi possível processar sua solicitação. Verifique o e-mail informado.'
      }
    );

    if (response && response.success) {
      success.value = true;
      
      // Redirecionar para a página de login após alguns segundos
      setTimeout(() => {
        router.push('/auth/login?reset=requested');
      }, 3000);
    } else {
      // Se a API retornar success: false, mas não lançar um erro HTTP
      error.value = response?.message || 'Não foi possível processar sua solicitação. Verifique o e-mail informado.';
    }
  } catch (err) {
    console.error('Erro ao solicitar recuperação de senha:', err);
    // A mensagem de erro já foi exibida pelo withLoading
    error.value = err.message || 'Ocorreu um erro ao processar sua solicitação. Tente novamente.';
  } finally {
    loading.value = false;
  }
};
</script>
