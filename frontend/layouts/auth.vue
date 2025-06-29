<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <!-- Header simples -->
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <NuxtLink to="/" class="flex justify-center">
        <Icon icon="lucide:layout-dashboard" class="w-12 h-12 text-blue-600" />
      </NuxtLink>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        {{ pageTitle }}
      </h2>
    </div>

    <!-- Conteúdo -->
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10 border border-gray-200">
        <slot />
      </div>
      
      <!-- Links auxiliares -->
      <div class="mt-6 text-center">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { Icon } from '@iconify/vue'

const route = useRoute()
const { isAuthenticated } = useAuth()

const pageTitle = computed(() => {
  const titles = {
    '/login': 'Faça login em sua conta',
    '/register': 'Crie sua conta'
  }
  return titles[route.path] || 'Autenticação'
})

// Verificar se usuário já está logado e redirecionar
onMounted(() => {
  if (isAuthenticated.value) {
    navigateTo('/dashboard')
  }
})
</script>
