<template>
  <!-- Full page container with gradient background and minimal padding on small screens -->
  <div class="min-h-screen relative overflow-hidden bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 dark:from-gray-900 dark:via-teal-900 dark:to-emerald-900 sm:p-4 p-2">

    <!-- Background animated gradient blobs -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <!-- Large blob top right -->
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-emerald-400 to-teal-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-0"></div>
      <!-- Large blob bottom left -->
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-cyan-400 to-emerald-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
      <!-- Large blob center -->
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-teal-400 to-emerald-400 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Floating particles (subtle animation) -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-[15%] w-2 h-2 bg-white rounded-full opacity-20 animate-float animation-delay-1000"></div>
      <div class="absolute top-[60%] right-[20%] w-1 h-1 bg-emerald-300 rounded-full opacity-30 animate-float animation-delay-3000"></div>
      <div class="absolute bottom-1/4 left-[25%] w-1.5 h-1.5 bg-teal-300 rounded-full opacity-25 animate-float animation-delay-5000"></div>
      <div class="absolute top-[10%] right-[10%] w-1 h-1 bg-cyan-300 rounded-full opacity-15 animate-float animation-delay-6000"></div>
      <div class="absolute bottom-[10%] right-[10%] w-1.5 h-1.5 bg-emerald-300 rounded-full opacity-20 animate-float animation-delay-7000"></div>
    </div>

    <!-- Main content area - centered -->
    <div class="relative z-10 flex min-h-screen items-center justify-center p-2 sm:p-4">
      <div class="w-full max-w-sm transform transition-all duration-500 hover:scale-[1.01] ease-in-out"> <!-- Reduced max-width and scale to match login -->

        <!-- Registration Card -->
        <div class="relative bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-xl shadow-xl border border-white/20 dark:border-gray-700/20 overflow-hidden">
          <!-- Gradient overlay inside card for subtle effect -->
          <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent pointer-events-none"></div>

          <!-- Card Content -->
          <div class="relative p-4 sm:p-5 space-y-4">

            <!-- Logo and Header Section -->
            <div class="text-center space-y-2">
              <div class="relative mx-auto w-12 h-12 mb-2">
                <!-- Pulsing background gradient -->
                <div class="absolute inset-0 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-lg transform rotate-6 animate-pulse-slow"></div>
                <!-- Logo container with its own gradient -->
                <div class="relative bg-gradient-to-br from-emerald-500 to-teal-500 rounded-lg w-full h-full flex items-center justify-center z-10">
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                </div>
              </div>

              <!-- Title and Subtitle -->
              <div class="space-y-0.5">
                <h1 class="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 dark:from-emerald-400 dark:to-teal-400 bg-clip-text text-transparent">
                  Criar conta
                </h1>
                <p class="text-gray-600 dark:text-gray-400 text-xs">
                  Preencha os dados para se registrar no Planify
                </p>
              </div>
            </div>

            <!-- Register Form -->
            <form @submit.prevent="handleRegistro" class="space-y-3">
              <div class="space-y-3">
                <!-- Nome de usuário -->
                <div class="space-y-1">
                  <label for="username" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Nome de usuário
                  </label>
                  <div class="relative group">
                    <input
                      id="username"
                      v-model="formData.username"
                      type="text"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="seu_usuario"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Email -->
                <div class="space-y-1">
                  <label for="email" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Email
                  </label>
                  <div class="relative group">
                    <input
                      id="email"
                      v-model="formData.email"
                      type="email"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="nome@exemplo.com"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Nome completo -->
                <div class="space-y-1">
                  <label for="full_name" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Nome completo
                  </label>
                  <div class="relative group">
                    <input
                      id="full_name"
                      v-model="formData.full_name"
                      type="text"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="Seu Nome Completo"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Senha -->
                <div class="space-y-1">
                  <label for="password" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Senha
                  </label>
                  <div class="relative group">
                    <input
                      id="password"
                      v-model="formData.password"
                      type="password"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="Digite sua senha"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Confirmar senha -->
                <div class="space-y-1">
                  <label for="re_password" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Confirmar senha
                  </label>
                  <div class="relative group">
                    <input
                      id="re_password"
                      v-model="formData.re_password"
                      type="password"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="Confirme sua senha"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Error and Success Messages -->
              <div v-if="errorMessage" class="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-xs">
                <div class="flex items-center space-x-2">
                  <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p class="text-red-700 dark:text-red-400">{{ errorMessage }}</p>
                </div>
              </div>
              
              <div v-if="successMessage" class="p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg text-xs">
                <div class="flex items-center space-x-2">
                  <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p class="text-emerald-700 dark:text-emerald-400">{{ successMessage }}</p>
                </div>
              </div>

              <!-- Terms and conditions checkbox -->
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center space-x-1.5">
                  <input
                    id="agree-terms"
                    type="checkbox"
                    class="w-3 h-3 text-emerald-600 bg-white border-gray-300 rounded focus:ring-emerald-500 focus:ring-1 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <label for="agree-terms" class="text-gray-700 dark:text-gray-300">
                    Concordo com os termos
                  </label>
                </div>
              </div>

              <!-- Register Button -->
              <button
                type="submit"
                :disabled="isLoading"
                class="w-full relative overflow-hidden bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-2 px-4 text-sm rounded-lg shadow-lg transform transition-all duration-300 hover:scale-[1.02] hover:shadow-xl disabled:hover:scale-100 disabled:cursor-not-allowed group"
              >
                <!-- Button hover effect overlay -->
                <span class="absolute inset-0 bg-gradient-to-r from-white/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                <span class="relative flex items-center justify-center space-x-2">
                  <svg v-if="isLoading" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ isLoading ? 'Registrando...' : 'Registrar' }}</span>
                </span>
              </button>
            </form>

            <!-- Divider -->
            <div class="relative my-3">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
              </div>
              <div class="relative flex justify-center text-xs">
                <span class="px-2 bg-white/80 dark:bg-gray-800/80 text-gray-500 dark:text-gray-400 backdrop-blur-sm">
                  Ou
                </span>
              </div>
            </div>

            <!-- Login Link -->
            <div class="text-center text-xs">
              <p class="text-gray-600 dark:text-gray-400">
                Já tem uma conta?
                <NuxtLink
                  to="/auth/login"
                  class="font-semibold text-emerald-600 hover:text-emerald-500 dark:text-emerald-400 dark:hover:text-emerald-300 transition-colors duration-200 ml-1"
                >
                  Faça login
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from "vue";
import { useAuth } from "@/composables/useAuth";
import { useNotification } from "@/composables/useNotification";
import { useRouter } from "vue-router";
import { definePageMeta } from "#imports";

