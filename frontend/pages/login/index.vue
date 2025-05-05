<template>
  <div class="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4 py-12 dark:bg-gray-900 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8">
      <div class="text-center">
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-600 text-white">
          <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-8 w-8">
            <path d="M2 17a5 5 0 0 0 10 0c0-2.76-2.5-5-5-3-2.5-2-5 .24-5 3Z"></path>
            <path d="M12 17a5 5 0 0 0 10 0c0-2.76-2.5-5-5-3-2.5-2-5 .24-5 3Z"></path>
            <path d="M7 14c3.22-2.91 4.29-8.75 5-12 1.66 2.38 4.94 9 5 12"></path>
            <path d="M22 9c-4.29 0-7.14-2.33-10-7 5.71 0 10 4.67 10 7Z"></path>
          </svg>
        </div>
        <h2 class="mt-6 text-3xl font-bold tracking-tight text-gray-900 dark:text-white">Planify</h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Entre com sua conta para acessar o sistema
        </p>
      </div>
      
      <div class="mt-8 rounded-lg border border-gray-200 bg-white p-6 shadow-md dark:border-gray-800 dark:bg-gray-800">
        <form class="space-y-6" @submit.prevent="login">
          <div v-if="error" class="rounded-md bg-red-50 p-4 dark:bg-red-900/30">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-5 w-5 text-red-400 dark:text-red-300">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" x2="12" y1="8" y2="12"></line>
                  <line x1="12" x2="12.01" y1="16" y2="16"></line>
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800 dark:text-red-200">Erro de autenticação</h3>
                <div class="mt-2 text-sm text-red-700 dark:text-red-300">
                  <p>{{ error }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Nome de usuário
            </label>
            <div class="mt-1">
              <input
                id="username"
                v-model="formData.username"
                name="username"
                type="text"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white sm:text-sm"
                :disabled="loading"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Senha
            </label>
            <div class="mt-1">
              <input
                id="password"
                v-model="formData.password"
                name="password"
                type="password"
                required
                class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white sm:text-sm"
                :disabled="loading"
              />
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="formData.rememberMe"
                name="remember-me"
                type="checkbox"
                class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900"
                :disabled="loading"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Lembrar-me
              </label>
            </div>

            <div class="text-sm">
              <NuxtLink to="/esqueci-senha" class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300">
                Esqueceu sua senha?
              </NuxtLink>
            </div>
          </div>

          <div>
            <button
              type="submit"
              class="flex w-full justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-700 dark:hover:bg-blue-600"
              :disabled="loading"
            >
              <svg v-if="loading" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4 animate-spin">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
              </svg>
              {{ loading ? 'Entrando...' : 'Entrar' }}
            </button>
          </div>
        </form>
      </div>
      
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Não tem uma conta?
          <NuxtLink to="/registro" class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300">
            Registre-se
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useNuxtApp } from '#app'

const router = useRouter()
const { $api } = useNuxtApp()

const loading = ref(false)
const error = ref('')

const formData = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const login = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await $api.post('/api/auth/token/', {
      username: formData.username,
      password: formData.password
    })
    
    // Armazenar o token no localStorage
    localStorage.setItem('auth_token', response.data.access)
    
    // Se houver refresh token, armazenar também
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh)
    }
    
    // Redirecionar para o dashboard
    router.push('/dashboard')
  } catch (err) {
    console.error('Erro ao fazer login:', err)
    
    if (err.response) {
      if (err.response.status === 401) {
        error.value = 'Nome de usuário ou senha incorretos.'
      } else if (err.response.data?.detail) {
        error.value = err.response.data.detail
      } else {
        error.value = 'Erro ao fazer login. Por favor, tente novamente.'
      }
    } else {
      error.value = 'Erro de conexão. Verifique sua internet e tente novamente.'
    }
  } finally {
    loading.value = false
  }
}
</script>
