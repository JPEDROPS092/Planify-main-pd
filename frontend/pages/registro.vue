<template>
  <div class="container flex h-screen w-screen flex-col items-center justify-center">
    <div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[400px]">
      <div class="flex flex-col space-y-2 text-center">
        <h1 class="text-2xl font-semibold tracking-tight">Criar uma conta</h1>
        <p class="text-sm text-muted-foreground">
          Preencha os dados abaixo para se registrar no Planify
        </p>
      </div>
      <div class="grid gap-6">
        <form @submit.prevent="handleRegistro">
          <div class="grid gap-4">
            <div class="grid gap-2">
              <label for="username" class="text-sm font-medium leading-none">
                Nome de usuário
              </label>
              <input
                id="username"
                v-model="formData.username"
                type="text"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                placeholder="seu_usuario"
                required
              />
            </div>
            <div class="grid gap-2">
              <label for="email" class="text-sm font-medium leading-none">
                Email
              </label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                placeholder="nome@exemplo.com"
                required
              />
            </div>
            <div class="grid gap-2">
              <label for="full_name" class="text-sm font-medium leading-none">
                Nome completo
              </label>
              <input
                id="full_name"
                v-model="formData.full_name"
                type="text"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                placeholder="Seu Nome Completo"
                required
              />
            </div>
            <div class="grid gap-2">
              <label for="password" class="text-sm font-medium leading-none">
                Senha
              </label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                required
              />
            </div>
            <div class="grid gap-2">
              <label for="re_password" class="text-sm font-medium leading-none">
                Confirmar senha
              </label>
              <input
                id="re_password"
                v-model="formData.re_password"
                type="password"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                required
              />
            </div>
            <button 
              type="submit" 
              class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Registrando...' : 'Registrar' }}
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
          Já tem uma conta?
          <NuxtLink to="/login" class="text-primary underline-offset-4 hover:underline">
            Faça login
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const { $api } = useNuxtApp()
const isLoading = ref(false)
const error = ref('')

const formData = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
  re_password: ''
})

const handleRegistro = async () => {
  // Validar se as senhas coincidem
  if (formData.password !== formData.re_password) {
    error.value = 'As senhas não coincidem'
    return
  }

  isLoading.value = true
  error.value = ''
  
  try {
    await $api.post('/api/auth/users/', {
      username: formData.username,
      email: formData.email,
      full_name: formData.full_name,
      password: formData.password,
      re_password: formData.re_password
    })
    
    // Redirecionar para a página de login com mensagem de sucesso
    navigateTo('/login?registered=true')
  } catch (err: any) {
    console.error('Erro ao registrar:', err)
    
    // Exibir mensagens de erro específicas da API
    if (err.response && err.response.data) {
      const errorData = err.response.data
      if (typeof errorData === 'object') {
        const errorMessages = Object.entries(errorData)
          .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
          .join('; ')
        error.value = errorMessages
      } else {
        error.value = 'Erro ao criar conta. Por favor, tente novamente.'
      }
    } else {
      error.value = 'Erro ao criar conta. Por favor, tente novamente.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
