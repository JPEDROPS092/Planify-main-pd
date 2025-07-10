<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-indigo-900 to-cyan-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden"
  >
    <!-- Background decorative elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div
        class="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-indigo-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"
      ></div>
      <div
        class="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"
        style="animation-delay: 2s"
      ></div>
      <div
        class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-br from-indigo-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse"
        style="animation-delay: 4s"
      ></div>
    </div>

    <!-- Register Card -->
    <div
      class="max-w-lg w-full space-y-6 bg-white/10 backdrop-blur-lg border border-white/20 p-8 rounded-3xl shadow-2xl relative z-10"
    >
      <!-- Logo e cabeçalho -->
      <div class="text-center">
        <div
          class="mx-auto h-16 w-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center mb-6 shadow-lg"
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
              d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
            />
          </svg>
        </div>
        <h2 class="text-4xl font-bold text-white mb-2">
          Plan<span class="text-blue-300">ify</span>
        </h2>
        <p class="text-blue-100 text-lg">Crie sua conta gratuitamente</p>
      </div>

      <!-- Formulário de registro -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <!-- Nome e Sobrenome -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label
              for="firstName"
              class="block text-sm font-medium text-blue-100 mb-2"
            >
              Nome *
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
                id="firstName"
                v-model="form.firstName"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
                placeholder="Seu nome"
              />
            </div>
          </div>
          <div>
            <label
              for="lastName"
              class="block text-sm font-medium text-blue-100 mb-2"
            >
              Sobrenome *
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
                id="lastName"
                v-model="form.lastName"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
                placeholder="Seu sobrenome"
              />
            </div>
          </div>
        </div>

        <!-- Username -->
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-blue-100 mb-2"
          >
            Nome de usuário *
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
                  d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                />
              </svg>
            </div>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="block w-full pl-10 pr-3 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
              placeholder="Nome de usuário único"
            />
          </div>
        </div>

        <!-- Email -->
        <div>
          <label
            for="email"
            class="block text-sm font-medium text-blue-100 mb-2"
          >
            E-mail *
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
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="block w-full pl-10 pr-3 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
              placeholder="seu@email.com"
            />
          </div>
        </div>

        <!-- Senha -->
        <div>
          <label
            for="password"
            class="block text-sm font-medium text-blue-100 mb-2"
          >
            Senha *
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
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="block w-full pl-10 pr-12 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
              placeholder="Mínimo 8 caracteres"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-blue-300 hover:text-blue-200 transition-colors"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  v-if="showPassword"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L12 12m-2.122-2.122L7.758 7.758M12 12l2.122 2.122m0 0L16.242 16.242M12 12l2.122-2.122m0 0L16.242 7.758"
                />
                <path
                  v-else
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Confirmar Senha -->
        <div>
          <label
            for="confirmPassword"
            class="block text-sm font-medium text-blue-100 mb-2"
          >
            Confirmar Senha *
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
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              required
              class="block w-full pl-10 pr-12 py-3 border border-white/20 placeholder-blue-300 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/10 backdrop-blur-sm transition-all duration-300"
              :class="{
                'border-red-400 ring-red-400':
                  form.confirmPassword &&
                  form.password !== form.confirmPassword,
              }"
              placeholder="Confirme sua senha"
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-blue-300 hover:text-blue-200 transition-colors"
            >
              <svg
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  v-if="showConfirmPassword"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L12 12m-2.122-2.122L7.758 7.758M12 12l2.122 2.122m0 0L16.242 16.242M12 12l2.122-2.122m0 0L16.242 7.758"
                />
                <path
                  v-else
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            </button>
          </div>
          <p
            v-if="
              form.confirmPassword && form.password !== form.confirmPassword
            "
            class="mt-2 text-sm text-red-300 flex items-center"
          >
            <svg
              class="h-4 w-4 mr-1"
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
            As senhas não coincidem
          </p>
        </div>

        <!-- Indicador de força da senha -->
        <div v-if="form.password" class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-sm text-blue-100">Força da senha:</span>
            <span class="text-sm font-medium" :class="passwordStrengthColor">
              {{ passwordStrengthText }}
            </span>
          </div>
          <div class="w-full bg-white/10 rounded-full h-2">
            <div
              class="h-2 rounded-full transition-all duration-300"
              :class="passwordStrengthColor"
              :style="{ width: passwordStrengthPercent + '%' }"
            ></div>
          </div>
        </div>

        <!-- Termos e Condições -->
        <div class="flex items-start space-x-3">
          <input
            id="acceptTerms"
            v-model="form.acceptTerms"
            type="checkbox"
            required
            class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-white/20 rounded bg-white/10 backdrop-blur-sm"
          />
          <label for="acceptTerms" class="text-sm text-blue-100 leading-5">
            Eu aceito os
            <a
              href="#"
              class="text-blue-300 hover:text-blue-200 underline underline-offset-2"
            >
              Termos de Uso
            </a>
            e a
            <a
              href="#"
              class="text-blue-300 hover:text-blue-200 underline underline-offset-2"
            >
              Política de Privacidade
            </a>
          </label>
        </div>

        <!-- Botão de Registro -->
        <button
          type="submit"
          :disabled="!isFormValid || isRegistering"
          class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transform transition-all duration-200 hover:scale-105 shadow-lg"
        >
          <span
            v-if="isRegistering"
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
          {{ isRegistering ? "Criando conta..." : "Criar Conta" }}
        </button>

        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-white/20"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-transparent text-blue-200">ou</span>
          </div>
        </div>

        <!-- Link para Login -->
        <div class="text-center">
          <p class="text-blue-100 text-sm">
            Já tem uma conta?
            <NuxtLink
              to="/login"
              class="font-medium text-blue-300 hover:text-blue-200 transition-colors duration-200 underline underline-offset-2"
            >
              Fazer login
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
import { ref, computed } from "vue";

