<template>
  <div
    class="container flex h-screen w-screen flex-col items-center justify-center"
  >
    <div
      class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]"
    >
      <div class="flex flex-col space-y-2 text-center">
        <h1 class="text-2xl font-semibold tracking-tight">Entrar no Planify</h1>
        <p class="text-sm text-muted-foreground">
          Digite suas credenciais para acessar o sistema
        </p>
      </div>
      <div class="grid gap-6">
        <form @submit.prevent="handleLogin">
          <div class="grid gap-4">
            <div class="grid gap-2">
              <label
                for="username"
                class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Nome de usuário
              </label>
              <input
                id="username"
                v-model="username"
                type="text"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                placeholder="seu_usuario"
                required
              />
            </div>
            <div class="grid gap-2">
              <div class="flex items-center justify-between">
                <label
                  for="password"
                  class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Senha
                </label>
                <NuxtLink
                  to="/esqueci-senha"
                  class="text-sm text-primary underline-offset-4 hover:underline"
                >
                  Esqueceu a senha?
                </NuxtLink>
              </div>
              <input
                id="password"
                v-model="password"
                type="password"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                required
              />
            </div>
            <button
              type="submit"
              class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Entrando...' : 'Entrar' }}
            </button>
            <div v-if="error" class="text-red-500 text-sm text-center">
              {{ error }}
            </div>
          </div>
        </form>
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <span class="w-full border-t"></span>
          </div>
          <div class="relative flex justify-center text-xs uppercase">
            <span class="bg-background px-2 text-muted-foreground">Ou</span>
          </div>
        </div>
        <div class="text-center text-sm">
          Não tem uma conta?
          <NuxtLink
            to="/registro"
            class="text-primary underline-offset-4 hover:underline"
          >
            Registre-se
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '~/composables/useAuth';
import { ref } from 'vue';
import { useNuxtApp } from '#app';

const { $api } = useNuxtApp();
const username = ref('');
const password = ref('');

const { login, isAuthenticated, error, isLoading } = useAuth();

const handleLogin = async () => {
  try {
    await login({
      username: username.value,
      password: password.value,
    });

    if (isAuthenticated.value) {
      navigateTo('/projetos');
    }
  } catch (err) {
    console.error('Erro ao fazer login na página:', err);
  }
};
</script>
