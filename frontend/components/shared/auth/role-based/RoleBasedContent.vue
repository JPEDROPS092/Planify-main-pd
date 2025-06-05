<template>
  <div>
    <!-- Renderiza o conteúdo principal se o usuário tiver as permissões/papéis necessários -->
    <slot v-if="showContent" />
    <!-- Renderiza um conteúdo alternativo se fornecido e o usuário não tiver acesso -->
    <slot v-else-if="$slots.fallback" name="fallback" />
    <!-- Se o usuário não tiver acesso e não houver fallback, nada será renderizado -->
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuth } from '~/composables/useAuth';

/**
 * Props do componente
 * 
 * @property {Array} roles - Lista de papéis que têm permissão para ver o conteúdo
 * @property {Array} permissions - Lista de permissões necessárias no formato "modulo:acao"
 * @property {Boolean} requireAll - Se true, o usuário precisa ter todas as permissões; se false, basta ter uma
 */
const props = defineProps({
  roles: {
    type: Array,
    required: false,
    default: () => [],
  },
  permissions: {
    type: Array,
    required: false,
    default: () => [],
  },
  requireAll: {
    type: Boolean,
    default: false,
  },
});

// Obtém as funções de autenticação e autorização do composable useAuth
const { userRole, hasPermission } = useAuth();

/**
 * Verifica se o usuário tem algum dos papéis necessários
 * Se nenhum papel for especificado, retorna true (acesso permitido)
 */
const hasRole = computed(() => {
  if (!props.roles || props.roles.length === 0) {
    return true;
  }
  return props.roles.includes(userRole.value);
});

/**
 * Verifica se o usuário tem as permissões necessárias
 * Se nenhuma permissão for especificada, retorna true (acesso permitido)
 * O formato de cada permissão deve ser "modulo:acao"
 */
const hasRequiredPermissions = computed(() => {
  if (!props.permissions || props.permissions.length === 0) {
    return true;
  }

  if (props.requireAll) {
    // Precisa ter todas as permissões listadas
    return props.permissions.every((permission) => {
      const [module, action] = permission.split(':');
      return hasPermission(module, action);
    });
  } else {
    // Precisa ter pelo menos uma das permissões listadas
    return props.permissions.some((permission) => {
      const [module, action] = permission.split(':');
      return hasPermission(module, action);
    });
  }
});

/**
 * Determina se o conteúdo deve ser exibido com base nos papéis e permissões
 * O usuário precisa ter TANTO um papel válido QUANTO as permissões necessárias
 */
const showContent = computed(() => {
  return hasRole.value && hasRequiredPermissions.value;
});
</script>
