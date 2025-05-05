<template>
  <div class="container flex h-screen w-screen flex-col items-center justify-center">
    <div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
      <div class="flex flex-col space-y-2 text-center">
        <h1 class="text-2xl font-semibold tracking-tight">Entrar no Planify</h1>
        <p class="text-sm text-muted-foreground">
          Digite suas credenciais para acessar o sistema
        </p>
      </div>
      <div class="grid gap-6">
        <form @submit.prevent="handleLogin">
          <div class="grid gap-4">
            <div class="grid gap-2">
              <label for="email" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                Email
              </label>
              <input
                id="email"
                v-model="email"
                type="email"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                placeholder="nome@exemplo.com"
                required
              />
            </div>
            <div class="grid gap-2">
              <div class="flex items-center justify-between">
                <label for="password" class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  Senha
                </label>
                <NuxtLink to="/esqueci-senha" class="text-sm text-primary underline-offset-4 hover:underline">
                  Esqueceu a senha?
                </NuxtLink>
              </div>
              <input
                id="password"
                v-model="password"
                type="password"
                class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                required
              />
            </div>
            <Button type="submit" :disabled="isLoading">
              {{ isLoading ? 'Entrando...' : 'Entrar' }}
            </Button>
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
          Não tem uma conta?
          <NuxtLink to="/registro" class="text-primary underline-offset-4 hover:underline">
            Registre-se
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const response = await axios.post('http://localhost:8001/api/auth/token/', {
      email: email.value,
      password: password.value
    })
    
    if (response.data.access) {
      // Salvar o token no localStorage
      localStorage.setItem('auth_token', response.data.access)
      
      // Redirecionar para a página inicial
      window.location.href = '/projetos'
    }
  } catch (err) {
    console.error('Erro ao fazer login:', err)
    error.value = 'Credenciais inválidas. Por favor, tente novamente.'
  } finally {
    isLoading.value = false
  }
}
</script>
