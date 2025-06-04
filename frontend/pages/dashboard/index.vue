<template>
  <div>
    <RoleBasedDashboard />
  </div>
</template>

<script setup>
import { useAuth } from '~/composables/useAuth';

// Define page metadata including layout and required middleware
definePageMeta({
  layout: 'dashboard',
  middleware: ['auth'],
  requiresAuth: true
});

// Get authentication state from the composable
const { user, isAuthenticated } = useAuth();
</script>