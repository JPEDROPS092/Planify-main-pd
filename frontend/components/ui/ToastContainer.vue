<!-- components/ui/ToastContainer.vue -->
<template>
  <div class="fixed top-4 right-4 z-50 space-y-2">
    <Toast
      v-for="toast in toasts"
      :key="toast.id"
      :show="true"
      :type="toast.type"
      :title="toast.title"
      :description="toast.description || ''"
      :duration="toast.duration"
      @close="dismissToast(toast.id)"
    />
  </div>
</template>

<script setup lang="ts">
import { useToast } from "../../composables/useToast";
import Toast from "./Toast.vue";

const { toasts, dismissToast } = useToast();
</script>
</script>
