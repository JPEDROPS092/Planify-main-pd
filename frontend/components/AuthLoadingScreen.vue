<template>
  <div class="fixed inset-0 bg-white flex items-center justify-center z-50">
    <div class="text-center">
      <!-- Spinner -->
      <div class="relative">
        <div
          class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"
        ></div>

        <!-- Logo opcional -->
        <div class="absolute inset-0 flex items-center justify-center">
          <Icon icon="lucide:layout-dashboard" class="w-6 h-6 text-blue-600" />
        </div>
      </div>

      <!-- Texto -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2">
        Verificando autenticação
      </h3>
      <p class="text-gray-600">Aguarde um momento...</p>

      <!-- Progress bar opcional -->
      <div
        class="w-48 h-1 bg-gray-200 rounded-full mt-4 mx-auto overflow-hidden"
      >
        <div class="h-full bg-blue-600 rounded-full animate-pulse"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Icon } from "@iconify/vue";
</script>