// Definir metadados da página
definePageMeta({
  layout: 'auth',
  middleware: ['guest']
});

// Composables
const router = useRouter();
const { register } = useAuth();
const { error: showError, success: showSuccess } = useNotification();

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
    showError('As senhas não coincidem');
    errorMessage.value = 'As senhas não coincidem';
    return;
  }

  // Limpar mensagens anteriores
  errorMessage.value = '';
  successMessage.value = '';
  isLoading.value = true;

  try {
    // Chamar o serviço de registro
    await register({
      username: formData.username,
      email: formData.email,
      full_name: formData.full_name,
      password: formData.password
    });

    // Atualizar mensagem de sucesso na interface
    showSuccess('Conta criada com sucesso!');
    successMessage.value = 'Conta criada com sucesso! Redirecionando para o login...';
    
    // Redirecionar para a página de login após um breve delay
    setTimeout(() => {
      router.push('/auth/login?registered=true');
    }, 1500);
  } catch (err) {
    // Tratamento de erro
    console.error('Erro ao registrar:', err);

    let errorMsg = 'Erro ao criar conta. Por favor, tente novamente.';

    // Verificar se temos um erro da API com dados estruturados
    if (err?.response?.data) {
      const errorData = err.response.data;
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
    } else if (err.message) {
      errorMsg = err.message;
    }
    
    // Exibir mensagem de erro
    showError(errorMsg);
    errorMessage.value = errorMsg;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Custom animation delays */
.animation-delay-0 { animation-delay: 0s; }
.animation-delay-1000 { animation-delay: 1s; }
.animation-delay-2000 { animation-delay: 2s; }
.animation-delay-3000 { animation-delay: 3s; }
.animation-delay-4000 { animation-delay: 4s; }
.animation-delay-5000 { animation-delay: 5s; }
.animation-delay-6000 { animation-delay: 6s; }
.animation-delay-7000 { animation-delay: 7s; }

/* Keyframes for the blob pulse animation */
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

/* Keyframes for the floating particle animation */
@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-5px) translateX(5px); }
  50% { transform: translateY(5px) translateX(-5px); }
  75% { transform: translateY(-5px) translateX(5px); }
}

/* Keyframes for a slower pulse animation */
@keyframes pulse-slow {
  0%, 100% { opacity: 0.8; transform: rotate(6deg) scale(1); }
  50% { opacity: 1; transform: rotate(6deg) scale(1.05); }
}

/* Applying the animations */
.animate-blob {
  animation: blob 7s infinite ease-in-out;
}

.animate-float {
  animation: float 10s infinite ease-in-out;
}

.animate-pulse-slow {
  animation: pulse-slow 3s infinite ease-in-out;
}
</style>