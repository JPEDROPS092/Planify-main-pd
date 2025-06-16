// components/NotificationToaster.vue
<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 space-y-2">
      <TransitionGroup
        name="notification"
        tag="div"
        class="space-y-2"
      >
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto',
            'ring-1 ring-black ring-opacity-5 overflow-hidden',
            'transform transition-all duration-300 ease-in-out',
          ]"
        >
          <div class="p-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <Icon
                  :name="getIcon(notification.type)"
                  :class="getIconClass(notification.type)"
                  class="w-5 h-5"
                />
              </div>
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p
                  v-if="notification.title"
                  class="text-sm font-medium text-gray-900"
                >
                  {{ notification.title }}
                </p>
                <p class="text-sm text-gray-500">
                  {{ notification.message }}
                </p>
              </div>
              <div class="ml-4 flex-shrink-0 flex">
                <button
                  @click="removeNotification(notification.id)"
                  class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <span class="sr-only">Fechar</span>
                  <Icon name="heroicons:x-mark" class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useGlobalNotification } from '../composables/useNotification';

const { notifications, removeNotification } = useGlobalNotification();

const getIcon = (type: string) => {
  switch (type) {
    case 'success':
      return 'heroicons:check-circle';
    case 'error':
      return 'heroicons:x-circle';
    case 'warning':
      return 'heroicons:exclamation-triangle';
    case 'info':
    default:
      return 'heroicons:information-circle';
  }
};

const getIconClass = (type: string) => {
  switch (type) {
    case 'success':
      return 'text-green-400';
    case 'error':
      return 'text-red-400';
    case 'warning':
      return 'text-yellow-400';
    case 'info':
    default:
      return 'text-blue-400';
  }
};
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>
