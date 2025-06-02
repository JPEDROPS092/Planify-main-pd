<template>
  <div>
    <slot v-if="showContent" />
    <slot v-else-if="$slots.fallback" name="fallback" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuth } from '~/stores/composables/useAuth';

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

const { userRole, hasPermission } = useAuth();

// Verifica se o usuário tem o papel necessário
const hasRole = computed(() => {
  if (!props.roles || props.roles.length === 0) {
    return true;
  }
  return props.roles.includes(userRole.value);
});

// Verifica se o usuário tem as permissões necessárias
const hasRequiredPermissions = computed(() => {
  if (!props.permissions || props.permissions.length === 0) {
    return true;
  }

  if (props.requireAll) {
    // Precisa ter todas as permissões
    return props.permissions.every((permission) => {
      const [module, action] = permission.split(':');
      return hasPermission(module, action);
    });
  } else {
    // Precisa ter pelo menos uma das permissões
    return props.permissions.some((permission) => {
      const [module, action] = permission.split(':');
      return hasPermission(module, action);
    });
  }
});

// Determina se o conteúdo deve ser exibido
const showContent = computed(() => {
  return hasRole.value && hasRequiredPermissions.value;
});
</script>
