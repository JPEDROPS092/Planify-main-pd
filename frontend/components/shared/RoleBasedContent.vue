<template>
  <div>
    <!-- Renderiza o conteúdo apenas se o usuário tiver o papel ou permissão necessária -->
    <slot v-if="shouldRender"></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props para definir quais papéis ou permissões podem ver o conteúdo
const props = defineProps({
  // Papéis que podem ver o conteúdo (array ou string única)
  roles: {
    type: [Array, String],
    default: () => []
  },
  // Permissões que podem ver o conteúdo (array ou string única)
  permissions: {
    type: [Array, String],
    default: () => []
  },
  // Módulo da permissão (usado quando permissions é fornecido)
  module: {
    type: String,
    default: ''
  },
  // Ação da permissão (usado quando permissions é fornecido)
  action: {
    type: String,
    default: ''
  },
  // Se verdadeiro, inverte a lógica (mostra para quem NÃO tem o papel/permissão)
  exclude: {
    type: Boolean,
    default: false
  }
})

// Importar o composable de autenticação
const { userRole, hasPermission } = useAuth()

// Normalizar roles para sempre ser um array
const normalizedRoles = computed(() => {
  if (!props.roles) return []
  return Array.isArray(props.roles) ? props.roles : [props.roles]
})

// Normalizar permissions para sempre ser um array
const normalizedPermissions = computed(() => {
  if (!props.permissions) return []
  return Array.isArray(props.permissions) ? props.permissions : [props.permissions]
})

// Verificar se o usuário tem algum dos papéis especificados
const hasRole = computed(() => {
  // Se não há papéis especificados, consideramos que qualquer papel pode ver
  if (normalizedRoles.value.length === 0) return true
  
  // Verificar se o papel do usuário está na lista de papéis permitidos
  return normalizedRoles.value.includes(userRole.value)
})

// Verificar se o usuário tem alguma das permissões especificadas
const hasRequiredPermission = computed(() => {
  // Se não há permissões especificadas, consideramos que qualquer permissão pode ver
  if (normalizedPermissions.value.length === 0) return true
  
  // Se há permissões específicas, verificamos cada uma
  if (props.module && props.action) {
    // Verificar permissão específica (módulo + ação)
    return hasPermission(props.module, props.action)
  } else {
    // Verificar se o usuário tem alguma das permissões listadas
    return normalizedPermissions.value.some(permission => {
      // Se a permissão contém um ponto, assumimos que é no formato "MODULO.ACAO"
      if (permission.includes('.')) {
        const [module, action] = permission.split('.')
        return hasPermission(module, action)
      }
      return false
    })
  }
})

// Determinar se o conteúdo deve ser renderizado
const shouldRender = computed(() => {
  const result = hasRole.value && hasRequiredPermission.value
  // Se exclude é true, invertemos o resultado
  return props.exclude ? !result : result
})
</script>
