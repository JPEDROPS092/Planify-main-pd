<template>
  <Teleport to="body">
    <div
      class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm"
      v-if="toasts.length > 0"
    >
      <TransitionGroup
        name="toast"
        tag="div"
        class="flex flex-col gap-2"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'rounded-lg border p-4 shadow-lg backdrop-blur-sm',
            'transform transition-all duration-300 ease-in-out',
            getToastClasses(toast.type)
          ]"
        >
          <div class="flex items-start gap-3">
            <!-- Ícone do toast -->
            <div class="flex-shrink-0 mt-0.5">
              <Icon
                :name="getToastIcon(toast.type)"
                :class="[
                  'w-5 h-5',
                  getToastIconClasses(toast.type)
                ]"
              />
            </div>

            <!-- Conteúdo do toast -->
            <div class="flex-1 min-w-0">
              <h4 class="text-sm font-medium">
                {{ toast.title }}
              </h4>
              <p
                v-if="toast.description"
                class="text-sm opacity-90 mt-1"
              >
                {{ toast.description }}
              </p>
            </div>

            <!-- Botão de fechar -->
            <button
              @click="dismissToast(toast.id)"
              class="flex-shrink-0 rounded-md p-1 hover:bg-black/10 transition-colors"
              type="button"
            >
              <Icon name="lucide:x" class="w-4 h-4" />
              <span class="sr-only">Fechar</span>
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { useToast, type Toast } from '~/composables/useToast'

const { toasts, dismissToast } = useToast()

function getToastClasses(type: Toast['type']): string {
  const baseClasses = 'border-l-4'
  
  switch (type) {
    case 'success':
      return `${baseClasses} bg-green-50 border-green-500 text-green-800`
    case 'error':
      return `${baseClasses} bg-red-50 border-red-500 text-red-800`
    case 'warning':
      return `${baseClasses} bg-yellow-50 border-yellow-500 text-yellow-800`
    case 'info':
      return `${baseClasses} bg-blue-50 border-blue-500 text-blue-800`
    default:
      return `${baseClasses} bg-gray-50 border-gray-500 text-gray-800`
  }
}

function getToastIcon(type: Toast['type']): string {
  switch (type) {
    case 'success':
      return 'lucide:check-circle'
    case 'error':
      return 'lucide:x-circle'
    case 'warning':
      return 'lucide:alert-triangle'
    case 'info':
      return 'lucide:info'
    default:
      return 'lucide:bell'
  }
}

function getToastIconClasses(type: Toast['type']): string {
  switch (type) {
    case 'success':
      return 'text-green-600'
    case 'error':
      return 'text-red-600'
    case 'warning':
      return 'text-yellow-600'
    case 'info':
      return 'text-blue-600'
    default:
      return 'text-gray-600'
  }
}
</script>

<style scoped>
/* Animações dos toasts */
.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.3s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>
