<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="modelValue" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex min-h-screen items-end justify-center px-4 pt-4 pb-20 text-center sm:block sm:p-0">
          <!-- Overlay de fundo -->
          <div 
            class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity dark:bg-gray-800 dark:bg-opacity-75" 
            aria-hidden="true"
            @click="closeOnBackdrop && $emit('update:modelValue', false)"
          ></div>

          <!-- Truque para centralizar o modal verticalmente -->
          <span class="hidden sm:inline-block sm:h-screen sm:align-middle" aria-hidden="true">&#8203;</span>

          <!-- Modal -->
          <Transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div 
              v-if="modelValue" 
              :class="[
                'inline-block transform overflow-hidden rounded-lg bg-white text-left align-bottom shadow-xl transition-all dark:bg-gray-900 sm:my-8 sm:align-middle',
                size === 'sm' ? 'sm:max-w-lg' : '',
                size === 'md' ? 'sm:max-w-2xl' : '',
                size === 'lg' ? 'sm:max-w-4xl' : '',
                size === 'xl' ? 'sm:max-w-6xl' : '',
                size === 'full' ? 'sm:max-w-full' : '',
                fullHeight ? 'sm:h-[calc(100vh-8rem)]' : ''
              ]"
            >
              <!-- Cabeçalho do Modal -->
              <div class="flex items-center justify-between border-b border-gray-200 px-6 py-4 dark:border-gray-700">
                <h3 class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ title }}
                </h3>
                <button
                  type="button"
                  class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-gray-900 dark:text-gray-500 dark:hover:text-gray-400"
                  @click="$emit('update:modelValue', false)"
                >
                  <span class="sr-only">Fechar</span>
                  <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <!-- Conteúdo do Modal -->
              <div :class="['px-6 py-4', fullHeight ? 'overflow-y-auto' : '']" :style="fullHeight ? 'max-height: calc(100vh - 14rem);' : ''">
                <slot></slot>
              </div>

              <!-- Rodapé do Modal (opcional) -->
              <div v-if="$slots.footer" class="border-t border-gray-200 px-6 py-4 dark:border-gray-700">
                <slot name="footer"></slot>
              </div>
            </div>
          </Transition>
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
      default: 'Modal'
    },
    size: {
      type: String,
      default: 'md',
      validator: (value: string) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
    },
    fullHeight: {
      type: Boolean,
      default: false
    },
    closeOnBackdrop: {
      type: Boolean,
      default: true
    }
  },
  emits: ['update:modelValue'],
  setup() {
    return {}
  }
})
</script>
