<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center">
    <div class="relative bg-white rounded-xl shadow-2xl max-w-md w-full mx-4 transform transition-all">
      <!-- Header -->
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-semibold text-gray-900">Criar Conta</h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 transition-colors">
            <Icon name="lucide:x" class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- Body -->
      <div class="px-6 py-6">
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
            <button @click="switchToLogin" class="text-blue-600 hover:text-blue-500 font-medium">
              Fazer login
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'

const emit = defineEmits(['close', 'success', 'switch-to-login'])

// Usar o composable de autenticação
const { register, isRegistering } = useAuth()

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
  
  const registerData = {
    username: form.value.username,
    email: form.value.email,
    first_name: form.value.firstName,
    last_name: form.value.lastName,
    password: form.value.password
  }

  try {
    await register(registerData)
    emit('success')
  } catch (error) {
    // Erro já tratado no composable useAuth
    console.error('Registration failed:', error)
  }
}

const switchToLogin = () => {
  emit('close')
  nextTick(() => {
    emit('switch-to-login')
  })
}
</script>
