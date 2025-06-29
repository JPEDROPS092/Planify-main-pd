<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
    <div class="relative bg-white rounded-xl shadow-2xl max-w-md w-full mx-4 transform transition-all">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-semibold text-gray-900">Entrar</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition-colors">
            <Icon name="lucide:x" class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- Body -->
      <div class="px-6 py-6">
        <!-- Logo -->
        <div class="text-center mb-6">
          <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-4">
            <Icon name="lucide:layout-dashboard" class="w-8 h-8 text-white" />
          </div>
          <h2 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Planify
          </h2>
          <p class="text-gray-600 text-sm">Gerencie seus projetos com inteligência</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              Nome de usuário
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Seu nome de usuário"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Senha
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Sua senha"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <Icon :name="showPassword ? 'lucide:eye-off' : 'lucide:eye'" class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Remember me -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember"
                v-model="form.remember"
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

          <!-- Login Button -->
          <button
            type="submit"
            :disabled="isLoggingIn || !form.username || !form.password"
            class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <Icon v-if="isLoggingIn" name="lucide:loader-2" class="w-4 h-4 mr-2 animate-spin" />
            {{ isLoggingIn ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <!-- Link para Registro -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Não tem uma conta?
            <button @click="switchToRegister" class="text-blue-600 hover:text-blue-500 font-medium">
              Criar conta grátis
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

const emit = defineEmits(['close', 'success', 'switch-to-register'])

// Usar o composable de autenticação
const { login, isLoggingIn } = useAuth()

// State
const form = ref({
  username: '',
  password: '',
  remember: false
})

const showPassword = ref(false)

// Methods
const handleLogin = async () => {
  if (!form.value.username || !form.value.password) return
  
  try {
    await login({
      username: form.value.username,
      password: form.value.password
    })
    
    emit('success')
    
    // Redirecionar para dashboard após login bem-sucedido
    await nextTick()
    await navigateTo('/dashboard')
  } catch (error) {
    // Erro já tratado no composable useAuth
    console.error('Login failed:', error)
  }
}

const switchToRegister = () => {
  emit('close')
  nextTick(() => {
    emit('switch-to-register')
  })
}
</script>