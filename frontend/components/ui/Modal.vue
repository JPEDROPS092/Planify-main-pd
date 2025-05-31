<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div 
        v-if="modelValue" 
        class="modal-backdrop"
        :class="{ 'modal-backdrop--fullheight': fullHeight }"
        @click="closeOnBackdrop && close()"
      >
        <div 
          class="modal-container"
          :class="{
            'modal-container--sm': size === 'sm',
            'modal-container--md': size === 'md',
            'modal-container--lg': size === 'lg',
            'modal-container--xl': size === 'xl',
            'modal-container--fullheight': fullHeight
          }"
          @click.stop
        >
          <div class="modal-header">
            <slot name="header">
              <h3 class="modal-title">{{ title }}</h3>
            </slot>
            <button 
              v-if="showCloseButton" 
              class="modal-close" 
              @click="close()"
              aria-label="Fechar"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div class="modal-body">
            <slot></slot>
          </div>
          
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Modal',
  
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md',
      validator: (value: string) => ['sm', 'md', 'lg', 'xl'].includes(value)
    },
    fullHeight: {
      type: Boolean,
      default: false
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    },
    showCloseButton: {
      type: Boolean,
      default: true
    }
  },
  
  emits: ['update:modelValue', 'close'],
  
  setup(props, { emit }) {
    // Função para fechar o modal
    const close = () => {
      emit('update:modelValue', false)
      emit('close')
    }
    
    return {
      close
    }
  }
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-backdrop--fullheight {
  padding: 0;
}

.modal-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 2rem);
  overflow: hidden;
}

.modal-container--fullheight {
  height: 100vh;
  max-height: 100vh;
  border-radius: 0;
}

.modal-container--sm {
  max-width: 24rem;
}

.modal-container--md {
  max-width: 32rem;
}

.modal-container--lg {
  max-width: 48rem;
}

.modal-container--xl {
  max-width: 64rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.modal-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary, #333);
}

.modal-close {
  background: transparent;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  color: var(--color-text-secondary, #666);
  transition: color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: var(--color-text-primary, #333);
}

.modal-close svg {
  width: 1.5rem;
  height: 1.5rem;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

/* Transições */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .modal-container,
.modal-fade-leave-active .modal-container {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.modal-fade-enter-from .modal-container,
.modal-fade-leave-to .modal-container {
  transform: translateY(20px);
  opacity: 0;
}

/* Tema escuro */
:root.dark .modal-container {
  background-color: var(--color-bg-secondary, #1e1e1e);
  color: var(--color-text-primary, #f0f0f0);
}

:root.dark .modal-header,
:root.dark .modal-footer {
  border-color: rgba(255, 255, 255, 0.1);
}
</style>
