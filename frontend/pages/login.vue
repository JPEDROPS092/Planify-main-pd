<script setup lang="ts">
import { ref } from 'vue';
import { useMutation } from '@tanstack/vue-query';
import { useAuth } from '~/composables/useAuth';
import { Icon } from '@iconify/vue';
import { useToast } from '~/composables/useToast';
import type { LoginRequest } from '~/api-types';

definePageMeta({
  layout: 'auth',
  middleware: 'guest',
});

const { login } = useAuth();
const { toast } = useToast();
const router = useRouter();
const route = useRoute();

const form = ref<LoginRequest>({
  username: '',
  password: '',
});

const loginMutation = useMutation({
  mutationFn: (credentials: LoginRequest) => login(credentials),
  onSuccess: () => {
    toast({
      title: 'Login realizado com sucesso',
      description: 'Bem-vindo ao Planify!',
    });
    const redirectPath = route.query.redirect?.toString() || '/';
    router.push(redirectPath);
  },
  onError: (error: any) => {
    toast({
      title: 'Erro ao fazer login',
      description: error.data?.detail || 'Credenciais inválidas. Por favor, tente novamente.',
      variant: 'destructive',
    });
  },
});

const handleSubmit = () => {
  if (!form.value.username || !form.value.password) {
    toast({
      title: 'Campos obrigatórios',
      description: 'Por favor, preencha o usuário e a senha.',
      variant: 'destructive',
    });
    return;
  }
  loginMutation.mutate(form.value);
};
</script>

<template>
  <div class="w-full max-w-md">
    <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
      <div class="text-center mb-6">
        <Icon icon="lucide:layout-dashboard" class="h-12 w-12 text-primary mx-auto" />
        <h2 class="mt-4 text-3xl font-extrabold text-gray-900">Planify</h2>
        <p class="mt-2 text-sm text-gray-600">
          Gerenciamento de Projetos
        </p>
      </div>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700">
            Usuário
          </label>
          <div class="mt-1">
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="Usuário"
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Senha
          </label>
          <div class="mt-1">
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="Senha"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loginMutation.isLoading"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loginMutation.isLoading" class="inline-block mr-2">
              <Icon icon="lucide:loader-2" class="h-4 w-4 animate-spin" />
            </span>
            Entrar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
