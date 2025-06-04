<template>
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-b from-slate-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
    <div class="w-full max-w-md p-8 space-y-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg">
      <div class="text-center">
        <img src="/img/logop.png" alt="Planify Logo" class="h-12 mx-auto" />
        <h1 class="mt-4 text-2xl font-bold text-gray-900 dark:text-white">Entrar no Planify</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Acesse sua conta para gerenciar seus projetos</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
            <input v-model="email" id="email" type="email" required class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Senha</label>
            <input v-model="password" id="password" type="password" required class="mt-1 block w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500" />
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" type="checkbox" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">Lembrar-me</label>
          </div>
          
          <div class="text-sm">
            <NuxtLink to="/auth/esqueci-senha" class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400">
              Esqueceu sua senha?
            </NuxtLink>
          </div>
        </div>
        
        <div>
          <button type="submit" :disabled="loading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            <span v-if="loading">Entrando...</span>
            <span v-else>Entrar</span>
          </button>
        </div>
      </form>
      
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Não tem uma conta? 
          <NuxtLink to="/auth/registro" class="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400">
            Registre-se
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '~/stores/composables/useAuth'
import { useNotification } from '~/stores/composables/useNotification'

definePageMeta({
  layout: 'auth',
  middleware: ['guest-only']
})

const router = useRouter()
const route = useRoute()
const { login } = useAuth()
const { error: showError, success: showSuccess } = useNotification()

const email = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  
  try {
    await login(email.value, password.value)
    
    // Redirecionamento após login bem-sucedido
    const redirectPath = route.query.redirect || '/dashboard'
    router.push(redirectPath)
    
    showSuccess('Login realizado com sucesso!')
  } catch (err) {
    console.error('Erro ao fazer login:', err)
    showError(err?.response?.data?.detail || 'Falha na autenticação. Verifique suas credenciais.')
  } finally {
    loading.value = false
  }
}
</script>