<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-900">Criar Conta</h2>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="register" class="space-y-4">
          <!-- Basic Info -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Nome *
              </label>
              <input
                v-model="form.firstName"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Seu nome"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Sobrenome *
              </label>
              <input
                v-model="form.lastName"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Seu sobrenome"
              />
            </div>
          </div>

          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Username *
            </label>
            <input
              v-model="form.username"
              type="text"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Escolha um username"
            />
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Email *
            </label>
            <input
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="seu@email.com"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Senha *
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Sua senha"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464M9.878 9.878l-1.415-1.414m4.242 4.242l1.415 1.414M14.12 14.12l1.415 1.415" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Confirmar Senha *
            </label>
            <div class="relative">
              <input
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                class="w-full px-3 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Confirme sua senha"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showConfirmPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464M9.878 9.878l-1.415-1.414m4.242 4.242l1.415 1.414M14.12 14.12l1.415 1.415" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Role -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Função
            </label>
            <select
              v-model="form.role"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="USER">Usuário</option>
              <option value="MANAGER">Gerente</option>
              <option value="ADMIN">Administrador</option>
            </select>
          </div>

          <!-- Profile Section -->
          <div class="space-y-3">
            <h3 class="text-lg font-medium text-gray-900">Perfil Profissional</h3>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Cargo
              </label>
              <input
                v-model="form.profile.cargo"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Seu cargo atual"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Departamento
              </label>
              <input
                v-model="form.profile.departamento"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Seu departamento"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Telefone
              </label>
              <input
                v-model="form.profile.telefone"
                type="tel"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="(11) 99999-9999"
              />
            </div>
          </div>

          <!-- Preferences -->
          <div class="space-y-3">
            <h3 class="text-lg font-medium text-gray-900">Preferências</h3>
            
            <div class="space-y-2">
              <label class="flex items-center">
                <input
                  v-model="form.profile.preferencias.notificacoes_email"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-sm text-gray-700">Receber notificações por email</span>
              </label>
              
              <label class="flex items-center">
                <input
                  v-model="form.profile.preferencias.notificacoes_push"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-sm text-gray-700">Receber notificações push</span>
              </label>
              
              <label class="flex items-center">
                <input
                  v-model="form.profile.preferencias.tema_escuro"
                  type="checkbox"
                  class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span class="ml-2 text-sm text-gray-700">Usar tema escuro</span>
              </label>
            </div>
          </div>

          <!-- Terms -->
          <div>
            <label class="flex items-start">
              <input
                v-model="form.acceptTerms"
                type="checkbox"
                required
                class="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span class="ml-2 text-sm text-gray-700">
                Eu aceito os 
                <a href="#" class="text-blue-600 hover:underline">Termos de Uso</a> 
                e a 
                <a href="#" class="text-blue-600 hover:underline">Política de Privacidade</a>
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-lg font-semibold transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <div v-if="loading" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            {{ loading ? 'Criando conta...' : 'Criar Conta' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">ou</span>
            </div>
          </div>
        </div>

        <!-- Switch to Login -->
        <div class="text-center">
          <p class="text-sm text-gray-600">
            Já tem uma conta?
            <button
              @click="switchToLogin"
              class="text-blue-600 hover:underline font-medium"
            >
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
import { useAuth } from '~/composables/useAuth'

const emit = defineEmits(['close', 'success', 'switch-to-login'])

const { $toast } = useNuxtApp()

// State
const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = ref({
  username: '',
  email: '',
  firstName: '',
  lastName: '',
  password: '',
  confirmPassword: '',
  role: 'USER',
  acceptTerms: false,
  profile: {
    cargo: '',
    departamento: '',
    telefone: '',
    preferencias: {
      notificacoes_email: true,
      notificacoes_push: true,
      tema_escuro: false
    }
  }
})

// Computed
const isFormValid = computed(() => {
  return form.value.username &&
         form.value.email &&
         form.value.firstName &&
         form.value.lastName &&
         form.value.password &&
         form.value.password === form.value.confirmPassword &&
         form.value.acceptTerms
})

// Methods
const register = async () => {
  if (!isFormValid.value) return
  
  loading.value = true
  
  try {
    const registerData = {
      username: form.value.username,
      email: form.value.email,
      full_name: `${form.value.firstName} ${form.value.lastName}`.trim(),
      password: form.value.password,
      role: form.value.role,
      profile: {
        phone: form.value.profile.telefone || '',
        profile_picture: '',
        theme_preference: form.value.profile.preferencias.tema_escuro ? 'DARK' : 'LIGHT',
        email_notifications: form.value.profile.preferencias.notificacoes_email,
        system_notifications: form.value.profile.preferencias.notificacoes_push
      }
    }

    console.log('Dados de registro:', registerData) // Para debug
    
    // Use useAuth register function
    const { register: authRegister } = useAuth()
    await authRegister(registerData)
    
    $toast.success('Conta criada com sucesso! Você pode fazer login agora.')
    emit('success')
  } catch (err: any) {
    console.error('Registration error:', err)
    
    // Handle different types of errors
    if (err?.response?.data) {
      const errorData = err.response.data
      console.log('Error data:', errorData) // Para debug
      
      if (errorData.username) {
        $toast.error(`Username: ${Array.isArray(errorData.username) ? errorData.username.join(', ') : errorData.username}`)
      } else if (errorData.email) {
        $toast.error(`Email: ${Array.isArray(errorData.email) ? errorData.email.join(', ') : errorData.email}`)
      } else if (errorData.password) {
        $toast.error(`Senha: ${Array.isArray(errorData.password) ? errorData.password.join(', ') : errorData.password}`)
      } else if (errorData.role) {
        $toast.error(`Role: ${Array.isArray(errorData.role) ? errorData.role.join(', ') : errorData.role}`)
      } else if (errorData.profile) {
        $toast.error(`Profile: ${JSON.stringify(errorData.profile)}`)
      } else if (errorData.detail || errorData.message) {
        $toast.error(errorData.detail || errorData.message)
      } else {
        $toast.error(`Erro ao criar conta: ${JSON.stringify(errorData)}`)
      }
    } else {
      $toast.error('Erro ao criar conta. Tente novamente.')
    }
  } finally {
    loading.value = false
  }
}

const switchToLogin = () => {
  emit('close')
  nextTick(() => {
    emit('switch-to-login')
  })
}
</script>
