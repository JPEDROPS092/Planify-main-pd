<template>
  <NuxtLayout name="auth">
    <div class="flex flex-col space-y-2 text-center mb-6">
      <h1 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Entrar no Planify</h1>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Digite suas credenciais para acessar o sistema
      </p>
    </div>
    <form @submit.prevent="handleLogin">
      <div class="space-y-4">
        <div class="space-y-2">
          <label
            for="username"
            class="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Usuário
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="Digite seu nome de usuário"
            required
          />
        </div>
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <label
              for="password"
              class="block text-sm font-medium text-gray-700 dark:text-gray-300"
            >
              Senha
            </label>
            <NuxtLink
              to="/auth/esqueci-senha"
              class="text-sm font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Esqueceu a senha?
            </NuxtLink>
          </div>
          <input
            id="password"
            v-model="password"
            type="password"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="Digite sua senha"
            required
          />
        </div>
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              type="checkbox"
              v-model="rememberMe"
              class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
              Lembrar-me
            </label>
          </div>
        </div>
        <div v-if="errorMessage" class="text-sm text-red-600 dark:text-red-400 mt-2">
          {{ errorMessage }}
        </div>
        <button
          type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="isLoading"
        >
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isLoading ? 'Entrando...' : 'Entrar' }}</span>
        </button>
      </div>
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
          Não tem uma conta?
          <NuxtLink
            to="/auth/registro"
            class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
          >
            Registre-se
          </NuxtLink>
        </p>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useNotification } from '~/composables/useNotification';
import { useRouter, useRoute } from 'vue-router';

// Definir metadados da página
definePageMeta({
  layout: false,
  middleware: ['guest-only']
});

// Composables
const auth = useAuth();
const notification = useNotification();
const router = useRouter();
const route = useRoute();

// Estado do formulário
const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

// Função para realizar o login
const handleLogin = async () => {
  if (!username.value || !password.value) {
    notification.error('Por favor, preencha todos os campos');
    errorMessage.value = 'Por favor, preencha todos os campos';
    return;
  }

  errorMessage.value = '';
  isLoading.value = true;
  
  try {
    // Usar o método withLoading para gerenciar automaticamente as notificações
    const result = await notification.withLoading(
      auth.login({
        username: username.value,
        password: password.value,
        remember: rememberMe.value
      }),
      {
        loadingMessage: 'Autenticando...',
        loadingTitle: 'Login',
        successMessage: 'Login realizado com sucesso!',
        errorMessage: 'Falha na autenticação. Verifique suas credenciais.'
      }
    );

    if (result && result.user) {
      // Redirecionamento baseado no papel do usuário
      let dashboardPath = '/dashboard';
      const role = result.user.role?.toLowerCase();
      if (role === 'admin') dashboardPath = '/dashboard';
      else if (role === 'project_manager') dashboardPath = '/dashboard';
      else if (role === 'team_leader') dashboardPath = '/dashboard';
      else if (role === 'team_member') dashboardPath = '/dashboard';
      else if (role === 'stakeholder') dashboardPath = '/dashboard';
      else if (role === 'auditor') dashboardPath = '/dashboard';
      // Se veio de rota protegida, prioriza o redirect original
      const redirectPath = route.query.redirect || dashboardPath;
      router.push(redirectPath.toString());
    } else {
      // Login falhou mas não lançou erro (caso improvável)
      errorMessage.value = 'Credenciais inválidas. Tente novamente.';
    }
  } catch (error) {
    console.error('Erro no login:', error);
    // A mensagem de erro já foi exibida pelo withLoading
    errorMessage.value = (error instanceof Error && error.message) || 'Ocorreu um erro durante o login. Tente novamente.';
  } finally {
    isLoading.value = false;
  }
};
</script>
