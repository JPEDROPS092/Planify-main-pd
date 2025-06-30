<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { Icon } from "@iconify/vue";
import { useToast } from "~/composables/useToast";
import type { TokenObtainPairRequest } from "~/api/schemas";
import { useAuthJwtCreateCreate } from "~/api/auth/auth";

definePageMeta({
  middleware: "guest",
  layout: false,
});

const authStore = useAuthStore();
const { toast } = useToast();
const router = useRouter();

const form = ref<TokenObtainPairRequest>({
  username: "",
  password: "",
});

// Chama o hook de mutação no setup.
// A renomeação de 'isPending' para 'isLoading' está correta para o template.
const { mutateAsync: performLogin, isPending: isLoading } =
  useAuthJwtCreateCreate();

const handleSubmit = async () => {
  if (!form.value.username || !form.value.password) {
    toast({
      title: "Campos obrigatórios",
      description: "Por favor, preencha o nome de usuário e a senha.",
      type: "warning",
    });
    return;
  }

  try {
    const response = await performLogin({ data: form.value });
    await authStore.setAuthData(response.data);

    toast({
      title: "Sucesso!",
      description: "Login realizado com sucesso. Bem-vindo de volta!",
      type: "success",
    });
    router.push("/dashboard");
  } catch (error: any) {
    console.error("Login falhou no componente:", error);
    toast({
      title: "Falha no Login",
      description:
        error.response?.data?.detail ||
        "Nome de usuário ou senha inválidos. Por favor, tente novamente.",
      type: "error",
    });
  }
};
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4 sm:px-6 lg:px-8"
  >
    <div class="max-w-md w-full space-y-8">
      <!-- Cabeçalho - pode ser renderizado no servidor -->
      <div>
        <div class="flex justify-center">
          <div
            class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center"
          >
            <Icon icon="lucide:layout-dashboard" class="w-8 h-8 text-white" />
          </div>
        </div>
        <h2
          class="mt-6 text-center text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"
        >
          Planify
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Faça login em sua conta
        </p>
      </div>

      <!-- ==================== CORREÇÃO PRINCIPAL ==================== -->
      <!-- Envolve o formulário com a tag <ClientOnly> para evitar erros de SSR -->
      <ClientOnly>
        <div
          class="bg-white py-8 px-6 shadow-xl rounded-xl border border-gray-100"
        >
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <div>
              <label
                for="username"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Nome de usuário
              </label>
              <input
                id="username"
                v-model="form.username"
                name="username"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Seu nome de usuário"
              />
            </div>

            <div>
              <label
                for="password"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Senha
              </label>
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Sua senha"
              />
            </div>

            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember"
                  type="checkbox"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label for="remember" class="ml-2 block text-sm text-gray-700">
                  Lembrar de mim
                </label>
              </div>
              <a href="#" class="text-sm text-blue-600 hover:text-blue-500">
                Esqueceu a senha?
              </a>
            </div>

            <button
              type="submit"
              :disabled="isLoading"
              class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Icon
                v-if="isLoading"
                icon="lucide:loader-2"
                class="w-4 h-4 mr-2 animate-spin"
              />
              {{ isLoading ? "Entrando..." : "Entrar" }}
            </button>
          </form>

          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              Não tem uma conta?
              <NuxtLink
                to="/register"
                class="text-blue-600 hover:text-blue-500 font-medium"
              >
                Criar conta grátis
              </NuxtLink>
            </p>
          </div>
        </div>

        <!-- Fallback que o Nuxt mostrará no lugar do conteúdo durante o SSR -->
        <template #fallback>
          <div
            class="bg-white py-8 px-6 shadow-xl rounded-xl border border-gray-100 opacity-50"
          >
            <p class="text-center text-gray-500">Carregando formulário...</p>
          </div>
        </template>
      </ClientOnly>
      <!-- ============================================================ -->

      <div class="text-center">
        <NuxtLink to="/" class="text-sm text-gray-500 hover:text-gray-700">
          ← Voltar ao início
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
