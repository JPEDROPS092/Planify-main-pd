<template>
  <NuxtLayout name="auth">
    <div class="flex flex-col space-y-2 text-center mb-6">
      <h1 class="text-2xl font-semibold tracking-tight text-gray-900 dark:text-white">Criar uma conta</h1>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Preencha os dados abaixo para se registrar no Planify
      </p>
    </div>
      <form @submit.prevent="handleRegistro" class="space-y-4">
        <div class="space-y-2">
          <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Nome de usuário
          </label>
          <input
            id="username"
            v-model="formData.username"
            type="text"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="seu_usuario"
            required
          />
        </div>
        <div class="space-y-2">
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Email
          </label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="nome@exemplo.com"
            required
          />
        </div>
        <div class="space-y-2">
          <label for="full_name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Nome completo
          </label>
          <input
            id="full_name"
            v-model="formData.full_name"
            type="text"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="Seu Nome Completo"
            required
          />
        </div>
        <div class="space-y-2">
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Senha
          </label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="Digite sua senha"
            required
          />
        </div>
        <div class="space-y-2">
          <label for="re_password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Confirmar senha
          </label>
          <input
            id="re_password"
            v-model="formData.re_password"
            type="password"
            class="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            placeholder="Confirme sua senha"
            required
          />
        </div>
        
        <div v-if="errorMessage" class="text-sm text-red-600 dark:text-red-400 mt-2">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="text-sm text-green-600 dark:text-green-400 mt-2">
          {{ successMessage }}
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
          <span>{{ isLoading ? 'Registrando...' : 'Registrar' }}</span>
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
            Já tem uma conta?
            <NuxtLink
              to="/auth/login"
              class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Faça login
            </NuxtLink>
          </p>
        </div>
      </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useAuth } from "~/stores/composables/useAuth";
import { useNotification } from "~/stores/composables/useNotification";
import { useRouter } from 'vue-router';

// Definir metadados da página
definePageMeta({
  layout: false,
  middleware: ['guest-only']
});

// Composables
const auth = useAuth();
const notification = useNotification();
const router = useRouter();

// Estado do formulário
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
  re_password: '',
});

const handleRegistro = async () => {
  // Validar se as senhas coincidem
  if (formData.password !== formData.re_password) {
    notification.error('As senhas não coincidem');
    errorMessage.value = 'As senhas não coincidem';
    return;
  }

  // Limpar mensagens anteriores
  errorMessage.value = '';
  successMessage.value = '';

  try {
    isLoading.value = true;
    
    // Usar o método withLoading para gerenciar automaticamente as notificações
    await notification.withLoading(
      auth.register({
        username: formData.username,
        email: formData.email,
        full_name: formData.full_name,
        password: formData.password,
        re_password: formData.re_password,
      }),
      {
        loadingMessage: 'Criando conta...',
        loadingTitle: 'Registro',
        successMessage: 'Conta criada com sucesso!',
        errorMessage: 'Erro ao criar conta. Verifique os dados informados.'
      }
    );

    // Atualizar mensagem de sucesso na interface
    successMessage.value = 'Conta criada com sucesso! Redirecionando para o login...';
    
    // Redirecionar para a página de login após um breve delay
    setTimeout(() => {
      router.push('/auth/login?registered=true');
    }, 1500);
  } catch (error) {
    // Tratamento de erro mais detalhado
    console.error('Erro ao registrar:', error);

    let errorMsg = 'Erro ao criar conta. Por favor, tente novamente.';

    // Verificar se temos um erro da API com dados estruturados
    if (error.originalError?.response?.data) {
      const errorData = error.originalError.response.data;
      if (typeof errorData === 'object') {
        // Formatar mensagens de erro da API
        const errorMessages = Object.entries(errorData)
          .map(([key, value]) => {
            // Traduzir campos comuns para português
            const fieldMap = {
              'username': 'Nome de usuário',
              'email': 'E-mail',
              'password': 'Senha',
              're_password': 'Confirmação de senha',
              'full_name': 'Nome completo'
            };
            
            const fieldName = fieldMap[key] || key;
            return `${fieldName}: ${Array.isArray(value) ? value.join(', ') : value}`;
          })
          .join('\n');
        errorMsg = errorMessages;
      }
    } else if (error.message) {
      errorMsg = error.message;
    }
    
    // A mensagem de erro já foi exibida pelo withLoading
    errorMessage.value = errorMsg;
  } finally {
    isLoading.value = false;
  }
};
</script>
