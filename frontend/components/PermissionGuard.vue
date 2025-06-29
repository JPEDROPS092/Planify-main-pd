<template>
  <div v-if="hasAccess">
    <slot />
  </div>
  <div v-else-if="showFallback">
    <slot name="fallback">
      <div class="flex items-center justify-center p-8 bg-gray-50 rounded-lg border border-gray-200">
        <div class="text-center">
          <Icon icon="lucide:shield-x" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">Acesso Negado</h3>
          <p class="text-gray-600">
            Você não tem permissão para acessar este conteúdo.
          </p>
        </div>
      </div>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'
import { usePermissions } from '~/composables/usePermissions'

interface Props {
  // Permissão específica necessária
  permission?: string
  // Lista de permissões (todas necessárias - AND)
  permissions?: string[]
  // Lista de permissões (pelo menos uma necessária - OR)
  anyPermissions?: string[]
  // Grupo necessário
  group?: string
  // Apenas para admins
  adminOnly?: boolean
  // Apenas para staff
  staffOnly?: boolean
  // Mostrar fallback quando não tem acesso (padrão: true)
  showFallback?: boolean
  // Inverter lógica (mostrar apenas se NÃO tiver a permissão)
  invert?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showFallback: true,
  invert: false
})

const { 
  hasPermission, 
  hasAllPermissions, 
  hasAnyPermission, 
  hasGroup, 
  isAdmin,
  userPermissions,
  isLoading 
} = usePermissions()

const hasAccess = computed(() => {
  // Se ainda está carregando, não mostrar conteúdo
  if (isLoading.value) return false
  
  let access = true

  // Verificar se é admin only
  if (props.adminOnly) {
    access = access && isAdmin.value
  }

  // Verificar se é staff only
  if (props.staffOnly) {
    access = access && (userPermissions.value?.is_staff || false)
  }

  // Verificar permissão específica
  if (props.permission) {
    access = access && hasPermission(props.permission)
  }

  // Verificar todas as permissões (AND)
  if (props.permissions && props.permissions.length > 0) {
    access = access && hasAllPermissions(props.permissions)
  }

  // Verificar qualquer permissão (OR)
  if (props.anyPermissions && props.anyPermissions.length > 0) {
    access = access && hasAnyPermission(props.anyPermissions)
  }

  // Verificar grupo
  if (props.group) {
    access = access && hasGroup(props.group)
  }

  // Inverter lógica se necessário
  return props.invert ? !access : access
})
</script>