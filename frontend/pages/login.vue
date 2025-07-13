<!-- filepath: pages/login.vue -->
<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-blue-900 to-blue-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden"
  >
    <!-- Background decorative elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div
        class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"
      ></div>
      <div
        class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-indigo-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"
        style="animation-delay: 2s"
      ></div>
      <div
        class="absolute top-40 left-40 w-60 h-60 bg-gradient-to-br from-green-400 to-teal-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"
        style="animation-delay: 4s"
      ></div>
    </div>

    <!-- Login Card -->
    <div
      class="max-w-md w-full space-y-8 bg-white/10 backdrop-blur-lg border border-white/20 p-8 rounded-3xl shadow-2xl relative z-10"
    >
      <!-- Logo e cabeçalho -->
      <div class="text-center">
        <div
          class="mx-auto h-16 w-16 bg-gradient-to-br from-blue-500 to-blue-500 rounded-2xl flex items-center justify-center mb-6 shadow-lg"
        >
          <svg
            class="h-8 w-8 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <h2 class="text-4xl font-bold text-white mb-2">
          Plan<span class="text-blue-300">ify</span>
        </h2>
        <p class="text-blue-100 text-lg">Entre na sua conta</p>
      </div>

      <!-- Formulário de login -->
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label
              for="username"
              class="block text-sm font-medium text-blue-100 mb-2"
            >
              Usuário ou Email
            </label>
            <div class="relative">
              <div
                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
              >
                <svg
                  class="h-5 w-5 text-blue-300"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <input
                id="username"
                v-model="credentials.username"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
                placeholder="Digite seu usuário ou email"
              />
            </div>
          </div>

          <div>
            <label
              for="password"
              class="block text-sm font-medium text-blue-100 mb-2"
            >
              Senha
            </label>
            <div class="relative">
              <div
                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
              >
                <svg
                  class="h-5 w-5 text-blue-300"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <input
                id="password"
                v-model="credentials.password"
                type="password"
                required
                class="block w-full pl-10 pr-3 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
                placeholder="Digite sua senha"
              />
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-white/20 rounded bg-white/10 backdrop-blur-sm"
            />
            <label for="remember-me" class="ml-2 block text-sm text-blue-100">
              Lembrar-me
            </label>
          </div>

          <div class="text-sm">
            <NuxtLink
              to="/forgot-password"
              class="font-medium text-blue-300 hover:text-blue-200 transition-colors duration-200"
            >
              Esqueceu sua senha?
            </NuxtLink>
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-blue-600 hover:from-blue-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-105 shadow-lg"
          >
            <span
              v-if="isLoading"
              class="absolute left-0 inset-y-0 flex items-center pl-3"
            >
              <svg
                class="animate-spin h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            </span>
            {{ isLoading ? "Entrando..." : "Entrar" }}
          </button>
        </div>

        <!-- Mensagem de erro -->
        <div
          v-if="isError"
          class="mt-4 bg-red-500/20 backdrop-blur-sm border border-red-400/30 text-red-100 px-4 py-3 rounded-xl"
        >
          <p class="flex items-center">
            <svg
              class="h-5 w-5 text-red-400 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            {{
              error?.message || "Verifique suas credenciais e tente novamente"
            }}
          </p>
        </div>

        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/20"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-transparent text-blue-200">ou</span>
          </div>
        </div>

        <!-- Register Link -->
        <div class="text-center">
          <p class="text-blue-100 text-sm">
            Não tem uma conta?
            <NuxtLink
              to="/register"
              class="font-medium text-blue-300 hover:text-blue-200 transition-colors duration-200 underline underline-offset-2"
            >
              Cadastre-se agora
            </NuxtLink>
          </p>
        </div>
      </form>
    </div>

    <!-- Footer -->
    <div class="absolute bottom-4 text-center text-blue-300 text-sm">
      <p>&copy; 2024 Planify. Todos os direitos reservados.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuth } from "@/composables/useAuth";
import type { TokenObtainPairRequest } from "@/api/schemas";

definePageMeta({
  middleware: ["guest"],
  layout: "auth",
});

const route = useRoute();
const { login, isLoading, isError, error } = useAuth();

const credentials = ref<TokenObtainPairRequest>({
  username: "",
  password: "",
});

const handleLogin = () => {
  if (!credentials.value.username || !credentials.value.password) {
    return;
  }

  const redirectPath = route.query.redirect?.toString() || "/dashboard";

  console.log(
    `Tentando fazer login... Redirecionar para ${redirectPath} em caso de sucesso.`
  );

  login(credentials.value, redirectPath);
};
</script>

<style scoped>
/* Glassmorphism effects */
.backdrop-blur-lg {
  backdrop-filter: blur(16px);
}

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Custom animations */
@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.3;
  }
}

/* Input focus effects */
input:focus {
  box-shadow: 0 0 0 3px rgba(6, 51, 159, 0.1);
}

/* Button hover effects */
button:hover:not(:disabled) {
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Smooth transitions */
* {
  transition: all 0.3s ease;
}
</style>