// Define que esta página não deve usar layout
definePageMeta({
  layout: false,
});
// State
const isRegistering = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const form = ref({
  username: "",
  email: "",
  firstName: "",
  lastName: "",
  password: "",
  confirmPassword: "",
  acceptTerms: false,
});

// Toast function
const showToast = (message: string, type: "success" | "error" = "success") => {
  alert(`${type.toUpperCase()}: ${message}`);
};

// Computed properties
const isFormValid = computed(() => {
  return (
    form.value.username &&
    form.value.email &&
    form.value.firstName &&
    form.value.lastName &&
    form.value.password &&
    form.value.password === form.value.confirmPassword &&
    form.value.acceptTerms &&
    form.value.password.length >= 8
  );
});

const passwordStrength = computed(() => {
  const password = form.value.password;
  if (!password) return 0;

  let strength = 0;

  // Length check
  if (password.length >= 8) strength += 1;
  if (password.length >= 12) strength += 1;

  // Character variety checks
  if (/[a-z]/.test(password)) strength += 1;
  if (/[A-Z]/.test(password)) strength += 1;
  if (/[0-9]/.test(password)) strength += 1;
  if (/[^A-Za-z0-9]/.test(password)) strength += 1;

  return strength;
});

const passwordStrengthPercent = computed(() => {
  return (passwordStrength.value / 6) * 100;
});

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value;
  if (strength <= 2) return "Fraca";
  if (strength <= 4) return "Média";
  return "Forte";
});

const passwordStrengthColor = computed(() => {
  const strength = passwordStrength.value;
  if (strength <= 2) return "text-red-400 bg-red-400";
  if (strength <= 4) return "text-yellow-400 bg-yellow-400";
  return "text-blue-400 bg-blue-400";
});

// Methods
const handleRegister = async () => {
  if (!isFormValid.value) return;

  isRegistering.value = true;

  try {
    // Simulação de registro
    await new Promise((resolve) => setTimeout(resolve, 1000));

    showToast(
      "Conta criada com sucesso! Agora você pode fazer login.",
      "success"
    );

    // Redirecionar para login
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
  } catch (error) {
    showToast("Erro ao criar conta. Tente novamente.", "error");
    console.error("Registration failed:", error);
  } finally {
    isRegistering.value = false;
  }
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
  box-shadow: 0 0 0 3px rgba(0, 112, 249, 0.1);
}

/* Button hover effects */
button:hover:not(:disabled) {
  box-shadow:
    0 20px 25px -5px rgba(0, 162, 255, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Smooth transitions */
* {
  transition: all 0.3s ease;
}
</style>
