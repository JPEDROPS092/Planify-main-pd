import { Icon } from '@iconify/vue'

export default defineNuxtPlugin((nuxtApp) => {
  // Register Iconify Icon component globally
  nuxtApp.vueApp.component('Icon', Icon)
})
