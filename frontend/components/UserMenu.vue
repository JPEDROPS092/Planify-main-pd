<template>
  <div class="ml-3 relative">
    <div>
      <button @click="isOpen = !isOpen" type="button" class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary" id="user-menu-button" aria-expanded="false" aria-haspopup="true">
        <span class="sr-only">Abrir menu do usuário</span>
        <div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-600">
          <Icon v-if="!user?.avatar" icon="lucide:user" class="h-5 w-5" />
          <img v-else :src="user.avatar" alt="Avatar do usuário" class="h-8 w-8 rounded-full" />
        </div>
      </button>
    </div>
    
    <div v-if="isOpen" @click.outside="isOpen = false" class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="user-menu-button" tabindex="-1">
      <div class="px-4 py-2 border-b border-gray-100">
        <p class="text-sm font-medium text-gray-900">{{ user?.nome || 'Usuário' }}</p>
        <p class="text-xs text-gray-500">{{ user?.email || '' }}</p>
      </div>
      <NuxtLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem" tabindex="-1" id="user-menu-item-0">Perfil</NuxtLink>
      <NuxtLink to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem" tabindex="-1" id="user-menu-item-1">Configurações</NuxtLink>
      <button @click="logout" class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem" tabindex="-1" id="user-menu-item-2">Sair</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue';
import { useAuth } from '~/composables/useAuth';
import { useToast } from '~/composables/useToast';

const isOpen = ref(false);
const router = useRouter();
const { user, logout: authLogout } = useAuth();
const { toast } = useToast();

const logout = async () => {
  try {
    await authLogout();
    isOpen.value = false;
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

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
