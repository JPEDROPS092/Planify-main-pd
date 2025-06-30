<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <div class="flex justify-center">
          <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
            <Icon name="lucide:layout-dashboard" class="w-8 h-8 text-white" />
          </div>
        </div>
        <h2 class="mt-6 text-center text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Planify
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Crie sua conta gratuitamente
        </p>
      </div>
      
      <div class="bg-white py-8 px-6 shadow-xl rounded-xl border border-gray-100">
        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Nome e Sobrenome -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">
                Nome *
              </label>
              <input
                id="firstName"
                v-model="form.firstName"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Seu nome"
              />
            </div>
            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">
                Sobrenome *
              </label>
              <input
                id="lastName"
                v-model="form.lastName"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Seu sobrenome"
              />
            </div>
          </div>

          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-1">
              Nome de usuário *
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="Nome de usuário único"
            />
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
              E-mail *
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              placeholder="seu@email.com"
            />
          </div>

          <!-- Senha -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1">
              Senha *
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="Mínimo 8 caracteres"
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

          <!-- Confirmar Senha -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1">
              Confirmar Senha *
            </label>
            <div class="relative">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                class="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                :class="{ 'border-red-300': form.confirmPassword && form.password !== form.confirmPassword }"
                placeholder="Confirme sua senha"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <Icon :name="showConfirmPassword ? 'lucide:eye-off' : 'lucide:eye'" class="w-5 h-5" />
              </button>
            </div>
            <p v-if="form.confirmPassword && form.password !== form.confirmPassword" 
               class="mt-1 text-sm text-red-600">
              As senhas não coincidem
            </p>
          </div>

          <!-- Termos e Condições -->
          <div class="flex items-start">
            <input
              id="acceptTerms"
              v-model="form.acceptTerms"
              type="checkbox"
              required
              class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="acceptTerms" class="ml-2 block text-sm text-gray-700">
              Eu aceito os 
              <a href="#" class="text-blue-600 hover:text-blue-500 underline">
                Termos de Uso
              </a>
              e a
              <a href="#" class="text-blue-600 hover:text-blue-500 underline">
                Política de Privacidade
              </a>
            </label>
          </div>

          <!-- Botão de Registro -->
          <button
            type="submit"
            :disabled="!isFormValid || isRegistering"
            class="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <Icon v-if="isRegistering" name="lucide:loader-2" class="w-4 h-4 mr-2 animate-spin" />
            {{ isRegistering ? 'Criando conta...' : 'Criar Conta' }}
          </button>
        </form>

        <!-- Link para Login -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Já tem uma conta?
            <NuxtLink to="/login" class="text-blue-600 hover:text-blue-500 font-medium">
              Fazer login
            </NuxtLink>
          </p>
        </div>
      </div>

      <div class="text-center">
        <NuxtLink to="/" class="text-sm text-gray-500 hover:text-gray-700">
          ← Voltar ao início
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Por enquanto, vou criar uma versão simplificada até resolver os composables
const isRegistering = ref(false)

const showToast = (message: string, type: 'success' | 'error' = 'success') => {
  // Implementação temporária de toast
  alert(`${type.toUpperCase()}: ${message}`)
}

// State
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = ref({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
})

// Computed
const isFormValid = computed(() => {
  return form.value.username &&
         form.value.email &&
         form.value.firstName &&
         form.value.lastName &&
         form.value.password &&
         form.value.password === form.value.confirmPassword &&
         form.value.acceptTerms &&
         form.value.password.length >= 8
})

// Methods
const handleRegister = async () => {
  if (!isFormValid.value) return
  
  isRegistering.value = true
  
  try {
    // Simulação de registro por enquanto
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showToast('Conta criada com sucesso! Agora você pode fazer login.', 'success')
    
    // Redirecionar para login após registro bem-sucedido
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
  } catch (error) {
    showToast('Erro ao criar conta. Tente novamente.', 'error')
    console.error('Registration failed:', error)
  } finally {
    isRegistering.value = false
  }
}
</script>

