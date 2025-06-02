<template>
  <NuxtLayout name="auth">
    <div class="flex flex-col space-y-2 text-center mb-6">
      <h1 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Redefinir senha</h1>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Digite sua nova senha abaixo
      </p>
    </div>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="space-y-2">
        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Nova senha
        </label>
        <input
          id="password"
          v-model="password"
          type="password"
          class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
          placeholder="••••••••"
          required
        />
      </div>
      
      <div class="space-y-2">
        <label for="password_confirmation" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Confirme a nova senha
        </label>
        <input
          id="password_confirmation"
          v-model="passwordConfirmation"
          type="password"
          class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
          placeholder="••••••••"
          required
        />
      </div>
      
      <div v-if="error" class="text-sm text-red-600 dark:text-red-400 mt-2">
        {{ error }}
      </div>
      
      <div v-if="success" class="text-sm text-green-600 dark:text-green-400 mt-2">
        Sua senha foi redefinida com sucesso. Você será redirecionado para a página de login.
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
        <span>{{ loading ? 'Processando...' : 'Redefinir senha' }}</span>
      </button>
    </form>
    
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
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuth } from '~/stores/composables/useAuth';
import { useNotification } from '~/stores/composables/useNotification';

// Definir metadados da página
definePageMeta({
  layout: false,
  middleware: ['guest-only']
});

// Composables
const router = useRouter();
const route = useRoute();
const auth = useAuth();
const notification = useNotification();

// Estado do formulário
const token = ref('');
const email = ref('');
const password = ref('');
const passwordConfirmation = ref('');
const loading = ref(false);
const error = ref('');
const success = ref(false);

// Extrair token e email da URL ao carregar a página
onMounted(() => {
  // Verificar se o token está presente na URL
  if (route.query.token) {
    token.value = route.query.token as string;
  } else {
    notification.error('Token de redefinição de senha inválido ou expirado');
    error.value = 'Token de redefinição de senha inválido ou expirado';
    setTimeout(() => {
      router.push('/auth/login');
    }, 3000);
  }

  // Verificar se o email está presente na URL
  if (route.query.email) {
    email.value = route.query.email as string;
  }
});

const handleSubmit = async () => {
  // Validar formulário
  if (!password.value) {
    notification.error('Por favor, informe uma nova senha');
    error.value = 'Por favor, informe uma nova senha';
    return;
  }

  if (password.value.length < 8) {
    notification.error('A senha deve ter pelo menos 8 caracteres');
    error.value = 'A senha deve ter pelo menos 8 caracteres';
    return;
  }

  if (password.value !== passwordConfirmation.value) {
    notification.error('As senhas não coincidem');
    error.value = 'As senhas não coincidem';
    return;
  }

  if (!token.value || !email.value) {
    notification.error('Token ou email inválido');
    error.value = 'Token ou email inválido';
    return;
  }

  try {
    loading.value = true;
    error.value = '';
    success.value = false;

    // Usar o método withLoading para gerenciar automaticamente as notificações
    const response = await notification.withLoading(
      auth.resetPassword({
        email: email.value,
        token: token.value,
        password: password.value,
        password_confirmation: passwordConfirmation.value
      }),
      {
        loadingMessage: 'Redefinindo sua senha...',
        loadingTitle: 'Redefinição de Senha',
        successMessage: 'Senha redefinida com sucesso!',
        errorMessage: 'Não foi possível redefinir sua senha. Verifique os dados informados.'
      }
    );

    if (response && response.success) {
      success.value = true;
      
      // Redirecionar para a página de login após alguns segundos
      setTimeout(() => {
        router.push('/auth/login?reset=success');
      }, 3000);
    } else {
      // Se a API retornar success: false, mas não lançar um erro HTTP
      error.value = response?.message || 'Não foi possível redefinir sua senha. Verifique os dados informados.';
    }
  } catch (err) {
    console.error('Erro ao redefinir senha:', err);
    // A mensagem de erro já foi exibida pelo withLoading
    error.value = err.message || 'Ocorreu um erro ao redefinir sua senha. Tente novamente.';
  } finally {
    loading.value = false;
  }
};
</script>
