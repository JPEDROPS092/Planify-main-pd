<template>
  <Icon 
    v-if="icon" 
    :icon="icon" 
    :class="className"
    v-bind="$attrs"
  />
  <component 
    v-else-if="name" 
    :is="getIconComponent(name)" 
    :class="className"
    v-bind="$attrs"
  />
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import * as LucideIcons from 'lucide-vue-next'

interface Props {
  icon?: string
  name?: string
  class?: string
}

const props = withDefaults(defineProps<Props>(), {
  icon: '',
  name: '',
  class: ''
})

const className = computed(() => props.class)

// Function to get Lucide icon component
const getIconComponent = (iconName: string) => {
  // Convert kebab-case to PascalCase for Lucide icons
  const pascalCase = iconName
    .split(':')[1] || iconName // Remove lucide: prefix if present
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join('')
  
  // Return the icon component from Lucide
  return (LucideIcons as any)[pascalCase] || (LucideIcons as any).HelpCircle
}
</script>
