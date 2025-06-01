<template>
  <div
    class="flex min-h-screen flex-col justify-center bg-gray-50 py-12 sm:px-6 lg:px-8"
  >
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="text-center text-3xl font-bold tracking-tight text-gray-900">
        Planify
      </h2>
      <h2
        class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900"
      >
        Recuperação de senha
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        Informe seu e-mail para receber instruções de recuperação
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700"
              >E-mail</label
            >
            <div class="mt-1">
              <input
                id="email"
                v-model="email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 placeholder-gray-400 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
              />
            </div>
            <p v-if="error" class="mt-2 text-sm text-red-600">{{ error }}</p>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="flex w-full justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <span v-if="loading">Processando...</span>
              <span v-else>Enviar instruções</span>
            </button>
          </div>
        </form>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="bg-white px-2 text-gray-500">Ou</span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-1 gap-3">
            <div>
              <NuxtLink
                to="/login"
                class="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-500 shadow-sm hover:bg-gray-50"
              >
                Voltar para o login
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useApiService } from '~/services/api';
import { useNotification } from '~/composables/useNotification';

const router = useRouter();
const api = useApiService();
const { notify } = useNotification();

const email = ref('');
const loading = ref(false);
const error = ref('');
const success = ref(false);

const handleSubmit = async () => {
  try {
    loading.value = true;
    error.value = '';

    // Aqui implementaríamos a chamada real à API para recuperação de senha
    // Por enquanto, vamos simular uma resposta bem-sucedida
    await new Promise((resolve) => setTimeout(resolve, 1000));

    success.value = true;
    notify({
      type: 'success',
      message:
        'Enviamos instruções para recuperar sua senha. Por favor, verifique seu e-mail.',
    });

    // Redirecionar para a página de login após alguns segundos
    setTimeout(() => {
      router.push('/login');
    }, 3000);
  } catch (err: any) {
    error.value =
      err.friendlyMessage ||
      'Ocorreu um erro ao processar sua solicitação. Tente novamente.';
    notify({
      type: 'error',
      message: error.value,
    });
  } finally {
    loading.value = false;
  }
};
</script>
