<template>
  <!-- Contêiner de página inteira com fundo gradiente e preenchimento mínimo em telas pequenas -->
  <div class="min-h-screen relative overflow-hidden bg-gradient-to-br from-blue-50 via-cyan-50 to-sky-50 dark:from-gray-900 dark:via-blue-900 dark:to-cyan-900 sm:p-4 p-2">

    <!-- Blobs de gradiente animados de fundo -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <!-- Blob grande no canto superior direito -->
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-cyan-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-0"></div>
      <!-- Blob grande no canto inferior esquerdo -->
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-sky-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
      <!-- Blob grande no centro -->
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-4000"></div>
    </div>

    <!-- Partículas flutuantes (animação sutil) -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-[15%] w-2 h-2 bg-white rounded-full opacity-20 animate-float animation-delay-1000"></div>
      <div class="absolute top-[60%] right-[20%] w-1 h-1 bg-blue-300 rounded-full opacity-30 animate-float animation-delay-3000"></div>
      <div class="absolute bottom-1/4 left-[25%] w-1.5 h-1.5 bg-cyan-300 rounded-full opacity-25 animate-float animation-delay-5000"></div>
      <div class="absolute top-[10%] right-[10%] w-1 h-1 bg-sky-300 rounded-full opacity-15 animate-float animation-delay-6000"></div>
      <div class="absolute bottom-[10%] right-[10%] w-1.5 h-1.5 bg-blue-300 rounded-full opacity-20 animate-float animation-delay-7000"></div>
    </div>

    <!-- Área de conteúdo principal - centralizada -->
    <div class="relative z-10 flex min-h-screen items-center justify-center p-2 sm:p-4">
      <div class="w-full max-w-sm transform transition-all duration-500 hover:scale-[1.01] ease-in-out"> <!-- Largura máxima reduzida e escala -->

        <!-- Card de Login -->
        <div class="relative bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-xl shadow-xl border border-white/20 dark:border-gray-700/20 overflow-hidden">
          <!-- Sobreposição de gradiente dentro do card para efeito sutil -->
          <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent pointer-events-none"></div>

          <!-- Conteúdo do Card -->
          <div class="relative p-4 sm:p-5 space-y-4">

            <!-- Seção do Logo e Cabeçalho -->
            <div class="text-center space-y-2">
              <div class="relative mx-auto w-12 h-12 mb-2">
                <!-- Fundo gradiente pulsante -->
                <div class="absolute inset-0 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg transform rotate-6 animate-pulse-slow"></div>
                <!-- Contêiner do logo com seu próprio gradiente -->
                <div class="relative bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg w-full h-full flex items-center justify-center z-10">
                  <img src="/img/logop.png" alt="Logo Planify" class="w-8 h-8 object-contain" />
                </div>
              </div>

              <!-- Título e Subtítulo -->
              <div class="space-y-0.5">
                <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 dark:from-blue-400 dark:to-cyan-400 bg-clip-text text-transparent">
                  Bem-vindo de volta
                </h1>
                <p class="text-gray-600 dark:text-gray-400 text-xs">
                  Acesse sua conta para gerenciar seus projetos
                </p>
              </div>
            </div>

            <!-- Formulário de Login -->
            <form @submit.prevent="handleLogin" class="space-y-3">
              <!-- Área de exibição de mensagens de erro (Card de Erro) -->
              <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg p-3 text-xs text-red-700 dark:text-red-300">
                <div class="flex items-start">
                  <svg class="h-4 w-4 text-red-500 dark:text-red-400 mt-0.5 mr-2 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  <div>
                    <p class="font-medium">{{ errorTitle }}</p>
                    <p class="mt-0.5">{{ errorMessage }}</p>
                    <p v-if="isUserNotFound" class="mt-1">
                      Não tem uma conta? <NuxtLink to="/auth/registro" class="text-red-700 dark:text-red-300 font-semibold underline hover:text-red-800">Registre-se agora</NuxtLink>.
                    </p>
                  </div>
                </div>
              </div>

              <div class="space-y-3">
                <!-- Campo de Nome de Usuário ou Email -->
                <div class="space-y-1">
                  <label for="username" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Nome de usuário ou Email
                  </label>
                  <div class="relative group">
                    <input
                      v-model="usernameOrEmail"
                      id="username"
                      type="text"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="nome.usuario ou email@exemplo.com"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                      </svg>
                    </div>
                  </div>
                </div>

                <!-- Campo de Senha -->
                <div class="space-y-1">
                  <label for="password" class="block text-xs font-medium text-gray-700 dark:text-gray-300">
                    Senha
                  </label>
                  <div class="relative group">
                    <input
                      v-model="password"
                      id="password"
                      type="password"
                      required
                      class="w-full px-3 py-2 text-sm bg-white/50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 rounded-lg shadow-sm backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent transition-all duration-300 group-hover:bg-white/70 dark:group-hover:bg-gray-700/70 text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                      placeholder="••••••••"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg class="w-4 h-4 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Lembrar-me e Esqueceu a senha -->
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center space-x-1.5">
                  <input
                    id="remember-me"
                    v-model="rememberMe"
                    type="checkbox"
                    class="w-3 h-3 text-blue-600 bg-white border-gray-300 rounded focus:ring-blue-500 focus:ring-1 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <label for="remember-me" class="text-gray-700 dark:text-gray-300">
                    Lembrar-me
                  </label>
                </div>

                <NuxtLink
                  to="/auth/esqueci-senha"
                  class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition-colors duration-200"
                >
                  Esqueceu sua senha?
                </NuxtLink>
              </div>

              <!-- Botão de Login -->
              <button
                type="submit"
                :disabled="loading"
                class="w-full relative overflow-hidden bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-2 px-4 text-sm rounded-lg shadow-lg transform transition-all duration-300 hover:scale-[1.02] hover:shadow-xl disabled:hover:scale-100 disabled:cursor-not-allowed group"
              >
                <!-- Efeito de sobreposição no hover do botão -->
                 <span class="absolute inset-0 bg-gradient-to-r from-white/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
                <span class="relative flex items-center justify-center space-x-2">
                  <svg v-if="loading" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>{{ loading ? 'Entrando...' : 'Entrar' }}</span>
                </span>
              </button>
            </form>

            <!-- Divisor -->
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

            <!-- Link para Registro -->
            <div class="text-center text-xs">
              <p class="text-gray-600 dark:text-gray-400">
                Não tem uma conta?
                <NuxtLink
                  to="/auth/registro"
                  class="font-semibold text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300 transition-colors duration-200 ml-1"
                >
                  Registre-se
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
// Assumindo que estes composables existem em sua aplicação Nuxt
import { useAuth } from '~/composables/useAuth';
import { useNotification } from '~/composables/useNotification';

