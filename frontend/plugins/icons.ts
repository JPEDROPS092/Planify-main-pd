/**
 * Plugin para integração de ícones Phosphor com o Nuxt
 * Registra os componentes de ícones globalmente na aplicação
 */
import { defineNuxtPlugin } from '#app'
import * as PhosphorIcons from '@phosphor-icons/vue'

export default defineNuxtPlugin((nuxtApp) => {
  // Registrar todos os ícones do pacote Phosphor Icons
  Object.entries(PhosphorIcons).forEach(([name, component]) => {
    // Registrar com o nome original
    nuxtApp.vueApp.component(name, component)
    
    // Também registrar com o prefixo Ph para compatibilidade retroativa
    nuxtApp.vueApp.component(`Ph${name}`, component)
  })
  
  console.log('Phosphor Icons carregados globalmente')
})