<template>
  <div class="fixed right-4 top-4 z-50 flex flex-col space-y-2">
    <transition-group name="notification">
      <div 
        v-for="notification in notifications" 
        :key="notification.id" 
        :class="[
          'flex w-96 items-center rounded-lg shadow-lg',
          getBackgroundClass(notification.type)
        ]"
      >
        <!-- Ícone -->
        <div class="flex h-12 w-12 flex-shrink-0 items-center justify-center">
          <svg v-if="notification.type === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="notification.type === 'error'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else-if="notification.type === 'warning'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <svg v-else-if="notification.type === 'info'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else-if="notification.type === 'loading'" class="h-6 w-6 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        
        <!-- Conteúdo -->
        <div class="flex-1 p-4">
          <div class="flex items-start justify-between">
            <p class="text-sm font-medium text-gray-900 dark:text-white">
              {{ notification.message }}
            </p>
            <button 
              @click="removeNotification(notification.id)" 
              class="ml-4 inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <span class="sr-only">Fechar</span>
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useNotification } from '~/composables/useNotification';

const { notifications, removeNotification } = useNotification();

// Obtém a classe de estilo com base no tipo de notificação
const getBackgroundClass = (type) => {
  switch (type) {
    case 'success':
      return 'bg-green-50 border-l-4 border-green-500 dark:bg-green-900/20 dark:border-green-500';
    case 'error':
      return 'bg-red-50 border-l-4 border-red-500 dark:bg-red-900/20 dark:border-red-500';
    case 'warning':
      return 'bg-yellow-50 border-l-4 border-yellow-500 dark:bg-yellow-900/20 dark:border-yellow-500';
    case 'info':
      return 'bg-blue-50 border-l-4 border-blue-500 dark:bg-blue-900/20 dark:border-blue-500';
    case 'loading':
      return 'bg-gray-50 border-l-4 border-gray-500 dark:bg-gray-900/20 dark:border-gray-500';
    default:
      return 'bg-gray-50 border-l-4 border-gray-500 dark:bg-gray-900/20 dark:border-gray-500';
  }
};
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  transform: translateX(30px);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(30px);
  opacity: 0;
}
</style>
