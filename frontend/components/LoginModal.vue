<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-96 shadow-lg rounded-xl bg-white">
      <div class="mt-3">
        <!-- Header -->
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-2xl font-bold text-gray-900">Entrar</h3>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <Icon name="heroicons:x-mark" class="w-6 h-6" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="login" class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Email ou Username
            </label>
            <input
              v-model="form.username"
              type="text"
              required
              class="w-full border border-gray-300 rounded-lg px-3 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Digite seu email ou username"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Senha
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full border border-gray-300 rounded-lg px-3 py-3 pr-10 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Digite sua senha"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <Icon
                  :name="showPassword ? 'heroicons:eye-slash' : 'heroicons:eye'"
                  class="w-5 h-5 text-gray-400"
                />
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                v-model="form.remember"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label class="ml-2 block text-sm text-gray-700">
                Lembrar de mim
              </label>
            </div>
            <a href="#" class="text-sm text-blue-600 hover:text-blue-700">
              Esqueceu a senha?
            </a>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 rounded-lg font-semibold transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            <div v-if="loading" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">Não tem uma conta?</span>
            </div>
          </div>
        </div>

        <!-- Register Link -->
        <button
          @click="switchToRegister"
          class="w-full border border-gray-300 hover:border-blue-300 text-gray-700 hover:text-blue-600 py-3 rounded-lg font-semibold transition-all"
        >
          Criar Nova Conta
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits(['close', 'success', 'switch-to-register'])

const { $toast } = useNuxtApp()
const { login: authLogin } = useAuth()

// State
const loading = ref(false)
const showPassword = ref(false)

const form = ref({
  username: '',
  password: '',
  remember: false
})

// Methods
const login = async () => {
  try {
    loading.value = true
    
    await authLogin(form.value.username, form.value.password)
    
    $toast.success('Login realizado com sucesso!')
    emit('success')
  } catch (err: any) {
    $toast.error('Credenciais inválidas')
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}

const switchToRegister = () => {
  emit('close')
  nextTick(() => {
    emit('switch-to-register')
  })
}
</script>
