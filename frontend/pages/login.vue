<!-- filepath: pages/login.vue -->
<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
      <!-- Logo e cabeçalho -->
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">Planify</h2>
        <p class="mt-2 text-sm text-gray-600">Faça login para continuar</p>
      </div>

      <!-- Formulário de login -->
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div class="rounded-md -space-y-px">
          <div class="mb-4">
            <label
              for="username"
              class="block text-sm font-medium text-gray-700 mb-1"
              >Usuário ou Email</label
            >
            <input
              id="username"
              v-model="credentials.username"
              type="text"
              required
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Digite seu usuário ou email"
            />
          </div>

          <div class="mb-4">
            <label
              for="password"
              class="block text-sm font-medium text-gray-700 mb-1"
              >Senha</label
            >
            <input
              id="password"
              v-model="credentials.password"
              type="password"
              required
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500 focus:z-10 sm:text-sm"
              placeholder="Digite sua senha"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900"
              >Lembrar-me</label
            >
          </div>

          <div class="text-sm">
            <a
              href="#"
              class="font-medium text-primary-600 hover:text-primary-500"
              >Esqueceu sua senha?</a
            >
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
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
          class="mt-2 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md"
        >
          <p class="flex items-center">
            <svg
              class="h-5 w-5 text-red-500 mr-2"
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
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useAuth } from "@/composables/useAuth";
import type { TokenObtainPairRequest } from "@/api/schemas";

// Define que esta é uma página pública (não requer autenticação)
definePageMeta({
  middleware: ["guest"],
});

const { login, isLoading, isError, error } = useAuth();

// Dados do formulário
const credentials = ref<TokenObtainPairRequest>({
  username: "",
  password: "",
});

// Função para lidar com o submit do formulário
const handleLogin = () => {
  if (!credentials.value.username || !credentials.value.password) {
    console.error("Usuário e senha são obrigatórios");
    return;
  }

  console.log("Tentando fazer login com:", {
    username: credentials.value.username,
  });

  // Execute o login através do composable
  login(credentials.value);
};
</script>