const router = useRouter();
const route = useRoute();
const { login } = useAuth(); // Usa a função de login do composable de autenticação
const { error: showError, success: showSuccess } = useNotification(); // Usa as funções de notificação

// Changed from 'email' to 'usernameOrEmail' to reflect both possibilities
const usernameOrEmail = ref('');
const password = ref('');
const rememberMe = ref(false);
const loading = ref(false);
const errorTitle = ref(''); // Título para o card de erro
const errorMessage = ref(''); // Mensagem principal para o card de erro
const isUserNotFound = ref(false);

const handleLogin = async () => {
  // Reseta os estados de erro
  errorTitle.value = '';
  errorMessage.value = '';
  isUserNotFound.value = false;

  // Validação básica do formulário
  if (!usernameOrEmail.value || !password.value) {
    errorTitle.value = 'Campos Obrigatórios';
    errorMessage.value = 'Por favor, preencha seu nome de usuário ou email e senha.';
    showError(errorMessage.value, { title: errorTitle.value });
    return;
  }

  loading.value = true;

  try {
    // Cria o objeto de credenciais com 'username' (usando o email) e 'password'
    const credentials = {
      username: usernameOrEmail.value, // O backend Django espera 'username' mesmo que seja um email
      password: password.value,
      remember: rememberMe.value
    };

    // Chama o composable de login com o objeto de credenciais
    const result = await login(credentials);

    if (result.success) {
      // Redirecionamento após login bem-sucedido
      const redirectPath = route.query.redirect || '/dashboard';
      router.push(redirectPath);
      showSuccess('Login realizado com sucesso!');
    } else {
      // Se login retornar success: false, exibir mensagem genérica
      // (normalmente não cairia aqui, pois o catch pegaria os erros)
      errorTitle.value = 'Falha na Autenticação';
      errorMessage.value = 'Não foi possível realizar o login. Verifique suas credenciais.';
      showError(errorMessage.value, { title: errorTitle.value });
    }

  } catch (err) {
    console.error('Erro ao fazer login:', err);
    
    // Determinar mensagem de erro baseado na resposta do backend
    if (err?.response?.data) {
      const data = err.response.data;
      
      // Verificar mensagens de erro específicas do Django REST Framework
      if (data.detail) {
        if (typeof data.detail === 'string') {
          if (data.detail.includes('No active account') || data.detail.includes('given credentials')) {
            errorTitle.value = 'Credenciais Inválidas';
            errorMessage.value = 'O nome de usuário/email ou a senha informados estão incorretos. Verifique e tente novamente.';
          } else if (data.detail.includes('not found') || data.detail.includes('inexistente')) {
            errorTitle.value = 'Usuário Não Encontrado';
            errorMessage.value = 'Este usuário não existe em nosso sistema.';
            isUserNotFound.value = true;
          } else {
            errorTitle.value = 'Erro de Autenticação';
            errorMessage.value = data.detail;
          }
        }
      } else if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
        // Django REST Framework frequentemente retorna erros de auth em non_field_errors
        errorTitle.value = 'Erro de Autenticação';
        errorMessage.value = data.non_field_errors[0];
        
        // Verificar se é erro de usuário não encontrado ou senha incorreta
        if (data.non_field_errors[0].toLowerCase().includes('no active account') || 
            data.non_field_errors[0].toLowerCase().includes('user') && 
            data.non_field_errors[0].toLowerCase().includes('not found')) {
          errorTitle.value = 'Usuário Não Encontrado';
          errorMessage.value = 'Este usuário não existe em nosso sistema.';
          isUserNotFound.value = true;
        } else if (data.non_field_errors[0].toLowerCase().includes('incorrect') || 
                  data.non_field_errors[0].toLowerCase().includes('invalid')) {
          errorTitle.value = 'Credenciais Inválidas';
          errorMessage.value = 'O nome de usuário/email ou a senha informados estão incorretos. Verifique e tente novamente.';
        }
      }
    } else {
      // Tratamento de erros genéricos ou baseados na mensagem do erro
      if (err.message?.includes('Usuário e/ou senha incorreto')) {
        errorTitle.value = 'Credenciais Inválidas';
        errorMessage.value = 'O nome de usuário/email ou a senha informados estão incorretos. Verifique e tente novamente.';
      } else if (err.message?.includes('inexistente') || (typeof err.message === 'string' && err.message.toLowerCase().includes('not found'))) {
        errorTitle.value = 'Usuário Não Encontrado';
        errorMessage.value = 'Este usuário não existe em nosso sistema.';
        isUserNotFound.value = true;
      } else if (err.message?.includes('bloqueada') || err.message?.includes('inativa')) {
        errorTitle.value = 'Conta Bloqueada';
        errorMessage.value = 'Sua conta está temporariamente bloqueada ou inativa. Por favor, contate o suporte.';
      } else if (err.message?.includes('Network Error') || err.response?.status === 0) {
        errorTitle.value = 'Erro de Conexão';
        errorMessage.value = 'Não foi possível conectar ao servidor. Verifique sua internet ou tente novamente mais tarde.';
      } else {
        // Mensagem de erro padrão
        errorTitle.value = 'Falha na Autenticação';
        errorMessage.value = err?.message || 'Ocorreu um erro inesperado. Tente novamente.';
      }
    }
    
    // Adicionar mensagem de erro abaixo do formulário
    const errorCard = document.createElement('div');
    errorCard.className = 'bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg p-3 mt-3 text-xs text-red-700 dark:text-red-300';
    errorCard.innerHTML = `
      <div class="flex items-start">
        <svg class="h-4 w-4 text-red-500 dark:text-red-400 mt-0.5 mr-2 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <div>
          <p class="font-medium">${errorTitle.value}</p>
          <p class="mt-0.5">${errorMessage.value}</p>
          ${isUserNotFound.value ? `<p class="mt-1">Não tem uma conta? <a href="/auth/registro" class="text-red-700 dark:text-red-300 font-semibold underline hover:text-red-800">Registre-se agora</a>.</p>` : ''}
        </div>
      </div>
    `;
    
    // Adicionar o card de erro após o formulário
    const form = document.querySelector('form');
    if (form) {
      // Remover mensagens de erro anteriores
      const previousErrors = document.querySelectorAll('.login-error-message');
      previousErrors.forEach(el => el.remove());
      
      // Adicionar classe para identificação
      errorCard.classList.add('login-error-message');
      
      // Inserir após o formulário
      form.parentNode?.insertBefore(errorCard, form.nextSibling);
    }
    
    // Mostra notificação (toast) com o erro - com visibilidade aprimorada
    showError(errorMessage.value, {
      title: errorTitle.value || 'Erro de Autenticação', // Usa o título específico ou um padrão
      duration: 6000, // Aumenta a duração para melhor leitura
      position: 'top-center'
    });
    
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Atrasos de animação personalizados */
.animation-delay-0 { animation-delay: 0s; }
.animation-delay-1000 { animation-delay: 1s; }
.animation-delay-2000 { animation-delay: 2s; }
.animation-delay-3000 { animation-delay: 3s; }
.animation-delay-4000 { animation-delay: 4s; }
.animation-delay-5000 { animation-delay: 5s; }
.animation-delay-6000 { animation-delay: 6s; }
.animation-delay-7000 { animation-delay: 7s; }


/* Keyframes para a animação de pulso do blob */
@keyframes blob {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

/* Keyframes para a animação de partículas flutuantes */
@keyframes float {
  0%, 100% { transform: translateY(0) translateX(0); }
  25% { transform: translateY(-5px) translateX(5px); }
  50% { transform: translateY(5px) translateX(-5px); }
  75% { transform: translateY(-5px) translateX(5px); }
}

/* Keyframes para uma animação de pulso mais lenta */
@keyframes pulse-slow {
    0%, 100% { opacity: 0.8; transform: rotate(6deg) scale(1); }
    50% { opacity: 1; transform: rotate(6deg) scale(1.05); }
}


/* Aplicando as animações */
.animate-blob {
  animation: blob 7s infinite ease-in-out;
}

.animate-float {
  animation: float 10s infinite ease-in-out; /* Animação de flutuação mais lenta */
}

.animate-pulse-slow {
  animation: pulse-slow 3s infinite ease-in-out; /* Pulso lento aplicado */
}

</style>