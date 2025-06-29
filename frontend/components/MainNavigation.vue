<template>
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <NuxtLink to="/" class="flex items-center">
              <Icon icon="lucide:layout-dashboard" class="h-8 w-8 text-primary" />
              <span class="ml-2 text-xl font-bold text-gray-900">Planify</span>
            </NuxtLink>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <NuxtLink to="/" class="border-primary text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" :class="{ 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700': $route.path !== '/' }">
              Dashboard
            </NuxtLink>
            <NuxtLink to="/projects" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" :class="{ 'border-primary text-gray-900': $route.path.startsWith('/projects') }">
              Projetos
            </NuxtLink>
            <NuxtLink to="/tasks" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" :class="{ 'border-primary text-gray-900': $route.path.startsWith('/tasks') }">
              Tarefas
            </NuxtLink>
            <NuxtLink to="/teams" class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" :class="{ 'border-primary text-gray-900': $route.path.startsWith('/teams') }">
              Equipes
            </NuxtLink>
          </div>
        </div>
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <NotificationDropdown />
          <UserMenu />
        </div>
        <div class="-mr-2 flex items-center sm:hidden">
          <button @click="mobileMenuOpen = !mobileMenuOpen" type="button" class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary" aria-controls="mobile-menu" :aria-expanded="mobileMenuOpen">
            <span class="sr-only">Abrir menu principal</span>
            <Icon v-if="!mobileMenuOpen" icon="lucide:menu" class="block h-6 w-6" />
            <Icon v-else icon="lucide:x" class="block h-6 w-6" />
          </button>
        </div>
      </div>
    </div>

    <div v-show="mobileMenuOpen" class="sm:hidden" id="mobile-menu">
      <div class="pt-2 pb-3 space-y-1">
        <NuxtLink to="/" class="bg-primary-50 border-primary text-primary-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium" :class="{ 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700': $route.path !== '/' }">
          Dashboard
        </NuxtLink>
        <NuxtLink to="/projects" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium" :class="{ 'bg-primary-50 border-primary text-primary-700': $route.path.startsWith('/projects') }">
          Projetos
        </NuxtLink>
        <NuxtLink to="/tasks" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium" :class="{ 'bg-primary-50 border-primary text-primary-700': $route.path.startsWith('/tasks') }">
          Tarefas
        </NuxtLink>
        <NuxtLink to="/teams" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium" :class="{ 'bg-primary-50 border-primary text-primary-700': $route.path.startsWith('/teams') }">
          Equipes
        </NuxtLink>
      </div>
      <div class="pt-4 pb-3 border-t border-gray-200">
        <div class="flex items-center px-4">
          <div class="flex-shrink-0">
            <Icon icon="lucide:user" class="h-10 w-10 rounded-full bg-gray-200 p-2 text-gray-600" />
          </div>
          <div class="ml-3">
            <div class="text-base font-medium text-gray-800">{{ user?.nome || 'Usuário' }}</div>
            <div class="text-sm font-medium text-gray-500">{{ user?.email || '' }}</div>
          </div>
        </div>
        <div class="mt-3 space-y-1">
          <NuxtLink to="/profile" class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
            Perfil
          </NuxtLink>
          <NuxtLink to="/settings" class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
            Configurações
          </NuxtLink>
          <button @click="logout" class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100">
            Sair
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import { useAuth } from '~/composables/useAuth';
import { useToast } from '~/composables/useToast';

const mobileMenuOpen = ref(false);
const router = useRouter();
const { user, logout: authLogout } = useAuth();
const { toast } = useToast();

const logout = async () => {
  try {
    await authLogout();
    toast({
      title: 'Logout realizado com sucesso',
      description: 'Você foi desconectado do sistema'
    });
    router.push('/login');
  } catch (error) {
    toast({
      title: 'Erro ao fazer logout',
      description: error.message,
      variant: 'destructive'
    });
  }
};
</script>
