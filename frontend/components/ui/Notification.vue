<template>
  <Teleport to="body">
    <Transition name="fade">
      <div 
        v-if="isVisible" 
        :class="[
          'fixed z-50 p-4 rounded-lg shadow-lg max-w-md',
          'top-4 right-4 transition-all duration-300 ease-in-out',
          typeClasses[type]
        ]"
      >
        <div class="flex items-start">
          <div class="flex-shrink-0 mr-3">
            <component :is="icons[type]" class="w-5 h-5" />
          </div>
          <div class="flex-1">
            <h3 v-if="title" class="text-sm font-medium">{{ title }}</h3>
            <div class="mt-1 text-sm">{{ message }}</div>
          </div>
          <button 
            @click="close" 
            class="ml-4 flex-shrink-0 inline-flex text-gray-400 hover:text-gray-500 focus:outline-none"
          >
            <span class="sr-only">Fechar</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, defineComponent, h } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value: string) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  message: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 5000 // 5 segundos por padrão
  },
  autoClose: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['close'])

const isVisible = ref(false)
let timer: NodeJS.Timeout | null = null

// Classes CSS baseadas no tipo de notificação
const typeClasses = {
  success: 'bg-green-50 text-green-800 border border-green-200',
  error: 'bg-red-50 text-red-800 border border-red-200',
  warning: 'bg-yellow-50 text-yellow-800 border border-yellow-200',
  info: 'bg-blue-50 text-blue-800 border border-blue-200'
}

// Ícones para cada tipo de notificação
const icons = {
  success: defineComponent({
    render: () => h('svg', { 
      xmlns: 'http://www.w3.org/2000/svg', 
      viewBox: '0 0 20 20', 
      fill: 'currentColor',
      class: 'text-green-500'
    }, [
      h('path', { 
        'fill-rule': 'evenodd', 
        d: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z', 
        'clip-rule': 'evenodd' 
      })
    ])
  }),
  error: defineComponent({
    render: () => h('svg', { 
      xmlns: 'http://www.w3.org/2000/svg', 
      viewBox: '0 0 20 20', 
      fill: 'currentColor',
      class: 'text-red-500'
    }, [
      h('path', { 
        'fill-rule': 'evenodd', 
        d: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z', 
        'clip-rule': 'evenodd' 
      })
    ])
  }),
  warning: defineComponent({
    render: () => h('svg', { 
      xmlns: 'http://www.w3.org/2000/svg', 
      viewBox: '0 0 20 20', 
      fill: 'currentColor',
      class: 'text-yellow-500'
    }, [
      h('path', { 
        'fill-rule': 'evenodd', 
        d: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z', 
        'clip-rule': 'evenodd' 
      })
    ])
  }),
  info: defineComponent({
    render: () => h('svg', { 
      xmlns: 'http://www.w3.org/2000/svg', 
      viewBox: '0 0 20 20', 
      fill: 'currentColor',
      class: 'text-blue-500'
    }, [
      h('path', { 
        'fill-rule': 'evenodd', 
        d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2h-1V9a1 1 0 00-1-1z', 
        'clip-rule': 'evenodd' 
      })
    ])
  })
}

// Mostrar a notificação
onMounted(() => {
  isVisible.value = true
  
  // Configurar timer para fechar automaticamente
  if (props.autoClose && props.duration > 0) {
    timer = setTimeout(() => {
      close()
    }, props.duration)
  }
})

// Limpar o timer quando o componente for desmontado
onUnmounted(() => {
  if (timer) {
    clearTimeout(timer)
  }
})

// Fechar a notificação
function close() {
  isVisible.value = false
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
  setTimeout(() => {
    emit('close')
  }, 300) // Tempo para a animação de saída
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
