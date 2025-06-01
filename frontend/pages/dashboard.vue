<template>
  <div>
    <RoleBasedDashboard />
  </div>
</template>

<script setup>
import { useAuth } from '~/composables/useAuth';

// Verificar autenticação
const { isAuthenticated, checkAuth } = useAuth();

// Verificar autenticação ao carregar a página
onMounted(async () => {
  await checkAuth();
});

// Definir layout
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
});
</script>
